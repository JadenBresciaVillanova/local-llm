# # backend/models/embedding.py
# from __future__ import annotations
# from sqlalchemy import String, ForeignKey, Text, Integer
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from pgvector.sqlalchemy import Vector
# from uuid import UUID, uuid4 # <--- IMPORTANT FOR UUIDS
# # from backend.db.session import Base
# from backend.models.file_metadata import FileMetadata  # Import FileMetadata


# from typing import TYPE_CHECKING
# from .base import Base
# if TYPE_CHECKING:
#     from .file_metadata import FileMetadata

# class DocumentChunk(Base): # <--- Model Name: DocumentChunk
#     __tablename__ = "document_chunks" # <--- Table Name: document_chunks

#     id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4) # <--- UUID ID
#     file_id: Mapped[UUID] = mapped_column(ForeignKey("file_metadata.id"), nullable=False)
#     chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
#     text_content: Mapped[str] = mapped_column(Text, nullable=False)
#     embedding: Mapped[Vector] = mapped_column(Vector(768), nullable=False) 

#     file: Mapped["FileMetadata"] = relationship(back_populates="chunks")