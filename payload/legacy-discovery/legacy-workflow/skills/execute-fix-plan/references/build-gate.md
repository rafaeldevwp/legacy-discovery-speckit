# TASK gates and bounded recovery

The approved DESIGN owns `solution_path` and `build_command`. The approved TASK owns `unit_test_gate` and `unit_test_command/scope`. The executor validates; it does not redesign gates.

## Gate order

1. Apply only the current TASK.
2. If `unit_test_gate: REQUIRED`, run the declared focused command/scope. Missing command or infrastructure is `PLAN_INVALID` or `ENVIRONMENT_BLOCKED`, not `NOT_APPLICABLE`.
3. Run the exact full-solution `build_command`. A project-only build may diagnose but never releases the gate.
4. Ensure no files change after the final solution build and before commit.

`NOT_APPLICABLE` is accepted only when already approved in TASKS. Do not reclassify it during execution.

## Shared recovery budget

Across unit test and solution build, allow at most two focused correction attempts total for the TASK. After each correction, restart applicable gates from unit test through full solution build.

Stop early when the same error repeats without new evidence, the fix leaves TASK/DESIGN scope, errors expand, a dependency/environment is missing, or package/infrastructure changes are required. Use codes from `failure-policy.md`.

## Success and block

- Success: declared unit gate passes or is approved N/A, and full solution build passes.
- Block: record reason code, command, first useful error, attempts, changed files, branch/HEAD, and next human action in EXECUTION. Do not commit or continue.

