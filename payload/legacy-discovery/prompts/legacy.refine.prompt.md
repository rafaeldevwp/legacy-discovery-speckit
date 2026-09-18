---
description: "PO técnico: refina a história do PM e gera o STORY_REFINEMENT com a skill refine-user-story."
argument-hint: "história do PM (literal) e, se houver, HANDOFF-NNNN"
agent: agent
---

# REFINAR HISTÓRIA

## Objetivo
Transformar a história do PM em refinamento técnico rastreável, reportando ao humano toda ambiguidade que nem o conhecimento nem o código respondem.

## Entradas Mínimas
- História do PM exatamente como foi escrita.
- HANDOFF relacionado (se não informado, procure no INDEX).
- Quem decide regra de negócio (pergunte se não informado).

## Passos
1. Leia e siga integralmente [`refine-user-story`](../skills/refine-user-story/SKILL.md) e suas referências.
2. Sem handoff relacionado: faça só a triagem e recomende `/legacy.handoff`.
3. Persista o `REFINEMENT` e rode validar → indexar → validar.
4. Se houver perguntas `OPEN_HUMAN`, mostre-as completas e pare.

## Saída Obrigatória
- Status e revisão do refinamento.
- Ambiguidades resolvidas por fonte (história/conhecimento/código/humano).
- Perguntas abertas, completas.
- Próximo comando: `/legacy.answer` ou `/legacy.approve`.

## Regras
- Nunca aplique a sugestão do PO sem resposta humana.
- Nunca marque `READY_FOR_SPECKIT` por este comando: aprovação é `/legacy.approve`.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
