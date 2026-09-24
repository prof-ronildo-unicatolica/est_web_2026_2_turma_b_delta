def test_cidades_cria_lista_e_rejeita_duplicada(client):
    primeira = client.post("/api/v1/cidades", json={"nome": "Sobral"})
    segunda = client.post("/api/v1/cidades", json={"nome": "Fortaleza"})
    duplicada = client.post("/api/v1/cidades", json={"nome": "Sobral"})

    assert primeira.status_code == 201
    assert segunda.status_code == 201
    assert duplicada.status_code == 409
    assert [cidade["nome"] for cidade in client.get("/api/v1/cidades").json()] == [
        "Fortaleza",
        "Sobral",
    ]


def test_cidade_com_nome_vazio_retorna_422(client):
    response = client.post("/api/v1/cidades", json={"nome": ""})
    assert response.status_code == 422


def test_hotel_cria_com_cidade_aninhada_e_filtra_por_cidade(client):
    cidade = client.post("/api/v1/cidades", json={"nome": "Aquiraz"}).json()
    outro = client.post("/api/v1/cidades", json={"nome": "Quixada"}).json()

    hotel = client.post(
        "/api/v1/hoteis",
        json={"nome": "Hotel Praia Bela", "cidade_id": cidade["id"]},
    )
    client.post(
        "/api/v1/hoteis",
        json={"nome": "Hotel Central", "cidade_id": outro["id"]},
    )

    assert hotel.status_code == 201
    assert hotel.json()["cidade"] == cidade
    assert len(client.get("/api/v1/hoteis").json()) == 2
    filtrados = client.get(
        "/api/v1/hoteis", params={"cidade_id": cidade["id"]}
    )
    assert filtrados.status_code == 200
    assert [item["nome"] for item in filtrados.json()] == ["Hotel Praia Bela"]


def test_hotel_com_cidade_inexistente_retorna_404(client):
    response = client.post(
        "/api/v1/hoteis",
        json={
            "nome": "Hotel Fantasma",
            "cidade_id": "00000000-0000-0000-0000-000000000000",
        },
    )
    assert response.status_code == 404


def test_hotel_com_cidade_id_invalido_retorna_422(client):
    response = client.get("/api/v1/hoteis", params={"cidade_id": "fortaleza"})
    assert response.status_code == 422
