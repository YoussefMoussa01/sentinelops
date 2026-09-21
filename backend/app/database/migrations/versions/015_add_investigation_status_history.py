"""Track investigation status changes."""
from alembic import op
import sqlalchemy as sa


revision = "015_status_history"
down_revision = "014_add_ai_audit_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "investigation_status_history",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("investigation_id", sa.String(36), nullable=False),
        sa.Column("changed_by", sa.String(36), nullable=True),
        sa.Column("from_status", sa.String(50), nullable=False),
        sa.Column("to_status", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["investigation_id"], ["investigations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["changed_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_investigation_status_history_investigation_id", "investigation_status_history", ["investigation_id"])
    op.create_index("ix_investigation_status_history_changed_by", "investigation_status_history", ["changed_by"])


def downgrade() -> None:
    op.drop_index("ix_investigation_status_history_changed_by", table_name="investigation_status_history")
    op.drop_index("ix_investigation_status_history_investigation_id", table_name="investigation_status_history")
    op.drop_table("investigation_status_history")
