from pydantic import BaseModel
from datetime import datetime

class ChatMessageBase(BaseModel):
    sender: str
    message: str

class ChatMessageCreate(ChatMessageBase):
    session_id: int

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime

    class Config:
        orm_mode = True