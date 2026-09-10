"""Investigation API routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.investigation_service import InvestigationService
from app.api.dependencies import check_permission
from app.models import Alert
from app.schemas import InvestigationCreate, InvestigationUpdate

router = APIRouter(prefix="/investigations", tags=["investigations"])


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_investigations"))])
async def list_investigations(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    investigations = InvestigationService.list_investigations(db, skip=skip, limit=limit)
    return [
        {
            "id": investigation.id,
            "title": investigation.title,
            "description": investigation.description,
            "severity": investigation.severity,
            "status": investigation.status,
            "risk_score": investigation.risk_score,
            "created_by": investigation.created_by,
            "created_at": investigation.created_at.isoformat(),
            "updated_at": investigation.updated_at.isoformat(),
        }
        for investigation in investigations
    ]


@router.get("/{investigation_id}", response_model=dict, dependencies=[Depends(check_permission("view_investigations"))])
async def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    investigation = InvestigationService.get_investigation(db, investigation_id)
    return {
        "id": investigation.id,
        "title": investigation.title,
        "description": investigation.description,
        "severity": investigation.severity,
        "status": investigation.status,
        "risk_score": investigation.risk_score,
        "created_by": investigation.created_by,
        "created_at": investigation.created_at.isoformat(),
        "updated_at": investigation.updated_at.isoformat(),
    }


@router.get("/{investigation_id}/timeline", response_model=list[dict], dependencies=[Depends(check_permission("view_investigations"))])
async def get_investigation_timeline(investigation_id: str, db: Session = Depends(get_db)):
    investigation = InvestigationService.get_investigation(db, investigation_id)
    events = [{
        "type": "investigation_created",
        "title": "Investigation created",
        "description": investigation.title,
        "timestamp": investigation.created_at.isoformat(),
    }]
    alerts = db.query(Alert).filter(Alert.investigation_id == investigation_id).all()
    events.extend({
        "type": "alert_linked",
        "title": alert.title,
        "description": f"{alert.severity} alert from {alert.source or 'unknown source'}",
        "timestamp": (alert.detection_time or alert.created_at).isoformat(),
    } for alert in alerts)
    return sorted(events, key=lambda event: event["timestamp"])


@router.post("", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def create_investigation(payload: InvestigationCreate, db: Session = Depends(get_db)):
    investigation = InvestigationService.create_investigation(
        db,
        **payload.model_dump(),
    )
    return {
        "id": investigation.id,
        "title": investigation.title,
        "description": investigation.description,
        "severity": investigation.severity,
        "status": investigation.status,
        "created_by": investigation.created_by,
        "risk_score": investigation.risk_score,
    }


@router.patch("/{investigation_id}", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def update_investigation(
    investigation_id: str, payload: InvestigationUpdate, db: Session = Depends(get_db)
):
    investigation = InvestigationService.update_investigation(
        db, investigation_id, **payload.model_dump(exclude_unset=True)
    )
    return {
        "id": investigation.id,
        "title": investigation.title,
        "description": investigation.description,
        "severity": investigation.severity,
        "status": investigation.status,
        "created_by": investigation.created_by,
        "risk_score": investigation.risk_score,
    }


@router.delete("/{investigation_id}", dependencies=[Depends(check_permission("manage_investigations"))])
async def delete_investigation(investigation_id: str, db: Session = Depends(get_db)):
    InvestigationService.delete_investigation(db, investigation_id)
    return {"status": "success", "message": "Investigation deleted"}
