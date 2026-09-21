"""Dashboard summary API."""
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import cast, Date, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, Investigation, User, Device
from app.api.dependencies import check_permission

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=dict, dependencies=[Depends(check_permission("view_alerts"))])
async def dashboard_stats(db: Session = Depends(get_db)):
    """Return live counts, most recent domain records, and chart-ready aggregates."""
    active_alerts = db.query(Alert).filter(Alert.status.notin_(["RESOLVED", "FALSE_POSITIVE"])).count()
    open_investigations = db.query(Investigation).filter(Investigation.status == "OPEN").count()
    recent_alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(5).all()
    recent_investigations = (
        db.query(Investigation).order_by(Investigation.created_at.desc()).limit(5).all()
    )

    severity_rows = (
        db.query(Alert.severity, func.count(Alert.id))
        .group_by(Alert.severity)
        .all()
    )
    severity_distribution = {str(row[0].value if hasattr(row[0], "value") else row[0]): row[1] for row in severity_rows}

    status_rows = (
        db.query(Alert.status, func.count(Alert.id))
        .group_by(Alert.status)
        .all()
    )
    status_distribution = {str(row[0].value if hasattr(row[0], "value") else row[0]): row[1] for row in status_rows}

    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    trend_rows = (
        db.query(
            cast(Alert.created_at, Date).label("day"),
            func.count(Alert.id),
        )
        .filter(Alert.created_at >= seven_days_ago)
        .group_by("day")
        .order_by("day")
        .all()
    )
    alert_trend = [{"date": str(row[0]), "count": row[1]} for row in trend_rows]

    investigation_risk_rows = (
        db.query(Investigation.status, func.avg(Investigation.risk_score), func.count(Investigation.id))
        .group_by(Investigation.status)
        .all()
    )
    investigation_risk = [
        {"status": str(row[0].value if hasattr(row[0], "value") else row[0]), "avg_risk": round(float(row[1] or 0), 1), "count": row[2]}
        for row in investigation_risk_rows
    ]

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
        "severity_distribution": severity_distribution,
        "status_distribution": status_distribution,
        "alert_trend": alert_trend,
        "investigation_risk": investigation_risk,
    }
