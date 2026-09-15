"""cria as tabelas cidades e hoteis"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cidades",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )
    op.create_table(
        "hoteis",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("cidade_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["cidade_id"], ["cidades.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_hoteis_cidade_id", "hoteis", ["cidade_id"])


def downgrade() -> None:
    op.drop_index("ix_hoteis_cidade_id", table_name="hoteis")
    op.drop_table("hoteis")
    op.drop_table("cidades")
