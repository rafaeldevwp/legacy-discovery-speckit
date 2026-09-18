---
description: "Registra as respostas humanas às perguntas AMB-NN de um refinamento."
argument-hint: "REFINEMENT-NNNN AMB-02: <resposta>; AMB-03: <resposta>"
agent: legacy-discovery
---

# RESPONDER PERGUNTAS

## Objetivo
Gravar respostas humanas literais no refinamento e fazer a próxima rodada.

## Entradas Mínimas
- ID do refinamento.
- Uma resposta por `AMB-NN`, e quem respondeu (se não for o `decision_owner`, registre o nome).

## Passos
1. Atue como [`refine-user-story`](../skills/refine-user-story/SKILL.md) sobre o refinamento informado (mesmo arquivo, mesmo id).
2. Para cada resposta: `ANSWERED_BY_HUMAN` (ou `ASSUMPTION_ACCEPTED` se aceitou literalmente a sugestão), resposta literal, quem e quando.
3. Resposta ambígua: não interprete — pergunte de novo. Nova dúvida gerada: novo `AMB-NN`.
4. Atualize AC/GR/fatias afetados, incremente `revision`, recalcule `open_questions`.
5. Mantenha `AWAITING_HUMAN` enquanto houver `OPEN_HUMAN`; sem nenhuma, grave `READY_FOR_REVIEW`. Rode validar → indexar → validar.

## Saída Obrigatória
- Perguntas que continuam abertas (completas) ou `NONE`.
- Próximo comando: `/legacy.answer` de novo ou `/legacy.approve`.

## Regras
- Não mude `Blocking` de YES para NO para acelerar.
- Não apague pergunta sem resposta.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
- Se a fechadura (hook) negar uma ação, não contorne: explique o motivo e indique a ação humana.
