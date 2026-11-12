from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
)


class AuthCredentials(BaseModel):
    email: Annotated[EmailStr, Field(max_length=100)]
    senha: str

    @field_validator("email", mode="before")
    @classmethod
    def normalizar_email(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value

    @field_validator("senha")
    @classmethod
    def limitar_senha_para_bcrypt(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("A senha excede o limite aceito pelo bcrypt.")
        return value


class RegisterRequest(AuthCredentials):
    nome: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100,
        ),
    ]
    senha: Annotated[str, StringConstraints(min_length=8)]


class LoginRequest(AuthCredentials):
    senha: Annotated[str, StringConstraints(min_length=1)]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegistrationAccepted(BaseModel):
    message: str = "Solicitação de cadastro recebida."


class UsuarioPublic(BaseModel):
    """Perfil publico do usuario (nunca expoe senha)."""

    model_config = ConfigDict(from_attributes=True)

    email: str
    nome: str
    is_admin: bool
