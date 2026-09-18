---
description: "Mapeia o AS-IS de uma área do legado com a skill analyze-legacy-solution."
argument-hint: "área, projeto ou pergunta sobre o sistema"
agent: agent
---

# ANALISAR LEGADO

## Objetivo
Entender e persistir como o sistema funciona hoje, sem propor TO-BE.

## Entradas Mínimas
- Área, projeto ou pergunta informada após o comando.
- Se vazio, pergunte o escopo antes de começar.

## Passos
1. Leia e siga integralmente [`analyze-legacy-solution`](../skills/analyze-legacy-solution/SKILL.md).
2. Comece pelo `.github/copilot-knowledge/INDEX.md`; abra código só para lacunas.
3. Persista os artefatos e rode validar → indexar → validar.

## Saída Obrigatória
- Resumo curto do que foi aprendido e do que ficou desconhecido.
- Artefatos criados/atualizados.
- Próximo comando sugerido (`/legacy.handoff` se houver mudança pretendida).

## Regras
- Não planeje modernização nem produza spec/plan/tasks.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
