# Impact artifact

Owned only by `analyze-change-impact`.

Risk: `HIGH` when an external/public contract is affected, or 2+ dependents lack scenario coverage; `MEDIUM` when any dependent exists or the target lacks coverage without a HIGH trigger; otherwise `LOW`.

```markdown
---
schema_version: 1
artifact_type: IMPACT_ANALYSIS
id: IMPACT-{YYYYMMDD}-{slug}
status: COMPLETE | PARTIAL | BLOCKED
owner_skill: analyze-change-impact
created_at: {ISO-8601}
updated_at: {ISO-8601}
target: {exact target}
risk: HIGH | MEDIUM | LOW
investigation: {link or null}
knowledge_updates: []
---

# Análise de impacto: {target}

## Risk rationale
{objective triggers}

## Direct dependents
| Project | Use | Evidence |
|---|---|---|
| {name} | {call/reference} | CONFIRMED_USAGE/PROJECT_REFERENCE_ONLY |

## Indirect/external dependents
| Consumer | Protocol | Boundary |
|---|---|---|
| {name} | {WCF/ASMX/HTTP/etc.} | LOCAL/EXTERNAL |

## Related decisions and tests
- ADRs: {links}
- Existing coverage: {tests/gaps}

## Documentation affected
- {artifact owned by analyze-legacy-solution}

## Unknowns and limits
- {facts}
```

Save as `.github/copilot-knowledge/impact-analyses/IMPACT-{YYYYMMDD}-{slug}.md`. Do not propose or implement the correction.

