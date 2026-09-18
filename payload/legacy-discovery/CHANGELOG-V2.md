# Changelog V2

## Added

- `prepare-speckit-context` skill.
- `SPECKIT_HANDOFF` artifact and `handoffs/` knowledge group.
- Knowledge Coverage matrix: structure, current behavior, business rules, dependencies, impact, external boundaries and tests.
- Coverage states: `COVERED`, `PARTIAL`, `UNKNOWN`, `STALE`, `NOT_APPLICABLE`.
- Bounded source-access policy and default discovery budget.
- Spec Kit integration reference for core SDD and official bug extension.
- `HANDOFF` support in `next_id.py`, `validate_artifacts.py` and `sync_index.py`.
- Migration and installation guides.

## Changed

- `analyze-legacy-solution` is explicitly AS-IS only.
- Reuse is now based on sufficiency/coverage, not just existence of `INDEX.md`.
- `.csproj` modification time is treated only as a structural staleness signal, not proof that business behavior is current.
- `investigate-legacy-bug` and `analyze-change-impact` hand off planned changes through `prepare-speckit-context`.
- Shared ownership/handoff/lifecycle contracts now reserve `.specify/` artifacts to Spec Kit.

## Archived from active discovery

- `coordinate-fix`.
- `execute-fix-plan`.
- `run-solution-regression`.

Their files remain under `legacy-workflow/` for history and rollback. V1 artifact validation remains supported.


## 2.1 — Prepare Feature Branch

- adicionada skill `prepare-feature-branch`;
- restaurado padrão `feature/mmYYYY/descricao-curta`;
- branch nasce de `main` após `fetch` + `pull --ff-only`;
- worktree sujo, divergência e branch existente bloqueiam;
- proibidos stash/reset/merge/rebase/force/push automáticos;
- `prepare-speckit-context` agora recomenda branch antes de `/speckit.specify`.

## 2.2 — Governance hardening, local-only skill artifacts and archive command

- politica de versionamento refinada: artefatos gerados por skill ficam local-only por padrao;
- artefatos do Spec Kit (`.specify/` e `specs/`) permanecem sob politica normal de versionamento do time;
- fluxo de governanca Git mantido sob responsabilidade da skill `prepare-feature-branch`;
- adicionada configuracao automatica de `.git/info/exclude` para evitar stage acidental de artefatos de skill;
- novo comando `archive_skill_artifacts.py` para arquivar e opcionalmente limpar artefatos/metadados de skill sem tocar dados de codigo do repositorio;
- orientacoes reforcadas para `constitution` do Spec Kit respeitar o AS-IS real do projeto;
- orientacoes reforcadas para `plan` respeitar a arquitetura existente e enriquecer decisoes com evidencias do handoff;
- maior interatividade nas skills ativas com checkpoints de confirmacao para reduzir ambiguidades.
