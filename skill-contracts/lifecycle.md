# Lifecycle contract

Schema version: `1`. Status values are machine-readable English constants; prose may remain Portuguese.

## Effective FIX state

```text
DRAFT → READY_FOR_APPROVAL → APPROVED → IN_PROGRESS → IMPLEMENTED
      ↘ BLOCKED              ↘ BLOCKED      ↘ BLOCKED
IMPLEMENTED → REGRESSION_PASSED → VERIFIED
IMPLEMENTED → REGRESSION_FAILED
IMPLEMENTED → REGRESSION_UNSTABLE
```

This is a derived state, not a mutable field in the approved SPEC/DESIGN/TASKS:

- any plan artifact `BLOCKED` → `BLOCKED`;
- all three plan artifacts approved, no execution → `APPROVED`;
- `FIX_EXECUTION.status: IN_PROGRESS` with remaining TASKS → `IN_PROGRESS`;
- every TASK resolved as `PUBLISHED` from remote history → `IMPLEMENTED`;
- `FIX_REGRESSION` maps to `REGRESSION_PASSED`, `REGRESSION_FAILED`, `REGRESSION_UNSTABLE`, or `BLOCKED`;
- `FIX_VERIFICATION.status: VERIFIED` → `VERIFIED`.

Only a human can move plan artifacts from `READY_FOR_APPROVAL` to `APPROVED`. `IMPLEMENTED` requires every planned TASK to have a published commit and a solution-build gate. Only `run-solution-regression` owns the regression result; only `coordinate-fix` owns final verification.

## TASK execution

Task definitions in `TASKS-FIX-NNNN.md` are immutable after approval. Runtime evidence lives in `EXECUTION-FIX-NNNN.md`; effective publication state is derived from that ledger plus remote Git history:

```text
PENDING → IN_PROGRESS → GATES_PASSED → PUBLISHED
                ↘ BLOCKED
GATES_PASSED → PUSH_BLOCKED
```

- `GATES_PASSED` requires the declared unit-test gate and a full solution build.
- `PUBLISHED` is derived from the remote Git history, not written by amending the task commit.
- A blocked task stops the FIX until a human resolves or replans it.

## Regression

Valid `FIX_REGRESSION` results: `PASSED`, `FAILED`, `UNSTABLE`, `BLOCKED`.

## FIX artifact statuses

- `FIX_SPEC`: `DRAFT`, `READY_FOR_APPROVAL`, `APPROVED`, `BLOCKED`.
- `FIX_DESIGN`, `FIX_TASKS`: `DRAFT`, `READY_FOR_APPROVAL`, `APPROVED`, `BLOCKED`.
- `FIX_EXECUTION`: `IN_PROGRESS`, `BLOCKED`. Completion is derived from all TASKS being remotely `PUBLISHED`.
- `FIX_VERIFICATION`: `VERIFIED`, `BLOCKED`.

## Knowledge and analysis artifacts

| Artifact type | Valid status values |
|---|---|
| `SOLUTION_OVERVIEW`, `PROJECT`, `DEEP_DIVE` | `CURRENT`, `STALE`, `BLOCKED` |
| `ADR` | `INFERRED`, `CONFIRMED`, `SUPERSEDED`, `BLOCKED` |
| `RFC` | `DRAFT`, `READY_FOR_REVIEW`, `ACCEPTED`, `REJECTED`, `SUPERSEDED` |
| `INVESTIGATION` | `STATIC_HYPOTHESIS`, `CONFIRMED`, `REFUTED`, `BLOCKED` |
| `IMPACT_ANALYSIS` | `COMPLETE`, `PARTIAL`, `BLOCKED` |

Use somente essas constantes no frontmatter. Texto de apresentação pode traduzi-las, mas não substituí-las.

## Common frontmatter

Every generated artifact except `INDEX.md` starts with:

```yaml
---
schema_version: 1
artifact_type: {registered type}
id: {stable artifact id}
status: {valid lifecycle status}
owner_skill: {single writer}
created_at: {ISO-8601}
updated_at: {ISO-8601}
---
```

FIX artifacts also require `fix_id: FIX-NNNN`. Status changes must respect this contract; do not invent synonyms.
