"""Device service."""
from sqlalchemy.orm import Session
from app.models.device import Device
from app.repositories.device_repository import DeviceRepository


class DeviceService:
    @staticmethod
    def create_device(db: Session, **kwargs) -> Device:
        return DeviceRepository.create(db, **kwargs)

    @staticmethod
    def get_device(db: Session, device_id: str) -> Device:
        return DeviceRepository.get_by_id(db, device_id)

    @staticmethod
    def list_devices(db: Session) -> list[Device]:
        return DeviceRepository.get_all(db)

    @staticmethod
    def update_device(db: Session, device_id: str, **kwargs) -> Device:
        return DeviceRepository.update(db, device_id, **kwargs)

    @staticmethod
    def delete_device(db: Session, device_id: str) -> None:
        DeviceRepository.delete(db, device_id)