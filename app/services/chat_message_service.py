from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate

def create_chat_message(db: Session, message_data: ChatMessageCreate) -> ChatMessage:
    db_message = ChatMessage(
        session_id=message_data.session_id,
        sender=message_data.sender,
        message=message_data.message,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages_by_session(db: Session, session_id: int) -> list[ChatMessage]:
    return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).all()

def delete_message(db: Session, message_id: int) -> bool:
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    if message:
        db.delete(message)
        db.commit()
        return True
    return False