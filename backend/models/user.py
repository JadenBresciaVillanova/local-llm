from __future__ import annotations

from sqlalchemy import String, DateTime, func, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from uuid import UUID, uuid4
from .base import Base


from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .file_metadata import FileMetadata
    from .chat_log import ChatLog


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=True) # For non-OAuth2 logins
    provider: Mapped[str] = mapped_column(String, nullable=True) # e.g., 'google', 'github'
    provider_id: Mapped[str] = mapped_column(String, nullable=True, unique=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    # Relationships
    files: Mapped[List["FileMetadata"]] = relationship(back_populates="user")
    chat_logs: Mapped[List["ChatLog"]] = relationship(back_populates="user")
