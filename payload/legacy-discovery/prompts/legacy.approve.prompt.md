---
description: "Prepara a aprovação humana de um refinamento: mostra o resumo e o comando que só você pode rodar."
argument-hint: "REFINEMENT-NNNN"
agent: legacy-discovery
---

# APROVAR REFINAMENTO

## Objetivo
Dar ao humano tudo o que ele precisa para aprovar com consciência — sem que o agente aprove.

## Entradas Mínimas
- ID do refinamento (deve estar `READY_FOR_REVIEW`).

## Passos
1. Rode `python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge`. Se falhar, liste os erros e pare.
2. Leia o refinamento e mostre um resumo: AC, GR (com a prova de cada um), fatias e o que não foi decidido.
3. Mostre ao humano o comando para ele rodar **no terminal dele**:
   `python .github/skill-contracts/scripts/approve_refinement.py --id REFINEMENT-NNNN --reviewer "<nome>"`
4. Explique: o script confere tudo de novo, grava revisor e data, e sela o conteúdo (`approval_digest`); qualquer edição depois invalida a aprovação.
5. Quando o humano disser que rodou: `sync_index.py`, validar de novo e mostrar o resultado.

## Saída Obrigatória
- Resumo para revisão.
- O comando de aprovação, pronto para copiar.
- Após a execução humana: `APPROVED` confirmado pelo validador, e próximo comando `/legacy.branch`.

## Regras
- Você nunca executa `approve_refinement.py`; a fechadura nega e a aprovação é ato humano.
- Nunca grave `reviewed_by`, `approval_digest` ou `READY_FOR_SPECKIT` em um refinamento.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
- Se a fechadura (hook) negar uma ação, não contorne: explique o motivo e indique a ação humana.
