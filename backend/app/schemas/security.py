"""Validation schemas for the Phase 4 security domain."""
from datetime import datetime
from ipaddress import ip_address

from pydantic import BaseModel, Field, field_validator

from app.core.constants import AlertSeverity, AlertStatus, InvestigationStatus


class AlertCreate(BaseModel):
    title: str = Field(default="New alert", min_length=1, max_length=200)
    description: str | None = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    status: AlertStatus = AlertStatus.NEW
    source: str | None = Field(default=None, max_length=100)
    detection_time: datetime | None = None
    user_id: str | None = None
    device_id: str | None = None
    ip_address_id: str | None = None
    ip_address: str | None = Field(default=None, max_length=45)
    investigation_id: str | None = None

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str | None) -> str | None:
        if value is not None:
            ip_address(value)
        return value


class AlertUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    severity: AlertSeverity | None = None
    status: AlertStatus | None = None
    source: str | None = Field(default=None, max_length=100)
    detection_time: datetime | None = None
    user_id: str | None = None
    device_id: str | None = None
    ip_address_id: str | None = None
    ip_address: str | None = Field(default=None, max_length=45)
    investigation_id: str | None = None

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str | None) -> str | None:
        if value is not None:
            ip_address(value)
        return value


class InvestigationCreate(BaseModel):
    title: str = Field(default="New investigation", min_length=1, max_length=200)
    description: str | None = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    risk_score: float = Field(default=0.0, ge=0.0, le=100.0)
    status: InvestigationStatus = InvestigationStatus.OPEN
    created_by: str | None = None
    assigned_to: str | None = None


class InvestigationUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    severity: AlertSeverity | None = None
    risk_score: float | None = Field(default=None, ge=0.0, le=100.0)
    status: InvestigationStatus | None = None
    assigned_to: str | None = None


class DeviceCreate(BaseModel):
    user_id: str | None = None
    ip_address_id: str | None = None
    hostname: str = Field(default="New device", min_length=1, max_length=150)
    ip_address: str | None = Field(default=None, max_length=45)
    device_type: str = Field(default="WORKSTATION", min_length=1, max_length=50)
    operating_system: str | None = Field(default=None, max_length=100)
    status: str = Field(default="ACTIVE", min_length=1, max_length=30)

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str | None) -> str | None:
        if value is not None:
            ip_address(value)
        return value


class DeviceUpdate(BaseModel):
    user_id: str | None = None
    ip_address_id: str | None = None
    hostname: str | None = Field(default=None, min_length=1, max_length=150)
    ip_address: str | None = Field(default=None, max_length=45)
    device_type: str | None = Field(default=None, min_length=1, max_length=50)
    operating_system: str | None = Field(default=None, max_length=100)
    status: str | None = Field(default=None, min_length=1, max_length=30)

    @field_validator("ip_address")
    @classmethod
    def validate_ip_address(cls, value: str | None) -> str | None:
        if value is not None:
            ip_address(value)
        return value


class IPAddressCreate(BaseModel):
    address: str = Field(min_length=1, max_length=45)
    is_private: bool = False
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    reputation_score: float = Field(default=50.0, ge=0, le=100)

    @field_validator("address")
    @classmethod
    def validate_address(cls, value: str) -> str:
        ip_address(value)
        return value


class IPAddressUpdate(BaseModel):
    is_private: bool | None = None
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    reputation_score: float | None = Field(default=None, ge=0, le=100)


class LocationCreate(BaseModel):
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    timezone: str | None = Field(default=None, max_length=100)
