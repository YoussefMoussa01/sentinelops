"""Add investigation evidence and notes."""
from alembic import op
import sqlalchemy as sa


revision = "007_add_investigation_resources"
down_revision = "006_add_user_roles"
branch_labels = None
depends_on = None


def upgrade() -> None:
    timestamp = sa.DateTime(timezone=True)
    op.create_table(
        "evidence",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("investigation_id", sa.String(36), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("evidence_type", sa.String(50), nullable=False, server_default="NOTE"),
        sa.Column("source", sa.String(150), nullable=True),
        sa.Column("reference", sa.String(500), nullable=True),
        sa.Column("collected_by", sa.String(36), nullable=True),
        sa.Column("created_at", timestamp, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", timestamp, server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_evidence_investigation_id", "evidence", ["investigation_id"])
    op.create_table(
        "investigation_notes",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("investigation_id", sa.String(36), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("author_id", sa.String(36), nullable=True),
        sa.Column("created_at", timestamp, server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", timestamp, server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_investigation_notes_investigation_id", "investigation_notes", ["investigation_id"])


def downgrade() -> None:
    op.drop_index("ix_investigation_notes_investigation_id", table_name="investigation_notes")
    op.drop_table("investigation_notes")
    op.drop_index("ix_evidence_investigation_id", table_name="evidence")
    op.drop_table("evidence")
