from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatSessionCreate(BaseModel):
    session_name: str

class ChatSessionResponse(BaseModel):
    id: int
    session_name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Para Pydantic v2
        orm_mode = True  # Para mantener compatibilidad con Pydantic v1