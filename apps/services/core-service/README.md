# Core Service - Backend (FastAPI + PostgreSQL + MongoDB)

Este diretório contém o **Core Service**, a API principal do Sistema de Reservas de Rede Hoteleira, desenvolvida em **FastAPI** (Python). 

Atualmente, o projeto inclui uma estrutura de tutorial acadêmico que demonstra o acesso e a manipulação de dados em bancos relacional (PostgreSQL via SQLAlchemy e Alembic) e NoSQL (MongoDB via Motor).

---

## Tecnologias e Dependências

* **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) (assíncrono e de alto desempenho).
* **Banco de Dados Relacional**: PostgreSQL (gerenciado via SQLAlchemy ORM).
* **Versionamento de Banco**: Alembic (gerencia migrações e seeds).
* **Banco de Dados NoSQL**: MongoDB (acessado assincronamente através da biblioteca Motor).
* **Validação de Dados**: Pydantic e Pydantic Settings (carrega variáveis do `.env`).
* **Segurança/Criptografia**: passlib com bcrypt (para criptografar senhas).

---

## Como Executar o Backend Localmente

### 1. Pré-requisitos
Certifique-se de que os containers do banco de dados estejam rodando na raiz do projeto:
```bash
# Na raiz do monorepo:
docker compose up -d
```

### 2. Configurar o Arquivo de Variáveis (.env)
Duplique o arquivo de modelo `env_example` com o nome `.env`:
* **Linux/macOS**: `cp env_example .env`
* **Windows (PowerShell)**: `copy env_example .env`

---

### 3. Instalação e Execução

#### Opção A: Com Virtualenv Padrão (`venv`)
1. **Criar e Ativar Ambiente Virtual**:
   * No Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * No Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
2. **Instalar Dependências**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Rodar Migrações e Seeds (Alembic)**:
   ```bash
   alembic upgrade head
   ```
4. **Executar o Servidor**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

#### Opção B: Com Poetry
1. **Instalar e Ativar Ambiente**:
   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   poetry shell
   ```
2. **Rodar Migrações e Seeds (Alembic)**:
   ```bash
   poetry run alembic upgrade head
   ```
3. **Executar o Servidor**:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```

---

## Rotas Disponíveis (Endpoints)

Após iniciar o servidor, acesse a documentação interativa oficial do Swagger em **`http://localhost:8000/docs`**.

* **`GET /`**: Rota raiz de boas-vindas.
* **`GET /api/v1/health`**: Verifica a saúde do sistema e testa ativamente a conexão com o Postgres e MongoDB.
* **`GET /api/v1/sobre`**: Retorna dados de equipes e relacionamentos complexos do banco (Professor, Disciplina, Stacks, Tecnologias e Linguagens).

---

## Estrutura de Diretórios Interna

```text
├── alembic/                  # Configurações e scripts de migração do banco relacional
│   └── versions/             # Histórico de alterações e dados seeds estruturados
├── app/
│   ├── api/
│   │   └── v1/               # Controladores e Rotas da API (health e sobre)
│   ├── core/
│   │   ├── config.py         # Variáveis e configurações obtidas do .env
│   │   ├── database.py       # Gerenciamento de conexões com Postgres e MongoDB
│   │   └── seed_mongo.py     # Script de inicialização automática de usuários no MongoDB
│   ├── models/               # Modelos ORM SQLAlchemy (relacionamento 1:1, 1:N, N:M)
│   ├── schemas/              # Schemas Pydantic (validação de dados e Swagger)
│   ├── repositories/         # Camada de abstracao de dados (queries SQL)
│   ├── services/             # Logica de negocio intermediaria
│   └── main.py               # Inicializador do app FastAPI e eventos de startup
├── env_example               # Template visível de variáveis de ambiente para os alunos
├── pyproject.toml            # Arquivo de dependências do Poetry
└── requirements.txt          # Dependências legíveis para instalação via pip tradicional
```
