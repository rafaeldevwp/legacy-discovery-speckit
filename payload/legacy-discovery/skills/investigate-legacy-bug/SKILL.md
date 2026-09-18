---
name: investigate-legacy-bug
description: Investiga onde um bug/comportamento inesperado provavelmente está, num monorepo .NET legado com múltiplos projetos e chamadas de serviço entre eles. NÃO corrige o código — só aponta o(s) ponto(s) mais prováveis da falha, com evidência e nível de confiança. Pode também gerar, sob pedido, um teste de regressão executável que reproduz o cenário relatado. Use quando alguém relatar um problema em produção/negócio (ex: "o cálculo X está dando resultado errado", "PO reportou bug em Y") e for preciso descobrir onde no código isso pode estar acontecendo, antes de decidir como corrigir.
---

# Investigate Legacy Bug

Você investiga onde um problema relatado provavelmente está — **não conserta, só localiza e explica com evidência.** É uma skill de triagem: sair de "temos um problema no cálculo X" para "provavelmente é aqui, e é por isso" o mais rápido e barato possível, mesmo numa esteira grande com múltiplos projetos e chamadas externas.

## Harness: reaproveite o que existir, e construa o que não existir

Se `.github/copilot-knowledge/` existir, leia `INDEX.md`, `projects/PROJECT-*.md`, `decisions/ADR-*.md` e `deep-dives/DEEP-DIVE-*.md`. Antes de gravar, leia os contratos de nomes, lifecycle, ownership, handoffs e falhas em `.github/skill-contracts/`.

**Se não existir nada ainda (cenário mais comum na prática — ninguém roda análise macro só por precaução), não bloqueie e não exija isso como pré-requisito.** Investigue normalmente. Preserve descobertas reutilizáveis no próprio `INVESTIGATION` e em `knowledge_updates`; não edite artefatos pertencentes a outra skill. Ver "Construção orgânica do harness" em `triage-process.md`.

## Interacao com humano

Antes da triagem tecnica, confirme:

1. sintoma observado e comportamento esperado;
2. ambiente e janela temporal do problema;
3. impacto de negocio e urgencia.

Quando houver mais de uma interpretacao possivel do bug, pergunte antes de aprofundar.

## Processo

1. `references/triage-process.md` — como estreitar do sintoma relatado até 1-3 candidatos prováveis, em fases de custo crescente. **Pare assim que a confiança for alta o suficiente** — não é preciso passar por todas as fases se a resposta já apareceu cedo.
2. `references/hypothesis-confidence.md` — critério de confiança específico para hipóteses de bug (diferente do critério de "padrão arquitetural" da outra skill — aqui é "o quanto a evidência aponta pra esse ser o ponto da falha").
3. `references/investigation-report-format.md` — formato do relatório final: hipóteses rankeadas, evidências, o que já foi descartado, e o próximo passo pra confirmar. **Nunca inclui uma correção proposta** — isso é fora do escopo desta skill por decisão explícita.
4. `references/regression-test-generation.md` — **opcional**, só carregar se o usuário pedir explicitamente um teste a partir de uma hipótese já investigada (confiança Média/Alta), executar esse teste ou registrar sua evidência. Gera um teste que assume o comportamento **esperado** (não o atual/bugado) — nasce vermelho de propósito, até alguém corrigir o código. Nunca usa dado pessoal real (CPF, etc.) — sempre sintético.

Depois de gravar o `INVESTIGATION`, execute `validate_artifacts.py`, `sync_index.py` e novamente `validate_artifacts.py` em `.github/skill-contracts/scripts/`.

## Regra inegociável

Esta skill nunca escreve, sugere ou aplica uma correção de código de produção. Se o usuário pedir a correção junto ("acha o bug e já corrige"), localize e explique o ponto da falha normalmente, e diga explicitamente que a correção é uma tarefa separada — não decida sozinho como corrigir regra de negócio legada sem revisão humana. **Gerar um teste de regressão (módulo opcional) não viola essa regra** — o teste prova a falha, não conserta ela.

## Handoff V2

Quando a investigação estiver suficiente para orientar uma mudança, não gere design nem plano de correção. Encaminhe para `prepare-speckit-context`, que reunirá esta evidência com impacto, constraints e knowledge coverage antes do Spec Kit.
