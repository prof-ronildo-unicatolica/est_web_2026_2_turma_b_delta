from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.reserva import Hospede, Quarto, Reserva, StatusReserva


class HospedeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nome: str, cpf: str, email: str, telefone: str | None) -> Hospede:
        hospede = Hospede(nome=nome, cpf=cpf, email=email, telefone=telefone)
        self.db.add(hospede)
        self.db.commit()
        self.db.refresh(hospede)
        return hospede

    def listar(self) -> list[Hospede]:
        return self.db.query(Hospede).order_by(Hospede.nome).all()

    def get_by_id(self, hospede_id: uuid.UUID) -> Hospede | None:
        return self.db.query(Hospede).filter(Hospede.id == hospede_id).first()

    def get_by_cpf(self, cpf: str) -> Hospede | None:
        return self.db.query(Hospede).filter(Hospede.cpf == cpf).first()

    def get_by_email(self, email: str) -> Hospede | None:
        return self.db.query(Hospede).filter(Hospede.email == email).first()


class QuartoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        hotel_id: uuid.UUID,
        numero: str,
        tipo: str,
        capacidade: int,
        preco_diaria,
    ) -> Quarto:
        quarto = Quarto(
            hotel_id=hotel_id,
            numero=numero,
            tipo=tipo,
            capacidade=capacidade,
            preco_diaria=preco_diaria,
        )
        self.db.add(quarto)
        self.db.commit()
        self.db.refresh(quarto)
        return quarto

    def _base_query(self):
        return self.db.query(Quarto).options(joinedload(Quarto.hotel))

    def listar(self, hotel_id: uuid.UUID | None = None) -> list[Quarto]:
        consulta = self._base_query()
        if hotel_id is not None:
            consulta = consulta.filter(Quarto.hotel_id == hotel_id)
        return consulta.order_by(Quarto.numero).all()

    def get_by_id(self, quarto_id: uuid.UUID) -> Quarto | None:
        return self._base_query().filter(Quarto.id == quarto_id).first()

    def get_by_hotel_e_numero(self, hotel_id: uuid.UUID, numero: str) -> Quarto | None:
        return (
            self.db.query(Quarto)
            .filter(Quarto.hotel_id == hotel_id, Quarto.numero == numero)
            .first()
        )

    def listar_disponiveis(
        self, hotel_id: uuid.UUID, check_in: date, check_out: date
    ) -> list[Quarto]:
        ocupados = select(Reserva.quarto_id).where(
            Reserva.status.in_(StatusReserva.OCUPAM_QUARTO),
            Reserva.check_in < check_out,
            Reserva.check_out > check_in,
        )
        return (
            self._base_query()
            .filter(Quarto.hotel_id == hotel_id, ~Quarto.id.in_(ocupados))
            .order_by(Quarto.numero)
            .all()
        )


class ReservaRepository:
    def __init__(self, db: Session):
        self.db = db

    def _base_query(self):
        return self.db.query(Reserva).options(
            joinedload(Reserva.hospede),
            joinedload(Reserva.quarto).joinedload(Quarto.hotel),
        )

    def create(
        self,
        hospede_id: uuid.UUID,
        quarto_id: uuid.UUID,
        check_in: date,
        check_out: date,
        hospedes_quantidade: int,
        valor_total,
    ) -> Reserva:
        reserva = Reserva(
            hospede_id=hospede_id,
            quarto_id=quarto_id,
            check_in=check_in,
            check_out=check_out,
            hospedes_quantidade=hospedes_quantidade,
            valor_total=valor_total,
            status=StatusReserva.PENDENTE,
        )
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def listar(
        self,
        hospede_id: uuid.UUID | None = None,
        quarto_id: uuid.UUID | None = None,
        status: str | None = None,
    ) -> list[Reserva]:
        consulta = self._base_query()
        if hospede_id is not None:
            consulta = consulta.filter(Reserva.hospede_id == hospede_id)
        if quarto_id is not None:
            consulta = consulta.filter(Reserva.quarto_id == quarto_id)
        if status is not None:
            consulta = consulta.filter(Reserva.status == status)
        return consulta.order_by(Reserva.check_in).all()

    def get_by_id(self, reserva_id: uuid.UUID) -> Reserva | None:
        return self._base_query().filter(Reserva.id == reserva_id).first()

    def existe_conflito(
        self,
        quarto_id: uuid.UUID,
        check_in: date,
        check_out: date,
        ignorar_reserva_id: uuid.UUID | None = None,
    ) -> bool:
        consulta = self.db.query(Reserva).filter(
            Reserva.quarto_id == quarto_id,
            Reserva.status.in_(StatusReserva.OCUPAM_QUARTO),
            Reserva.check_in < check_out,
            Reserva.check_out > check_in,
        )
        if ignorar_reserva_id is not None:
            consulta = consulta.filter(Reserva.id != ignorar_reserva_id)
        return self.db.query(consulta.exists()).scalar()

    def atualizar_status(self, reserva: Reserva, status: str) -> Reserva:
        reserva.status = status
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
