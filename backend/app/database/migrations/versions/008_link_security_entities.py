"""Link users, devices, logs, alerts and investigations."""
from alembic import op
import sqlalchemy as sa

revision = "008_link_security_entities"
down_revision = "007_add_investigation_resources"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("devices", sa.Column("user_id", sa.String(36), nullable=True))
    op.create_index("ix_devices_user_id", "devices", ["user_id"])
    op.create_foreign_key(
        "fk_devices_user_id_users",
        "devices",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.add_column("log_events", sa.Column("device_id", sa.String(36), nullable=True))
    op.create_index("ix_log_events_device_id", "log_events", ["device_id"])
    op.create_foreign_key(
        "fk_log_events_device_id_devices",
        "log_events",
        "devices",
        ["device_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_foreign_key(
        "fk_alerts_user_id_users",
        "alerts",
        "users",
        ["user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_alerts_device_id_devices",
        "alerts",
        "devices",
        ["device_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_alerts_investigation_id_investigations",
        "alerts",
        "investigations",
        ["investigation_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_foreign_key(
        "fk_investigations_created_by_users",
        "investigations",
        "users",
        ["created_by"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_investigations_created_by_users", "investigations", type_="foreignkey")

    op.drop_constraint("fk_alerts_investigation_id_investigations", "alerts", type_="foreignkey")
    op.drop_constraint("fk_alerts_device_id_devices", "alerts", type_="foreignkey")
    op.drop_constraint("fk_alerts_user_id_users", "alerts", type_="foreignkey")

    op.drop_constraint("fk_log_events_device_id_devices", "log_events", type_="foreignkey")
    op.drop_index("ix_log_events_device_id", table_name="log_events")
    op.drop_column("log_events", "device_id")

    op.drop_constraint("fk_devices_user_id_users", "devices", type_="foreignkey")
    op.drop_index("ix_devices_user_id", table_name="devices")
    op.drop_column("devices", "user_id")
