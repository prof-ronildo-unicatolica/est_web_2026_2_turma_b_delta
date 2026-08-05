import uuid
from unittest.mock import patch

from app.repositories.tutorial_repository import TutorialRepository


# 1. Teste de 200 OK
def test_get_sobre_returns_200(client, db_session):
    repo = TutorialRepository(db_session)
    repo.create_professor(
        nome="Ronildo Silva",
        email="ronildo@ufc.br",
        sala="Sala 07",
        biografia="Professor",
    )

    response = client.get("/api/v1/sobre")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["equipe"] == "Alpha"
    assert json_data["professor"]["nome"] == "Ronildo Silva"


# 2. Teste de 404 Not Found
def test_get_professor_inexistente_returns_404(client):
    id_fake = uuid.uuid4()
    response = client.get(f"/api/v1/sobre/professores/{id_fake}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Professor nao encontrado"


# 3. Teste de 201 Created para Disciplina
@patch("app.services.tutorial_service.publish_event")
def test_criar_disciplina_returns_201(mock_publish, client, db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Ronildo Silva",
        email="ronildo@ufc.br",
        sala="Sala 07",
        biografia="Professor",
    )
    payload = {
        "nome": "Inteligencia Artificial",
        "ano": 2026,
        "semestre": 2,
        "professor_id": str(prof.id),
    }
    response = client.post("/api/v1/sobre/disciplinas", json=payload)
    assert response.status_code == 201
    assert response.json()["nome"] == "Inteligencia Artificial"
    mock_publish.assert_called_once()


# 4. Teste de 422 Unprocessable Entity para Disciplina
def test_criar_disciplina_com_dados_invalidos_returns_422(client):
    payload = {
        "nome": "Disciplina Sem Ano",
        "semestre": 2,
    }
    response = client.post("/api/v1/sobre/disciplinas", json=payload)
    assert response.status_code == 422


# 5. Teste de 500 Internal Server Error
def test_trigger_server_error_returns_500(client):
    response = client.get("/api/v1/debug/error")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
