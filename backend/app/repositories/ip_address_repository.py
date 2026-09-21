"""Repositories for IP address intelligence."""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.ip_address import IPAddress, Location


class IPAddressRepository:
    @staticmethod
    def create(db: Session, **values) -> IPAddress:
        if db.query(IPAddress).filter(IPAddress.address == values["address"]).first():
            raise ConflictError("IP address already exists")
        has_location = any(
            values.get(key) is not None for key in ("country", "city", "latitude", "longitude")
        )
        item = IPAddress(**values)
        if has_location:
            item.locations.append(
                Location(
                    country=values.get("country"),
                    city=values.get("city"),
                    latitude=values.get("latitude"),
                    longitude=values.get("longitude"),
                )
            )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get(db: Session, ip_id: str) -> IPAddress:
        item = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
        if not item:
            raise NotFoundError("IP address")
        return item

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> list[IPAddress]:
        return db.query(IPAddress).order_by(IPAddress.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, ip_id: str, **values) -> IPAddress:
        item = IPAddressRepository.get(db, ip_id)
        for key, value in values.items():
            if value is not None:
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, ip_id: str) -> None:
        item = IPAddressRepository.get(db, ip_id)
        db.delete(item)
        db.commit()

    @staticmethod
    def add_location(db: Session, ip_id: str, **values) -> Location:
        item = IPAddressRepository.get(db, ip_id)
        location = Location(ip_address=item, **values)
        db.add(location)
        db.commit()
        db.refresh(location)
        return location

