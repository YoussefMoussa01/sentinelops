"""Add monitored devices."""
from alembic import op
import sqlalchemy as sa

revision = "004_add_devices"
down_revision = "003_link_alerts_investigations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("hostname", sa.String(150), nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("device_type", sa.String(50), nullable=False, server_default="WORKSTATION"),
        sa.Column("operating_system", sa.String(100), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="ACTIVE"),
        sa.Column("last_seen", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("devices")