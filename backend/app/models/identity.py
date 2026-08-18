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

    # Relationships (will be added in later phases)
    # devices = relationship("Device", back_populates="user")
    # alerts = relationship("Alert", back_populates="user")

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
