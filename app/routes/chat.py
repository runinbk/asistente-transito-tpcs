from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_session import ChatSessionCreate, ChatSessionResponse
from app.db.database import get_db
from app.services import chat_session_service

router = APIRouter()

@router.post("/chat_sessions", response_model=ChatSessionResponse)
def create_chat_session(session_data: ChatSessionCreate, db: Session = Depends(get_db)):
    return chat_session_service.create_chat_session(db, session_data)

@router.get("/chat_sessions", response_model=list[ChatSessionResponse])
def get_all_chat_sessions(db: Session = Depends(get_db)):
    return chat_session_service.get_all_chat_sessions(db)

@router.get("/chat_sessions/{session_id}", response_model=ChatSessionResponse)
def get_chat_session(session_id: int, db: Session = Depends(get_db)):
    session = chat_session_service.get_chat_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return session

@router.delete("/chat_sessions/{session_id}")
def delete_chat_session(session_id: int, db: Session = Depends(get_db)):
    success = chat_session_service.delete_chat_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"message": "Chat session deleted successfully"}