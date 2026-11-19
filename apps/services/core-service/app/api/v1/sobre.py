import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.schemas.tutorial import (
    DisciplinaCreateSchema,
    DisciplinaResponseSimpleSchema,
    ProfessorBaseSchema,
    SobreResponseSchema,
)
from app.services.tutorial_service import TutorialService

router = APIRouter()


@router.get("/sobre", response_model=SobreResponseSchema)
def get_sobre(db: Session = Depends(get_db)):
    service = TutorialService(db)
    return service.get_sobre_data()


@router.get("/sobre/professores/{professor_id}", response_model=ProfessorBaseSchema)
def get_professor_por_id(professor_id: uuid.UUID, db: Session = Depends(get_db)):
    service = TutorialService(db)
    prof = service.get_professor_by_id(professor_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor nao encontrado")
    return prof


@router.post("/sobre/disciplinas", response_model=DisciplinaResponseSimpleSchema, status_code=201)
async def criar_disciplina(
    payload: DisciplinaCreateSchema,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    service = TutorialService(db)
    return await service.create_disciplina(payload)
