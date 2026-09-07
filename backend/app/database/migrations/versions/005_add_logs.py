"""Add security log events."""
from alembic import op
import sqlalchemy as sa

revision = "005_add_logs"
down_revision = "004_add_devices"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "log_events",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("level", sa.String(20), nullable=False, server_default="INFO"),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("log_events")