---
description: "Investiga um bug no legado com a skill investigate-legacy-bug (localiza, não corrige)."
argument-hint: "sintoma observado e comportamento esperado"
agent: agent
---

# INVESTIGAR BUG

## Objetivo
Localizar o ponto provável da falha com evidência e nível de confiança.

## Entradas Mínimas
- Sintoma, comportamento esperado, ambiente e urgência.
- Se faltar algum, pergunte antes da triagem.

## Passos
1. Leia e siga integralmente [`investigate-legacy-bug`](../skills/investigate-legacy-bug/SKILL.md).
2. Persista o `INVESTIGATION` e rode validar → indexar → validar.

## Saída Obrigatória
- Hipóteses rankeadas com evidência.
- Caminho do artefato.
- Próximo comando: `/speckit.bug.assess` (correção pontual) ou `/legacy.impact` → `/legacy.handoff` (mudança que precisa de spec).

## Regras
- Nunca escreva nem sugira correção de código de produção.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
