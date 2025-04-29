from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.message import MessageCreate, MessageResponse
from app.services import message_service
from app.db.database import get_db
from typing import List

router = APIRouter(
    prefix="/messages",
    tags=["messages"]
)

@router.post("/", response_model=MessageResponse)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(db, message)

@router.get("/session/{session_id}", response_model=List[MessageResponse])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return message_service.get_messages_by_session(db, session_id)
