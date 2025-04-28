
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse
from app.db.database import get_db
from app.services import chat_message_service

router = APIRouter()

@router.post("/chat_messages", response_model=ChatMessageResponse)
def create_chat_message(message_data: ChatMessageCreate, db: Session = Depends(get_db)):
    return chat_message_service.create_chat_message(db, message_data)

@router.get("/chat_messages/session/{session_id}", response_model=list[ChatMessageResponse])
def get_messages_by_session(session_id: int, db: Session = Depends(get_db)):
    return chat_message_service.get_messages_by_session(db, session_id)

@router.delete("/chat_messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    success = chat_message_service.delete_message(db, message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Chat message deleted successfully"}