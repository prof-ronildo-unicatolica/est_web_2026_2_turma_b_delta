import uuid
from typing import Any
from sqlalchemy.orm import Session, joinedload

from app.models.tutorial import (
    Disciplina,
    Professor,
    ProfessorDetail,
    Stack,
    Tecnologia,
)


class TutorialRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_professor_with_details(self) -> list[Professor]:
        return (
            self.db.query(Professor)
            .options(
                joinedload(Professor.detalhe),
                joinedload(Professor.disciplinas).joinedload(Disciplina.tecnologias),
            )
            .all()
        )

    def get_stacks_with_tecnologias(self) -> list[Stack]:
        return (
            self.db.query(Stack)
            .options(joinedload(Stack.tecnologias).joinedload(Tecnologia.linguagens))
            .all()
        )

    def get_professor_by_id(self, professor_id) -> Professor | None:
        return (
            self.db.query(Professor)
            .options(joinedload(Professor.detalhe))
            .filter(Professor.id == professor_id)
            .first()
        )

    def create_professor(
        self,
        nome: str,
        email: str,
        sala: str,
        biografia: str = None,
        biografia_mapa: dict = None,
    ) -> Professor:
        prof = Professor(nome=nome, email=email)
        self.db.add(prof)
        self.db.flush()

        detail = ProfessorDetail(
            professor_id=prof.id,
            sala=sala,
            biografia=biografia,
            biografia_mapa=biografia_mapa,
        )
        self.db.add(detail)
        self.db.commit()
        self.db.refresh(prof)
        return prof

    def create_disciplina(
        self,
        nome: str,
        ano: int,
        semestre: int,
        professor_id: Any,
    ) -> Disciplina:
        if isinstance(professor_id, str):
            professor_id = uuid.UUID(professor_id)
        disciplina = Disciplina(
            nome=nome,
            ano=ano,
            semestre=semestre,
            professor_id=professor_id,
        )
        self.db.add(disciplina)
        self.db.commit()
        self.db.refresh(disciplina)
        return disciplina
