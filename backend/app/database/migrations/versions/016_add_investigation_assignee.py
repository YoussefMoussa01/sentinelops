"""Add investigation assignee."""
from alembic import op
import sqlalchemy as sa


revision = "016_add_investigation_assignee"
down_revision = "015_status_history"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "investigations",
        sa.Column("assigned_to", sa.String(36), nullable=True),
    )
    op.create_foreign_key(
        "fk_investigations_assigned_to_users",
        "investigations",
        "users",
        ["assigned_to"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_investigations_assigned_to", "investigations", ["assigned_to"])


def downgrade() -> None:
    op.drop_index("ix_investigations_assigned_to", table_name="investigations")
    op.drop_constraint("fk_investigations_assigned_to_users", "investigations", type_="foreignkey")
    op.drop_column("investigations", "assigned_to")