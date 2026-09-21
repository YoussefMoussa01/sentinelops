"""Investigation API routes."""
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.investigation_service import InvestigationService
from app.api.dependencies import check_permission, get_current_user
from app.models import Alert, User
from app.schemas import InvestigationCreate, InvestigationUpdate

router = APIRouter(prefix="/investigations", tags=["investigations"])


def serialize(investigation) -> dict:
    return {
        "id": investigation.id,
        "title": investigation.title,
        "description": investigation.description,
        "severity": investigation.severity,
        "status": investigation.status,
        "risk_score": investigation.risk_score,
        "created_by": investigation.created_by,
        "creator": {"id": investigation.creator.id, "username": investigation.creator.username}
        if investigation.creator else None,
        "assigned_to": investigation.assigned_to,
        "assignee": {"id": investigation.assignee.id, "username": investigation.assignee.username}
        if investigation.assignee else None,
        "created_at": investigation.created_at.isoformat(),
        "updated_at": investigation.updated_at.isoformat(),
    }


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_investigations"))])
async def list_investigations(
    response: Response,
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    search: str | None = Query(default=None, max_length=120),
    status: str | None = Query(default=None),
    severity: str | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    sort_dir: str = Query(default="desc", pattern="^(asc|desc)$"),
):
    investigations = InvestigationService.list_investigations(
        db, skip=skip, limit=limit, search=search, status=status,
        severity=severity, sort_by=sort_by, sort_dir=sort_dir,
    )
    response.headers["X-Total-Count"] = str(
        InvestigationService.count_investigations(db, search=search, status=status, severity=severity)
    )
    return [serialize(investigation) for investigation in investigations]


@router.get("/assignees", response_model=list[dict], dependencies=[Depends(check_permission("manage_investigations"))])
async def list_investigation_assignees(db: Session = Depends(get_db)):
    """Return the minimal user data needed to assign an investigator to a case."""
    users = (
        db.query(User)
        .filter(User.is_active.is_(True))
        .order_by(User.username.asc())
        .all()
    )
    return [{"id": user.id, "username": user.username} for user in users]


@router.get("/{investigation_id}", response_model=dict, dependencies=[Depends(check_permission("view_investigations"))])
async def get_investigation(investigation_id: str, db: Session = Depends(get_db)):
    return serialize(InvestigationService.get_investigation(db, investigation_id))


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
    events.extend({
        "type": "status_changed",
        "title": "Investigation status changed",
        "description": f"Status changed from {change.from_status} to {change.to_status} by {change.user.username if change.user else 'unknown user'}",
        "timestamp": change.created_at.isoformat(),
        "details": {"from_status": change.from_status, "to_status": change.to_status, "changed_by": change.user.username if change.user else None},
    } for change in investigation.status_history)
    return sorted(events, key=lambda event: event["timestamp"])


@router.post("", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def create_investigation(payload: InvestigationCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    data = payload.model_dump()
    if not data.get("created_by"):
        data["created_by"] = current_user.id
    investigation = InvestigationService.create_investigation(
        db,
        **data,
    )
    return serialize(investigation)


@router.patch("/{investigation_id}", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def update_investigation(
    investigation_id: str, payload: InvestigationUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    investigation = InvestigationService.update_investigation(
        db, investigation_id, changed_by=current_user.id, **payload.model_dump(exclude_unset=True)
    )
    return serialize(investigation)


@router.delete("/{investigation_id}", dependencies=[Depends(check_permission("manage_investigations"))])
async def delete_investigation(investigation_id: str, db: Session = Depends(get_db)):
    InvestigationService.delete_investigation(db, investigation_id)
    return {"status": "success", "message": "Investigation deleted"}
