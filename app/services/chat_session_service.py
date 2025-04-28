
from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.schemas.chat_session import ChatSessionCreate

def create_chat_session(db: Session, session_data: ChatSessionCreate) -> ChatSession:
    new_session = ChatSession(**session_data.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_all_chat_sessions(db: Session):
    return db.query(ChatSession).all()

def get_chat_session_by_id(db: Session, session_id: int):
    return db.query(ChatSession).filter(ChatSession.id == session_id).first()

def delete_chat_session(db: Session, session_id: int):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False
