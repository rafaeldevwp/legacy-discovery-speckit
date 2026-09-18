# SPEC → DESIGN → TASKS

Read `.github/skill-contracts/{artifact-naming,lifecycle,ownership,handoffs}.md` first. Allocate one `FIX-NNNN` with `.github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type FIX`; all three artifacts share it and are owned by `coordinate-fix`.

## Gates

1. Investigation must be `CONFIRMED`; otherwise create drafts only and set `status: BLOCKED` with `block_reason: PLAN_INVALID`.
2. Impact analysis must cover the exact target and external boundaries.
3. Generate SPEC, then DESIGN, then TASKS. Human approval moves each from `READY_FOR_APPROVAL` to `APPROVED`.
4. After approval, the three artifacts are immutable. New information requires a coordinated revision of all affected artifacts, a new human approval, and an entry in `revision_history`.

## `SPEC-FIX-{NNNN}.md`

```markdown
---
schema_version: 1
artifact_type: FIX_SPEC
id: SPEC-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: READY_FOR_APPROVAL
owner_skill: coordinate-fix
created_at: {ISO-8601}
updated_at: {ISO-8601}
investigation: {relative link}
impact_analysis: {relative link}
approver: null
approved_at: null
---

# FIX-{NNNN} — SPEC: {objetivo}

## Problema e objetivo
{comportamento confirmado e resultado esperado, sem solução técnica}

## Escopo
- Incluído: {itens}
- Fora do escopo: {itens}

## Requisitos funcionais
### REQ-001 — {nome}
- Regra: O sistema deve {comportamento observável}.
- Aceite: Dado {contexto}, quando {ação}, então {resultado verificável}.

## Requisitos não funcionais
### NFR-001 — {nome}
- Medida verificável: {compatibilidade/desempenho/segurança/observabilidade}

## Restrições e perguntas abertas
- {restrição ou pergunta com responsável}

## Revision history
- {ISO-8601}: versão inicial
```

## `DESIGN-FIX-{NNNN}.md`

```markdown
---
schema_version: 1
artifact_type: FIX_DESIGN
id: DESIGN-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: READY_FOR_APPROVAL
owner_skill: coordinate-fix
created_at: {ISO-8601}
updated_at: {ISO-8601}
spec: SPEC-FIX-{NNNN}.md
solution_path: {relative path to .sln}
build_configuration: Release
build_command: {official full-solution command}
regression_command: {official complete regression command/script}
regression_scope: {pipeline/solution suites that define complete}
approver: null
approved_at: null
---

# FIX-{NNNN} — DESIGN: {objetivo}

## Solução e componentes
| Componente | Alteração | Requisitos |
|---|---|---|
| {projeto/classe/contrato} | {responsabilidade} | REQ-001, NFR-001 |

## Contratos e dados
{assinaturas/DTOs/compatibilidade, ou "sem alteração de contrato"}

## Decisões
### DEC-001 — {decisão}
- Escolha: {abordagem}
- Alternativas: {opções reais}
- Trade-offs: {custos e benefícios}
- Requisitos: REQ-001

## Mitigação por dependente
| Dependente | Risco | Mitigação | Evidência |
|---|---|---|---|
| {impact analysis} | {risco} | {ação} | {gate concreto} |

## Estratégia de testes
- Teste que comprovou o bug: {arquivo::teste}
- Unitários por TASK: {regra}
- Regressão completa: {comando, suites e ambiente não produtivo}

## Observabilidade e rollback
{sinais, limites e procedimento fornecido pelo time; não executar deploy}

## Revision history
- {ISO-8601}: versão inicial
```

`solution_path`, `build_command`, `regression_command` and `regression_scope` are mandatory. Multiple solutions without one designated root block approval.

## `TASKS-FIX-{NNNN}.md`

This is an immutable plan, not a runtime checklist. Execution state belongs exclusively to `EXECUTION-FIX-{NNNN}.md`.

```markdown
---
schema_version: 1
artifact_type: FIX_TASKS
id: TASKS-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: READY_FOR_APPROVAL
owner_skill: coordinate-fix
created_at: {ISO-8601}
updated_at: {ISO-8601}
spec: SPEC-FIX-{NNNN}.md
design: DESIGN-FIX-{NNNN}.md
approver: null
approved_at: null
---

# FIX-{NNNN} — TASKS: {objetivo}

## TASK-001 — {resultado coeso}
- Requisitos: REQ-001
- Design: DEC-001, {componente}
- Dependências: nenhuma
- Arquivos prováveis: {paths}
- Resultado verificável: {condição objetiva}
- Unit test gate: REQUIRED | NOT_APPLICABLE
- Unit test command/scope: {comando focado ou justificativa aprovada}

## TASK-002 — {resultado coeso}
- Requisitos: REQ-001, NFR-001
- Design: {decisão/componente}
- Dependências: TASK-001
- Arquivos prováveis: {paths}
- Resultado verificável: {condição}
- Unit test gate: REQUIRED | NOT_APPLICABLE
- Unit test command/scope: {comando ou justificativa}

## Traceability
| Requirement | Design | Tasks | Evidence expected |
|---|---|---|---|
| REQ-001 | DEC-001 | TASK-001, TASK-002 | {test/check} |

## Revision history
- {ISO-8601}: versão inicial
```

`NOT_APPLICABLE` is valid only for non-executable changes and requires an approved reason. Every requirement and mitigation must map to at least one TASK. Do not create tasks mechanically per file.
