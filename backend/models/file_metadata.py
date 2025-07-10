from __future__ import annotations

from sqlalchemy import String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4
# from backend.db.session import Base 

from typing import List, TYPE_CHECKING
from .base import Base
if TYPE_CHECKING:
    from .user import User
    # from .embedding import DocumentChunk

# class FileMetadata(Base):
#     __tablename__ = "file_metadata"

#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
#     file_name: Mapped[str] = mapped_column(String, nullable=False)
#     file_path: Mapped[str] = mapped_column(String, nullable=False) # Path on disk/S3
#     file_size: Mapped[int] = mapped_column(Integer, nullable=False)
#     file_type: Mapped[str] = mapped_column(String, nullable=False) # e.g., 'application/pdf'
#     upload_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
#     processing_status: Mapped[str] = mapped_column(String, default="uploaded") # uploaded, processing, completed, failed
    
#     # Relationships
#     user: Mapped["User"] = relationship(back_populates="files")
#     chunks: Mapped[List["DocumentChunk"]] = relationship(back_populates="file")

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)
    upload_date: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    processing_status: Mapped[str] = mapped_column(String, default="uploaded")
    
    # --- ADD THIS LINE ---
    chunk_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relationships (no change)
    user: Mapped["User"] = relationship(back_populates="files")
    # This relationship is now unused by LangChain, but it's harmless to keep.
    # chunks: Mapped[List["DocumentChunk"]] = relationship(back_populates="file")