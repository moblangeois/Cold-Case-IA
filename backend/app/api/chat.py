from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import ChatRequest, ChatResponse
from app.services.claude_service import ClaudeService
from app.services.embeddings import EmbeddingsService
import uuid
from typing import Dict

router = APIRouter()

# In-memory conversation storage (in production, use Redis or database)
conversations: Dict[str, list] = {}

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, app_request: Request):
    """
    Chat with Claude about a cold case

    - **message**: User message
    - **conversation_id**: Optional conversation ID to continue a conversation
    - **case_id**: Case ID to query (default: kyron_horman)
    - **use_rag**: Whether to use RAG for context (default: true)
    - **max_tokens**: Maximum tokens in response
    """
    try:
        # Get services
        embeddings_service: EmbeddingsService = app_request.app.state.embeddings_service
        claude_service = ClaudeService()

        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid.uuid4())
        conversation_history = conversations.get(conversation_id, [])

        # Perform RAG search if enabled
        context_documents = []
        sources = []

        if request.use_rag:
            search_results = await embeddings_service.search(
                query=request.message,
                n_results=5,
                content_types=request.case_id if request.case_id else None
            )

            context_documents = [
                {
                    "content": result["content"][:2000],  # Limit content size
                    "content_type": result["metadata"].get("content_type", "unknown"),
                    "filename": result["metadata"].get("filename", "unknown")
                }
                for result in search_results
            ]

            sources = [
                {
                    "filename": result["metadata"].get("filename", "unknown"),
                    "content_type": result["metadata"].get("content_type", "unknown"),
                    "relevance": 1 - result.get("distance", 0) if result.get("distance") else None
                }
                for result in search_results
            ]

        # Get response from Claude
        if context_documents:
            response = await claude_service.chat_with_context(
                message=request.message,
                context_documents=context_documents,
                conversation_history=conversation_history,
                max_tokens=request.max_tokens
            )
        else:
            response = await claude_service.chat(
                message=request.message,
                conversation_history=conversation_history,
                max_tokens=request.max_tokens
            )

        # Update conversation history
        conversation_history.append({"role": "user", "content": request.message})
        conversation_history.append({"role": "assistant", "content": response["content"]})
        conversations[conversation_id] = conversation_history

        # Return response
        return ChatResponse(
            message=response["content"],
            conversation_id=conversation_id,
            sources=sources if sources else None,
            tokens_used=response["usage"]["input_tokens"] + response["usage"]["output_tokens"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation history"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation cleared"}
    return {"message": "Conversation not found"}

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id in conversations:
        return {"conversation_id": conversation_id, "messages": conversations[conversation_id]}
    raise HTTPException(status_code=404, detail="Conversation not found")
