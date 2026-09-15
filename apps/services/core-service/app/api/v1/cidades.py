from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.hotel import CidadeCreateSchema, CidadeResponseSchema
from app.services.hotel_service import CidadeJaExisteError, CidadeService

router = APIRouter(prefix="/cidades", tags=["Cidades"])


@router.post(
    "",
    response_model=CidadeResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def criar_cidade(payload: CidadeCreateSchema, db: Session = Depends(get_db)):
    try:
        return CidadeService(db).criar(nome=payload.nome)
    except CidadeJaExisteError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(error)
        ) from error


@router.get("", response_model=list[CidadeResponseSchema])
def listar_cidades(db: Session = Depends(get_db)):
    return CidadeService(db).listar()
