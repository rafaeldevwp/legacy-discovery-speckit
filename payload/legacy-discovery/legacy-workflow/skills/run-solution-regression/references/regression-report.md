# Regression artifact

Owned only by `run-solution-regression`.

```markdown
---
schema_version: 1
artifact_type: FIX_REGRESSION
id: REGRESSION-FIX-{NNNN}
fix_id: FIX-{NNNN}
status: PASSED | FAILED | UNSTABLE | BLOCKED
owner_skill: run-solution-regression
created_at: {ISO-8601}
updated_at: {ISO-8601}
branch: {feature/mmYYYY/slug}
tested_commit: {remote HEAD}
solution_path: {path}
build_command: {command}
regression_command: {command/script}
block_reason: null
---

# FIX-{NNNN} — REGRESSION

## Solution build
- Result: PASSED/FAILED/BLOCKED
- Evidence: {minimal output}

## Test inventory
| Suite/project | Discovered | Executed | Passed | Failed | Skipped/not run |
|---|---:|---:|---:|---:|---:|
| {name} | {n} | {n} | {n} | {n} | {n} |

## Original bug test
- Test: {path::name}
- Result: PASSED/FAILED/NOT_DISCOVERED

## Failures and diagnostic rerun
- {test, category, minimal error, rerun result}

## Omissions and limitations
- {none or explicit blockers}

## Conclusion
{why PASSED/FAILED/UNSTABLE/BLOCKED}
```

Only `PASSED` is eligible for final verification. Do not edit code/tests or hide skipped tests.

