"""Alert API routes."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alert_service import AlertService
from app.api.dependencies import check_permission

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_alerts"))])
async def list_alerts(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    alerts = AlertService.list_alerts(db, skip=skip, limit=limit)
    return [
        {
            "id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "status": alert.status,
            "source": alert.source,
            "investigation_id": alert.investigation_id,
            "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
            "created_at": alert.created_at.isoformat(),
            "updated_at": alert.updated_at.isoformat(),
        }
        for alert in alerts
    ]


@router.get("/{alert_id}", response_model=dict, dependencies=[Depends(check_permission("view_alerts"))])
async def get_alert(alert_id: str, db: Session = Depends(get_db)):
    try:
        alert = AlertService.get_alert(db, alert_id)
        return {
            "id": alert.id,
            "title": alert.title,
            "description": alert.description,
            "severity": alert.severity,
            "status": alert.status,
            "source": alert.source,
            "investigation_id": alert.investigation_id,
            "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
            "created_at": alert.created_at.isoformat(),
            "updated_at": alert.updated_at.isoformat(),
        }
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("", response_model=dict, dependencies=[Depends(check_permission("view_alerts"))])
async def create_alert(payload: dict, db: Session = Depends(get_db)):
    detection_time = payload.get("detection_time")
    if detection_time and isinstance(detection_time, str):
        detection_time = datetime.fromisoformat(detection_time.replace("Z", "+00:00"))

    alert = AlertService.create_alert(
        db,
        title=payload.get("title", "New alert"),
        description=payload.get("description"),
        severity=payload.get("severity", "MEDIUM"),
        status=payload.get("status", "NEW"),
        source=payload.get("source"),
        detection_time=detection_time,
        user_id=payload.get("user_id"),
        device_id=payload.get("device_id"),
        ip_address=payload.get("ip_address"),
        investigation_id=payload.get("investigation_id"),
    )
    return {
        "id": alert.id,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "status": alert.status,
        "source": alert.source,
        "investigation_id": alert.investigation_id,
        "detection_time": alert.detection_time.isoformat() if alert.detection_time else None,
    }


@router.patch("/{alert_id}", response_model=dict, dependencies=[Depends(check_permission("view_alerts"))])
async def update_alert(alert_id: str, payload: dict, db: Session = Depends(get_db)):
    alert = AlertService.update_alert(db, alert_id, **payload)
    return {
        "id": alert.id,
        "title": alert.title,
        "description": alert.description,
        "severity": alert.severity,
        "status": alert.status,
        "source": alert.source,
        "investigation_id": alert.investigation_id,
    }


@router.delete("/{alert_id}", dependencies=[Depends(check_permission("view_alerts"))])
async def delete_alert(alert_id: str, db: Session = Depends(get_db)):
    AlertService.delete_alert(db, alert_id)
    return {"status": "success", "message": "Alert deleted"}
