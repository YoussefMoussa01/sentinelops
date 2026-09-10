"""IP address intelligence service."""
from sqlalchemy.orm import Session

from app.models.ip_address import IPAddress, Location
from app.repositories.ip_address_repository import IPAddressRepository


class IPAddressService:
    @staticmethod
    def create(db: Session, **values) -> IPAddress:
        return IPAddressRepository.create(db, **values)

    @staticmethod
    def get(db: Session, ip_id: str) -> IPAddress:
        return IPAddressRepository.get(db, ip_id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[IPAddress]:
        return IPAddressRepository.list(db, skip, limit)

    @staticmethod
    def update(db: Session, ip_id: str, **values) -> IPAddress:
        return IPAddressRepository.update(db, ip_id, **values)

    @staticmethod
    def delete(db: Session, ip_id: str) -> None:
        IPAddressRepository.delete(db, ip_id)

    @staticmethod
    def add_location(db: Session, ip_id: str, **values) -> Location:
        return IPAddressRepository.add_location(db, ip_id, **values)

