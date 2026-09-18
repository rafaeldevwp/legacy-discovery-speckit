# Final verification

Read the shared contracts. `coordinate-fix` owns only `VERIFICATION-FIX-NNNN.md`; it must not edit structural knowledge owned by another skill. Record needed refreshes under `knowledge_updates`.

## Preconditions

- SPEC, DESIGN, and TASKS are `APPROVED` and unchanged since execution began.
- Git proves every TASK has one published `[TASK-NNN]` commit.
- `EXECUTION-FIX-NNNN.md` contains solution build gates for every TASK.
- `REGRESSION-FIX-NNNN.md` has `status: PASSED` and tests the published HEAD.

Anything else produces `status: BLOCKED`; do not rerun build/tests in this skill.

## `VERIFICATION-FIX-{NNNN}.md`

```markdown
---
schema_version: 1
artifact_type: FIX_VERIFICATION
id: VERIFICATION-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: VERIFIED | BLOCKED
owner_skill: coordinate-fix
created_at: {ISO-8601}
updated_at: {ISO-8601}
spec: SPEC-FIX-{NNNN}.md
design: DESIGN-FIX-{NNNN}.md
tasks: TASKS-FIX-{NNNN}.md
execution: EXECUTION-FIX-{NNNN}.md
regression: REGRESSION-FIX-{NNNN}.md
verified_commit: {published HEAD}
knowledge_updates: []
---

# FIX-{NNNN} — VERIFICATION

## Requirements
| Requirement | Task commits | Regression evidence | Result |
|---|---|---|---|
| REQ-001 | {hashes} | {suite/test} | PASSED/BLOCKED |

## External contracts and limitations
- {evidence or explicit not-verified block}

## Knowledge updates requested
- {target owner/type and reason; do not apply here}

## Conclusion
{why the FIX is VERIFIED or BLOCKED}
```

Only an effective `REGRESSION_PASSED → VERIFIED` transition is valid. Derive it from the owned artifacts; do not mutate approved SPEC/DESIGN/TASKS. Preserve investigation history; never rewrite a confirmed bug as if it never existed.
