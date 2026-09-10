"""Device repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.device import Device


class DeviceRepository:
    @staticmethod
    def create(db: Session, *, user_id: str | None, hostname: str, ip_address: str | None,
               device_type: str, operating_system: str | None,
               status: str, last_seen=None) -> Device:
        device = Device(user_id=user_id, hostname=hostname, ip_address=ip_address,
                        device_type=device_type, operating_system=operating_system,
                        status=status, last_seen=last_seen)
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def get_by_id(db: Session, device_id: str) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Device]:
        return db.query(Device).order_by(Device.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, device_id: str, **kwargs) -> Device:
        device = DeviceRepository.get_by_id(db, device_id)
        if not device:
            raise NotFoundError("Device")
        for key, value in kwargs.items():
            if value is not None and hasattr(device, key):
                setattr(device, key, value)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def delete(db: Session, device_id: str) -> None:
        device = DeviceRepository.get_by_id(db, device_id)
        if not device:
            raise NotFoundError("Device")
        db.delete(device)
        db.commit()
