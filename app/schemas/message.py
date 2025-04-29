from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    session_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    session_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  # Antes era orm_mode = True en Pydantic v1
