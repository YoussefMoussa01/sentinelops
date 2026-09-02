"""Investigation repository."""
from typing import Optional
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.investigation import Investigation


class InvestigationRepository:
    """Repository for investigation CRUD operations."""

    @staticmethod
    def create(db: Session, *, title: str, description: str | None, severity: str, risk_score: float,
               status: str, created_by: str | None) -> Investigation:
        investigation = Investigation(
            title=title,
            description=description,
            severity=severity,
            risk_score=risk_score,
            status=status,
            created_by=created_by,
        )
        db.add(investigation)
        db.commit()
        db.refresh(investigation)
        return investigation

    @staticmethod
    def get_by_id(db: Session, investigation_id: str) -> Optional[Investigation]:
        return db.query(Investigation).filter(Investigation.id == investigation_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Investigation]:
        return db.query(Investigation).offset(skip).limit(limit).all()

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
