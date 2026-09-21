"""initial schema

Revision ID: 500df0e2efe2
Revises:
Create Date: 2026-07-03 20:30:31.666433
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "500df0e2efe2"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the initial users table."""

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "email",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    op.create_index(
        op.f("ix_users_id"),
        "users",
        ["id"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_users_email",
        "users",
        ["email"],
    )


def downgrade() -> None:
    """Drop the users table."""

    op.drop_constraint(
        "uq_users_email",
        "users",
        type_="unique",
    )

    op.drop_index(
        op.f("ix_users_id"),
        table_name="users",
    )

    op.drop_table("users")
