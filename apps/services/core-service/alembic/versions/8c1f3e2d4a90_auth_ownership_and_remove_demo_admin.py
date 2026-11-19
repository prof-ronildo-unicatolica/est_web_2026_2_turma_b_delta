"""link guest profiles to accounts and remove the seeded admin account

Revision ID: 8c1f3e2d4a90
Revises: d593fdad4170
Create Date: 2026-11-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8c1f3e2d4a90"
down_revision: Union[str, Sequence[str], None] = "d593fdad4170"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "hospedes",
        sa.Column("usuario_id", sa.Uuid(), nullable=True),
    )
    op.create_foreign_key(
        "fk_hospedes_usuario_id_usuarios",
        "hospedes",
        "usuarios",
        ["usuario_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_hospedes_usuario_id",
        "hospedes",
        ["usuario_id"],
        unique=True,
    )
    # Invalidate the fixed administrator created by the legacy migration.
    op.execute(
        sa.text(
            """
            DELETE FROM usuarios
            WHERE id = '00000000-0000-0000-0000-000000000001'
              AND is_admin = TRUE
            """
        )
    )


def downgrade() -> None:
    # Do not recreate the removed administrator or its reusable credential.
    op.drop_index("ix_hospedes_usuario_id", table_name="hospedes")
    op.drop_constraint(
        "fk_hospedes_usuario_id_usuarios",
        "hospedes",
        type_="foreignkey",
    )
    op.drop_column("hospedes", "usuario_id")
