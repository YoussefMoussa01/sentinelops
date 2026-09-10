"""Add IP address and location intelligence tables."""
from alembic import op
import sqlalchemy as sa


revision = "009_add_ip_intelligence"
down_revision = "008_link_security_entities"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ip_addresses",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("address", sa.String(45), nullable=False),
        sa.Column("is_private", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("reputation_score", sa.Float(), nullable=False, server_default="50.0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("address"),
    )
    op.create_index("ix_ip_addresses_address", "ip_addresses", ["address"], unique=True)

    op.create_table(
        "locations",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("ip_address_id", sa.String(36), nullable=False),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("timezone", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["ip_address_id"], ["ip_addresses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_locations_ip_address_id", "locations", ["ip_address_id"])


def downgrade() -> None:
    op.drop_index("ix_locations_ip_address_id", table_name="locations")
    op.drop_table("locations")
    op.drop_index("ix_ip_addresses_address", table_name="ip_addresses")
    op.drop_table("ip_addresses")
