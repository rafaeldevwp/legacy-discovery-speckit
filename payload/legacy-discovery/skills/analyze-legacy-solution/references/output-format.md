# Formato de saída e persistência local

O conhecimento gerado deve ser **gravado em disco** (use a ferramenta de edição de arquivos), não só mostrado no chat:

```
.github/copilot-knowledge/
├── INDEX.md                      ← ponto de entrada único, leia SEMPRE primeiro
├── SOLUTION-OVERVIEW.md
├── projects/
│   ├── PROJECT-nome-do-projeto-1.md
│   └── PROJECT-nome-do-projeto-2.md
├── decisions/                    ← ADRs inferidos (ver adr-format.md)
│   └── ADR-0001-acesso-a-dados.md
├── deep-dives/                   ← aprofundamentos por classe/módulo, só sob pedido (ver deep-dive.md)
│   └── DEEP-DIVE-negocio-calculadora-de-desconto.md
├── investigations/
│   └── INVESTIGATION-20260825-calculo-incorreto.md
├── impact-analyses/
│   └── IMPACT-20260825-calcular-frete.md
└── handoffs/
    └── HANDOFF-0001-alterar-consulta.md
```

Antes de criar qualquer saída, leia `.github/skill-contracts/artifact-naming.md` e `.github/skill-contracts/lifecycle.md`.

## `INDEX.md` — leia este arquivo antes de qualquer outro

É só uma tabela/manifesto, sem prosa — o arquivo mais barato de ler de toda a base de conhecimento. Serve para responder rápido "o que já existe?" sem abrir `SOLUTION-OVERVIEW.md` inteiro.

```markdown
# Índice de conhecimento — {NomeDaSolution}

> Leia este arquivo primeiro, sempre. Ele diz o que existe; os outros arquivos têm o conteúdo.

**Última atualização:** {DATA_ISO}

## Overview
- [SOLUTION-OVERVIEW.md](./SOLUTION-OVERVIEW.md)

## Projetos
| Projeto | Módulo/Área | Profundidade | Última análise | Baseado em (.csproj modificado em) | Arquivo |
|---|---|---|---|---|---|
| {Nome} | {ex: Faturamento} | Estrutural (Fase 1-2) / Completa (Fase 3+) | {DATA_ISO} | {DATA_ISO} | [projects/PROJECT-{slug}.md](./projects/PROJECT-{slug}.md) |

## Decisões arquiteturais (ADRs)
| ID | Título | Confiança | Arquivo |
|---|---|---|---|
| ADR-0001 | {título} | Alta/Média/Baixa | [decisions/ADR-0001-....md](./decisions/ADR-0001-....md) |


## Aprofundamentos (deep-dives)
| Classe/Módulo | Projeto | Métodos cobertos | Última atualização | Arquivo |
|---|---|---|---|---|
| {NomeDaClasse} | {Nome} | {MétodoA, MétodoB, ...} | {DATA_ISO} | [deep-dives/DEEP-DIVE-{project-slug}-{class-slug}.md](./deep-dives/DEEP-DIVE-{project-slug}-{class-slug}.md) |

## Investigações de bug (skill investigate-legacy-bug)
| Sintoma | Data | Confiança da hipótese | Arquivo |
|---|---|---|---|
| {resumo} | {DATA_ISO} | {Alta/Média/Baixa} | [investigations/INVESTIGATION-{YYYYMMDD}-{slug}.md](./investigations/INVESTIGATION-{YYYYMMDD}-{slug}.md) |

## Análises de impacto (skill analyze-change-impact)
| Alvo | Data | Nível de risco | Arquivo |
|---|---|---|---|
| {classe/método} | {DATA_ISO} | {Alto/Médio/Baixo} | [impact-analyses/IMPACT-{YYYYMMDD}-{slug}.md](./impact-analyses/IMPACT-{YYYYMMDD}-{slug}.md) |

```

**Regra de manutenção (obrigatória):** nunca edite o `INDEX.md` manualmente. Depois de criar ou atualizar artefatos, execute `.github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge`. O script é o único writer do índice e deve reconstruí-lo de forma determinística a partir do frontmatter. Se ele não puder ser executado, informe a falha explicitamente; não faça manutenção parcial à mão.

## `SOLUTION-OVERVIEW.md`

Comece com:

```yaml
---
schema_version: 1
artifact_type: SOLUTION_OVERVIEW
id: SOLUTION-OVERVIEW
status: CURRENT
owner_skill: analyze-legacy-solution
created_at: {ISO-8601}
updated_at: {ISO-8601}
solution_name: {NomeDaSolution}
solution_path: {caminho relativo}
---
```

- Nome da solution, quantidade de projetos, framework(s) — se for híbrida (parte moderna, parte .NET Framework clássico), deixe isso explícito logo no topo.
- **Visão de arquitetura em 2 níveis, inspirada em C4** (sem gerar diagrama visual — só a estrutura textual, que já é o que o grafo de dependências dá):
  - *Nível Contexto:* 1-2 frases sobre o que o sistema faz como um todo e quem/o que interage com ele (se identificável pelo código — ex: outra API consumida, fila de mensageria, banco externo).
  - *Nível Contêineres (= projetos):* **dois grafos, não um só**:
    - **Grafo de compilação** (`ProjectReference`): ex: `Api → Application → Domain ← Infra`.
    - **Grafo de chamadas de serviço** (WS/WCF/ASMX/HTTP entre projetos, da Fase 2.5): ex: `ProjetoA.WS → chama → ProjetoB.Negocio`. **Este é o que costuma revelar acoplamento escondido** — projetos sem relação nenhuma no grafo de compilação podem aparecer fortemente ligados aqui. Se um projeto de destino não foi encontrado localmente, marque como "externo".
- Padrão arquitetural identificado (Clean Architecture, N-Layer, Monolito) — ou "a confirmar". Inclua `(confiança: Alta/Média/Baixa)` — ver `confidence-criteria.md`.
- Tabela: `Projeto | Camada | Resumo em 1 linha | Link para projects/PROJECT-{slug}.md`.
- Seção "Decisões arquiteturais inferidas": lista curta com link para cada ADR gerado em `decisions/`.
- Riscos gerais da solution (3-6 bullets).
- Data da última análise completa (ISO 8601).

## `projects/PROJECT-{project-slug}.md`

Siga exatamente `project-template.md`.

## `decisions/ADR-*.md`

Gerados durante a Fase 4 da análise, quando uma decisão arquitetural de peso é identificada. Siga `adr-format.md`. Não gerar um ADR por detalhe pequeno — só decisões que importam de verdade.

## Artefatos TO-BE

A V2 desta skill **não gera RFC de modernização, SPEC, DESIGN ou TASKS**. Quando o usuário quiser mudar o sistema, preserve o entendimento AS-IS e encaminhe para `prepare-speckit-context`, que produzirá o `SPECKIT_HANDOFF` para o Spec Kit. RFCs V1 existentes continuam válidos como histórico e são aceitos pelos scripts de compatibilidade.

## `deep-dives/*.md`

**Não gerar durante a análise padrão.** Só quando o usuário pedir explicitamente para aprofundar uma regra/classe/método específico. Siga `deep-dive.md` — **um arquivo `DEEP-DIVE-{project-slug}-{class-slug}.md` por classe/módulo, com uma seção por método**. Referencie-o no `projects/PROJECT-{project-slug}.md` correspondente e reconstrua o índice pelo script compartilhado.

## Regra de staleness (evita reprocessar sem necessidade)

`source_modified_at` do `.csproj` é um **sinal estrutural**, não prova de frescor comportamental. Use-o para decidir se a estrutura do projeto precisa ser atualizada, mas não para afirmar que regras/métodos continuam idênticos.

Antes de reprocessar:

1. verifique se o artefato relevante está `CURRENT`;
2. verifique se existe sinal concreto de mudança no alvo (pedido de refresh, diff/commit conhecido, arquivo relevante alterado, inconsistência com investigação recente);
3. se não houver sinal e o pedido estiver coberto, reutilize o conhecimento;
4. se houver sinal, revalide **somente a área afetada** e marque/atualize o conhecimento correspondente.

Refresh parcial ("atualiza só o projeto X") → regrave apenas o projeto e artefatos diretamente afetados. Refresh completo → repita o processo para todos os projetos somente quando solicitado.

## Resposta no chat

Depois de gravar os arquivos, responda com um resumo curto (visão geral + tabela de projetos) e avise que os detalhes completos ficaram em `.github/copilot-knowledge/`. Não cole trechos grandes de código. Se não tiver certeza de algo, escreva "a confirmar".
