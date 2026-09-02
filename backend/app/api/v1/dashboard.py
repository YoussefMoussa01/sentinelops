"""Dashboard summary API."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, Investigation, User, Device

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=dict)
async def dashboard_stats(db: Session = Depends(get_db)):
    """Return live counts and the most recent domain records."""
    active_alerts = db.query(Alert).filter(Alert.status.notin_(["RESOLVED", "FALSE_POSITIVE"])).count()
    open_investigations = db.query(Investigation).filter(Investigation.status == "OPEN").count()
    recent_alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(5).all()
    recent_investigations = (
        db.query(Investigation).order_by(Investigation.created_at.desc()).limit(5).all()
    )

    return {
        "active_alerts": active_alerts,
        "open_investigations": open_investigations,
        "monitored_users": db.query(User).filter(User.is_active.is_(True)).count(),
        "devices": db.query(Device).count(),
        "recent_alerts": [
            {
                "id": alert.id,
                "title": alert.title,
                "severity": alert.severity,
                "status": alert.status,
                "source": alert.source,
            }
            for alert in recent_alerts
        ],
        "recent_investigations": [
            {
                "id": investigation.id,
                "title": investigation.title,
                "severity": investigation.severity,
                "status": investigation.status,
                "risk_score": investigation.risk_score,
            }
            for investigation in recent_investigations
        ],
    }