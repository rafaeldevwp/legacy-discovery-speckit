---
description: "Arquiva os artefatos locais das skills num ZIP fora do repositório (e opcionalmente limpa)."
argument-hint: "(opcional) limpar"
agent: legacy-discovery
---

# ARQUIVAR

## Objetivo
Reduzir poluição local sem tocar código nem artefatos do Spec Kit.

## Entradas Mínimas
- Informe `limpar` para também remover os artefatos após arquivar.

## Passos
1. Sem `limpar`: `python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive`.
2. Com `limpar`: mostre o que será removido, peça confirmação explícita e só então rode com `--mode archive-and-clean`.

## Saída Obrigatória
- Caminho do arquivo gerado e, se limpou, o que foi removido.

## Regras
- Nunca use `archive-and-clean` sem confirmação explícita nesta conversa.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
- Se a fechadura (hook) negar uma ação, não contorne: explique o motivo e indique a ação humana.
