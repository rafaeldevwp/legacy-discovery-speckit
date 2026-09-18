# Investigation artifact

Owned only by `investigate-legacy-bug`. Never include a production correction. Structural documentation changes are `knowledge_updates`, not direct writes.

```markdown
---
schema_version: 1
artifact_type: INVESTIGATION
id: INVESTIGATION-{YYYYMMDD}-{slug}
status: STATIC_HYPOTHESIS | CONFIRMED | REFUTED | BLOCKED
owner_skill: investigate-legacy-bug
created_at: {ISO-8601}
updated_at: {ISO-8601}
symptom: {short summary}
confidence: HIGH | MEDIUM | LOW
confirmed_test: null
knowledge_updates: []
---

# Investigação: {sintoma}

## Contexto
- Esperado: {value}
- Observado: {value}
- Exemplo concreto: {synthetic/sanitized case or not informed}

## Hypotheses
### 1. {candidate}
- Confidence: HIGH/MEDIUM/LOW
- Location: {project/class/method/approximate line}
- Evidence: {traceable code path}
- How to confirm: {focused action}

## Discarded
- {candidate and reason}

## Service boundaries
{local/external consumers and limits}

## Execution evidence
- Test: {path::name or NOT_EXECUTED}
- Command/environment: {sanitized}
- Result: FAILED_AS_EXPECTED | PASSED_UNEXPECTEDLY | INCONCLUSIVE | NOT_EXECUTED
- Minimal output: {assert/error only}
- Conclusion: {CONFIRMS/REFUTES/INCONCLUSIVE}

## Knowledge updates requested
- {target owner/type and reason}

## Limitations and next step
- {facts}
```

Save as `.github/copilot-knowledge/investigations/INVESTIGATION-{YYYYMMDD}-{slug}.md`. `CONFIRMED` requires a concrete reproducing test failure matching the symptom; environment/build failures are `BLOCKED` or `INCONCLUSIVE`.

