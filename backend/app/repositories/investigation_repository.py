"""Investigation repository."""
from typing import Optional
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.investigation import Investigation
from app.utils.sorting import apply_sort


class InvestigationRepository:
    """Repository for investigation CRUD operations."""

    SORTABLE = {
        "created_at": Investigation.created_at,
        "updated_at": Investigation.updated_at,
        "severity": Investigation.severity,
        "status": Investigation.status,
        "risk_score": Investigation.risk_score,
        "title": Investigation.title,
    }

    @staticmethod
    def create(db: Session, *, title: str, description: str | None, severity: str, risk_score: float,
               status: str, created_by: str | None, assigned_to: str | None = None) -> Investigation:
        investigation = Investigation(
            title=title,
            description=description,
            severity=severity,
            risk_score=risk_score,
            status=status,
            created_by=created_by,
            assigned_to=assigned_to,
        )
        db.add(investigation)
        db.commit()
        db.refresh(investigation)
        return investigation

    @staticmethod
    def get_by_id(db: Session, investigation_id: str) -> Optional[Investigation]:
        return db.query(Investigation).filter(Investigation.id == investigation_id).first()

    @staticmethod
    def build_query(db: Session, *, search: str | None = None, status: str | None = None,
                    severity: str | None = None):
        query = db.query(Investigation)
        if search:
            pattern = f"%{search.lower()}%"
            query = query.filter(or_(
                func.lower(Investigation.title).like(pattern),
                func.lower(Investigation.description).like(pattern),
            ))
        if status and status != "ALL":
            query = query.filter(Investigation.status == status)
        if severity and severity != "ALL":
            query = query.filter(Investigation.severity == severity)
        return query

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, *, search: str | None = None,
                status: str | None = None, severity: str | None = None,
                sort_by: str = "created_at", sort_dir: str = "desc") -> list[Investigation]:
        query = InvestigationRepository.build_query(db, search=search, status=status, severity=severity)
        query = apply_sort(query, InvestigationRepository.SORTABLE, sort_by, sort_dir, "created_at")
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def count(db: Session, *, search: str | None = None, status: str | None = None,
              severity: str | None = None) -> int:
        return InvestigationRepository.build_query(db, search=search, status=status, severity=severity).count()

    @staticmethod
    def update(db: Session, investigation_id: str, **kwargs) -> Investigation:
        investigation = InvestigationRepository.get_by_id(db, investigation_id)
        if not investigation:
            raise NotFoundError("Investigation")

        for key, value in kwargs.items():
            if value is not None:
                setattr(investigation, key, value)

        db.commit()
        db.refresh(investigation)
        return investigation

    @staticmethod
    def delete(db: Session, investigation_id: str) -> None:
        investigation = InvestigationRepository.get_by_id(db, investigation_id)
        if not investigation:
            raise NotFoundError("Investigation")
        db.delete(investigation)
        db.commit()
