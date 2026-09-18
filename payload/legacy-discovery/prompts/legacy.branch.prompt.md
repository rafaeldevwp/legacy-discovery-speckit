---
description: "Cria a branch feature/mmYYYY/descricao-curta a partir da main atualizada (prepare-feature-branch)."
argument-hint: "descrição curta da mudança (e opcionalmente REFINEMENT-NNNN)"
agent: agent
---

# CRIAR BRANCH

## Objetivo
Criar a branch de trabalho com baseline Git seguro antes do /speckit.specify.

## Entradas Mínimas
- Descrição curta para o slug.
- Refinamento/handoff da mudança, se houver.

## Passos
1. Rode `python .github/skill-contracts/scripts/story_status.py --root .github/copilot-knowledge` e localize a história.
2. Gate adicional: se existe `REFINEMENT` da história e ele não está `READY_FOR_SPECKIT`, pare e indique o comando pendente. Só siga sem refinamento se o usuário disser explicitamente que esta mudança não terá refinamento.
3. Leia e siga integralmente [`prepare-feature-branch`](../skills/prepare-feature-branch/SKILL.md) (pré-condições, confirmação do slug, script único).

## Saída Obrigatória
- `BRANCH_READY` com branch e commit base, ou o bloqueio.
- Próximo comando: `/speckit.specify <história>` lendo o HANDOFF e o REFINEMENT.

## Regras
- Nunca stash, reset, merge, rebase, force ou push.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
