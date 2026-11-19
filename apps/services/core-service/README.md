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
Tenha Docker Compose e Python instalados. Configure os arquivos de ambiente
antes de iniciar os serviços.

### 2. Configurar o Arquivo de Variáveis (.env)
Duplique o arquivo `.env.exemplo` da raiz com o nome `.env`. Preencha as
credenciais de PostgreSQL, MongoDB e RabbitMQ com valores próprios do ambiente.
O exemplo deixa os campos secretos vazios para impedir que um valor padrão seja
usado sem querer.

Para executar a API diretamente no host, copie também `env_example` deste
diretório para `.env` e configure os endereços locais dos bancos nesse arquivo.

Gere uma chave JWT forte em vez de reutilizar uma chave do exemplo:

```bash
openssl rand -hex 32
```

Configure o resultado em `SECRET_KEY`. `CORS_ALLOWED_ORIGINS` deve conter apenas
as origens reais do frontend, separadas por vírgula.

Na raiz do projeto, inicie os serviços depois de preencher `.env`:

```bash
docker compose up -d --build
```

### 3. Administrador e credenciais antigas

O seed de administrador do PostgreSQL foi removido por uma nova migração. As
credenciais antigas de MongoDB não são mais criadas no início da API; para
remover a conta de demonstração que já possa existir nesse banco, execute uma
vez após iniciar os serviços de dados:

```bash
docker compose exec core-service poetry run python -m app.core.cleanup_legacy_mongo_admin
```

Depois de aplicar as migrações (`alembic upgrade head`), crie um administrador
informando valores somente no ambiente do processo. O script não imprime nem
armazena a senha em texto:

```bash
# Informe cada valor quando solicitado; a senha não aparece na tela.
read -r ADMIN_NAME
read -r ADMIN_EMAIL
read -r -s ADMIN_PASSWORD
export ADMIN_NAME ADMIN_EMAIL ADMIN_PASSWORD
docker compose exec \
  -e ADMIN_NAME="$ADMIN_NAME" \
  -e ADMIN_EMAIL="$ADMIN_EMAIL" \
  -e ADMIN_PASSWORD="$ADMIN_PASSWORD" \
  core-service poetry run python -m app.core.create_admin
unset ADMIN_PASSWORD
```

Credenciais que já foram usadas em um deploy precisam ser rotacionadas no
provedor que mantém esse ambiente e atualizadas nos segredos de execução; um PR
não consegue confirmar nem alterar segredos de infraestrutura. Trocar
`SECRET_KEY` invalida os JWTs existentes.

---

### 4. Instalação e Execução

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
3. **Rodar Migrações (Alembic)**:
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
2. **Rodar Migrações (Alembic)**:
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
* **`POST /api/v1/auth/register`** e **`POST /api/v1/auth/login`**: Cadastro e login com JWT.
* **`GET /api/v1/hospedes/me`**: Perfil de hóspede vinculado à conta autenticada.

As portas de PostgreSQL, MongoDB e RabbitMQ no Compose ficam vinculadas a
`127.0.0.1`; não as publique diretamente na internet.

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
│   │   ├── create_admin.py   # Criação explícita de administrador via ambiente
│   │   └── cleanup_legacy_mongo_admin.py # Remoção pontual da conta antiga de demonstração
│   ├── models/               # Modelos ORM SQLAlchemy (relacionamento 1:1, 1:N, N:M)
│   ├── schemas/              # Schemas Pydantic (validação de dados e Swagger)
│   ├── repositories/         # Camada de abstracao de dados (queries SQL)
│   ├── services/             # Logica de negocio intermediaria
│   └── main.py               # Inicializador do app FastAPI e eventos de startup
├── env_example               # Template visível de variáveis de ambiente para os alunos
├── pyproject.toml            # Arquivo de dependências do Poetry
└── requirements.txt          # Dependências legíveis para instalação via pip tradicional
```
