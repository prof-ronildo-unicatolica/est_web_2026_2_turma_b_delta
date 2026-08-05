"""initial schema and seed

Revision ID: 001
Revises:
Create Date: 2026-06-28 12:00:00.000000

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# Identificadores de revisão, usados pelo Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criar tabela de Stacks
    op.create_table(
        "stacks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # 2. Criar tabela de Linguagens
    op.create_table(
        "linguagens",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # 3. Criar tabela de Professores
    op.create_table(
        "professores",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # 4. Criar tabela de ProfessorDetalhes (1:1 com Professor)
    op.create_table(
        "professor_detalhes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("professor_id", sa.UUID(), nullable=False),
        sa.Column("sala", sa.String(length=50), nullable=False),
        sa.Column("biografia", sa.Text(), nullable=True),
        sa.Column("biografia_mapa", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["professor_id"], ["professores.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("professor_id"),
    )

    # 5. Criar tabela de Disciplinas (1:N com Professor)
    op.create_table(
        "disciplinas",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("semestre", sa.Integer(), nullable=False),
        sa.Column("professor_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["professor_id"], ["professores.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # 6. Criar tabela de Tecnologias (1:N com Stack)
    op.create_table(
        "tecnologias",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.Column("stack_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["stack_id"], ["stacks.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # 7. Criar tabela de DisciplinaTecnologia (N:M entre Disciplina e Tecnologia)
    op.create_table(
        "disciplina_tecnologia",
        sa.Column("disciplina_id", sa.UUID(), nullable=False),
        sa.Column("tecnologia_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["disciplina_id"], ["disciplinas.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tecnologia_id"], ["tecnologias.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("disciplina_id", "tecnologia_id"),
    )

    # 8. Criar tabela de TecnologiaLinguagem (N:M entre Tecnologia e Linguagem)
    op.create_table(
        "tecnologia_linguagem",
        sa.Column("tecnologia_id", sa.UUID(), nullable=False),
        sa.Column("linguagem_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["linguagem_id"], ["linguagens.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tecnologia_id"], ["tecnologias.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("tecnologia_id", "linguagem_id"),
    )

    # --- INGESTÃO DE DADOS INICIAIS (SEED) ---
    prof_id = uuid.UUID("bed023d2-c85c-4973-9c3d-79d77a5519f1")
    prof_detail_id = uuid.uuid4()
    disc_web_id = uuid.uuid4()
    disc_redes_id = uuid.uuid4()
    disc_fsi_id = uuid.uuid4()
    disc_arq_id = uuid.uuid4()

    stack_backend_id = uuid.uuid4()
    stack_frontend_id = uuid.uuid4()
    stack_db_id = uuid.uuid4()

    lang_python_id = uuid.uuid4()
    lang_sql_id = uuid.uuid4()
    lang_js_id = uuid.uuid4()
    lang_css_id = uuid.uuid4()
    lang_assembly_id = uuid.uuid4()

    tech_fastapi_id = uuid.uuid4()
    tech_alembic_id = uuid.uuid4()
    tech_react_id = uuid.uuid4()
    tech_tailwind_id = uuid.uuid4()
    tech_postgres_id = uuid.uuid4()
    tech_mongo_id = uuid.uuid4()
    tech_wireshark_id = uuid.uuid4()
    tech_assembly_id = uuid.uuid4()

    # Inserir Professor
    op.execute(
        f"INSERT INTO professores (id, nome, email) VALUES ('{prof_id}', 'Ronildo Silva', 'ronildosilva@unicatolicaquixada.edu.br')"
    )
    # Inserir Detalhes do Professor (1:1)
    geojson_str = (
        '{"type": "FeatureCollection", "features": ['
        '{"type": "Feature", "properties": {"local": "Fortaleza - CE", "descricao": "Cientista de dados / Gerente de projetos"}, "geometry": {"type": "Point", "coordinates": [-38.5267, -3.7319]}},'
        '{"type": "Feature", "properties": {"local": "Quixada - CE", "descricao": "Professor universitario"}, "geometry": {"type": "Point", "coordinates": [-39.0152, -4.9715]}},'
        '{"type": "Feature", "properties": {"local": "Crateus - CE", "descricao": "Instrutor de inteligencia artificial"}, "geometry": {"type": "Point", "coordinates": [-40.6728, -5.1764]}},'
        '{"type": "Feature", "properties": {"local": "Cedro - CE", "descricao": "Instrutor de desenvolvimento mobile"}, "geometry": {"type": "Point", "coordinates": [-39.0625, -6.6074]}},'
        '{"type": "Feature", "properties": {"local": "Belo Horizonte - MG", "descricao": "Engenheiro de dados"}, "geometry": {"type": "Point", "coordinates": [-43.9378, -19.9191]}},'
        '{"type": "Feature", "properties": {"local": "Sao Paulo - SP", "descricao": "Desenvolvedor de software"}, "geometry": {"type": "Point", "coordinates": [-46.6333, -23.5505]}},'
        '{"type": "Feature", "properties": {"local": "Rio de Janeiro - RJ", "descricao": "Especialista em backend"}, "geometry": {"type": "Point", "coordinates": [-43.1729, -22.9068]}},'
        '{"type": "Feature", "properties": {"local": "Florianopolis - SC", "descricao": "Engenheiro de inteligencia artificial"}, "geometry": {"type": "Point", "coordinates": [-48.5480, -27.5954]}},'
        '{"type": "Feature", "properties": {"local": "Lisboa - PT", "descricao": "Chefe de tecnologia da informação"}, "geometry": {"type": "Point", "coordinates": [-9.1393, 38.7223]}}'
        "]}"
    )
    op.execute(
        f"INSERT INTO professor_detalhes (id, professor_id, sala, biografia, biografia_mapa) VALUES ('{prof_detail_id}', '{prof_id}', 'Sala 07 , Bloco D', 'Professor da disciplina de Estágio II no curso de Sistemas de Informação.', '{geojson_str}')"
    )
    # Inserir Disciplinas (1:N)
    op.execute(
        f"INSERT INTO disciplinas (id, nome, ano, semestre, professor_id) VALUES ('{disc_web_id}', 'Linguagens e Tecnologias para Desenvolvimento WEB', 2026, 2, '{prof_id}')"
    )
    op.execute(
        f"INSERT INTO disciplinas (id, nome, ano, semestre, professor_id) VALUES ('{disc_redes_id}', 'Redes de Computadores', 2026, 1, '{prof_id}')"
    )
    op.execute(
        f"INSERT INTO disciplinas (id, nome, ano, semestre, professor_id) VALUES ('{disc_fsi_id}', 'Fundamentos de Sistemas de Informação', 2026, 1, '{prof_id}')"
    )
    op.execute(
        f"INSERT INTO disciplinas (id, nome, ano, semestre, professor_id) VALUES ('{disc_arq_id}', 'Arquitetura de Computadores', 2026, 1, '{prof_id}')"
    )

    # Inserir Stacks
    op.execute(
        f"INSERT INTO stacks (id, nome) VALUES ('{stack_backend_id}', 'Backend')"
    )
    op.execute(
        f"INSERT INTO stacks (id, nome) VALUES ('{stack_frontend_id}', 'Frontend')"
    )
    op.execute(
        f"INSERT INTO stacks (id, nome) VALUES ('{stack_db_id}', 'Banco de Dados')"
    )

    # Inserir Linguagens
    op.execute(
        f"INSERT INTO linguagens (id, nome) VALUES ('{lang_python_id}', 'Python')"
    )
    op.execute(f"INSERT INTO linguagens (id, nome) VALUES ('{lang_sql_id}', 'SQL')")
    op.execute(
        f"INSERT INTO linguagens (id, nome) VALUES ('{lang_js_id}', 'JavaScript')"
    )
    op.execute(f"INSERT INTO linguagens (id, nome) VALUES ('{lang_css_id}', 'CSS')")
    op.execute(
        f"INSERT INTO linguagens (id, nome) VALUES ('{lang_assembly_id}', 'Assembly')"
    )

    # Inserir Tecnologias (1:N com Stacks)
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_fastapi_id}', 'FastAPI', '{stack_backend_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_alembic_id}', 'Alembic', '{stack_backend_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_react_id}', 'React', '{stack_frontend_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_tailwind_id}', 'Tailwind CSS', '{stack_frontend_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_postgres_id}', 'PostgreSQL', '{stack_db_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_mongo_id}', 'MongoDB', '{stack_db_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_wireshark_id}', 'Wireshark', '{stack_backend_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologias (id, nome, stack_id) VALUES ('{tech_assembly_id}', 'Assembly', '{stack_backend_id}')"
    )

    # Inserir relacionamentos DisciplinaTecnologia (N:M)
    for t_id in [
        tech_fastapi_id,
        tech_alembic_id,
        tech_react_id,
        tech_tailwind_id,
        tech_postgres_id,
        tech_mongo_id,
    ]:
        op.execute(
            f"INSERT INTO disciplina_tecnologia (disciplina_id, tecnologia_id) VALUES ('{disc_web_id}', '{t_id}')"
        )
    op.execute(
        f"INSERT INTO disciplina_tecnologia (disciplina_id, tecnologia_id) VALUES ('{disc_redes_id}', '{tech_wireshark_id}')"
    )
    for t_id in [tech_postgres_id, tech_mongo_id]:
        op.execute(
            f"INSERT INTO disciplina_tecnologia (disciplina_id, tecnologia_id) VALUES ('{disc_fsi_id}', '{t_id}')"
        )
    op.execute(
        f"INSERT INTO disciplina_tecnologia (disciplina_id, tecnologia_id) VALUES ('{disc_arq_id}', '{tech_assembly_id}')"
    )

    # Inserir relacionamentos TecnologiaLinguagem (N:M)
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_fastapi_id}', '{lang_python_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_alembic_id}', '{lang_python_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_alembic_id}', '{lang_sql_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_react_id}', '{lang_js_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_tailwind_id}', '{lang_css_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_tailwind_id}', '{lang_js_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_postgres_id}', '{lang_sql_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_mongo_id}', '{lang_js_id}')"
    )
    op.execute(
        f"INSERT INTO tecnologia_linguagem (tecnologia_id, linguagem_id) VALUES ('{tech_assembly_id}', '{lang_assembly_id}')"
    )


def downgrade() -> None:
    op.drop_table("tecnologia_linguagem")
    op.drop_table("disciplina_tecnologia")
    op.drop_table("tecnologias")
    op.drop_table("disciplinas")
    op.drop_table("professor_detalhes")
    op.drop_table("professores")
    op.drop_table("linguagens")
    op.drop_table("stacks")
