"""Investigation service logic."""
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError, ValidationError
from app.models.investigation import Investigation
from app.models.investigation_status import InvestigationStatusHistory
from app.repositories.investigation_repository import InvestigationRepository
from app.repositories.user_repository import UserRepository


INVESTIGATION_STATUS_TRANSITIONS: dict[str, set[str]] = {
    "OPEN": {"CLOSED", "ARCHIVED"},
    "CLOSED": {"OPEN", "ARCHIVED"},
    "ARCHIVED": {"OPEN"},
}


class InvestigationService:
    """Business logic for investigations."""

    @staticmethod
    def create_investigation(db: Session, **kwargs) -> Investigation:
        InvestigationService._validate_assignment(db, kwargs.get("assigned_to"))
        return InvestigationRepository.create(db, **kwargs)

    @staticmethod
    def get_investigation(db: Session, investigation_id: str) -> Investigation:
        investigation = InvestigationRepository.get_by_id(db, investigation_id)
        if not investigation:
            raise NotFoundError("Investigation")
        return investigation

    @staticmethod
    def list_investigations(db: Session, skip: int = 0, limit: int = 100, *, search: str | None = None,
                            status: str | None = None, severity: str | None = None,
                            sort_by: str = "created_at", sort_dir: str = "desc") -> list[Investigation]:
        return InvestigationRepository.get_all(
            db, skip=skip, limit=limit, search=search, status=status,
            severity=severity, sort_by=sort_by, sort_dir=sort_dir,
        )

    @staticmethod
    def count_investigations(db: Session, *, search: str | None = None, status: str | None = None,
                             severity: str | None = None) -> int:
        return InvestigationRepository.count(db, search=search, status=status, severity=severity)

    @staticmethod
    def _validate_assignment(db: Session, assigned_to: str | None) -> None:
        if assigned_to is None:
            return
        user = UserRepository.get_by_id(db, assigned_to)
        if user is None or not user.is_active:
            raise ValidationError("The assigned investigator must be an active user")

    @staticmethod
    def _validate_status_transition(current_status: str, requested_status: str) -> None:
        current = str(getattr(current_status, "value", current_status)).upper()
        requested = str(getattr(requested_status, "value", requested_status)).upper()
        if current == requested:
            return
        allowed = INVESTIGATION_STATUS_TRANSITIONS.get(current, set())
        if requested not in allowed:
            raise ValidationError(
                f"Status transition {current} -> {requested} is not allowed"
            )

    @staticmethod
    def update_investigation(db: Session, investigation_id: str, changed_by: str | None = None, **kwargs) -> Investigation:
        current = InvestigationService.get_investigation(db, investigation_id)
        previous_status = getattr(current.status, "value", current.status)
        requested_status = kwargs.get("status")
        if requested_status is not None:
            InvestigationService._validate_status_transition(previous_status, requested_status)

        assigned_to_provided = "assigned_to" in kwargs
        assigned_to_value = kwargs.pop("assigned_to", None)
        if assigned_to_provided:
            InvestigationService._validate_assignment(db, assigned_to_value)

        updated = InvestigationRepository.update(db, investigation_id, **kwargs)
        if assigned_to_provided:
            updated.assigned_to = assigned_to_value
            db.commit()
            db.refresh(updated)

        next_status = getattr(updated.status, "value", updated.status)
        if requested_status is not None and previous_status != next_status:
            db.add(InvestigationStatusHistory(
                investigation_id=updated.id,
                changed_by=changed_by,
                from_status=previous_status,
                to_status=next_status,
            ))
            db.commit()
            db.refresh(updated)
        return updated

    @staticmethod
    def delete_investigation(db: Session, investigation_id: str) -> None:
        InvestigationRepository.delete(db, investigation_id)
