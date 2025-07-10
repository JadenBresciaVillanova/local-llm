# backend/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    provider: str
    provider_id: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    provider: str

    model_config = {
        "from_attributes": True
    }
