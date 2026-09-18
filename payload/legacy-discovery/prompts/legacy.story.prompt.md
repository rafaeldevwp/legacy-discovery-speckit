---
description: "Fluxo guiado de uma história do PM: handoff → refinamento, parando em cada decisão humana."
argument-hint: "história do PM (literal)"
agent: agent
---

# HISTÓRIA — FLUXO GUIADO

## Objetivo
Levar uma história do PM até o refinamento pronto, encadeando as skills na ordem certa e parando sempre que o humano precisar decidir.

## Entradas Mínimas
- História do PM exatamente como foi escrita.
- Quem decide regra de negócio.

## Passos
1. Rode `python .github/skill-contracts/scripts/story_status.py --root .github/copilot-knowledge` e procure handoff/refinamento desta história. Se existir, retome do ponto em que parou.
2. Sem handoff `READY_FOR_SPECKIT`: siga [`prepare-speckit-context`](../skills/prepare-speckit-context/SKILL.md) com a história literal.
   - Se o handoff ficar `PARTIAL`/`BLOCKED`: pare, mostre os unknowns bloqueantes e o que o humano precisa fazer.
3. Com handoff pronto: siga [`refine-user-story`](../skills/refine-user-story/SKILL.md).
   - `AWAITING_HUMAN`: mostre as perguntas completas e pare. Oriente `/legacy.answer`.
   - `BLOCKED`: mostre o motivo e o menor passo para destravar; pare.
   - Sem pergunta bloqueante: mostre o resumo e oriente `/legacy.approve`; pare.
4. Rode validar → indexar → validar a cada artefato gravado.

## Saída Obrigatória
- Onde a história parou, por quê e qual comando o humano deve dar.

## Regras
- Não crie branch nem chame o Spec Kit: o fluxo termina no refinamento.
- Não aprove o refinamento: isso é `/legacy.approve`, digitado pelo humano.
- Cada skill mantém seus próprios checkpoints de confirmação.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
