"""Create an administrator using one-time environment inputs."""

import os

from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import RegisterRequest


def main() -> int:
    name = os.environ.get("ADMIN_NAME", "")
    email = os.environ.get("ADMIN_EMAIL", "")
    password = os.environ.get("ADMIN_PASSWORD", "")
    if not name or not email or not password:
        raise SystemExit(
            "Defina ADMIN_NAME, ADMIN_EMAIL e ADMIN_PASSWORD para criar o admin."
        )

    try:
        account = RegisterRequest(
            nome=name,
            email=email,
            senha=password,
        )
    except ValidationError:
        raise SystemExit(
            "Dados inválidos; nenhum administrador foi criado."
        ) from None

    with SessionLocal() as db:
        repository = UsuarioRepository(db)
        if repository.get_by_email(str(account.email)):
            raise SystemExit(
                "A conta já existe; nenhum dado foi alterado."
            )
        try:
            repository.create(
                nome=account.nome,
                email=str(account.email),
                senha_hash=hash_password(account.senha),
                is_admin=True,
            )
        except IntegrityError:
            db.rollback()
            raise SystemExit(
                "A conta já existe; nenhum dado foi alterado."
            ) from None

    print("Conta administrativa criada.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
