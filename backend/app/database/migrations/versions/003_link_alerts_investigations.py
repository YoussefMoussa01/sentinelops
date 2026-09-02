"""Link alerts to investigations."""

from alembic import op
import sqlalchemy as sa


revision = "003_link_alerts_investigations"
down_revision = "002_add_alerts_investigations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("alerts", sa.Column("investigation_id", sa.String(36), nullable=True))
    op.create_index("ix_alerts_investigation_id", "alerts", ["investigation_id"])


def downgrade() -> None:
    op.drop_index("ix_alerts_investigation_id", table_name="alerts")
    op.drop_column("alerts", "investigation_id")