import uuid

from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

    def get_by_id(self, usuario_id: uuid.UUID) -> Usuario | None:
        return (
            self.db.query(Usuario)
            .filter(Usuario.id == usuario_id)
            .first()
        )

    def create(
        self,
        nome: str,
        email: str,
        senha_hash: str,
        is_admin: bool = False,
    ) -> Usuario:
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            is_admin=is_admin,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
