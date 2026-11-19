from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.repositories.reserva_repository import HospedeRepository
from app.schemas.reserva import ReservaCreateSchema, ReservaResponseSchema
from app.services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post(
    "", response_model=ReservaResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_reserva(
    payload: ReservaCreateSchema,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    return ReservaService(db).criar(
        usuario_id=usuario_atual.id,
        hospede_id=payload.hospede_id,
        quarto_id=payload.quarto_id,
        check_in=payload.check_in,
        check_out=payload.check_out,
        hospedes_quantidade=payload.hospedes_quantidade,
        is_admin=usuario_atual.is_admin,
    )


@router.get("", response_model=list[ReservaResponseSchema])
def listar_reservas(
    hospede_id: uuid.UUID | None = Query(default=None),
    quarto_id: uuid.UUID | None = Query(default=None),
    status_reserva: str | None = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    if not usuario_atual.is_admin:
        hospede = HospedeRepository(db).get_by_usuario_id(usuario_atual.id)
        if hospede is None:
            return []
        hospede_id = hospede.id

    return ReservaService(db).listar(
        hospede_id=hospede_id, quarto_id=quarto_id, status=status_reserva
    )


@router.get("/{reserva_id}", response_model=ReservaResponseSchema)
def buscar_reserva(
    reserva_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    reserva = ReservaService(db).buscar(reserva_id)
    if not usuario_atual.is_admin and reserva.hospede.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada.")
    return reserva


@router.patch("/{reserva_id}/confirmar", response_model=ReservaResponseSchema)
def confirmar_reserva(
    reserva_id: uuid.UUID,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return ReservaService(db).confirmar(reserva_id)


@router.patch("/{reserva_id}/cancelar", response_model=ReservaResponseSchema)
def cancelar_reserva(
    reserva_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    reserva = ReservaService(db).buscar(reserva_id)
    if not usuario_atual.is_admin and reserva.hospede.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada.")
    return ReservaService(db).cancelar(reserva_id)
