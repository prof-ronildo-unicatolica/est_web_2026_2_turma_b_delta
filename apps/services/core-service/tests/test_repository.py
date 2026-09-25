from sqlalchemy import event

from app.models.hotel import Cidade
from app.repositories.hotel_repository import HotelRepository
from app.repositories.tutorial_repository import TutorialRepository


def test_create_professor_in_repository(db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Professor de Teste",
        email="teste@unicatolica.edu.br",
        sala="Sala Teste, Bloco T",
        biografia="Uma biografia de teste.",
    )

    assert prof.id is not None
    assert prof.nome == "Professor de Teste"
    assert prof.email == "teste@unicatolica.edu.br"
    assert prof.detalhe is not None
    assert prof.detalhe.sala == "Sala Teste, Bloco T"
    assert prof.detalhe.biografia == "Uma biografia de teste."


def test_get_professor_by_id_in_repository(db_session):
    repo = TutorialRepository(db_session)
    created_prof = repo.create_professor(
        nome="Outro Prof",
        email="outro@unicatolica.edu.br",
        sala="Sala B",
    )

    fetched_prof = repo.get_professor_by_id(created_prof.id)
    assert fetched_prof is not None
    assert fetched_prof.id == created_prof.id
    assert fetched_prof.nome == "Outro Prof"


def test_create_hotel_in_repository(db_session):
    cidade = Cidade(nome="Fortaleza")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)
    hotel = repo.create(nome="Hotel de Teste", cidade_id=cidade.id)

    assert hotel.id is not None
    assert hotel.nome == "Hotel de Teste"
    assert hotel.cidade_id == cidade.id


def test_list_hotels_in_repository(db_session):
    cidade = Cidade(nome="Sobral")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)
    repo.create(nome="Hotel A", cidade_id=cidade.id)
    repo.create(nome="Hotel B", cidade_id=cidade.id)

    hotels = repo.list()

    assert len(hotels) == 2
    assert hotels[0].nome == "Hotel A"
    assert hotels[1].nome == "Hotel B"
    assert hotels[0].cidade.id == cidade.id
    assert hotels[1].cidade.id == cidade.id


def test_list_hotels_by_cidade_in_repository(db_session):
    cidade_fortaleza = Cidade(nome="Fortaleza")
    cidade_sobral = Cidade(nome="Sobral")
    db_session.add_all([cidade_fortaleza, cidade_sobral])
    db_session.commit()
    db_session.refresh(cidade_fortaleza)
    db_session.refresh(cidade_sobral)

    repo = HotelRepository(db_session)
    repo.create(nome="Hotel Fortaleza 1", cidade_id=cidade_fortaleza.id)
    repo.create(nome="Hotel Fortaleza 2", cidade_id=cidade_fortaleza.id)
    repo.create(nome="Hotel Sobral", cidade_id=cidade_sobral.id)

    hotels = repo.list_by_cidade(cidade_fortaleza.id)

    assert len(hotels) == 2
    assert all(hotel.cidade_id == cidade_fortaleza.id for hotel in hotels)
    assert all(hotel.cidade.id == cidade_fortaleza.id for hotel in hotels)


def test_get_hotel_by_id_in_repository(db_session):
    cidade = Cidade(nome="Quixadá")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)
    created_hotel = repo.create(nome="Hotel Quixadá", cidade_id=cidade.id)

    hotel = repo.get_by_id(created_hotel.id)

    assert hotel is not None
    assert hotel.id == created_hotel.id
    assert hotel.nome == "Hotel Quixadá"
    assert hotel.cidade_id == cidade.id
    assert hotel.cidade.id == cidade.id


def test_list_hotels_uses_joinedload_for_cidade(db_session):
    cidade = Cidade(nome="Baturité")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    repo = HotelRepository(db_session)
    repo.create(nome="Hotel 1", cidade_id=cidade.id)
    repo.create(nome="Hotel 2", cidade_id=cidade.id)

    statements = []

    def count_selects(conn, cursor, statement, parameters, context, executemany):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(db_session.bind, "before_cursor_execute", count_selects)

    try:
        hotels = repo.list()

        for hotel in hotels:
            _ = hotel.cidade.nome
    finally:
        event.remove(db_session.bind, "before_cursor_execute", count_selects)

    assert len(statements) == 1
