from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """User model for identity management."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__("uuid").uuid4()))
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String(50), default="VIEWER", nullable=False)

    devices = relationship("Device", back_populates="user")
    alerts = relationship("Alert", back_populates="user", foreign_keys="Alert.user_id")
    created_investigations = relationship(
        "Investigation",
        back_populates="creator",
        foreign_keys="Investigation.created_by",
    )
    collected_evidence = relationship("Evidence", back_populates="collector", foreign_keys="Evidence.collected_by")
    investigation_notes = relationship("InvestigationNote", back_populates="author", foreign_keys="InvestigationNote.author_id")
    ai_conversations = relationship("AIConversation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class Role(Base):
    """Role model for RBAC."""

    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__("uuid").uuid4()))
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"


class Permission(Base):
    """Permission model for fine-grained access control."""

    __tablename__ = "permissions"

    id = Column(String(36), primary_key=True, default=lambda: str(__import__("uuid").uuid4()))
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Permission(id={self.id}, name={self.name})>"
