"""reserve id 0 for root admin

Revision ID: d46b828e2440
Revises: 360aa28b4842
Create Date: 2026-08-19 16:09:00.209255
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import text


revision: str = "d46b828e2440"
down_revision: Union[str, Sequence[str], None] = "360aa28b4842"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Reserve ID 0 for the root administrator."""

    connection = op.get_bind()

    result = connection.execute(
        text(
            """
            SELECT id
            FROM users
            WHERE id = 14
              AND role = 'admin'
            """
        )
    )

    row = result.fetchone()

    if row is None:
        raise RuntimeError(
            "No se encontró el administrador esperado en id=14 con role='admin'."
        )

    connection.execute(
        text(
            """
            UPDATE users
            SET id = 0
            WHERE id = 14
              AND role = 'admin'
            """
        )
    )

    connection.execute(
        text(
            """
            SELECT setval('users_id_seq', 1, false)
            """
        )
    )


def downgrade() -> None:
    """Restore the root administrator to ID 14."""

    connection = op.get_bind()

    result = connection.execute(
        text(
            """
            SELECT id
            FROM users
            WHERE id = 0
              AND role = 'admin'
            """
        )
    )

    row = result.fetchone()

    if row is None:
        raise RuntimeError(
            "No se encontró el administrador esperado en id=0."
        )

    connection.execute(
        text(
            """
            UPDATE users
            SET id = 14
            WHERE id = 0
              AND role = 'admin'
            """
        )
    )

    connection.execute(
        text(
            """
            SELECT setval('users_id_seq', 14, true)
            """
        )
    )
