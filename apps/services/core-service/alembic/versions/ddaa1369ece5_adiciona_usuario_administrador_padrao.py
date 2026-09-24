"""adiciona usuario administrador padrao

Revision ID: ddaa1369ece5
Revises: 02d0814ce397
Create Date: 2026-09-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ddaa1369ece5"
down_revision: Union[str, None] = "02d0814ce397"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            INSERT INTO usuarios (id, nome, email, senha_hash, is_admin)
            VALUES (
                '00000000-0000-0000-0000-000000000001',
                'Admin',
                'admin@exemplo.com',
                '$2b$12$udNTRMgiIPeZur.5A2Xzd.0AwbJbhGPVDMnnLMaO/lb7rLs5.nWx6',
                TRUE
            )
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM usuarios
            WHERE email = 'admin@exemplo.com'
            """
        )
    )
