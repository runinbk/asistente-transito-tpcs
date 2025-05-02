from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.schemas.message import MessageCreate

def create_message(db: Session, message: MessageCreate):
    db_message = ChatMessage(
        session_id=message.session_id,
        sender=message.sender,
        message=message.message,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_session(db: Session, session_id: int):
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()

def delete_message(db: Session, message_id: int):
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False