"""Dependencias de autenticacao/autorizacao - VERSAO BASICA (placeholder).

⚠️ ATENCAO: implementacao PROPOSITALMENTE simplificada (apenas if/else,
SEM hash de senha e SEM JWT). Existe apenas para o exemplo base funcionar
ponta a ponta e dar um contrato de API estavel ao frontend.

A implementacao REAL (senha em bcrypt + JWT assinado + RBAC via banco de
dados) e a ATIVIDADE DA SPRINT 2:
    docs/02_engenharia_software/atividade_auth_sprint2.md
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# "Banco" de usuarios em memoria (placeholder). Na atividade da Sprint 2
# isto sera substituido pela tabela `usuarios` no PostgreSQL, com as
# senhas armazenadas em hash bcrypt.
USUARIOS_DEMO = {
    "admin@hotel.com": {
        "nome": "Administrador da Franquia",
        "senha": "admin123",
        "is_admin": True,
    },
    "cliente@hotel.com": {
        "nome": "Cliente Demonstracao",
        "senha": "cliente123",
        "is_admin": False,
    },
}

bearer_scheme = HTTPBearer(description="Use o token retornado por POST /auth/login")


def autenticar_credenciais(email: str, senha: str) -> dict | None:
    """Confere e-mail/senha por comparacao direta (SEM hash). Placeholder."""
    usuario = USUARIOS_DEMO.get(email)
    # Autenticacao basica: apenas um if/else comparando a senha em texto plano.
    if usuario is None or usuario["senha"] != senha:
        return None
    return {"email": email, **usuario}


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> dict:
    """Valida o 'token' e retorna o usuario autenticado.

    VERSAO BASICA: o 'token' e simplesmente o proprio e-mail, sem
    assinatura nem expiracao. Na Sprint 2 isto passa a decodificar um JWT.
    """
    email = credentials.credentials
    usuario = USUARIOS_DEMO.get(email)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"email": email, **usuario}


def get_current_admin(usuario: dict = Depends(get_current_user)) -> dict:
    """Autorizacao (RBAC) basica: exige is_admin=True. Apenas um if/else."""
    if not usuario["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return usuario
