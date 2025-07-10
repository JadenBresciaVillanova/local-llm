# backend/schemas/chat_schema.py
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    prompt: str
    conversation_id: Optional[str] = None # To continue a conversation
    user_email: Optional[str] = None
    file_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str