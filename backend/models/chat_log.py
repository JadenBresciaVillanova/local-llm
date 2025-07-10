# backend/models/chat_log.py
from __future__ import annotations
from sqlalchemy import String, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
# from backend.db.session import Base
from backend.models.user import User


from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user import User

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    model_version_used: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship
    user: Mapped["User"] = relationship(back_populates="chat_logs")