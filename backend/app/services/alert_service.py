"""Alert service logic."""
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository


class AlertService:
    """Business logic for alerts."""

    @staticmethod
    def create_alert(db: Session, **kwargs) -> Alert:
        return AlertRepository.create(db, **kwargs)

    @staticmethod
    def get_alert(db: Session, alert_id: str) -> Alert:
        alert = AlertRepository.get_by_id(db, alert_id)
        if not alert:
            raise NotFoundError("Alert")
        return alert

    @staticmethod
    def list_alerts(db: Session, skip: int = 0, limit: int = 100, *, search: str | None = None,
                    status: str | None = None, severity: str | None = None,
                    sort_by: str = "created_at", sort_dir: str = "desc") -> list[Alert]:
        return AlertRepository.get_all(
            db, skip=skip, limit=limit, search=search, status=status,
            severity=severity, sort_by=sort_by, sort_dir=sort_dir,
        )

    @staticmethod
    def count_alerts(db: Session, *, search: str | None = None, status: str | None = None,
                     severity: str | None = None) -> int:
        return AlertRepository.count(db, search=search, status=status, severity=severity)

    @staticmethod
    def update_alert(db: Session, alert_id: str, **kwargs) -> Alert:
        return AlertRepository.update(db, alert_id, **kwargs)

    @staticmethod
    def delete_alert(db: Session, alert_id: str) -> None:
        AlertRepository.delete(db, alert_id)
