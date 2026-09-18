# Formato de ADR (Architecture Decision Record) inferido

Use este template quando, durante a análise (Fases 2-4 de `discovery-process.md`), você identificar uma **decisão arquitetural significativa** já embutida no código — mesmo sem documentação original. Exemplos de decisões que merecem um ADR:

- Escolha de acesso a dados (ex: EF Core vs EF6 vs Dapper vs ADO.NET puro).
- Estilo de comunicação entre serviços (ex: WCF/SOAP vs REST vs mensageria).
- Estratégia de autenticação/autorização (ex: Forms Auth clássico vs JWT vs Identity).
- Padrão de camadas/modularização (ex: monolito vs Clean Architecture vs N-Layer; ou, em legado clássico, Modelo/Dados/Negócio).
- Framework alvo por projeto, quando há decisão explícita de não migrar (.NET Framework mantido propositalmente em um projeto específico).
- **Acoplamento entre projetos via chamada de serviço (WS/WCF/ASMX) em vez de referência direta** — quando um projeto chama a camada de Negócio de outro via rede em vez de `ProjectReference`. Registre isso como ADR sempre que for um padrão consistente (não uma exceção isolada). **Não presuma o motivo** — pode ser um padrão de camadas deliberado (Negócio exposto como serviço para reaproveitamento entre projetos), pode ser resultado de reorganização histórica do repositório, pode ser outra coisa. Descreva só o que foi observado no código (quem chama quem, com que frequência/consistência) e deixe qualquer hipótese de causa na seção "Perguntas em aberto" do ADR — nunca na seção "Contexto" ou "Decisão".

**Não gere ADR para cada detalhe pequeno.** Só para decisões que, se erradas ou mudadas, teriam impacto real na arquitetura. Se um projeto não revelar nenhuma decisão desse porte, não force a criação de um ADR.

## Critério de "Confiança"

Segue o critério único da skill — ver `confidence-criteria.md`. Resumo: baseado em repetição/consistência do padrão no código, nunca em quão certo o modelo está do motivo por trás dele.

## Template (baseado no formato Nygard, adaptado)

```markdown
---
schema_version: 1
artifact_type: ADR
id: ADR-{NNNN}
status: INFERRED
owner_skill: analyze-legacy-solution
created_at: {ISO-8601}
updated_at: {ISO-8601}
title: {Título curto da decisão}
confidence: HIGH | MEDIUM | LOW
---

# ADR-{NNNN}: {Título curto da decisão}

**Status:** Inferido a partir do código (não é um registro histórico oficial — a equipe pode confirmar ou corrigir)
**Data da inferência:** {DATA_ISO}
**Projeto(s) afetado(s):** {NomeDoProjeto ou lista}
**Confiança:** Alta | Média | Baixa <!-- ver critério objetivo acima -->

## Contexto
(O que no código levou a essa conclusão — sem especular motivação de negócio que não está no código.)

## Decisão (observada)
(Qual foi, aparentemente, a escolha feita — em 1-2 frases.)

## Evidências
- (arquivo/padrão 1 que sustenta a inferência)
- (arquivo/padrão 2, se houver)

## Consequências observadas
- (o que essa escolha implica hoje, positivo ou negativo, com base no que foi visto no código — ex: acoplamento, dificuldade de teste, débito técnico)

## Perguntas em aberto
- (o que só o time consegue confirmar: foi decisão deliberada ou acidente histórico? há plano de mudar?)
```

## Onde salvar

`.github/copilot-knowledge/decisions/ADR-{NNNN}-{slug-do-titulo}.md`, com ID obtido por `.github/skill-contracts/scripts/next_id.py`. Referencie em `SOLUTION-OVERVIEW.md` e reconstrua o `INDEX.md` pelo script compartilhado.
