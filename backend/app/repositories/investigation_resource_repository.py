from sqlalchemy.orm import Session

from app.models import Evidence, InvestigationNote


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
    def list_notes(db: Session, investigation_id: str) -> list[InvestigationNote]:
        return db.query(InvestigationNote).filter(InvestigationNote.investigation_id == investigation_id).order_by(InvestigationNote.created_at.desc()).all()

    @staticmethod
    def create_note(db: Session, investigation_id: str, **kwargs) -> InvestigationNote:
        note = InvestigationNote(investigation_id=investigation_id, **kwargs)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
