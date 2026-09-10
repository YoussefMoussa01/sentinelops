"""IP address intelligence API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import check_permission
from app.database import get_db
from app.schemas import IPAddressCreate, IPAddressUpdate, LocationCreate
from app.services.ip_address_service import IPAddressService

router = APIRouter(prefix="/ip-addresses", tags=["ip-addresses"])


def serialize_location(location):
    return {
        "id": location.id,
        "ip_address_id": location.ip_address_id,
        "country": location.country,
        "city": location.city,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "timezone": location.timezone,
        "created_at": location.created_at.isoformat(),
    }


def serialize_ip(item):
    return {
        "id": item.id,
        "address": item.address,
        "is_private": item.is_private,
        "country": item.country,
        "city": item.city,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "reputation_score": item.reputation_score,
        "locations": [serialize_location(location) for location in item.locations],
        "created_at": item.created_at.isoformat(),
        "updated_at": item.updated_at.isoformat(),
    }


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_ip_addresses"))])
async def list_ip_addresses(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return [serialize_ip(item) for item in IPAddressService.list(db, skip, limit)]


@router.get("/{ip_id}", response_model=dict, dependencies=[Depends(check_permission("view_ip_addresses"))])
async def get_ip_address(ip_id: str, db: Session = Depends(get_db)):
    return serialize_ip(IPAddressService.get(db, ip_id))


@router.post("", response_model=dict, dependencies=[Depends(check_permission("manage_ip_addresses"))])
async def create_ip_address(payload: IPAddressCreate, db: Session = Depends(get_db)):
    return serialize_ip(IPAddressService.create(db, **payload.model_dump()))


@router.patch("/{ip_id}", response_model=dict, dependencies=[Depends(check_permission("manage_ip_addresses"))])
async def update_ip_address(ip_id: str, payload: IPAddressUpdate, db: Session = Depends(get_db)):
    item = IPAddressService.update(db, ip_id, **payload.model_dump(exclude_unset=True))
    return serialize_ip(item)


@router.delete("/{ip_id}", dependencies=[Depends(check_permission("manage_ip_addresses"))])
async def delete_ip_address(ip_id: str, db: Session = Depends(get_db)):
    IPAddressService.delete(db, ip_id)
    return {"status": "success", "message": "IP address deleted"}


@router.post("/{ip_id}/locations", response_model=dict, dependencies=[Depends(check_permission("manage_ip_addresses"))])
async def add_location(ip_id: str, payload: LocationCreate, db: Session = Depends(get_db)):
    return serialize_location(IPAddressService.add_location(db, ip_id, **payload.model_dump()))
