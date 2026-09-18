# Handoff contracts

## Investigation → impact/design

Required: `INVESTIGATION-*` with `status: CONFIRMED`, a synthetic-data regression test reference, expected behavior, and minimal execution evidence. A static hypothesis may produce draft planning only.

## Impact → coordinate

Required: `IMPACT-*` with target, risk level, direct/indirect dependents, external boundaries, affected documentation, and test coverage gaps.

## Coordinate → executor

Required in one FIX directory:

- approved `SPEC-FIX-NNNN.md`;
- approved `DESIGN-FIX-NNNN.md`;
- approved immutable `TASKS-FIX-NNNN.md`;
- `solution_path`, `build_command`, and regression command/scope;
- each TASK declares dependencies, unit-test gate, unit-test command/scope, and verifiable result.

## Executor → regression

Required:

- clean feature branch whose local HEAD equals its remote tracking branch;
- all TASK commits discoverable by `[TASK-NNN]` in Git history;
- `EXECUTION-FIX-NNNN.md` contains gates for every TASK;
- full solution build passed after each TASK;
- no blocked or push-blocked TASK.

## Regression → verification

Required: `REGRESSION-FIX-NNNN.md` with result, solution build, complete inventory, original bug test, omissions, and commit tested. Only `PASSED` is eligible for `VERIFIED`.

