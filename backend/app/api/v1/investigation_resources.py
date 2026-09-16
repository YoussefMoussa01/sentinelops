from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import check_permission, get_current_user
from app.database import get_db
from app.schemas import EvidenceCreate, NoteCreate
from app.services.investigation_service import InvestigationService
from app.repositories.investigation_resource_repository import InvestigationResourceRepository
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/investigations", tags=["investigation-resources"])


def evidence_response(item):
    return {"id": item.id, "investigation_id": item.investigation_id, "title": item.title, "description": item.description, "evidence_type": item.evidence_type, "source": item.source, "reference": item.reference, "collected_by": item.collected_by, "created_at": item.created_at.isoformat()}


def note_response(item):
    return {"id": item.id, "investigation_id": item.investigation_id, "content": item.content, "author_id": item.author_id, "created_at": item.created_at.isoformat()}


@router.get("/{investigation_id}/evidence", response_model=list[dict], dependencies=[Depends(check_permission("view_investigations"))])
async def list_evidence(investigation_id: str, db: Session = Depends(get_db)):
    InvestigationService.get_investigation(db, investigation_id)
    return [evidence_response(item) for item in InvestigationResourceRepository.list_evidence(db, investigation_id)]


@router.post("/{investigation_id}/evidence", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def create_evidence(investigation_id: str, payload: EvidenceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    InvestigationService.get_investigation(db, investigation_id)
    item = InvestigationResourceRepository.create_evidence(db, investigation_id, **payload.model_dump(), collected_by=current_user.id)
    return evidence_response(item)


@router.delete("/{investigation_id}/evidence/{evidence_id}", dependencies=[Depends(check_permission("manage_investigations"))])
async def delete_evidence(investigation_id: str, evidence_id: str, db: Session = Depends(get_db)):
    InvestigationService.get_investigation(db, investigation_id)
    InvestigationResourceRepository.delete_evidence(db, evidence_id, investigation_id)
    return {"status": "success", "message": "Evidence deleted"}


@router.get("/{investigation_id}/notes", response_model=list[dict], dependencies=[Depends(check_permission("view_investigations"))])
async def list_notes(investigation_id: str, db: Session = Depends(get_db)):
    InvestigationService.get_investigation(db, investigation_id)
    return [note_response(item) for item in InvestigationResourceRepository.list_notes(db, investigation_id)]


@router.post("/{investigation_id}/notes", response_model=dict, dependencies=[Depends(check_permission("manage_investigations"))])
async def create_note(investigation_id: str, payload: NoteCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    InvestigationService.get_investigation(db, investigation_id)
    item = InvestigationResourceRepository.create_note(db, investigation_id, content=payload.content, author_id=current_user.id)
    return note_response(item)


@router.delete("/{investigation_id}/notes/{note_id}", dependencies=[Depends(check_permission("manage_investigations"))])
async def delete_note(investigation_id: str, note_id: str, db: Session = Depends(get_db)):
    InvestigationService.get_investigation(db, investigation_id)
    InvestigationResourceRepository.delete_note(db, note_id, investigation_id)
    return {"status": "success", "message": "Note deleted"}
