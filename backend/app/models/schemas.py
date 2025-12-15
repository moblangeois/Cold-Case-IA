from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    case_id: str = "kyron_horman"
    use_rag: bool = True
    max_tokens: int = Field(default=4096, le=8192)

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    sources: Optional[List[Dict[str, Any]]] = None
    tokens_used: Optional[int] = None

class CaseInfo(BaseModel):
    id: str
    name: str
    description: str
    date: Optional[str] = None
    location: Optional[str] = None
    status: str
    documents_count: int
    images_count: int
    texts_count: int

class SearchRequest(BaseModel):
    query: str
    case_id: str = "kyron_horman"
    limit: int = Field(default=5, le=20)
    content_types: Optional[List[str]] = None

class SearchResult(BaseModel):
    content: str
    content_type: str
    filename: str
    score: float
    metadata: Optional[Dict[str, Any]] = None

class DocumentInfo(BaseModel):
    filename: str
    content_type: str
    file_type: str
    size: Optional[int] = None
    path: str
    preview: Optional[str] = None
