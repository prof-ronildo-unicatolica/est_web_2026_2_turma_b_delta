"""Casos complementares das rotas de Cidade (issue #16) que não estavam
cobertos por `test_hotel_api.py`. Complementa, não substitui."""


def test_criar_cidade_sem_nome_retorna_422(client):
    """`nome` é obrigatório em CidadeCreateSchema."""
    response = client.post("/api/v1/cidades", json={})
    assert response.status_code == 422


def test_criar_cidade_com_nome_muito_longo_retorna_422(client):
    """`max_length=100` do schema deve barrar nome com 101 caracteres."""
    response = client.post("/api/v1/cidades", json={"nome": "a" * 101})
    assert response.status_code == 422


def test_criar_cidade_devolve_recurso_com_id_e_nome(client):
    """201 Created devolve o recurso criado (id + nome), não vazio."""
    response = client.post("/api/v1/cidades", json={"nome": "São Gonçalo"})
    assert response.status_code == 201

    corpo = response.json()
    assert set(corpo.keys()) == {"id", "nome"}
    assert corpo["nome"] == "São Gonçalo"
    assert corpo["id"]


def test_listar_cidades_em_banco_vazio_retorna_lista_vazia(client):
    """GET /cidades sem registros -> 200 com lista vazia, não 500."""
    response = client.get("/api/v1/cidades")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_cidades_apos_criar_varias_em_ordem_alfabetica(client):
    """GET /cidades devolve em ordem alfabética, independente da ordem de criação."""
    for nome in ["Caucaia", "Aquiraz", "Sobral", "Maracanau"]:
        client.post("/api/v1/cidades", json={"nome": nome})

    response = client.get("/api/v1/cidades")
    assert response.status_code == 200

    nomes = [c["nome"] for c in response.json()]
    assert nomes == sorted(nomes)
    assert nomes == ["Aquiraz", "Caucaia", "Maracanau", "Sobral"]