"""Casos complementares da issue #17 que não estavam cobertos por
`test_hotel_api.py`: validações de entrada e o filtro por cidade
inexistente."""

UUID_INEXISTENTE = "00000000-0000-0000-0000-000000000000"


def test_criar_hotel_sem_cidade_id_retorna_422(client):
    """`cidade_id` é obrigatório em HotelCreateSchema."""
    response = client.post("/api/v1/hoteis", json={"nome": "Hotel Sem Cidade"})
    assert response.status_code == 422


def test_criar_hotel_com_nome_vazio_retorna_422(client):
    """`nome` tem min_length=1 em HotelCreateSchema."""
    cidade = client.post("/api/v1/cidades", json={"nome": "Cidade Vazia"}).json()
    response = client.post(
        "/api/v1/hoteis",
        json={"nome": "", "cidade_id": cidade["id"]},
    )
    assert response.status_code == 422


def test_criar_hotel_com_cidade_id_invalido_retorna_422(client):
    """`cidade_id` precisa ser UUID -- string arbitrária deve dar 422."""
    response = client.post(
        "/api/v1/hoteis",
        json={"nome": "Hotel Fantasma", "cidade_id": "fortaleza"},
    )
    assert response.status_code == 422


def test_listar_hoteis_filtrando_por_cidade_inexistente_retorna_404(client):
    """UUID válido que não existe no banco -> 404, nunca 500."""
    response = client.get("/api/v1/hoteis", params={"cidade_id": UUID_INEXISTENTE})
    assert response.status_code == 404


def test_listar_hoteis_sem_registros_retorna_lista_vazia(client):
    """GET /hoteis em banco vazio -> 200 com []."""
    response = client.get("/api/v1/hoteis")
    assert response.status_code == 200
    assert response.json() == []


def test_listar_hoteis_sem_filtro_retorna_todos(client):
    """GET /hoteis sem query devolve todos, com cidade aninhada completa."""
    cidade_a = client.post("/api/v1/cidades", json={"nome": "Cidade A"}).json()
    cidade_b = client.post("/api/v1/cidades", json={"nome": "Cidade B"}).json()

    client.post("/api/v1/hoteis", json={"nome": "Hotel A", "cidade_id": cidade_a["id"]})
    client.post("/api/v1/hoteis", json={"nome": "Hotel B", "cidade_id": cidade_b["id"]})

    response = client.get("/api/v1/hoteis")
    assert response.status_code == 200

    corpo = response.json()
    assert len(corpo) == 2

    for hotel in corpo:
        assert set(hotel.keys()) == {"id", "nome", "cidade"}
        assert set(hotel["cidade"].keys()) == {"id", "nome"}