from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    session_id: int
    sender: str  # <<<<<< Añadido
    message: str  # <<<<<< Cambiado de 'content' a 'message'

class MessageResponse(BaseModel):
    id: int
    session_id: int
    sender: str  # <<<<<< Añadido
    message: str  # <<<<<< Cambiado de 'content' a 'message'
    created_at: datetime

    class Config:
        from_attributes = True  # Correcto para Pydantic v2
