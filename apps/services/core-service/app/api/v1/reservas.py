from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reserva import ReservaCreateSchema, ReservaResponseSchema
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "", response_model=ReservaResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_reserva(payload: ReservaCreateSchema, db: Session = Depends(get_db)):
    return ReservaService(db).criar(
        hospede_id=payload.hospede_id,
        quarto_id=payload.quarto_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
        hospedes_quantidade=payload.hospedes_quantidade,
    )


@router.get("", response_model=list[ReservaResponseSchema])
def listar_reservas(
    hospede_id: uuid.UUID | None = Query(default=None),
    quarto_id: uuid.UUID | None = Query(default=None),
    status_reserva: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    return ReservaService(db).listar(
        hospede_id=hospede_id, quarto_id=quarto_id, status=status_reserva
    )


@router.get("/{reserva_id}", response_model=ReservaResponseSchema)
def buscar_reserva(reserva_id: uuid.UUID, db: Session = Depends(get_db)):
    return ReservaService(db).buscar(reserva_id)


@router.patch("/{reserva_id}/confirmar", response_model=ReservaResponseSchema)
def confirmar_reserva(reserva_id: uuid.UUID, db: Session = Depends(get_db)):
    return ReservaService(db).confirmar(reserva_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponseSchema)
def cancelar_reserva(reserva_id: uuid.UUID, db: Session = Depends(get_db)):
    return ReservaService(db).cancelar(reserva_id)
