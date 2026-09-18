# One-TASK transaction

## Select

Read immutable `TASKS-FIX-NNNN.md` and `EXECUTION-FIX-NNNN.md`. Choose exactly one TASK whose dependencies are `PUBLISHED` in execution ledger + Git history. Record `IN_PROGRESS` in the ledger before editing. Never execute more than one TASK per human authorization.

## Implement

- Read only linked REQ/NFR/DEC/component context.
- Change only what is needed for the TASK's verifiable result.
- No opportunistic refactor or unplanned package/infrastructure change.
- A new requirement or design change blocks with `PLAN_INVALID`; return to `coordinate-fix` for revision and human reapproval.

## Validate, commit, and publish

1. Run `build-gate.md`.
2. Before commit, update the TASK entry in EXECUTION to `GATES_PASSED`, with `commit_ref: SELF`, gate commands/results, and changed files.
3. Run `validate_artifacts.py`, `sync_index.py`, and `validate_artifacts.py` again. Stage only TASK changes, the ledger, and the generated `INDEX.md`. Verify the staged diff contains no other TASK.
4. Commit once using `<type>(<scope>): <summary> [TASK-NNN]`.
5. Do not edit the ledger after commit and do not amend. `SELF` means the commit containing that entry.
6. Push using `git-workflow.md`.
7. Verify remote history contains the local HEAD and `[TASK-NNN]`. This derived fact makes the TASK `PUBLISHED`; no post-commit artifact mutation is needed.

If push fails, the TASK is `PUSH_BLOCKED` operationally even though the committed ledger says `GATES_PASSED`. The next run derives the effective state from Git plus the ledger.

## Human gate

After successful push, report TASK, gates, solution build, commit hash, remote branch, and next eligible TASK. Ask explicitly whether to continue, then stop.

## `EXECUTION-FIX-{NNNN}.md`

```markdown
---
schema_version: 1
artifact_type: FIX_EXECUTION
id: EXECUTION-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: IN_PROGRESS | BLOCKED
owner_skill: execute-fix-plan
created_at: {ISO-8601}
updated_at: {ISO-8601}
branch: feature/mmYYYY/slug
remote_url: {origin URL}
base_commit: {main HEAD}
base_build: PASSED
solution_path: {path from DESIGN}
spec_digest: {sha256}
design_digest: {sha256}
tasks_digest: {sha256}
block_reason: null
---

# FIX-{NNNN} — EXECUTION

## TASK-001
- State at commit: GATES_PASSED
- Commit ref: SELF
- Unit gate: REQUIRED | NOT_APPLICABLE
- Unit command/result: {command/result or approved reason}
- Solution build command/result: {command}/PASSED
- Files: {list}
- Attempts: {0-2}
- Completed at: {ISO-8601}
```

On resume, resolve `SELF` through commits containing `[TASK-NNN]`. When all TASKS are remotely published, derive effective execution state `IMPLEMENTED`; keep the committed ledger unchanged and do not create a metadata-only commit.
