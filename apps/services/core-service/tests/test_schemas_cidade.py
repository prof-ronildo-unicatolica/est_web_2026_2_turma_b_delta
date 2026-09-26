"""Testes dos schemas de Cidade (issue #11).

Valida o comportamento de CidadeCreateSchema e CidadeResponseSchema
conforme descrito na issue: entrada sem id, saída com id, validação
de nome, e suporte a objetos SQLAlchemy (from_attributes)."""

import uuid

import pytest
from pydantic import ValidationError

from app.schemas.hotel import CidadeCreateSchema, CidadeResponseSchema

# ---------------------------------------------------------------- Create

def test_create_aceita_nome_valido():
    schema = CidadeCreateSchema(nome="Fortaleza")
    assert schema.nome == "Fortaleza"


def test_create_nao_tem_campo_id():
    """Entrada não deve expor 'id' -- quem gera é o servidor."""
    assert "id" not in CidadeCreateSchema.model_fields


def test_create_rejeita_nome_vazio():
    """min_length=1 deve barrar string vazia."""
    with pytest.raises(ValidationError) as exc:
        CidadeCreateSchema(nome="")
    msg = exc.value.errors()[0]["msg"]
    assert "at least 1 character" in msg


def test_create_rejeita_nome_acima_de_100():
    """max_length=100 deve bater com o String(100) do model."""
    with pytest.raises(ValidationError):
        CidadeCreateSchema(nome="a" * 101)


def test_create_ignora_campos_desconhecidos():
    """Pydantic ignora extras por padrão -- 'id' enviado pelo cliente
    não deve causar erro nem virar atributo."""
    schema = CidadeCreateSchema(nome="Sobral", id="qualquer-coisa")  # type: ignore[call-arg]
    assert schema.nome == "Sobral"
    assert not hasattr(schema, "id")


# ---------------------------------------------------------------- Response

def test_response_tem_id_e_nome():
    campos = set(CidadeResponseSchema.model_fields.keys())
    assert campos == {"id", "nome"}


def test_response_id_e_uuid():
    """Declarar uuid.UUID (e não str) valida o formato."""
    cid = uuid.uuid4()
    schema = CidadeResponseSchema(id=cid, nome="Aquiraz")
    assert schema.id == cid
    assert isinstance(schema.id, uuid.UUID)


def test_response_rejeita_id_invalido():
    with pytest.raises(ValidationError):
        CidadeResponseSchema(id="nao-e-uuid", nome="Aquiraz")


def test_response_usa_from_attributes():
    """from_attributes=True permite montar o schema a partir de
    um objeto que tenha atributos .id e .nome (caso do SQLAlchemy)."""
    class FakeCidade:
        def __init__(self):
            self.id = uuid.uuid4()
            self.nome = "Maracanau"

    obj = FakeCidade()
    schema = CidadeResponseSchema.model_validate(obj)
    assert schema.id == obj.id
    assert schema.nome == "Maracanau"


def test_response_serializa_uuid_como_string_no_json():
    """O JSON de saída traz o id como string, não como objeto."""
    cid = uuid.uuid4()
    schema = CidadeResponseSchema(id=cid, nome="Caucaia")
    dados = schema.model_dump(mode="json")
    assert isinstance(dados["id"], str)
    assert dados["id"] == str(cid)