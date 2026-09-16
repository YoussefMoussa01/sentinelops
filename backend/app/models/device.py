"""Monitored device model."""
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.base import TimestampMixin


class Device(Base, TimestampMixin):
    __tablename__ = "devices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    ip_address_id = Column(String(36), ForeignKey("ip_addresses.id", ondelete="SET NULL"), nullable=True, index=True)
    hostname = Column(String(150), nullable=False)
    ip_address = Column(String(45), nullable=True)
    device_type = Column(String(50), nullable=False, default="WORKSTATION")
    operating_system = Column(String(100), nullable=True)
    status = Column(String(30), nullable=False, default="ACTIVE")
    last_seen = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="devices")
    alerts = relationship("Alert", back_populates="device", foreign_keys="Alert.device_id")
    logs = relationship("LogEvent", back_populates="device")
    ip_record = relationship("IPAddress", back_populates="devices")
