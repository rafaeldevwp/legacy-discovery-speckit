# Handoff contracts

Schema version: `2`.

## Discovery → Spec Kit (V2 primary contract)

Required: one `SPECKIT_HANDOFF` produced by `prepare-speckit-context`.

A handoff `READY_FOR_SPECKIT` must contain:

- the user request without a TO-BE reinterpretation;
- coverage matrix for structure, current behavior, business rules, dependencies, impact, external boundaries and tests;
- current behavior and relevant components;
- compatibility constraints derived from the AS-IS;
- impact surface and external boundaries;
- evidence references;
- blocking and non-blocking unknowns;
- an explicit section stating what Discovery did **not** decide;
- target flow (`SDD` or `BUG`);
- suggested Spec Kit invocation referencing the handoff.

Forbidden in this handoff:

- architecture TO-BE;
- library/framework selection;
- implementation tasks;
- remediation proposal presented as decided design;
- writes to `.specify/`.

## Handoff → Story refinement

`refine-user-story` consome um `SPECKIT_HANDOFF` relacionado à história. Sem handoff, o refinamento só pode ficar `AWAITING_HUMAN` ou `BLOCKED` (`HANDOFF_MISSING`). Handoff `PARTIAL`/`BLOCKED` impede refinamento `READY_FOR_SPECKIT`; seus unknowns bloqueantes entram no registro de ambiguidades.

## Story refinement → Spec Kit

A `STORY_REFINEMENT` `READY_FOR_SPECKIT` must contain:

- a história do PM literal, separada da interpretação;
- registro de ambiguidades com fonte (`STORY`, `KNOWLEDGE`, `CODE`, `HUMAN`) e evidência ou resposta humana;
- nenhuma ambiguidade `OPEN_HUMAN` bloqueante;
- critérios de aceite `AC-NN` com origem (`STORY`, `HUMAN:AMB-NN` respondida, `AS-IS:<evidência>`);
- guardrails de regressão `GR-NN` com prova (`EXISTING_TEST`, `CHARACTERIZATION_TEST_REQUIRED`, `MANUAL_CHECK`);
- plano de execução em fatias `SLICE-NN` cobrindo todo AC e todo GR, sem ciclo;
- seção explícita do que **não** foi decidido;
- revisão humana registrada.

Forbidden in this refinement:

- arquitetura TO-BE, biblioteca/framework, nova camada;
- tasks de código, arquivos a alterar, estimativa em horas;
- AC derivado de suposição não confirmada pelo humano;
- writes to `.specify/`, `specs/` ou artefatos de outro owner.

O `/speckit.specify` lê o handoff (AS-IS) **e** o refinamento (AC, respostas humanas, guardrails, fatias). O refinamento não substitui `/speckit.clarify`: ambiguidades não bloqueantes seguem para lá.

## Investigation → handoff

A confirmed investigation may be consumed by `prepare-speckit-context` when the requested change is related to the investigated behavior. `STATIC_HYPOTHESIS` can support only `PARTIAL` handoff unless independent evidence closes the uncertainty.

## Impact → handoff

For behavior or contract changes, prefer a relevant `IMPACT_ANALYSIS`. If none exists, `prepare-speckit-context` may perform bounded impact discovery, but must mark any unseen external consumer explicitly.

## V1 compatibility contracts

The contracts below apply only to legacy FIX artifacts already present or when the team deliberately restores the archived V1 workflow.

### Investigation → impact/design

Required: `INVESTIGATION-*` with `status: CONFIRMED`, a synthetic-data regression test reference, expected behavior, and minimal execution evidence. A static hypothesis may produce draft planning only.

### Impact → coordinate

Required: `IMPACT-*` with target, risk level, direct/indirect dependents, external boundaries, affected documentation, and test coverage gaps.

### Coordinate → executor

Required in one FIX directory:

- approved `SPEC-FIX-NNNN.md`;
- approved `DESIGN-FIX-NNNN.md`;
- approved immutable `TASKS-FIX-NNNN.md`;
- `solution_path`, `build_command`, and regression command/scope;
- each TASK declares dependencies, unit-test gate, unit-test command/scope, and verifiable result.

### Executor → regression

Required:

- clean feature branch whose local HEAD equals its remote tracking branch;
- all TASK commits discoverable by `[TASK-NNN]` in Git history;
- `EXECUTION-FIX-NNNN.md` contains gates for every TASK;
- full solution build passed after each TASK;
- no blocked TASK.

### Regression → verification

Required: `REGRESSION-FIX-NNNN.md` with result, solution build, complete inventory, original bug test, omissions, and commit tested. Only `PASSED` is eligible for `VERIFIED`.
