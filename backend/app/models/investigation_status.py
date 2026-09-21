"""Investigation status history model."""
import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class InvestigationStatusHistory(Base, TimestampMixin):
    __tablename__ = "investigation_status_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False, index=True)
    changed_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    from_status = Column(String(50), nullable=False)
    to_status = Column(String(50), nullable=False)

    investigation = relationship("Investigation", back_populates="status_history")
    user = relationship("User", back_populates="investigation_status_changes")
