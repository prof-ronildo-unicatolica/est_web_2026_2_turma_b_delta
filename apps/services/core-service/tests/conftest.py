import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set a local-only key before importing the app in tests.
os.environ.setdefault("SECRET_KEY", "pytest-only-not-for-production-32chars")
os.environ.setdefault("POSTGRES_USER", "pytest")
os.environ.setdefault("POSTGRES_PASSWORD", "pytest-only")
os.environ.setdefault("MONGODB_URL", "mongodb://localhost")
os.environ.setdefault("RABBITMQ_URL", "amqp://guest:guest@localhost/")

from app.core.database import get_db  # noqa: E402
from app.core.security import create_access_token, hash_password  # noqa: E402
from app.main import app  # noqa: E402
from app.models.tutorial import Base  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402

# Banco SQLite em arquivo temporario para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Desativamos raise_server_exceptions para validar retornos de erro 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(db_session):
    admin = Usuario(
        nome="Admin de Teste",
        email="joao@teste.com",
        senha_hash=hash_password("senha-fixture-administrador"),
        is_admin=True,
    )
    db_session.add(admin)
    db_session.commit()
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as client:
        client.headers.update(
            {"Authorization": f"Bearer {create_access_token(str(admin.id))}"}
        )
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def criar_usuario(db_session):
    def criar(email: str, nome: str = "Conta de Teste", is_admin: bool = False):
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=hash_password("senha-fixture-usuario"),
            is_admin=is_admin,
        )
        db_session.add(usuario)
        db_session.commit()
        return usuario, {
            "Authorization": f"Bearer {create_access_token(str(usuario.id))}"
        }

    return criar
