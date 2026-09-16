"""Read-only log search service used by the API and AI tools."""
from sqlalchemy.orm import Session

from app.models import LogEvent


class LogService:
    @staticmethod
    def search(db: Session, query: str | None = None, limit: int = 20) -> list[LogEvent]:
        statement = db.query(LogEvent)
        if query and query.strip():
            pattern = f"%{query.strip()}%"
            statement = statement.filter(
                LogEvent.message.ilike(pattern)
                | LogEvent.source.ilike(pattern)
                | LogEvent.level.ilike(pattern)
            )
        return statement.order_by(LogEvent.created_at.desc()).limit(limit).all()
