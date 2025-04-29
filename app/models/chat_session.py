from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, unique=True, index=True)

    # Relación con ChatMessage
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
