"""add password hash

Revision ID: 01b34a378667
Revises: 500df0e2efe2
Create Date: 2026-07-07 19:51:12.350285
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "01b34a378667"
down_revision: Union[str, Sequence[str], None] = "500df0e2efe2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "password_hash")


