from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate

def create_chat_message(db: Session, message: ChatMessageCreate):
    db_message = ChatMessage(
        session_id=message.session_id,
        sender=message.sender,
        message=message.message
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_session(db: Session, session_id: int):
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()
