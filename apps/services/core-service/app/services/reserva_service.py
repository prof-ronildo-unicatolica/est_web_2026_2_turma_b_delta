from __future__ import annotations

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.reserva import Hospede, Quarto, Reserva, StatusReserva
from app.repositories.hotel_repository import HotelRepository
from app.repositories.reserva_repository import (
    HospedeRepository,
    QuartoRepository,
    ReservaRepository,
)


class RegraDeNegocioError(Exception):
    pass


class RecursoNaoEncontradoError(RegraDeNegocioError):
    pass


class ConflitoDeDadosError(RegraDeNegocioError):
    pass


class PeriodoInvalidoError(RegraDeNegocioError):
    pass


class QuartoIndisponivelError(RegraDeNegocioError):
    pass


class TransicaoDeStatusInvalidaError(RegraDeNegocioError):
    pass


class HospedeService:
    def __init__(self, db: Session):
        self.repository = HospedeRepository(db)

    def criar(self, nome: str, cpf: str, email: str, telefone: str | None) -> Hospede:
        nome = nome.strip()
        email = email.strip().lower()
        if self.repository.get_by_cpf(cpf):
            raise ConflitoDeDadosError(f"Ja existe um hospede com o CPF {cpf}.")
        if self.repository.get_by_email(email):
            raise ConflitoDeDadosError(f"Ja existe um hospede com o e-mail {email}.")
        return self.repository.create(
            nome=nome, cpf=cpf, email=email, telefone=telefone
        )

    def listar(self) -> list[Hospede]:
        return self.repository.listar()

    def buscar(self, hospede_id: uuid.UUID) -> Hospede:
        hospede = self.repository.get_by_id(hospede_id)
        if hospede is None:
            raise RecursoNaoEncontradoError(
                f"Nao existe hospede com id '{hospede_id}'."
            )
        return hospede


class QuartoService:
    def __init__(self, db: Session):
        self.repository = QuartoRepository(db)
        self.hoteis = HotelRepository(db)

    def criar(
        self,
        hotel_id: uuid.UUID,
        numero: str,
        tipo: str,
        capacidade: int,
        preco_diaria: Decimal,
    ) -> Quarto:
        numero = numero.strip()
        tipo = tipo.strip().lower()
        if not self.hoteis.get_by_id(hotel_id):
            raise RecursoNaoEncontradoError(f"Nao existe hotel com id '{hotel_id}'.")
        if self.repository.get_by_hotel_e_numero(hotel_id, numero):
            raise ConflitoDeDadosError(
                f"O quarto '{numero}' ja esta cadastrado nesse hotel."
            )
        return self.repository.create(
            hotel_id=hotel_id,
            numero=numero,
            tipo=tipo,
            capacidade=capacidade,
            preco_diaria=preco_diaria,
        )

    def listar(self, hotel_id: uuid.UUID | None = None) -> list[Quarto]:
        if hotel_id is not None and not self.hoteis.get_by_id(hotel_id):
            raise RecursoNaoEncontradoError(f"Nao existe hotel com id '{hotel_id}'.")
        return self.repository.listar(hotel_id=hotel_id)

    def buscar(self, quarto_id: uuid.UUID) -> Quarto:
        quarto = self.repository.get_by_id(quarto_id)
        if quarto is None:
            raise RecursoNaoEncontradoError(f"Nao existe quarto com id '{quarto_id}'.")
        return quarto

    def listar_disponiveis(
        self, hotel_id: uuid.UUID, check_in: date, check_out: date
    ) -> list[Quarto]:
        validar_periodo(check_in, check_out)
        if not self.hoteis.get_by_id(hotel_id):
            raise RecursoNaoEncontradoError(f"Nao existe hotel com id '{hotel_id}'.")
        return self.repository.listar_disponiveis(hotel_id, check_in, check_out)


def validar_periodo(check_in: date, check_out: date) -> int:
    if check_out <= check_in:
        raise PeriodoInvalidoError(
            "A data de check-out deve ser posterior a data de check-in."
        )
    if check_in < date.today():
        raise PeriodoInvalidoError("A data de check-in nao pode estar no passado.")
    return (check_out - check_in).days


class ReservaService:
    def __init__(self, db: Session):
        self.repository = ReservaRepository(db)
        self.hospedes = HospedeRepository(db)
        self.quartos = QuartoRepository(db)

    def criar(
        self,
        hospede_id: uuid.UUID,
        quarto_id: uuid.UUID,
        check_in: date,
        check_out: date,
        hospedes_quantidade: int,
    ) -> Reserva:
        diarias = validar_periodo(check_in, check_out)

        if self.hospedes.get_by_id(hospede_id) is None:
            raise RecursoNaoEncontradoError(
                f"Nao existe hospede com id '{hospede_id}'."
            )

        quarto = self.quartos.get_by_id(quarto_id)
        if quarto is None:
            raise RecursoNaoEncontradoError(f"Nao existe quarto com id '{quarto_id}'.")

        if hospedes_quantidade > quarto.capacidade:
            raise QuartoIndisponivelError(
                f"O quarto comporta ate {quarto.capacidade} hospede(s)."
            )

        if self.repository.existe_conflito(quarto_id, check_in, check_out):
            raise QuartoIndisponivelError(
                "O quarto ja possui uma reserva ativa nesse periodo."
            )

        valor_total = Decimal(quarto.preco_diaria) * diarias
        return self.repository.create(
            hospede_id=hospede_id,
            quarto_id=quarto_id,
            check_in=check_in,
            check_out=check_out,
            hospedes_quantidade=hospedes_quantidade,
            valor_total=valor_total,
        )

    def listar(
        self,
        hospede_id: uuid.UUID | None = None,
        quarto_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list[Reserva]:
        if status is not None and status not in StatusReserva.TODOS:
            raise PeriodoInvalidoError(
                f"Status invalido. Use um destes: {', '.join(StatusReserva.TODOS)}."
            )
        return self.repository.listar(
            hospede_id=hospede_id, quarto_id=quarto_id, status=status
        )

    def buscar(self, reserva_id: uuid.UUID) -> Reserva:
        reserva = self.repository.get_by_id(reserva_id)
        if reserva is None:
            raise RecursoNaoEncontradoError(
                f"Nao existe reserva com id '{reserva_id}'."
            )
        return reserva

    def confirmar(self, reserva_id: uuid.UUID) -> Reserva:
        reserva = self.buscar(reserva_id)
        if reserva.status != StatusReserva.PENDENTE:
            raise TransicaoDeStatusInvalidaError(
                f"So e possivel confirmar reservas pendentes. Status atual: "
                f"{reserva.status}."
            )
        return self.repository.atualizar_status(reserva, StatusReserva.CONFIRMADA)

    def cancelar(self, reserva_id: uuid.UUID) -> Reserva:
        reserva = self.buscar(reserva_id)
        if reserva.status not in StatusReserva.OCUPAM_QUARTO:
            raise TransicaoDeStatusInvalidaError(
                f"Nao e possivel cancelar uma reserva com status {reserva.status}."
            )
        return self.repository.atualizar_status(reserva, StatusReserva.CANCELADA)
