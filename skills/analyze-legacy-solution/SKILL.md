---
name: analyze-legacy-solution
description: Analisa uma solution .NET (C#) legada — moderna (SDK-style) ou clássica (.NET Framework) — e produz entendimento da arquitetura geral e do core de cada projeto, incluindo ADRs inferidos das decisões arquiteturais embutidas no código. Use quando o usuário pedir para entender, documentar, mapear ou explicar uma solution/projeto .NET legado, perguntar "o que faz o projeto X", ou pedir um plano/RFC de modernização. Mantém conhecimento persistido localmente em .github/copilot-knowledge/ para reuso barato.
---

# Analyze Legacy .NET Solution

Você entende e documenta solutions .NET (C#) legadas de forma **econômica em tokens**, reaproveitando conhecimento já persistido em disco sempre que possível.

## Antes de tudo: existe conhecimento salvo?

Verifique `.github/copilot-knowledge/INDEX.md` primeiro — é o arquivo mais barato, e diz exatamente o que já existe (sem precisar abrir mais nada ainda).

- **Existe e o pedido não é de refresh** → use `SOLUTION-OVERVIEW.md`, `projects/PROJECT-*.md`, `decisions/ADR-*.md` e `deep-dives/DEEP-DIVE-*.md`. **Pare aqui — não escaneie o código.**
- **Não existe (nem o INDEX), ou o usuário pediu para atualizar/reanalisar** → siga `references/discovery-process.md` para escanear o código, e `references/output-format.md` para saber exatamente o que gerar, onde salvar, e como manter o `INDEX.md` sincronizado.
- **O usuário pediu explicitamente para aprofundar/detalhar/explicar uma regra, classe ou método específico** → carregue `references/deep-dive.md` em vez do processo padrão. Esse módulo é diferente de tudo o resto: lê código função por função, não é macro.

## Estrutura de referências desta Skill

- `references/discovery-process.md` — como escanear a solution em fases (estrutural → dependências → arquivos-âncora → busca dirigida), cobrindo `.csproj` moderno e clássico, e como dividir o trabalho em monorepos grandes por módulo/área.
- `references/frontend-legacy-patterns.md` — anchors específicos para front-end legado (ASP.NET Web Forms/ASPX, AngularJS, e o padrão híbrido dos dois combinados). Carregar quando o projeto analisado for de UI/Web.
- `.github/skill-contracts/` — contratos compartilhados de nomes, lifecycle, ownership, handoffs e falhas. Leia `artifact-naming.md`, `lifecycle.md` e `ownership.md` antes de criar artefatos.
- `references/output-format.md` — formato exato do `SOLUTION-OVERVIEW.md` e de cada `projects/PROJECT-{slug}.md`, e regra de staleness.
- `references/confidence-criteria.md` — critério único de confiança para inferências.
- `references/deep-dive.md` — **opcional**, só carregar quando o usuário pedir explicitamente para aprofundar/explicar em detalhe uma regra, classe ou método específico. Diferente do resto da skill (macro por padrão), este módulo lê o código função por função.
- `references/project-template.md` — template de `projects/PROJECT-{project-slug}.md`.
- `references/adr-format.md` — como registrar decisões arquiteturais **inferidas** do código como ADR (Architecture Decision Record). Carregue durante a Fase 4 de `discovery-process.md`, quando identificar uma decisão de peso (acesso a dados, comunicação entre serviços, auth, camadas).
- `references/rfc-improvement-proposal.md` — **opcional, só carregar se o usuário pedir explicitamente** um plano de modernização/melhoria (não faz parte da análise padrão de entendimento).

Carregue cada arquivo de `references/` só no momento em que precisar dele — não leia todos de uma vez se a tarefa for só consultar conhecimento já salvo.

Depois de gravar, execute `validate_artifacts.py` e só então `sync_index.py`, ambos em `.github/skill-contracts/scripts/`. IDs de ADR e RFC vêm de `next_id.py`; não derive IDs por contagem manual.
