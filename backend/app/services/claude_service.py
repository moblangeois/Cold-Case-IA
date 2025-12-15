import anthropic
import os
from typing import List, Dict, Optional, AsyncIterator
import json

class ClaudeService:
    """Service for interacting with Claude Sonnet 4.5 API"""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"  # Claude Sonnet 4.5

    async def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0
    ) -> Dict[str, any]:
        """
        Send a message to Claude and get a response

        Args:
            message: User message
            conversation_history: Previous messages in the conversation
            system_prompt: System prompt to guide Claude's behavior
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            Dictionary with response and metadata
        """
        messages = []

        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)

        # Add current message
        messages.append({
            "role": "user",
            "content": message
        })

        # Default system prompt for cold case analysis
        if not system_prompt:
            system_prompt = """Tu es un assistant d'investigation spécialisé dans l'analyse de cold cases.
            Tu as accès à des documents, images et transcriptions de podcasts relatifs à des affaires non résolues.

            Tes capacités incluent :
            - Analyser des documents et extraire des informations pertinentes
            - Identifier des connexions entre différents éléments de preuve
            - Proposer des pistes d'investigation basées sur les données disponibles
            - Répondre aux questions avec précision et objectivité

            Important :
            - Reste factuel et base tes réponses sur les documents fournis
            - Indique clairement quand tu fais des hypothèses
            - Sois respectueux envers toutes les personnes mentionnées
            - N'invente jamais d'informations
            """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=messages
            )

            return {
                "content": response.content[0].text,
                "id": response.id,
                "model": response.model,
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}")

    async def chat_with_context(
        self,
        message: str,
        context_documents: List[Dict[str, str]],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 4096
    ) -> Dict[str, any]:
        """
        Chat with Claude using RAG context

        Args:
            message: User message
            context_documents: Relevant documents from vector search
            conversation_history: Previous messages
            max_tokens: Maximum tokens in response

        Returns:
            Dictionary with response and metadata
        """
        # Build context from documents
        context_text = "\n\n".join([
            f"Document {i+1} ({doc.get('content_type', 'unknown')}):\n{doc['content']}"
            for i, doc in enumerate(context_documents)
        ])

        # Enhanced system prompt with context
        system_prompt = f"""Tu es un assistant d'investigation spécialisé dans l'analyse de cold cases.

        CONTEXTE PERTINENT:
        {context_text}

        Utilise ces documents pour répondre à la question de l'utilisateur de manière précise et détaillée.
        Cite les documents spécifiques quand tu te bases sur eux.
        Si la réponse n'est pas dans les documents fournis, indique-le clairement.
        """

        return await self.chat(
            message=message,
            conversation_history=conversation_history,
            system_prompt=system_prompt,
            max_tokens=max_tokens
        )

    async def analyze_document(
        self,
        document_content: str,
        document_type: str,
        analysis_type: str = "summary"
    ) -> str:
        """
        Analyze a specific document

        Args:
            document_content: Content of the document
            document_type: Type of document (text, pdf, transcript, etc.)
            analysis_type: Type of analysis (summary, key_facts, timeline, etc.)

        Returns:
            Analysis result
        """
        prompts = {
            "summary": f"Résume ce document en identifiant les points clés et informations importantes.",
            "key_facts": f"Extrais tous les faits et informations factuelles importants de ce document.",
            "timeline": f"Identifie tous les événements et dates mentionnés et présente-les sous forme de chronologie.",
            "people": f"Liste toutes les personnes mentionnées dans ce document avec leur rôle et les informations les concernant.",
            "locations": f"Identifie tous les lieux mentionnés dans ce document."
        }

        prompt = prompts.get(analysis_type, prompts["summary"])
        message = f"{prompt}\n\nDocument ({document_type}):\n{document_content}"

        response = await self.chat(message=message, max_tokens=2048)
        return response["content"]
