# RFC de modernização/melhoria (módulo OPCIONAL — só usar se solicitado explicitamente)

Diferente do resto desta skill (que documenta o que **é**), este arquivo serve para propor o que **poderia mudar**. Só entre aqui se o usuário pedir algo como "sugere um plano de modernização", "como migraríamos X", "RFC para trocar Y" — nunca por padrão durante uma análise de entendimento.

Não gere RFC junto com a análise inicial. RFC pressupõe que já existe entendimento consolidado (idealmente com ADRs já registrados) — gerar os dois juntos mistura "o que é" com "o que devia ser" e encarece a execução à toa.

## Template (inspirado em RFC de engenharia, não no formato IETF)

```markdown
---
schema_version: 1
artifact_type: RFC
id: RFC-{NNNN}
status: DRAFT
owner_skill: analyze-legacy-solution
created_at: {ISO-8601}
updated_at: {ISO-8601}
title: {Título da proposta}
---

# RFC-{NNNN}: {Título da proposta}

**Status:** Draft
**Autor:** Gerado por IA a partir da análise da solution — requer revisão humana antes de virar decisão
**Data:** {DATA_ISO}
**ADRs relacionados:** {links para .github/copilot-knowledge/decisions/*.md, se existirem}

## Resumo
(2-3 frases: o que está sendo proposto)

## Motivação / Problema
(Por que isso importa — baseado em pontos de atenção já registrados nos projects/*.md, não em suposições novas)

## Proposta
(O que mudaria, em termos concretos)

## Alternativas consideradas
- (Alternativa 1 — por que não foi a escolhida)
- (Alternativa 2)

## Riscos e trade-offs
- (o que se perde ou arrisca com essa mudança)

## Impacto em outros projetos da solution
(quais projetos do grafo de dependências seriam afetados)

## Perguntas em aberto para o time
- (decisões que só humanos devem tomar — ex: prioridade, orçamento, tolerância a risco)
```

## Onde salvar

`.github/copilot-knowledge/proposals/RFC-{NNNN}-{slug-do-titulo}.md`, com ID obtido por `.github/skill-contracts/scripts/next_id.py`. Deixe explícito no chat que é um rascunho para discussão humana, não uma decisão tomada.
