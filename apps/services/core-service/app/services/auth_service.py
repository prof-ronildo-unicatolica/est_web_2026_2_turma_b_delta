from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def registrar(
        self,
        nome: str,
        email: str,
        senha: str,
        is_admin: bool = False,
    ):
        usuario_existente = self.repository.get_by_email(email)

        if usuario_existente:
            return None

        senha_hash = hash_password(senha)

        return self.repository.create(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            is_admin=is_admin,
        )

    def autenticar(self, email: str, senha: str):
        usuario = self.repository.get_by_email(email)

        if usuario is None:
            return None

        if not verify_password(senha, usuario.senha_hash):
            return None

        return usuario

    def gerar_token(self, usuario) -> str:
        return create_access_token(subject=str(usuario.id))
