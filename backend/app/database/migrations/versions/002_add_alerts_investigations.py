"""Add alerts and investigations tables.

Revision ID: 002_add_alerts_investigations
Revises: 001_initial_schema
Create Date: 2026-09-02 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "002_add_alerts_investigations"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "alerts",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(50), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(50), nullable=False, server_default="NEW"),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("detection_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("device_id", sa.String(36), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "investigations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("severity", sa.String(50), nullable=False, server_default="MEDIUM"),
        sa.Column("risk_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("status", sa.String(50), nullable=False, server_default="OPEN"),
        sa.Column("created_by", sa.String(36), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("investigations")
    op.drop_table("alerts")