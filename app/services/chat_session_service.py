from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.schemas.chat_session import ChatSessionCreate
from datetime import datetime

def create_chat_session(db: Session, session_data: ChatSessionCreate) -> ChatSession:
    new_session = ChatSession(**session_data.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

def get_all_chat_sessions(db: Session):
    # Asegúrate de que todas las sesiones tengan created_at
    sessions = db.query(ChatSession).all()
    for session in sessions:
        if session.created_at is None:
            session.created_at = datetime.utcnow()
    
    if sessions and any(session.created_at is None for session in sessions):
        db.commit()  # Guardar los cambios si se actualizó algún created_at
    
    return sessions

def get_chat_session_by_id(db: Session, session_id: int):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session and session.created_at is None:
        session.created_at = datetime.utcnow()
        db.commit()
    return session

def delete_chat_session(db: Session, session_id: int):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False