from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.schemas.usuario import LoginRequest, RegisterRequest, Token, UsuarioPublic
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post(
    "/register",
    response_model=UsuarioPublic,
    status_code=status.HTTP_201_CREATED,
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    usuario = service.registrar(
        nome=payload.nome,
        email=payload.email,
        senha=payload.senha,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado",
        )

    return usuario


@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    usuario = service.autenticar(
        email=payload.email,
        senha=payload.senha,
    )

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )

    return Token(
        access_token=service.gerar_token(usuario),
    )


@router.get("/me", response_model=UsuarioPublic)
def get_me(
    usuario_atual=Depends(get_current_user),
):
    return usuario_atual


@router.get("/admin/verificacao")
def somente_admin(
    admin=Depends(get_current_admin),
):
    return {
        "mensagem": f"Acesso administrativo concedido para {admin.nome}"
    }
