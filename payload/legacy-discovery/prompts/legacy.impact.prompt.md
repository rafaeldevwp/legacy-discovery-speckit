---
description: "Mapeia o raio de impacto de uma mudança com a skill analyze-change-impact."
argument-hint: "classe, método, endpoint ou contrato alvo"
agent: legacy-discovery
---

# ANALISAR IMPACTO

## Objetivo
Mostrar quem depende do alvo antes de alterá-lo.

## Entradas Mínimas
- Alvo exato, tipo da mudança e limite da análise.
- Se o alvo for amplo, proponha um recorte e aguarde.

## Passos
1. Leia e siga integralmente [`analyze-change-impact`](../skills/analyze-change-impact/SKILL.md).
2. Persista o `IMPACT` e rode validar → indexar → validar.

## Saída Obrigatória
- Nível de risco com critério.
- Dependentes diretos/indiretos e o que não foi possível ver.
- Próximo comando: `/legacy.handoff`.

## Regras
- Não decida se a mudança deve ser feita nem como fazê-la.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
- Se a fechadura (hook) negar uma ação, não contorne: explique o motivo e indique a ação humana.
