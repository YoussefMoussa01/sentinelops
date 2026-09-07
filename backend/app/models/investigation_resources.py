"""Evidence and notes attached to investigations."""
import uuid

from sqlalchemy import Column, String, Text

from app.database.session import Base
from app.models.base import TimestampMixin


class Evidence(Base, TimestampMixin):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    evidence_type = Column(String(50), nullable=False, default="NOTE")
    source = Column(String(150), nullable=True)
    reference = Column(String(500), nullable=True)
    collected_by = Column(String(36), nullable=True)


class InvestigationNote(Base, TimestampMixin):
    __tablename__ = "investigation_notes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String(36), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(String(36), nullable=True)
