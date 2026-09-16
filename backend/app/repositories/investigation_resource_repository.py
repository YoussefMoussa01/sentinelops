from sqlalchemy.orm import Session

from app.models import Evidence, InvestigationNote
from app.core.exceptions import NotFoundError


class InvestigationResourceRepository:
    @staticmethod
    def list_evidence(db: Session, investigation_id: str) -> list[Evidence]:
        return db.query(Evidence).filter(Evidence.investigation_id == investigation_id).order_by(Evidence.created_at.desc()).all()

    @staticmethod
    def create_evidence(db: Session, investigation_id: str, **kwargs) -> Evidence:
        item = Evidence(investigation_id=investigation_id, **kwargs)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_evidence(db: Session, evidence_id: str, investigation_id: str) -> None:
        item = db.query(Evidence).filter(
            Evidence.id == evidence_id,
            Evidence.investigation_id == investigation_id,
        ).first()
        if not item:
            raise NotFoundError("Evidence")
        db.delete(item)
        db.commit()

    @staticmethod
    def list_notes(db: Session, investigation_id: str) -> list[InvestigationNote]:
        return db.query(InvestigationNote).filter(InvestigationNote.investigation_id == investigation_id).order_by(InvestigationNote.created_at.desc()).all()

    @staticmethod
    def create_note(db: Session, investigation_id: str, **kwargs) -> InvestigationNote:
        note = InvestigationNote(investigation_id=investigation_id, **kwargs)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    @staticmethod
    def delete_note(db: Session, note_id: str, investigation_id: str) -> None:
        item = db.query(InvestigationNote).filter(
            InvestigationNote.id == note_id,
            InvestigationNote.investigation_id == investigation_id,
        ).first()
        if not item:
            raise NotFoundError("Investigation note")
        db.delete(item)
        db.commit()
