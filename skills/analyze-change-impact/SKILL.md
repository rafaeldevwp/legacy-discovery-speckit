---
name: analyze-change-impact
description: Mapeia o raio de impacto de uma mudança planejada num monorepo .NET legado — quem depende dessa classe/método/projeto, por referência direta ou por chamada de serviço, antes de você mexer nele. NÃO faz a mudança e não avalia se ela é boa ideia — só mostra o que pode ser afetado, pra você decidir com mais informação. Use quando alguém disser algo como "preciso alterar X, o que isso pode impactar", "quem depende desse método", "é seguro mexer aqui" — antes de começar a editar, não depois de já ter mudado.
---

# Analyze Change Impact

Você mapeia o **raio de impacto** de uma mudança planejada, antes que ela aconteça — reaproveitando ao máximo o que já foi descoberto pelas outras skills deste conjunto (`analyze-legacy-solution`, `investigate-legacy-bug`), em vez de escanear a solution inteira de novo a cada pergunta.

## Harness: comece sempre pelo que já existe

Se `.github/copilot-knowledge/` existir, use `SOLUTION-OVERVIEW.md`, `projects/PROJECT-*.md`, `decisions/ADR-*.md` e `deep-dives/DEEP-DIVE-*.md`. Antes de gravar, leia os contratos de nomes, lifecycle, ownership, handoffs e falhas em `.github/skill-contracts/`. Registre conhecimento estrutural descoberto em `knowledge_updates`; não edite artefatos de outro owner.

## Estrutura de referências

- `references/impact-mapping-process.md` — como levantar dependentes diretos (compilação), indiretos (chamada de serviço/WS), decisões arquiteturais relacionadas, e cobertura de teste existente — em fases de custo crescente, como as outras skills deste conjunto.
- `references/risk-report-format.md` — formato do relatório: nível de risco com critério objetivo, dependentes encontrados, e o que a análise não conseguiu ver (ex: projetos fora deste repositório).

Depois de gravar o `IMPACT`, execute `validate_artifacts.py`, `sync_index.py` e novamente `validate_artifacts.py` em `.github/skill-contracts/scripts/`.

## Regra inegociável

Esta skill nunca decide se a mudança deve ser feita, nem sugere como fazê-la com segurança — isso é julgamento do time, com contexto de negócio que a skill não tem. Ela só responde "o que existe hoje que depende disso" com a maior precisão possível dentro do que é observável no código.
