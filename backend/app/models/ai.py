"""Persistent AI conversation models."""
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, JSON, String, Text
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class AIConversation(Base, TimestampMixin):
    """A private assistant conversation owned by one user."""

    __tablename__ = "ai_conversations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False, default="New SentinelOps conversation")
    is_archived = Column(Boolean, nullable=False, default=False, server_default="false", index=True)

    user = relationship("User", back_populates="ai_conversations")
    messages = relationship(
        "AIMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AIMessage.created_at",
    )


class AIMessage(Base, TimestampMixin):
    """One user or assistant message in a conversation."""

    __tablename__ = "ai_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    provider = Column(String(100), nullable=True)
    reasoning_details = Column(JSON, nullable=True)

    conversation = relationship("AIConversation", back_populates="messages")
