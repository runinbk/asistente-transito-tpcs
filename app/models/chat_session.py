from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)  # Usar func.now() y marcar como no nulo

    # Relación con ChatMessage
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")