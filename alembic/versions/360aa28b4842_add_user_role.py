"""add user role

Revision ID: 360aa28b4842
Revises: 01b34a378667
Create Date: 2026-08-12 19:41:24.608773
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "360aa28b4842"
down_revision: Union[str, Sequence[str], None] = "01b34a378667"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add role column to users."""

    # 1. Añadimos la columna permitiendo NULL temporalmente.
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=True,
        ),
    )

    # 2. Asignamos "user" a los usuarios que ya existen.
    op.execute(
        "UPDATE users SET role = 'user' WHERE role IS NULL"
    )

    # 3. Ahora que todos tienen un valor, hacemos la columna NOT NULL.
    op.alter_column(
        "users",
        "role",
        nullable=False,
    )


def downgrade() -> None:
    """Remove role column from users."""

    op.drop_column("users", "role")



