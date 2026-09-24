from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.hotel import Hotel
from app.models.tutorial import Base


class StatusReserva:
    PENDENTE = "pendente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluida"

    TODOS = (PENDENTE, CONFIRMADA, CANCELADA, CONCLUIDA)
    OCUPAM_QUARTO = (PENDENTE, CONFIRMADA)


class Hospede(Base):
    __tablename__ = "hospedes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    reservas: Mapped[list[Reserva]] = relationship(
        back_populates="hospede", cascade="all, delete-orphan"
    )


class Quarto(Base):
    __tablename__ = "quartos"
    __table_args__ = (
        UniqueConstraint("hotel_id", "numero", name="uq_quartos_hotel_numero"),
        CheckConstraint("capacidade > 0", name="ck_quartos_capacidade_positiva"),
        CheckConstraint("preco_diaria > 0", name="ck_quartos_preco_positivo"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    hotel_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hoteis.id", ondelete="CASCADE"), nullable=False, index=True
    )
    numero: Mapped[str] = mapped_column(String(10), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco_diaria: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    hotel: Mapped[Hotel] = relationship()
    reservas: Mapped[list[Reserva]] = relationship(
        back_populates="quarto", cascade="all, delete-orphan"
    )


class Reserva(Base):
    __tablename__ = "reservas"
    __table_args__ = (
        CheckConstraint("check_out > check_in", name="ck_reservas_periodo_valido"),
        CheckConstraint(
            "hospedes_quantidade > 0", name="ck_reservas_hospedes_positivo"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    hospede_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hospedes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    quarto_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("quartos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    check_in: Mapped[date] = mapped_column(Date, nullable=False)
    check_out: Mapped[date] = mapped_column(Date, nullable=False)
    hospedes_quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=StatusReserva.PENDENTE, index=True
    )
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    criada_em: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    hospede: Mapped[Hospede] = relationship(back_populates="reservas")
    quarto: Mapped[Quarto] = relationship(back_populates="reservas")
