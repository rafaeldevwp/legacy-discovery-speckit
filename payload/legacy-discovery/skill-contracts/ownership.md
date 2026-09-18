# Artifact ownership contract

Each artifact type has one writer. Other skills may read it or record a requested change in their own output, but must not edit it.

## V2 active ownership

| Artifact/source | Owner |
|---|---|
| `SOLUTION-OVERVIEW`, `PROJECT`, `ADR`, `DEEP-DIVE` | `analyze-legacy-solution` |
| `INVESTIGATION` and the bug-demonstrating test | `investigate-legacy-bug` |
| `IMPACT` | `analyze-change-impact` |
| `SPECKIT_HANDOFF` | `prepare-speckit-context` |
| `INDEX.md` | deterministic `sync_index.py` script |
| Spec Kit `spec.md`, `plan.md`, `tasks.md` and managed `.specify/` artifacts | **Spec Kit**, nunca estas skills |

## V1 compatibility ownership

Artefatos existentes continuam com seus owners históricos para validação e auditoria:

| Artifact/source | Legacy owner |
|---|---|
| `RFC` | `analyze-legacy-solution` |
| `FIX_SPEC`, `FIX_DESIGN`, `FIX_TASKS`, `FIX_VERIFICATION` | `coordinate-fix` |
| `FIX_EXECUTION` | `execute-fix-plan` |
| `FIX_REGRESSION` | `run-solution-regression` |

As skills V1 estão arquivadas fora da pasta ativa na distribuição V2.

## Knowledge deltas

If a non-owner discovers stale or missing structural knowledge, it records a `knowledge_updates` entry in its own artifact:

```yaml
knowledge_updates:
  - target_type: DEEP_DIVE
    target: PROJECT-x / ClassY
    reason: comportamento observado durante investigação
```

The owner applies the delta in a later explicit refresh. Never silently cross-write another owner's artifact.

## Regra de fronteira com Spec Kit

Nenhuma skill desta camada escreve diretamente em `.specify/` ou altera artefatos gerenciados pelo Spec Kit. A integração acontece exclusivamente por leitura/referência de `SPECKIT_HANDOFF`.
