from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Añadido campo created_at

    # Relación con ChatMessage
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")