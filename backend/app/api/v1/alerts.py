"""Alert API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alert_service import AlertService
from app.api.dependencies import check_permission
from app.schemas import AlertCreate, AlertUpdate
from app.models import Device, IPAddress

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_alerts"))])
async def list_alerts(
    response: Response,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=120),
    status_filter: str | None = Query(default=None, alias="status"),
    severity: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
):
    alerts = AlertService.list_alerts(
        db, skip=skip, limit=limit, search=search, status=status_filter,
        severity=severity, sort_by=sort_by, sort_dir=sort_dir,
    )
    response.headers["X-Total-Count"] = str(
        AlertService.count_alerts(db, search=search, status=status_filter, severity=severity)
    )
    return [
        {
            "id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "status": alert.status,
            "source": alert.source,
            "user_id": alert.user_id,
            "device_id": alert.device_id,
            "device": {
                "hostname": alert.device.hostname,
                "ip_address": alert.device.ip_address,
                "status": alert.device.status,
            } if alert.device else None,
            "investigation_id": alert.investigation_id,
            "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
            "created_at": alert.created_at.isoformat(),
            "updated_at": alert.updated_at.isoformat(),
        }
        for alert in alerts
    ]


@router.get("/{alert_id}", response_model=dict, dependencies=[Depends(check_permission("view_alerts"))])
async def get_alert(alert_id: str, db: Session = Depends(get_db)):
    alert = AlertService.get_alert(db, alert_id)
    return {
        "id": alert.id,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "status": alert.status,
        "source": alert.source,
        "user_id": alert.user_id,
        "device_id": alert.device_id,
        "ip_address_id": alert.ip_address_id,
        "investigation_id": alert.investigation_id,
        "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
        "created_at": alert.created_at.isoformat(),
        "updated_at": alert.updated_at.isoformat(),
    }


@router.post("", response_model=dict, dependencies=[Depends(check_permission("manage_alerts"))])
async def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    if data.get("device_id") and not data.get("ip_address"):
        device = db.query(Device).filter(Device.id == data["device_id"]).first()
        if not device:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Device not found")
        data["ip_address"] = device.ip_address
    if data.get("ip_address_id"):
        ip_record = db.query(IPAddress).filter(IPAddress.id == data["ip_address_id"]).first()
        if not ip_record:
            raise HTTPException(status_code=400, detail="IP address not found")
        data["ip_address"] = ip_record.address
    alert = AlertService.create_alert(
        db,
        **data,
    )
    return {
        "id": alert.id,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "status": alert.status,
        "source": alert.source,
        "user_id": alert.user_id,
        "device_id": alert.device_id,
        "ip_address_id": alert.ip_address_id,
        "device": {
            "hostname": alert.device.hostname,
            "ip_address": alert.device.ip_address,
            "status": alert.device.status,
        } if alert.device else None,
        "investigation_id": alert.investigation_id,
        "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
    }


@router.patch("/{alert_id}", response_model=dict, dependencies=[Depends(check_permission("manage_alerts"))])
async def update_alert(alert_id: str, payload: AlertUpdate, db: Session = Depends(get_db)):
    alert = AlertService.update_alert(db, alert_id, **payload.model_dump(exclude_unset=True))
    return {
        "id": alert.id,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "status": alert.status,
        "source": alert.source,
        "user_id": alert.user_id,
        "device_id": alert.device_id,
        "ip_address_id": alert.ip_address_id,
        "device": {
            "hostname": alert.device.hostname,
            "ip_address": alert.device.ip_address,
            "status": alert.device.status,
        } if alert.device else None,
        "investigation_id": alert.investigation_id,
    }


@router.delete("/{alert_id}", dependencies=[Depends(check_permission("manage_alerts"))])
async def delete_alert(alert_id: str, db: Session = Depends(get_db)):
    AlertService.delete_alert(db, alert_id)
    return {"status": "success", "message": "Alert deleted"}
