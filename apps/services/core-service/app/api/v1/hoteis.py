import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hotel import HotelCreateSchema, HotelResponseSchema
from app.services.hotel_service import CidadeNaoEncontradaError, HotelService

router = APIRouter(prefix="/hoteis", tags=["Hoteis"])


@router.post(
    "",
    response_model=HotelResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def criar_hotel(payload: HotelCreateSchema, db: Session = Depends(get_db)):
    try:
        return HotelService(db).criar(
            nome=payload.nome, cidade_id=payload.cidade_id
        )
    except CidadeNaoEncontradaError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error


@router.get("", response_model=list[HotelResponseSchema])
def listar_hoteis(
    cidade_id: uuid.UUID | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return HotelService(db).listar(cidade_id=cidade_id)
    except CidadeNaoEncontradaError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(error)
        ) from error
