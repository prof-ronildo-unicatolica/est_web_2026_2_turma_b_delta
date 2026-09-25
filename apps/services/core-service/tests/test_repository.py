from app.repositories.hotel_repository import CidadeRepository
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


def test_create_cidade_in_repository(db_session):
    repo = CidadeRepository(db_session)

    cidade = repo.create(nome="Fortaleza")

    assert cidade.id is not None
    assert cidade.nome == "Fortaleza"


def test_list_cidades_in_repository_sorted_by_name(db_session):
    repo = CidadeRepository(db_session)

    repo.create(nome="Fortaleza")
    repo.create(nome="Quixadá")
    repo.create(nome="Baturité")

    cidades = repo.list()

    assert [cidade.nome for cidade in cidades] == [
        "Baturité",
        "Fortaleza",
        "Quixadá",
    ]


def test_get_cidade_by_id_in_repository(db_session):
    repo = CidadeRepository(db_session)

    cidade = repo.create(nome="Fortaleza")

    encontrada = repo.get_by_id(cidade.id)

    assert encontrada is not None
    assert encontrada.id == cidade.id
    assert encontrada.nome == "Fortaleza"


def test_get_cidade_by_nome_in_repository(db_session):
    repo = CidadeRepository(db_session)

    cidade = repo.create(nome="Fortaleza")

    encontrada = repo.get_by_nome("Fortaleza")

    assert encontrada is not None
    assert encontrada.id == cidade.id
    assert encontrada.nome == "Fortaleza"


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
