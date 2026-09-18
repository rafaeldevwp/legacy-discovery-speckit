---
description: "Gera o SPECKIT_HANDOFF (AS-IS da mudança) com a skill prepare-speckit-context."
argument-hint: "descrição da mudança ou história do PM"
agent: agent
---

# HANDOFF

## Objetivo
Produzir contexto AS-IS suficiente e rastreável para a mudança, reaproveitando o conhecimento salvo.

## Entradas Mínimas
- Mudança/história informada após o comando.
- Confirme objetivo, critério de pronto e fluxo alvo (SDD ou BUG).

## Passos
1. Leia e siga integralmente [`prepare-speckit-context`](../skills/prepare-speckit-context/SKILL.md).
2. Knowledge preflight antes de abrir código; respeite o orçamento de discovery.
3. Persista o `HANDOFF` e rode validar → indexar → validar.

## Saída Obrigatória
- Status do handoff, acesso a código (quanto), unknowns bloqueantes, caminho.
- Próximo comando: `/legacy.refine` quando `READY_FOR_SPECKIT`.

## Regras
- Não crie solução TO-BE, spec, plan ou tasks.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
