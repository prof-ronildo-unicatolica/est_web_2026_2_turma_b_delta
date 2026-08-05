# Estágio II em Desenvolvimento Web — Turma B · Equipe Delta

Repositório oficial da equipe **Delta** (Turma B) na disciplina de **Estágio II em
Desenvolvimento Web** — 2026.2.

## Integrantes

- Mateus Peixoto de Sousa
- Ester Luiza de Souza Lima
- Thiago de Sousa Silva
- João Victor Crispim Pinheiro
- Maria Sharon Silva Oliveira

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
