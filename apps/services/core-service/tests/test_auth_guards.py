from datetime import date, timedelta

from app.core.database import get_mongo_db
from app.main import app


def test_catalog_writes_require_an_administrator(
    client, admin_client, criar_usuario
):
    _, headers = criar_usuario("cliente-catalogo@teste.com")

    assert client.get("/api/v1/cidades").status_code == 200
    assert client.post("/api/v1/cidades", json={"nome": "Quixada"}).status_code == 401
    assert (
        client.post(
            "/api/v1/cidades",
            json={"nome": "Quixada"},
            headers=headers,
        ).status_code
        == 403
    )

    cidade = admin_client.post(
        "/api/v1/cidades", json={"nome": "Quixada"}
    ).json()
    hotel_payload = {"nome": "Hotel Delta", "cidade_id": cidade["id"]}
    assert (
        client.post("/api/v1/hoteis", json=hotel_payload, headers=headers).status_code
        == 403
    )
    hotel = admin_client.post("/api/v1/hoteis", json=hotel_payload).json()

    quarto_payload = {
        "hotel_id": hotel["id"],
        "numero": "101",
        "tipo": "standard",
        "capacidade": 2,
        "preco_diaria": "150.00",
    }
    assert (
        client.post("/api/v1/quartos", json=quarto_payload, headers=headers).status_code
        == 403
    )
    assert admin_client.post("/api/v1/quartos", json=quarto_payload).status_code == 201


def test_guest_profiles_and_reservations_are_owned_by_the_authenticated_user(
    client, admin_client, criar_usuario
):
    _, headers1 = criar_usuario("cliente1@teste.com", "Cliente Um")
    _, headers2 = criar_usuario("cliente2@teste.com", "Cliente Dois")

    guest1 = client.post(
        "/api/v1/hospedes",
        headers=headers1,
        json={
            "nome": "Cliente Um",
            "cpf": "11122233344",
            "email": "cliente1@teste.com",
            "telefone": "88999990001",
        },
    )
    guest2 = client.post(
        "/api/v1/hospedes",
        headers=headers2,
        json={
            "nome": "Cliente Dois",
            "cpf": "55566677788",
            "email": "cliente2@teste.com",
            "telefone": "88999990002",
        },
    )
    assert guest1.status_code == guest2.status_code == 201
    assert client.get("/api/v1/hospedes").status_code == 401
    assert client.get("/api/v1/reservas").status_code == 401
    assert client.get("/api/v1/hospedes", headers=headers2).status_code == 403
    assert (
        client.get(f"/api/v1/hospedes/{guest1.json()['id']}", headers=headers2).status_code
        == 404
    )
    assert client.get("/api/v1/hospedes/me", headers=headers1).json()["id"] == guest1.json()["id"]

    cidade = admin_client.post(
        "/api/v1/cidades", json={"nome": "Aquiraz"}
    ).json()
    hotel = admin_client.post(
        "/api/v1/hoteis",
        json={"nome": "Hotel Praia", "cidade_id": cidade["id"]},
    ).json()
    quarto = admin_client.post(
        "/api/v1/quartos",
        json={
            "hotel_id": hotel["id"],
            "numero": "201",
            "tipo": "standard",
            "capacidade": 2,
            "preco_diaria": "200.00",
        },
    ).json()
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=2)
    reservation = client.post(
        "/api/v1/reservas",
        headers=headers1,
        json={
            "hospede_id": guest1.json()["id"],
            "quarto_id": quarto["id"],
            "check_in": check_in.isoformat(),
            "check_out": check_out.isoformat(),
        },
    )
    assert reservation.status_code == 201

    assert len(client.get("/api/v1/reservas", headers=headers1).json()) == 1
    assert (
        client.get(
            "/api/v1/reservas",
            params={"hospede_id": guest1.json()["id"]},
            headers=headers2,
        ).json()
        == []
    )
    assert (
        client.get(
            f"/api/v1/reservas/{reservation.json()['id']}", headers=headers2
        ).status_code
        == 404
    )
    assert (
        client.patch(
            f"/api/v1/reservas/{reservation.json()['id']}/cancelar",
            headers=headers2,
        ).status_code
        == 404
    )
    assert (
        client.post(
            "/api/v1/reservas",
            headers=headers2,
            json={
                "hospede_id": guest1.json()["id"],
                "quarto_id": quarto["id"],
                "check_in": (check_out + timedelta(days=1)).isoformat(),
                "check_out": (check_out + timedelta(days=2)).isoformat(),
            },
        ).status_code
        == 404
    )
    assert (
        client.patch(
            f"/api/v1/reservas/{reservation.json()['id']}/confirmar",
            headers=headers1,
        ).status_code
        == 403
    )
    assert (
        client.patch(
            f"/api/v1/reservas/{reservation.json()['id']}/cancelar",
            headers=headers1,
        ).status_code
        == 200
    )

    admin_reservation = client.post(
        "/api/v1/reservas",
        headers=admin_client.headers,
        json={
            "hospede_id": guest1.json()["id"],
            "quarto_id": quarto["id"],
            "check_in": (check_out + timedelta(days=1)).isoformat(),
            "check_out": (check_out + timedelta(days=2)).isoformat(),
        },
    )
    assert admin_reservation.status_code == 201
    assert len(client.get("/api/v1/reservas", headers=admin_client.headers).json()) == 2


def test_health_endpoint_hides_database_error_details(
    client, db_session, monkeypatch, caplog
):
    private_detail = "private connection diagnostic"

    def fail_database_probe(*_args, **_kwargs):
        raise RuntimeError(private_detail)

    class FailingMongo:
        async def command(self, _command):
            raise RuntimeError(private_detail)

    monkeypatch.setattr(db_session, "execute", fail_database_probe)
    app.dependency_overrides[get_mongo_db] = lambda: FailingMongo()

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json() == {"detail": "Serviço temporariamente indisponível."}
    assert private_detail not in response.text
    assert private_detail in caplog.text


def test_cors_rejects_unknown_origins(client):
    blocked = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )
    allowed = client.options(
        "/api/v1/auth/login",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "access-control-allow-origin" not in blocked.headers
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
