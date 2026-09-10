"""IP address and geolocation models."""
import uuid

from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database.session import Base
from app.models.base import TimestampMixin


class IPAddress(Base, TimestampMixin):
    __tablename__ = "ip_addresses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    address = Column(String(45), unique=True, nullable=False, index=True)
    is_private = Column(Boolean, nullable=False, default=False)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reputation_score = Column(Float, nullable=False, default=50.0)

    locations = relationship("Location", back_populates="ip_address", cascade="all, delete-orphan")


class Location(Base, TimestampMixin):
    __tablename__ = "locations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ip_address_id = Column(
        String(36),
        ForeignKey("ip_addresses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    timezone = Column(String(100), nullable=True)

    ip_address = relationship("IPAddress", back_populates="locations")
