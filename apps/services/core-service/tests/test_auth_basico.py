import pytest
from pydantic import ValidationError

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.schemas.usuario import RegisterRequest

BASE = "/api/v1/auth"


def criar_cliente(client):
    return client.post(
        f"{BASE}/register",
        json={
            "nome": "Cliente Teste",
            "email": "cliente@teste.com",
            "senha": "Cliente@123",
        },
    )


def criar_admin(db_session):
    admin = Usuario(
        nome="Admin Teste",
        email="admin@teste.com",
        senha_hash=hash_password("Admin@123"),
        is_admin=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


def obter_token(client, email, senha):
    resp = client.post(
        f"{BASE}/login",
        json={"email": email, "senha": senha},
    )
    return resp.json()["access_token"]


def test_register_cria_usuario_com_hash_sem_expor_credenciais(client, db_session):
    resp = criar_cliente(client)

    assert resp.status_code == 202
    body = resp.json()

    assert body == {"message": "Solicitação de cadastro recebida."}
    usuario = (
        db_session.query(Usuario)
        .filter(Usuario.email == "cliente@teste.com")
        .one()
    )
    assert usuario.senha_hash != "Cliente@123"
    assert usuario.senha_hash.startswith("$2b$")


def test_register_email_duplicado_nao_revela_se_conta_existe(client, db_session):
    primeira_resposta = criar_cliente(client)
    segunda_resposta = criar_cliente(client)

    assert primeira_resposta.status_code == segunda_resposta.status_code == 202
    assert primeira_resposta.json() == segunda_resposta.json()
    assert db_session.query(Usuario).count() == 1


def test_register_normaliza_email_e_login_aceita_variacoes(client, db_session):
    resp = client.post(
        f"{BASE}/register",
        json={
            "nome": "Cliente Teste",
            "email": "  Cliente@Teste.com ",
            "senha": "Cliente@123",
        },
    )

    assert resp.status_code == 202
    usuario = (
        db_session.query(Usuario)
        .filter(Usuario.email == "cliente@teste.com")
        .one()
    )
    assert usuario.email == "cliente@teste.com"

    login = client.post(
        f"{BASE}/login",
        json={"email": " CLIENTE@TESTE.COM ", "senha": "Cliente@123"},
    )
    assert login.status_code == 200


@pytest.mark.parametrize(
    ("senha", "valid"),
    [
        ("a" * 72, True),
        ("a" * 73, False),
        ("é" * 36, True),
        ("é" * 37, False),
    ],
)
def test_schema_respeita_limite_bcrypt_em_bytes(senha, valid):
    payload = {
        "nome": "Cliente Teste",
        "email": "cliente@teste.com",
        "senha": senha,
    }

    if valid:
        RegisterRequest.model_validate(payload)
    else:
        with pytest.raises(ValidationError):
            RegisterRequest.model_validate(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"nome": "   ", "email": "cliente@teste.com", "senha": "Cliente@123"},
        {"nome": "Cliente", "email": "email-invalido", "senha": "Cliente@123"},
        {"nome": "Cliente", "email": "cliente@teste.com", "senha": "curta"},
    ],
)
def test_register_rejeita_nome_email_ou_senha_invalidos(client, payload):
    resp = client.post(f"{BASE}/register", json=payload)

    assert resp.status_code == 422


def test_login_valido_retorna_token(client):
    criar_cliente(client)

    resp = client.post(
        f"{BASE}/login",
        json={
            "email": "cliente@teste.com",
            "senha": "Cliente@123",
        },
    )

    assert resp.status_code == 200

    body = resp.json()

    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalido_retorna_401(client):
    criar_cliente(client)

    resp = client.post(
        f"{BASE}/login",
        json={
            "email": "cliente@teste.com",
            "senha": "senha_errada",
        },
    )

    assert resp.status_code == 401


def test_login_nao_revela_se_email_existe(client):
    criar_cliente(client)

    usuario_existente = client.post(
        f"{BASE}/login",
        json={"email": "cliente@teste.com", "senha": "senha_errada"},
    )
    usuario_inexistente = client.post(
        f"{BASE}/login",
        json={"email": "inexistente@teste.com", "senha": "senha_errada"},
    )

    assert usuario_existente.status_code == usuario_inexistente.status_code == 401
    assert usuario_existente.json() == usuario_inexistente.json()


def test_rota_protegida_sem_token_retorna_401(client):
    resp = client.get(f"{BASE}/me")

    assert resp.status_code == 401


def test_rota_protegida_com_token_retorna_perfil(client):
    criar_cliente(client)

    token = obter_token(
        client,
        "cliente@teste.com",
        "Cliente@123",
    )

    resp = client.get(
        f"{BASE}/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200

    body = resp.json()

    assert body["email"] == "cliente@teste.com"
    assert body["nome"] == "Cliente Teste"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body


def test_token_invalido_retorna_401(client):
    resp = client.get(
        f"{BASE}/me",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert resp.status_code == 401

def test_token_expirado_retorna_401(client):
    from app.core.security import create_access_token

    token = create_access_token("usuario-teste", expires_minutes=-1)

    resp = client.get(
        f"{BASE}/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 401

    
def test_cliente_nao_acessa_rota_admin(client):
    criar_cliente(client)

    token = obter_token(
        client,
        "cliente@teste.com",
        "Cliente@123",
    )

    resp = client.get(
        f"{BASE}/admin/verificacao",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client, db_session):
    criar_admin(db_session)

    token = obter_token(
        client,
        "admin@teste.com",
        "Admin@123",
    )

    resp = client.get(
        f"{BASE}/admin/verificacao",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200