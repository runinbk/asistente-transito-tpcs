
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.chat_session import ChatSession

router = APIRouter()

@router.get("/chat_sessions")
def get_chat_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ChatSession).all()
    return sessions
