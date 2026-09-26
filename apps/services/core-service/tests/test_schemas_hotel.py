import uuid

import pytest
from pydantic import ValidationError

from app.schemas.hotel import (
    CidadeComHoteisSchema,
    CidadeResponseSchema,
    HotelCreateSchema,
    HotelResponseSchema,
)


def test_hotel_create_aceita_nome_e_cidade_id():
    cidade_id = uuid.uuid4()

    schema = HotelCreateSchema(nome="Hotel Beira-Mar", cidade_id=cidade_id)

    assert schema.nome == "Hotel Beira-Mar"
    assert schema.cidade_id == cidade_id
    assert "id" not in schema.model_fields


def test_hotel_create_rejeita_cidade_id_invalido():
    with pytest.raises(ValidationError):
        HotelCreateSchema(nome="Hotel Beira-Mar", cidade_id="fortaleza")


def test_hotel_create_rejeita_nome_vazio():
    with pytest.raises(ValidationError):
        HotelCreateSchema(nome="", cidade_id=uuid.uuid4())


def test_hotel_response_tem_cidade_aninhada():
    cidade_id = uuid.uuid4()
    hotel_id = uuid.uuid4()

    schema = HotelResponseSchema(
        id=hotel_id,
        nome="Hotel Beira-Mar",
        cidade=CidadeResponseSchema(id=cidade_id, nome="Fortaleza"),
    )

    assert schema.cidade.id == cidade_id
    assert schema.cidade.nome == "Fortaleza"
    assert schema.model_dump(mode="json")["cidade"] == {
        "id": str(cidade_id),
        "nome": "Fortaleza",
    }


def test_hotel_response_le_objeto_com_cidade_aninhada():
    class FakeCidade:
        id = uuid.uuid4()
        nome = "Fortaleza"

    class FakeHotel:
        id = uuid.uuid4()
        nome = "Hotel Beira-Mar"
        cidade = FakeCidade()

    schema = HotelResponseSchema.model_validate(FakeHotel())

    assert schema.id == FakeHotel.id
    assert schema.nome == "Hotel Beira-Mar"
    assert schema.cidade.id == FakeCidade.id
    assert schema.cidade.nome == "Fortaleza"


def test_cidade_com_hoteis_inicia_com_lista_vazia():
    cidade = CidadeComHoteisSchema(id=uuid.uuid4(), nome="Fortaleza")

    assert cidade.hoteis == []


def test_cidade_com_hoteis_nao_compartilha_lista():
    primeira = CidadeComHoteisSchema(id=uuid.uuid4(), nome="Fortaleza")
    segunda = CidadeComHoteisSchema(id=uuid.uuid4(), nome="Sobral")

    primeira.hoteis.append(
        HotelResponseSchema(
            id=uuid.uuid4(),
            nome="Hotel Beira-Mar",
            cidade=CidadeResponseSchema(id=primeira.id, nome=primeira.nome),
        )
    )

    assert len(primeira.hoteis) == 1
    assert segunda.hoteis == []