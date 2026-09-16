"""Add archive state for AI conversations."""
from alembic import op
import sqlalchemy as sa


revision = "013_manage_ai_conversations"
down_revision = "012_add_ai_conversations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "ai_conversations",
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index(
        "ix_ai_conversations_is_archived",
        "ai_conversations",
        ["is_archived"],
    )


def downgrade() -> None:
    op.drop_index("ix_ai_conversations_is_archived", table_name="ai_conversations")
    op.drop_column("ai_conversations", "is_archived")
