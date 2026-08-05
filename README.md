# Estágio II em Desenvolvimento Web — Turma B · Equipe Delta

Repositório oficial da equipe **Delta** (Turma B) na disciplina de **Estágio II em
Desenvolvimento Web** — 2026.2.

## Integrantes

- Mateus Peixoto de Sousa
- Ester Luiza de Souza Lima
- Thiago de Sousa Silva
- João Victor Crispim Pinheiro
- Maria Sharon Silva Oliveira

## Começando

Este repositório **já vem com o projeto-base pronto**: backend em FastAPI, frontend em
React e toda a infraestrutura (PostgreSQL, MongoDB, RabbitMQ) em Docker. Você não
precisa criar a estrutura do zero — seu trabalho é evoluí-la a cada sprint.

Para colocar tudo no ar:

```bash
# 1. Clone o repositório (o clone já cai na branch develop)
git clone <url-ssh-deste-repositorio>
cd <pasta-do-repositorio>

# 2. Suba a stack completa (a primeira vez demora alguns minutos)
docker compose up -d --build

# 3. Confirme que a API respondeu
curl http://localhost:8000/health
```

| Serviço | Endereço |
| :--- | :--- |
| Frontend | http://localhost:5173 |
| API + Swagger | http://localhost:8000/docs |
| Painel do RabbitMQ | http://localhost:15672 |

📖 **Passo a passo completo** — pré-requisitos de instalação, como rodar o backend fora
do Docker, o que já vem pronto e solução de problemas comuns:
[**Guia de Primeiros Passos**](https://github.com/prof-ronildo-unicatolica/estagio-desenvolvimento-web/blob/main/docs/04_guias_tutoriais/guia_primeiros_passos.md)

## Fluxo de trabalho

A branch padrão do repositório é a **`develop`** — é nela que o trabalho da equipe
acontece. A `main` é reservada para versões estáveis e **não** recebe commits diretos.

**Regras:**

1. Trabalhe sempre a partir da `develop`, e nunca faça commit direto nela.
2. Crie sua branch **a partir da `develop`**, com nome descritivo
   (ex: `feature/cadastro-hospede`, `fix/validacao-cpf`).
3. Abra o **Pull Request sempre com destino à `develop`** — nunca para a `main`.
4. O PR precisa da revisão de pelo menos um colega antes do merge.

Revisar os Pull Requests dos colegas também conta como contribuição avaliada.

```bash
# 1. Garanta que sua develop local está atualizada
git checkout develop
git pull origin develop

# 2. Crie sua branch a partir da develop
git checkout -b feature/minha-tarefa

# 3. Trabalhe, comite e envie
git add .
git commit -m "feat: descreve o que foi feito"
git push -u origin feature/minha-tarefa

# 4. Abra o Pull Request no GitHub com destino à branch develop
```

## Documentação da disciplina

Plano de ensino, arquitetura, roadmap das sprints e guias de instalação:
https://github.com/prof-ronildo-unicatolica/estagio-desenvolvimento-web
