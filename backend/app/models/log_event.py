"""Security log event model."""
import uuid
from sqlalchemy import Column, DateTime, String, Text
from app.database.session import Base
from app.models.base import TimestampMixin


class LogEvent(Base, TimestampMixin):
    __tablename__ = "log_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    level = Column(String(20), nullable=False, default="INFO")
    source = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    event_time = Column(DateTime(timezone=True), nullable=True)