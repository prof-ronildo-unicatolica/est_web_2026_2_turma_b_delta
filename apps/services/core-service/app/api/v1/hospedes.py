from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reserva import HospedeCreateSchema, HospedeResponseSchema
from app.services.reserva_service import HospedeService

router = APIRouter(prefix="/hospedes", tags=["Hospedes"])


@router.post(
    "", response_model=HospedeResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_hospede(payload: HospedeCreateSchema, db: Session = Depends(get_db)):
    return HospedeService(db).criar(
        nome=payload.nome,
        cpf=payload.cpf,
        email=payload.email,
        telefone=payload.telefone,
    )


@router.get("", response_model=list[HospedeResponseSchema])
def listar_hospedes(db: Session = Depends(get_db)):
    return HospedeService(db).listar()


@router.get("/{hospede_id}", response_model=HospedeResponseSchema)
def buscar_hospede(hospede_id: uuid.UUID, db: Session = Depends(get_db)):
    return HospedeService(db).buscar(hospede_id)
