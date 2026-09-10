"""Security logs API."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LogEvent
from app.api.dependencies import check_permission

router = APIRouter(prefix="/logs", tags=["logs"])


def serialize(log):
    return {"id": log.id, "device_id": log.device_id, "level": log.level, "source": log.source, "message": log.message,
            "event_time": log.event_time.isoformat() if log.event_time else None,
            "created_at": log.created_at.isoformat()}


@router.get("", response_model=list[dict], dependencies=[Depends(check_permission("view_logs"))])
async def list_logs(db: Session = Depends(get_db), query: str | None = Query(default=None)):
    statement = db.query(LogEvent)
    if query:
        search = f"%{query}%"
        statement = statement.filter(
            LogEvent.message.ilike(search) |
            LogEvent.source.ilike(search) |
            LogEvent.level.ilike(search)
        )
    return [serialize(log) for log in statement.order_by(LogEvent.created_at.desc()).limit(100).all()]
