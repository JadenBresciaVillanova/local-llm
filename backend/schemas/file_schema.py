from pydantic import BaseModel, ConfigDict
from uuid import UUID
import datetime

class FileMetadataRead(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    file_size: int
    file_type: str
    upload_date: datetime.datetime
    processing_status: str
    chunk_count: int  # <-- ADD THIS LINE

    # Use the Pydantic V2 style for configuration
    model_config = ConfigDict(from_attributes=True)