"""Alert repository."""
from typing import Optional
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.alert import Alert
from app.utils.sorting import apply_sort


class AlertRepository:
    """Repository for alert CRUD operations."""

    SORTABLE = {
        "created_at": Alert.created_at,
        "updated_at": Alert.updated_at,
        "detection_time": Alert.detection_time,
        "severity": Alert.severity,
        "status": Alert.status,
        "title": Alert.title,
        "source": Alert.source,
    }

    @staticmethod
    def create(db: Session, *, title: str, description: str | None, severity: str, status: str,
               source: str | None, detection_time, user_id: str | None, device_id: str | None,
               ip_address: str | None, investigation_id: str | None = None,
               ip_address_id: str | None = None) -> Alert:
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
            ip_address_id=ip_address_id,
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

    @staticmethod
    def get_by_id(db: Session, alert_id: str) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == alert_id).first()

    @staticmethod
    def build_query(db: Session, *, search: str | None = None, status: str | None = None,
                    severity: str | None = None):
        query = db.query(Alert)
        if search:
            pattern = f"%{search.lower()}%"
            query = query.filter(or_(
                func.lower(Alert.title).like(pattern),
                func.lower(Alert.description).like(pattern),
                func.lower(Alert.source).like(pattern),
            ))
        if status and status != "ALL":
            query = query.filter(Alert.status == status)
        if severity and severity != "ALL":
            query = query.filter(Alert.severity == severity)
        return query

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, *, search: str | None = None,
                status: str | None = None, severity: str | None = None,
                sort_by: str = "created_at", sort_dir: str = "desc") -> list[Alert]:
        query = AlertRepository.build_query(db, search=search, status=status, severity=severity)
        query = apply_sort(query, AlertRepository.SORTABLE, sort_by, sort_dir, "created_at")
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, *, search: str | None = None, status: str | None = None,
              severity: str | None = None) -> int:
        return AlertRepository.build_query(db, search=search, status=status, severity=severity).count()

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
