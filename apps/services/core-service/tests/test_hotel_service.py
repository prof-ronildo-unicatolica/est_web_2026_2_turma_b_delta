import uuid

import pytest

from app.models.hotel import Cidade
from app.services.hotel_service import (
    CidadeJaExisteError,
    CidadeNaoEncontradaError,
    CidadeService,
    HotelService,
)


def test_cidade_service_criar_aplica_strip(db_session):
    service = CidadeService(db_session)

    cidade = service.criar("  Fortaleza  ")

    assert cidade.id is not None
    assert cidade.nome == "Fortaleza"


def test_cidade_service_rejeita_cidade_duplicada(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")

    with pytest.raises(CidadeJaExisteError):
        service.criar("Fortaleza")


def test_cidade_service_listar(db_session):
    service = CidadeService(db_session)

    service.criar("Fortaleza")
    service.criar("Sobral")

    cidades = service.listar()

    assert [cidade.nome for cidade in cidades] == ["Fortaleza", "Sobral"]


def test_hotel_service_criar_com_cidade_existente(db_session):
    cidade = Cidade(nome="Fortaleza")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    service = HotelService(db_session)

    hotel = service.criar("Hotel Teste", cidade.id)

    assert hotel.id is not None
    assert hotel.nome == "Hotel Teste"
    assert hotel.cidade_id == cidade.id


def test_hotel_service_rejeita_cidade_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(CidadeNaoEncontradaError):
        service.criar("Hotel Fantasma", uuid.uuid4())


def test_hotel_service_listar_todos(db_session):
    cidade = Cidade(nome="Fortaleza")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    service = HotelService(db_session)

    service.criar("Hotel A", cidade.id)
    service.criar("Hotel B", cidade.id)

    hotels = service.listar()

    assert [hotel.nome for hotel in hotels] == ["Hotel A", "Hotel B"]


def test_hotel_service_listar_por_cidade(db_session):
    cidade_fortaleza = Cidade(nome="Fortaleza")
    cidade_sobral = Cidade(nome="Sobral")
    db_session.add_all([cidade_fortaleza, cidade_sobral])
    db_session.commit()
    db_session.refresh(cidade_fortaleza)
    db_session.refresh(cidade_sobral)

    service = HotelService(db_session)

    service.criar("Hotel Fortaleza", cidade_fortaleza.id)
    service.criar("Hotel Sobral", cidade_sobral.id)

    hotels = service.listar(cidade_fortaleza.id)

    assert [hotel.nome for hotel in hotels] == ["Hotel Fortaleza"]


def test_hotel_service_listar_rejeita_cidade_inexistente(db_session):
    service = HotelService(db_session)

    with pytest.raises(CidadeNaoEncontradaError):
        service.listar(uuid.uuid4())
