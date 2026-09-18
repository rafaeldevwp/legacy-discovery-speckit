---
description: "Valida os contratos dos artefatos das skills e reconstrói o INDEX."
agent: agent
---

# VALIDAR

## Objetivo
Garantir que os artefatos respeitam nomes, owners, lifecycle e guardrails.

## Entradas Mínimas
- Nenhuma.

## Passos
1. `python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge`
2. Se passar: `python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge` e validar de novo.
3. Se falhar: liste cada erro com o owner do artefato e o comando que corrige.

## Saída Obrigatória
- `validation passed` com contagem, ou a lista de erros com owner e comando sugerido.

## Regras
- Não corrija artefatos automaticamente; cada correção é feita pelo owner.
- Nunca edite o `INDEX.md` à mão.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
