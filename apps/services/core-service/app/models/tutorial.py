import uuid
from typing import List

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Tabela Associativa N:M entre Disciplina e Tecnologia
disciplina_tecnologia = Table(
    "disciplina_tecnologia",
    Base.metadata,
    Column(
        "disciplina_id",
        ForeignKey("disciplinas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tecnologia_id",
        ForeignKey("tecnologias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# Tabela Associativa N:M entre Tecnologia (ex: Tailwind) e Linguagem (ex: CSS, JS)
tecnologia_linguagem = Table(
    "tecnologia_linguagem",
    Base.metadata,
    Column(
        "tecnologia_id",
        ForeignKey("tecnologias.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "linguagem_id",
        ForeignKey("linguagens.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Professor(Base):
    __tablename__ = "professores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relação 1:1 (Professor -> ProfessorDetail)
    detalhe: Mapped["ProfessorDetail"] = relationship(
        back_populates="professor", uselist=False, cascade="all, delete-orphan"
    )

    # Relação 1:N (Professor -> Disciplina)
    disciplinas: Mapped[List["Disciplina"]] = relationship(
        back_populates="professor", cascade="all, delete-orphan"
    )


class ProfessorDetail(Base):
    __tablename__ = "professor_detalhes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    professor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professores.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    sala: Mapped[str] = mapped_column(String(50), nullable=False)
    biografia: Mapped[str] = mapped_column(Text, nullable=True)
    biografia_mapa: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Relacionamento inverso 1:1
    professor: Mapped["Professor"] = relationship(back_populates="detalhe")


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relação 1:N (Disciplina pertence a um Professor)
    professor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("professores.id", ondelete="CASCADE"), nullable=False
    )
    professor: Mapped["Professor"] = relationship(back_populates="disciplinas")

    # Relação N:M (Disciplina <-> Tecnologia)
    tecnologias: Mapped[List["Tecnologia"]] = relationship(
        secondary=disciplina_tecnologia, back_populates="disciplinas"
    )


class Stack(Base):
    __tablename__ = "stacks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relação 1:N (Stack -> Tecnologia)
    tecnologias: Mapped[List["Tecnologia"]] = relationship(
        back_populates="stack", cascade="all, delete-orphan"
    )


class Tecnologia(Base):
    __tablename__ = "tecnologias"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    stack_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("stacks.id", ondelete="CASCADE"), nullable=False
    )

    # Relação 1:N (Tecnologia pertence a uma Stack)
    stack: Mapped["Stack"] = relationship(back_populates="tecnologias")

    # Relação N:M (Tecnologia <-> Disciplina)
    disciplinas: Mapped[List["Disciplina"]] = relationship(
        secondary=disciplina_tecnologia, back_populates="tecnologias"
    )

    # Relação N:M (Tecnologia <-> Linguagem)
    linguagens: Mapped[List["Linguagem"]] = relationship(
        secondary=tecnologia_linguagem, back_populates="tecnologias"
    )


class Linguagem(Base):
    __tablename__ = "linguagens"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Relação N:M (Linguagem <-> Tecnologia)
    tecnologias: Mapped[List["Tecnologia"]] = relationship(
        secondary=tecnologia_linguagem, back_populates="linguagens"
    )
