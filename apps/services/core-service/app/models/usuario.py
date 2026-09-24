import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.tutorial import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )