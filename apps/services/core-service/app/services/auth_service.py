from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.usuario_repository import UsuarioRepository

_DUMMY_PASSWORD_HASH = hash_password(
    "senha-dummy-para-equalizar-o-tempo-de-login"
)


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
        # Executa bcrypt nos dois caminhos para reduzir diferença de tempo
        # entre um e-mail existente e um endereço novo.
        senha_hash = hash_password(senha)
        usuario_existente = self.repository.get_by_email(email)

        if usuario_existente:
            return None

        try:
            return self.repository.create(
                nome=nome,
                email=email,
                senha_hash=senha_hash,
                is_admin=is_admin,
            )
        except IntegrityError:
            # Também cobre duas solicitações simultâneas para o mesmo e-mail.
            self.repository.db.rollback()
            return None

    def autenticar(self, email: str, senha: str):
        usuario = self.repository.get_by_email(email)

        if usuario is None:
            verify_password(senha, _DUMMY_PASSWORD_HASH)
            return None

        if not verify_password(senha, usuario.senha_hash):
            return None

        return usuario

    def gerar_token(self, usuario) -> str:
        return create_access_token(subject=str(usuario.id))
