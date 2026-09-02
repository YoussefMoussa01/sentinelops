"""Alert repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.alert import Alert


class AlertRepository:
    """Repository for alert CRUD operations."""

    @staticmethod
    def create(db: Session, *, title: str, description: str | None, severity: str, status: str,
               source: str | None, detection_time, user_id: str | None, device_id: str | None,
               ip_address: str | None, investigation_id: str | None = None) -> Alert:
        alert = Alert(
            title=title,
            description=description,
            severity=severity,
            status=status,
            source=source,
            detection_time=detection_time,
            user_id=user_id,
            device_id=device_id,
            ip_address=ip_address,
            investigation_id=investigation_id,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_by_id(db: Session, alert_id: str) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Alert]:
        return db.query(Alert).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, alert_id: str, **kwargs) -> Alert:
        alert = AlertRepository.get_by_id(db, alert_id)
        if not alert:
            raise NotFoundError("Alert")

        for key, value in kwargs.items():
            if value is not None:
                setattr(alert, key, value)

        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def delete(db: Session, alert_id: str) -> None:
        alert = AlertRepository.get_by_id(db, alert_id)
        if not alert:
            raise NotFoundError("Alert")
        db.delete(alert)
        db.commit()
