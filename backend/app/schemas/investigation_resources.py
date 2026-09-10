from pydantic import BaseModel, Field


class EvidenceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    evidence_type: str = Field(default="NOTE", min_length=1, max_length=50)
    source: str | None = Field(default=None, max_length=150)
    reference: str | None = Field(default=None, max_length=500)


class NoteCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
