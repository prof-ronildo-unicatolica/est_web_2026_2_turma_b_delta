"""Testes de fumaca do auth BASICO (placeholder).

Documentam o contrato atual da API de autenticacao. Quando os alunos
implementarem a versao real (JWT/RBAC) na Sprint 2, estes testes devem
ser adaptados/substituidos pela suite definitiva da atividade.
"""

BASE = "/api/v1/auth"


def test_login_valido_retorna_token(client):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalido_retorna_401(client):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "errada"}
    )
    assert resp.status_code == 401


def test_rota_protegida_sem_token_e_bloqueada(client):
    resp = client.get(f"{BASE}/me")
    assert resp.status_code in (401, 403)


def test_rota_protegida_com_token_retorna_perfil(client):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(f"{BASE}/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "cliente@hotel.com"
    assert body["is_admin"] is False
    assert "senha" not in body  # a senha nunca deve vazar na resposta


def test_cliente_nao_acessa_rota_admin(client):
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client):
    token = client.post(
        f"{BASE}/login", json={"email": "admin@hotel.com", "senha": "admin123"}
    ).json()["access_token"]
    resp = client.get(
        f"{BASE}/admin/verificacao", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
