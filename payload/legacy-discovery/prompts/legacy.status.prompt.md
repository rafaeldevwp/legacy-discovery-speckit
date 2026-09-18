---
description: "Mostra o estado de cada história (handoff, refinamento, perguntas abertas) e o próximo comando."
argument-hint: "(opcional) HANDOFF-NNNN ou REFINEMENT-NNNN"
agent: legacy-discovery
---

# STATUS

## Objetivo
Dar visão rápida e determinística do andamento das histórias.

## Entradas Mínimas
- Opcionalmente um ID.

## Passos
1. Execute `python .github/skill-contracts/scripts/story_status.py --root .github/copilot-knowledge` (com `--id <ID>` se informado).
2. Mostre a saída como está.

## Saída Obrigatória
- A tabela gerada pelo script, sem reinterpretação.

## Regras
- Somente leitura.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
- Se a fechadura (hook) negar uma ação, não contorne: explique o motivo e indique a ação humana.
