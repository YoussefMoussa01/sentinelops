"""Monitored device model."""
import uuid
from sqlalchemy import Column, DateTime, String
from app.database.session import Base
from app.models.base import TimestampMixin


class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = Column(String(150), nullable=False)
    ip_address = Column(String(45), nullable=True)
    device_type = Column(String(50), nullable=False, default="WORKSTATION")
    operating_system = Column(String(100), nullable=True)
    status = Column(String(30), nullable=False, default="ACTIVE")
    last_seen = Column(DateTime(timezone=True), nullable=True)