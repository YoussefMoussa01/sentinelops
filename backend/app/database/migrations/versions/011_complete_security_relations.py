"""Complete security entity foreign keys and IP alert relation."""
from alembic import op
import sqlalchemy as sa

revision = "011_complete_security_relations"
down_revision = "010_link_devices_ip_addresses"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("alerts", sa.Column("ip_address_id", sa.String(36), nullable=True))
    op.create_index("ix_alerts_ip_address_id", "alerts", ["ip_address_id"])
    op.create_foreign_key("fk_alerts_ip_address_id", "alerts", "ip_addresses", ["ip_address_id"], ["id"], ondelete="SET NULL")

    op.create_foreign_key("fk_evidence_investigation_id", "evidence", "investigations", ["investigation_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_evidence_collected_by", "evidence", "users", ["collected_by"], ["id"], ondelete="SET NULL")
    op.create_foreign_key("fk_notes_investigation_id", "investigation_notes", "investigations", ["investigation_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key("fk_notes_author_id", "investigation_notes", "users", ["author_id"], ["id"], ondelete="SET NULL")


def downgrade() -> None:
    op.drop_constraint("fk_notes_author_id", "investigation_notes", type_="foreignkey")
    op.drop_constraint("fk_notes_investigation_id", "investigation_notes", type_="foreignkey")
    op.drop_constraint("fk_evidence_collected_by", "evidence", type_="foreignkey")
    op.drop_constraint("fk_evidence_investigation_id", "evidence", type_="foreignkey")
    op.drop_constraint("fk_alerts_ip_address_id", "alerts", type_="foreignkey")
    op.drop_index("ix_alerts_ip_address_id", table_name="alerts")
    op.drop_column("alerts", "ip_address_id")