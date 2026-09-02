"""Investigation service logic."""
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.models.investigation import Investigation
from app.repositories.investigation_repository import InvestigationRepository


class InvestigationService:
    """Business logic for investigations."""

    @staticmethod
    def create_investigation(db: Session, **kwargs) -> Investigation:
        return InvestigationRepository.create(db, **kwargs)

    @staticmethod
    def get_investigation(db: Session, investigation_id: str) -> Investigation:
        investigation = InvestigationRepository.get_by_id(db, investigation_id)
        if not investigation:
            raise NotFoundError("Investigation")
        return investigation

    @staticmethod
    def list_investigations(db: Session, skip: int = 0, limit: int = 100) -> list[Investigation]:
        return InvestigationRepository.get_all(db, skip=skip, limit=limit)

    @staticmethod
    def update_investigation(db: Session, investigation_id: str, **kwargs) -> Investigation:
        return InvestigationRepository.update(db, investigation_id, **kwargs)

    @staticmethod
    def delete_investigation(db: Session, investigation_id: str) -> None:
        InvestigationRepository.delete(db, investigation_id)
