---
description: "Registra a revisão humana de um refinamento e o libera como READY_FOR_SPECKIT, se os guardrails passarem."
argument-hint: "REFINEMENT-NNNN revisor: <seu nome>"
agent: agent
---

# APROVAR REFINAMENTO

## Objetivo
Transformar a revisão do humano, feita por este comando, em registro auditável — sem burlar nenhum guardrail.

## Entradas Mínimas
- ID do refinamento.
- Nome do revisor, digitado pelo humano. Se faltar, pergunte; nunca infira.

## Passos
1. Leia o refinamento e mostre um resumo: AC, GR, fatias e o que não foi decidido.
2. Confirme em uma frase: "Aprovar REFINEMENT-NNNN como <revisor>?" e aguarde "sim".
3. Atuando como [`refine-user-story`](../skills/refine-user-story/SKILL.md): `status: READY_FOR_SPECKIT`, `reviewed_by`, `reviewed_at` (agora, ISO-8601), `block_reason: null`, `revision` + 1.
4. Rode `python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge`.
5. Se falhar: restaure o status anterior, limpe `reviewed_by`/`reviewed_at`, rode validar de novo e liste os motivos.
6. Se passar: `sync_index.py` e validar de novo.

## Saída Obrigatória
- `APPROVED` com revisor e data, ou `NOT_APPROVED` com os erros do validador.
- Próximo comando: `/legacy.branch`.

## Regras
- Este comando só pode ser executado pelo humano; o agente nunca se autoaprova.
- Nunca relaxe regra do validador para aprovar.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
