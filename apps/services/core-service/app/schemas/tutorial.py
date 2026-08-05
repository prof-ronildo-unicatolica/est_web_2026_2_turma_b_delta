from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ProfessorBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    email: str
    sala: str
    biografia: Optional[str] = None
    biografia_mapa: Optional[Dict[str, Any]] = None


class DisciplinaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    ano: int
    semestre: int
    tecnologias: List[str]


class TecnologiaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    linguagens: List[str]


class StackResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    tecnologias: List[TecnologiaResponseSchema]


class SobreResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    equipe: str
    ano: int
    semestre: int
    professor: Optional[ProfessorBaseSchema] = None
    disciplinas: List[DisciplinaResponseSchema]
    stacks: List[StackResponseSchema]


class ProfessorCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    email: str
    sala: str
    biografia: Optional[str] = None
    biografia_mapa: Optional[Dict[str, Any]] = None


class DisciplinaCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
    ano: int
    semestre: int
    professor_id: Any = "bed023d2-c85c-4973-9c3d-79d77a5519f1"


class DisciplinaResponseSimpleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Any
    nome: str
    ano: int
    semestre: int
    professor_id: Any
