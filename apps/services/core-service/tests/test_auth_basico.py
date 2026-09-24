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
    from app.models.usuario import Usuario
    from app.core.security import hash_password

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


def test_register_cria_usuario_sem_expor_senha(client):
    resp = criar_cliente(client)

    assert resp.status_code == 201
    body = resp.json()

    assert body["nome"] == "Cliente Teste"
    assert body["email"] == "cliente@teste.com"
    assert body["is_admin"] is False
    assert "senha" not in body
    assert "senha_hash" not in body


def test_register_email_duplicado_retorna_409(client):
    criar_cliente(client)

    resp = criar_cliente(client)

    assert resp.status_code == 409


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