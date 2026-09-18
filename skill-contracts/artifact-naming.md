# Artifact naming contract

Schema version: `1`.

Use type-first names. Sequential IDs use four digits; dates use `YYYYMMDD`; slugs are lowercase ASCII with hyphens. Never add `final`, `v2`, `new`, timestamps, or review suffixes.

| Artifact | Canonical name |
|---|---|
| Knowledge index | `INDEX.md` |
| Solution overview | `SOLUTION-OVERVIEW.md` |
| Project | `PROJECT-{project-slug}.md` |
| Architecture decision | `ADR-{NNNN}-{slug}.md` |
| Proposal | `RFC-{NNNN}-{slug}.md` |
| Deep dive | `DEEP-DIVE-{project-slug}-{class-slug}.md` |
| Investigation | `INVESTIGATION-{YYYYMMDD}-{slug}.md` |
| Impact analysis | `IMPACT-{YYYYMMDD}-{slug}.md` |
| Fix directory | `FIX-{NNNN}-{slug}/` |
| Fix specification | `SPEC-FIX-{NNNN}.md` |
| Fix design | `DESIGN-FIX-{NNNN}.md` |
| Fix task plan | `TASKS-FIX-{NNNN}.md` |
| Fix execution ledger | `EXECUTION-FIX-{NNNN}.md` |
| Fix regression | `REGRESSION-FIX-{NNNN}.md` |
| Fix verification | `VERIFICATION-FIX-{NNNN}.md` |

All artifacts in one FIX share the directory's `FIX-{NNNN}`. Do not rename legacy artifacts automatically. A migration must update inbound links and rebuild `INDEX.md` atomically.

Allocate sequential IDs with `.github/skill-contracts/scripts/next_id.py`; do not infer the next value from file count. Allocation is serialized by the human workflow: immediately validate after writing. `validate_artifacts.py` rejects duplicate IDs, so concurrent allocations must be reconciled before approval.
