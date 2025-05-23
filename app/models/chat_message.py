from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)

    sender = Column(Text, nullable=False)  # 'user' o 'assistant'
    message = Column(Text, nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)  # Usar func.now() y marcar como no nulo

    # Relación con ChatSession
    session = relationship("ChatSession", back_populates="messages")