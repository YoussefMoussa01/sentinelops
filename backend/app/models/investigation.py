"""Investigation model."""
from __future__ import annotations

import uuid
from sqlalchemy import Column, Float, String, Text, Enum as SAEnum
from app.core.constants import InvestigationStatus
from app.database.session import Base
from app.models.base import TimestampMixin


class Investigation(Base, TimestampMixin):
    """Cybersecurity investigation record."""

    __tablename__ = "investigations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(50), default="MEDIUM", nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    status = Column(
        SAEnum(InvestigationStatus),
        default=InvestigationStatus.OPEN,
        nullable=False,
    )
    created_by = Column(String(36), nullable=True)

    def __repr__(self) -> str:
        return f"<Investigation(id={self.id}, title={self.title})>"
