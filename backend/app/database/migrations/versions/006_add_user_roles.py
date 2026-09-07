"""Add roles to users."""
from alembic import op
import sqlalchemy as sa

revision = "006_add_user_roles"
down_revision = "005_add_logs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(50), nullable=False, server_default="VIEWER"))
    op.execute("UPDATE users SET role = 'SOC_ADMIN' WHERE username = 'admin'")
    op.execute("UPDATE users SET role = 'INVESTIGATOR' WHERE username = 'investigator'")


def downgrade() -> None:
    op.drop_column("users", "role")