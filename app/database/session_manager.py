"""Session and message management with SQLite/PostgreSQL support."""
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class ChatSession(Base):
    """Chat session model."""
    __tablename__ = "chat_sessions"
    
    session_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(255), nullable=False, index=True)
    title = Column(String(255), default="New Chat")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Message(Base):
    """Message model for storing conversation history."""
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("chat_sessions.session_id"), nullable=False)
    role = Column(String(10))  # "user" or "assistant"
    content = Column(String(8000))
    source = Column(String(50))  # "rag", "web", or "agent"
    metadata = Column(JSON, default=dict)  # {tokens, latency, doc_ids}
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class SessionManager:
    """Manage chat sessions and message history."""
    
    def __init__(self, db_url: Optional[str] = None):
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "sqlite:///./chat_history.db")
        
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        logger.info(f"Connected to database: {db_url}")
    
    def create_session(self, user_id: str, title: str = "New Chat") -> str:
        """Create a new chat session."""
        db = self.SessionLocal()
        session = ChatSession(user_id=user_id, title=title)
        db.add(session)
        db.commit()
        session_id = session.session_id
        db.close()
        logger.info(f"Created session {session_id} for user {user_id}")
        return session_id
    
    def add_message(self, session_id: str, role: str, content: str, source: str, metadata: dict = None) -> str:
        """Add message to session."""
        db = self.SessionLocal()
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            source=source,
            metadata=metadata or {}
        )
        db.add(message)
        db.commit()
        msg_id = message.id
        db.close()
        return msg_id
    
    def get_session_history(self, session_id: str) -> List[dict]:
        """Get all messages in a session."""
        db = self.SessionLocal()
        messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at).all()
        history = [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "source": msg.source,
                "timestamp": msg.created_at.isoformat()
            }
            for msg in messages
        ]
        db.close()
        return history
