"""Security log event model."""
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.base import TimestampMixin


class LogEvent(Base, TimestampMixin):
    __tablename__ = "log_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(36), ForeignKey("devices.id", ondelete="SET NULL"), nullable=True, index=True)
    level = Column(String(20), nullable=False, default="INFO")
    source = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    event_time = Column(DateTime(timezone=True), nullable=True)

    device = relationship("Device", back_populates="logs")
