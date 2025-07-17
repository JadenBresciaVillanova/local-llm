# backend/schemas/chat_schema.py
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    prompt: str
    conversation_id: Optional[str] = None # To continue a conversation
    user_email: Optional[str] = None
    file_id: Optional[UUID] = None
    selected_file_ids: Optional[List[UUID]] = None
    selected_model: str = "llama3:8b"
    custom_prompt_template: Optional[str] = None
    temperature: float = 0.8
    top_p: float = 1.0
    max_tokens: int = 1024

class TokenCounts(BaseModel):
    prompt_tokens: int
    response_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    token_counts: Optional[TokenCounts] = None

