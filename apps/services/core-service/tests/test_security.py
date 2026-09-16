from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_nao_salva_senha_em_texto_plano():
    senha = "Senha@123"

    senha_hash = hash_password(senha)

    assert senha_hash != senha
    assert senha_hash.startswith("$2b$")


def test_verify_password_valida_senha_correta():
    senha = "Senha@123"
    senha_hash = hash_password(senha)

    assert verify_password(senha, senha_hash) is True


def test_verify_password_rejeita_senha_incorreta():
    senha_hash = hash_password("Senha@123")

    assert verify_password("SenhaErrada@123", senha_hash) is False


def test_create_access_token_tem_sub_e_exp():
    token = create_access_token("usuario-teste", expires_minutes=60)

    payload = decode_access_token(token)

    assert payload["sub"] == "usuario-teste"
    assert "exp" in payload


def test_decode_access_token_retorna_payload():
    token = create_access_token("usuario-teste", expires_minutes=60)

    payload = decode_access_token(token)

    assert payload["sub"] == "usuario-teste"
