"""Security audit event model."""
import uuid

from sqlalchemy import Column, ForeignKey, JSON, String
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class AuditEvent(Base, TimestampMixin):
    """Immutable application event attributed to an authenticated user."""

    __tablename__ = "audit_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    actor_user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(80), nullable=False)
    resource_id = Column(String(36), nullable=True)
    event_metadata = Column("metadata", JSON, nullable=True)

    actor = relationship("User", back_populates="audit_events")
