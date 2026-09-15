import uuid

from pydantic import BaseModel, ConfigDict, Field


class CidadeCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class CidadeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class HotelCreateSchema(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    cidade_id: uuid.UUID


class HotelResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    cidade: CidadeResponseSchema


class CidadeComHoteisSchema(CidadeResponseSchema):
    hoteis: list[HotelResponseSchema] = Field(default_factory=list)
