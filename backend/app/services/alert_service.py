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
    def list_alerts(db: Session, skip: int = 0, limit: int = 100) -> list[Alert]:
        return AlertRepository.get_all(db, skip=skip, limit=limit)

    @staticmethod
    def update_alert(db: Session, alert_id: str, **kwargs) -> Alert:
        return AlertRepository.update(db, alert_id, **kwargs)

    @staticmethod
    def delete_alert(db: Session, alert_id: str) -> None:
        AlertRepository.delete(db, alert_id)
