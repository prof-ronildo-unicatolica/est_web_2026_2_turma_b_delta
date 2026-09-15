from datetime import date, timedelta

import pytest

HOJE = date.today()
AMANHA = HOJE + timedelta(days=1)
DEPOIS = HOJE + timedelta(days=4)


def criar_hotel(client):
    cidade = client.post("/api/v1/cidades", json={"nome": "Quixada"}).json()
    return client.post(
        "/api/v1/hoteis", json={"nome": "Hotel Delta", "cidade_id": cidade["id"]}
    ).json()


def criar_quarto(client, hotel_id, numero="101", capacidade=2, preco="150.00"):
    return client.post(
        "/api/v1/quartos",
        json={
            "hotel_id": hotel_id,
            "numero": numero,
            "tipo": "standard",
            "capacidade": capacidade,
            "preco_diaria": preco,
        },
    )


def criar_hospede(client, cpf="12345678901", email="joao@teste.com"):
    return client.post(
        "/api/v1/hospedes",
        json={
            "nome": "Joao Victor",
            "cpf": cpf,
            "email": email,
            "telefone": "88999998888",
        },
    )


@pytest.fixture
def cenario(client):
    hotel = criar_hotel(client)
    quarto = criar_quarto(client, hotel["id"]).json()
    hospede = criar_hospede(client).json()
    return {"hotel": hotel, "quarto": quarto, "hospede": hospede}


def test_criar_hospede_returns_201(client):
    resposta = criar_hospede(client)
    assert resposta.status_code == 201
    assert resposta.json()["cpf"] == "12345678901"


def test_criar_hospede_com_cpf_duplicado_returns_409(client):
    criar_hospede(client)
    resposta = criar_hospede(client, email="outro@teste.com")
    assert resposta.status_code == 409


def test_criar_hospede_com_cpf_invalido_returns_422(client):
    resposta = client.post(
        "/api/v1/hospedes",
        json={"nome": "Teste", "cpf": "123", "email": "a@b.com"},
    )
    assert resposta.status_code == 422


def test_criar_quarto_returns_201(client):
    hotel = criar_hotel(client)
    resposta = criar_quarto(client, hotel["id"])
    assert resposta.status_code == 201
    assert resposta.json()["hotel"]["nome"] == "Hotel Delta"


def test_criar_quarto_com_numero_duplicado_returns_409(client):
    hotel = criar_hotel(client)
    criar_quarto(client, hotel["id"])
    resposta = criar_quarto(client, hotel["id"])
    assert resposta.status_code == 409


def test_criar_quarto_em_hotel_inexistente_returns_404(client):
    resposta = criar_quarto(client, "00000000-0000-0000-0000-000000000000")
    assert resposta.status_code == 404


def test_criar_reserva_calcula_valor_total(client, cenario):
    resposta = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
            "hospedes_quantidade": 2,
        },
    )
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["status"] == "pendente"
    assert float(corpo["valor_total"]) == 450.00


def test_criar_reserva_com_periodo_sobreposto_returns_409(client, cenario):
    payload = {
        "hospede_id": cenario["hospede"]["id"],
        "quarto_id": cenario["quarto"]["id"],
        "check_in": AMANHA.isoformat(),
        "check_out": DEPOIS.isoformat(),
        "hospedes_quantidade": 1,
    }
    assert client.post("/api/v1/reservas", json=payload).status_code == 201
    resposta = client.post("/api/v1/reservas", json=payload)
    assert resposta.status_code == 409


def test_criar_reserva_com_check_out_antes_do_check_in_returns_422(client, cenario):
    resposta = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": DEPOIS.isoformat(),
            "check_out": AMANHA.isoformat(),
        },
    )
    assert resposta.status_code == 422


def test_criar_reserva_no_passado_returns_422(client, cenario):
    resposta = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": (HOJE - timedelta(days=2)).isoformat(),
            "check_out": AMANHA.isoformat(),
        },
    )
    assert resposta.status_code == 422


def test_criar_reserva_acima_da_capacidade_returns_409(client, cenario):
    resposta = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
            "hospedes_quantidade": 5,
        },
    )
    assert resposta.status_code == 409


def test_criar_reserva_com_hospede_inexistente_returns_404(client, cenario):
    resposta = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": "00000000-0000-0000-0000-000000000000",
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
        },
    )
    assert resposta.status_code == 404


def test_confirmar_e_cancelar_reserva(client, cenario):
    reserva = client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
        },
    ).json()

    confirmada = client.patch(f"/api/v1/reservas/{reserva['id']}/confirmar")
    assert confirmada.status_code == 200
    assert confirmada.json()["status"] == "confirmada"

    assert (
        client.patch(f"/api/v1/reservas/{reserva['id']}/confirmar").status_code == 409
    )

    cancelada = client.patch(f"/api/v1/reservas/{reserva['id']}/cancelar")
    assert cancelada.status_code == 200
    assert cancelada.json()["status"] == "cancelada"

    assert client.patch(f"/api/v1/reservas/{reserva['id']}/cancelar").status_code == 409


def test_cancelamento_libera_o_quarto(client, cenario):
    payload = {
        "hospede_id": cenario["hospede"]["id"],
        "quarto_id": cenario["quarto"]["id"],
        "check_in": AMANHA.isoformat(),
        "check_out": DEPOIS.isoformat(),
    }
    reserva = client.post("/api/v1/reservas", json=payload).json()
    client.patch(f"/api/v1/reservas/{reserva['id']}/cancelar")
    assert client.post("/api/v1/reservas", json=payload).status_code == 201


def test_listar_quartos_disponiveis_exclui_quarto_reservado(client, cenario):
    criar_quarto(client, cenario["hotel"]["id"], numero="102")
    client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
        },
    )
    resposta = client.get(
        "/api/v1/quartos/disponiveis",
        params={
            "hotel_id": cenario["hotel"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
        },
    )
    assert resposta.status_code == 200
    numeros = [quarto["numero"] for quarto in resposta.json()]
    assert numeros == ["102"]


def test_filtrar_reservas_por_status(client, cenario):
    client.post(
        "/api/v1/reservas",
        json={
            "hospede_id": cenario["hospede"]["id"],
            "quarto_id": cenario["quarto"]["id"],
            "check_in": AMANHA.isoformat(),
            "check_out": DEPOIS.isoformat(),
        },
    )
    resposta = client.get("/api/v1/reservas", params={"status": "pendente"})
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert client.get("/api/v1/reservas", params={"status": "cancelada"}).json() == []


def test_buscar_reserva_inexistente_returns_404(client):
    resposta = client.get("/api/v1/reservas/00000000-0000-0000-0000-000000000000")
    assert resposta.status_code == 404
