"""Link devices to managed IP addresses."""
from alembic import op
import sqlalchemy as sa

revision = "010_link_devices_ip_addresses"
down_revision = "009_add_ip_intelligence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("ip_address_id", sa.String(36), nullable=True))
    op.create_foreign_key("fk_devices_ip_address_id", "devices", "ip_addresses", ["ip_address_id"], ["id"], ondelete="SET NULL")
    op.create_index("ix_devices_ip_address_id", "devices", ["ip_address_id"])


def downgrade() -> None:
    op.drop_index("ix_devices_ip_address_id", table_name="devices")
    op.drop_constraint("fk_devices_ip_address_id", "devices", type_="foreignkey")
    op.drop_column("devices", "ip_address_id")