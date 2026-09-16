from pydantic import BaseModel, ConfigDict


class RegisterRequest(BaseModel):
    nome: str
    email: str
    senha: str


class LoginRequest(BaseModel):
    email: str
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioPublic(BaseModel):
    """Perfil publico do usuario (nunca expoe senha)."""

    model_config = ConfigDict(from_attributes=True)

    email: str
    nome: str
    is_admin: bool
