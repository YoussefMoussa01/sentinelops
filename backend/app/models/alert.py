"""Alert model."""
from __future__ import annotations

import uuid
from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import AlertSeverity, AlertStatus
from app.database.session import Base
from app.models.base import TimestampMixin


class Alert(Base, TimestampMixin):
    """Security alert record."""

    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(
        SAEnum(AlertSeverity),
        default=AlertSeverity.MEDIUM,
        nullable=False,
    )
    status = Column(
        SAEnum(AlertStatus),
        default=AlertStatus.NEW,
        nullable=False,
    )
    source = Column(String(100), nullable=True)
    detection_time = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    device_id = Column(String(36), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True)
    ip_address = Column(String(45), nullable=True)
    investigation_id = Column(
        String(36),
        ForeignKey("investigations.id", ondelete="SET NULL"),
        nullable=True,
    )

    user = relationship("User", back_populates="alerts", foreign_keys=[user_id])
    device = relationship("Device", back_populates="alerts", foreign_keys=[device_id])
    investigation = relationship("Investigation", back_populates="alerts")

    def __repr__(self) -> str:
        return f"<Alert(id={self.id}, title={self.title})>"
