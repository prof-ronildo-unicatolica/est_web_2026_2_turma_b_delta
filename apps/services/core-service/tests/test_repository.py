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
