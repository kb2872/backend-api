"""promote root user to superadmin

Revision ID: ef9916d012d4
Revises: d46b828e2440
Create Date: 2026-09-23
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


revision: str = "ef9916d012d4"
down_revision: Union[str, Sequence[str], None] = "d46b828e2440"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()

    connection.execute(
        text(
            """
            UPDATE users
            SET role = 'superadmin'
            WHERE id = 0
              AND role = 'admin'
            """
        )
    )


def downgrade() -> None:
    connection = op.get_bind()

    connection.execute(
        text(
            """
            UPDATE users
            SET role = 'admin'
            WHERE id = 0
              AND role = 'superadmin'
            """
        )
    )
