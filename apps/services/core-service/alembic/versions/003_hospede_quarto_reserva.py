"""cria as tabelas hospedes, quartos e reservas"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hospedes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("telefone", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cpf"),
        sa.UniqueConstraint("email"),
    )

    op.create_table(
        "quartos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("hotel_id", sa.UUID(), nullable=False),
        sa.Column("numero", sa.String(length=10), nullable=False),
        sa.Column("tipo", sa.String(length=20), nullable=False),
        sa.Column("capacidade", sa.Integer(), nullable=False),
        sa.Column("preco_diaria", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["hotel_id"], ["hoteis.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hotel_id", "numero", name="uq_quartos_hotel_numero"),
        sa.CheckConstraint("capacidade > 0", name="ck_quartos_capacidade_positiva"),
        sa.CheckConstraint("preco_diaria > 0", name="ck_quartos_preco_positivo"),
    )
    op.create_index("ix_quartos_hotel_id", "quartos", ["hotel_id"])

    op.create_table(
        "reservas",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("hospede_id", sa.UUID(), nullable=False),
        sa.Column("quarto_id", sa.UUID(), nullable=False),
        sa.Column("check_in", sa.Date(), nullable=False),
        sa.Column("check_out", sa.Date(), nullable=False),
        sa.Column("hospedes_quantidade", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("valor_total", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "criada_em",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(["hospede_id"], ["hospedes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["quarto_id"], ["quartos.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint("check_out > check_in", name="ck_reservas_periodo_valido"),
        sa.CheckConstraint(
            "hospedes_quantidade > 0", name="ck_reservas_hospedes_positivo"
        ),
    )
    op.create_index("ix_reservas_hospede_id", "reservas", ["hospede_id"])
    op.create_index("ix_reservas_quarto_id", "reservas", ["quarto_id"])
    op.create_index("ix_reservas_status", "reservas", ["status"])


def downgrade() -> None:
    op.drop_index("ix_reservas_status", table_name="reservas")
    op.drop_index("ix_reservas_quarto_id", table_name="reservas")
    op.drop_index("ix_reservas_hospede_id", table_name="reservas")
    op.drop_table("reservas")
    op.drop_index("ix_quartos_hotel_id", table_name="quartos")
    op.drop_table("quartos")
    op.drop_table("hospedes")
