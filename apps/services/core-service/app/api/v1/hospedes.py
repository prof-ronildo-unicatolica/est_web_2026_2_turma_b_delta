from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.schemas.reserva import HospedeCreateSchema, HospedeResponseSchema
from app.services.reserva_service import (
    ConflitoDeDadosError,
    HospedeService,
    RecursoNaoEncontradoError,
)

router = APIRouter(prefix="/hospedes", tags=["Hospedes"])


@router.post(
    "", response_model=HospedeResponseSchema, status_code=status.HTTP_201_CREATED
)
def criar_hospede(
    payload: HospedeCreateSchema,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    if payload.email.strip().lower() != usuario_atual.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O e-mail do perfil deve corresponder à conta autenticada.",
        )
    try:
        return HospedeService(db).criar(
            nome=payload.nome,
            cpf=payload.cpf,
            email=usuario_atual.email,
            telefone=payload.telefone,
            usuario_id=usuario_atual.id,
        )
    except ConflitoDeDadosError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error


@router.get("/me", response_model=HospedeResponseSchema)
def buscar_meu_hospede(
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    try:
        return HospedeService(db).buscar_do_usuario(usuario_atual.id)
    except RecursoNaoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


@router.get("", response_model=list[HospedeResponseSchema])
def listar_hospedes(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return HospedeService(db).listar()


@router.get("/{hospede_id}", response_model=HospedeResponseSchema)
def buscar_hospede(
    hospede_id: uuid.UUID,
    db: Session = Depends(get_db),
    usuario_atual=Depends(get_current_user),
):
    try:
        hospede = HospedeService(db).buscar(hospede_id)
    except RecursoNaoEncontradoError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error
    if not usuario_atual.is_admin and hospede.usuario_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de hospede nao encontrado.",
        )
    return hospede
