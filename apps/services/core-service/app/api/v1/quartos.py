from __future__ import annotations

import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reserva import QuartoCreateSchema, QuartoResponseSchema
from app.services.reserva_service import QuartoService

router = APIRouter(prefix="/quartos", tags=["Quartos"])


@router.post(
    "", response_model=QuartoResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_quarto(payload: QuartoCreateSchema, db: Session = Depends(get_db)):
    return QuartoService(db).criar(
        hotel_id=payload.hotel_id,
        numero=payload.numero,
        tipo=payload.tipo,
        capacidade=payload.capacidade,
        preco_diaria=payload.preco_diaria,
    )


@router.get("", response_model=list[QuartoResponseSchema])
def listar_quartos(
    hotel_id: uuid.UUID | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return QuartoService(db).listar(hotel_id=hotel_id)


@router.get("/disponiveis", response_model=list[QuartoResponseSchema])
def listar_quartos_disponiveis(
    hotel_id: uuid.UUID = Query(),
    check_in: date = Query(),
    check_out: date = Query(),
    db: Session = Depends(get_db),
):
    return QuartoService(db).listar_disponiveis(
        hotel_id=hotel_id, check_in=check_in, check_out=check_out
    )


@router.get("/{quarto_id}", response_model=QuartoResponseSchema)
def buscar_quarto(quarto_id: uuid.UUID, db: Session = Depends(get_db)):
    return QuartoService(db).buscar(quarto_id)
