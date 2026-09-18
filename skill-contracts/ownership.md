# Artifact ownership contract

Each artifact type has one writer. Other skills may read it or record a requested change in their own output, but must not edit it.

| Artifact/source | Owner |
|---|---|
| `SOLUTION-OVERVIEW`, `PROJECT`, `ADR`, `RFC`, `DEEP-DIVE` | `analyze-legacy-solution` |
| `INVESTIGATION` and the bug-demonstrating test | `investigate-legacy-bug` |
| `IMPACT` | `analyze-change-impact` |
| `FIX_SPEC`, `FIX_DESIGN`, `FIX_TASKS`, `FIX_VERIFICATION` | `coordinate-fix` |
| Production/test implementation commits and `FIX_EXECUTION` | `execute-fix-plan` |
| `FIX_REGRESSION` | `run-solution-regression` |
| `INDEX.md` | deterministic `sync_index.py` script |

## Knowledge deltas

If a non-owner discovers stale or missing structural knowledge, it records a `knowledge_updates` entry in its own artifact:

```yaml
knowledge_updates:
  - target_type: DEEP_DIVE
    target: PROJECT-x / ClassY
    reason: behavior changed by FIX-0001
```

The owner applies the delta in a later explicit refresh. Never silently cross-write another owner's artifact.
