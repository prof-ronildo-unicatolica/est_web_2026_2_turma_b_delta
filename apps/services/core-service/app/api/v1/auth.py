"""Rotas de autenticacao/autorizacao - VERSAO BASICA (placeholder).

⚠️ Implementacao simplificada (if/else, sem hash, sem JWT) para o exemplo
base funcionar. A versao completa e a ATIVIDADE DA SPRINT 2:
    docs/02_engenharia_software/atividade_auth_sprint2.md
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import autenticar_credenciais, get_current_admin, get_current_user
from app.schemas.usuario import LoginRequest, Token, UsuarioPublic

router = APIRouter(prefix="/auth", tags=["Auth (basico)"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest):
    """Login basico: valida as credenciais e devolve um 'token'."""
    usuario = autenticar_credenciais(payload.email, payload.senha)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )
    # VERSAO BASICA: o "token" e apenas o e-mail. Na Sprint 2 sera um JWT.
    return Token(access_token=usuario["email"])


@router.get("/me", response_model=UsuarioPublic)
def get_me(usuario_atual: dict = Depends(get_current_user)):
    """Rota protegida: retorna o perfil do usuario autenticado."""
    return usuario_atual


@router.get("/admin/verificacao")
def somente_admin(admin: dict = Depends(get_current_admin)):
    """Rota administrativa de exemplo (autorizacao por is_admin)."""
    return {"mensagem": f"Acesso administrativo concedido para {admin['nome']}"}
