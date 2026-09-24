from __future__ import annotations

import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.hotel import HotelResponseSchema


class HospedeCreateSchema(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    cpf: str = Field(min_length=11, max_length=14)
    email: EmailStr
    telefone: str | None = Field(default=None, max_length=20)

    @field_validator("cpf")
    @classmethod
    def normalizar_cpf(cls, valor: str) -> str:
        digitos = "".join(caractere for caractere in valor if caractere.isdigit())
        if len(digitos) != 11:
            raise ValueError("O CPF deve conter exatamente 11 digitos.")
        return digitos


class HospedeResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    cpf: str
    email: EmailStr
    telefone: str | None = None


class QuartoCreateSchema(BaseModel):
    hotel_id: uuid.UUID
    numero: str = Field(min_length=1, max_length=10)
    tipo: str = Field(min_length=3, max_length=20)
    capacidade: int = Field(gt=0, le=10)
    preco_diaria: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class QuartoResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    numero: str
    tipo: str
    capacidade: int
    preco_diaria: Decimal
    hotel: HotelResponseSchema


class ReservaCreateSchema(BaseModel):
    hospede_id: uuid.UUID
    quarto_id: uuid.UUID
    check_in: date
    check_out: date
    hospedes_quantidade: int = Field(default=1, gt=0, le=10)


class ReservaResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    check_in: date
    check_out: date
    hospedes_quantidade: int
    status: str
    valor_total: Decimal
    criada_em: datetime
    hospede: HospedeResponseSchema
    quarto: QuartoResponseSchema
