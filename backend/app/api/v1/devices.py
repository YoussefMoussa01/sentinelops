"""Device API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.device_service import DeviceService
from app.api.dependencies import check_permission
from app.schemas import DeviceCreate, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])


def serialize(device):
    return {"id": device.id, "hostname": device.hostname, "ip_address": device.ip_address,
            "device_type": device.device_type, "operating_system": device.operating_system,
            "status": device.status, "last_seen": device.last_seen.isoformat() if device.last_seen else None,
            "created_at": device.created_at.isoformat(), "updated_at": device.updated_at.isoformat()}


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_devices"))])
async def list_devices(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    return [serialize(device) for device in DeviceService.list_devices(db, skip=skip, limit=limit)]


@router.get("/{device_id}", response_model=dict, dependencies=[Depends(check_permission("view_devices"))])
async def get_device(device_id: str, db: Session = Depends(get_db)):
    return serialize(DeviceService.get_device(db, device_id))


@router.post("", response_model=dict, dependencies=[Depends(check_permission("manage_devices"))])
async def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    device = DeviceService.create_device(
        db, **payload.model_dump(), last_seen=None)
    return serialize(device)


@router.patch("/{device_id}", response_model=dict, dependencies=[Depends(check_permission("manage_devices"))])
async def update_device(device_id: str, payload: DeviceUpdate, db: Session = Depends(get_db)):
    return serialize(
        DeviceService.update_device(db, device_id, **payload.model_dump(exclude_unset=True))
    )


@router.delete("/{device_id}", dependencies=[Depends(check_permission("manage_devices"))])
async def delete_device(device_id: str, db: Session = Depends(get_db)):
    DeviceService.delete_device(db, device_id)
    return {"status": "success", "message": "Device deleted"}
