# Contract scripts

Stdlib-only utilities. Run from the repository root:

```text
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type HANDOFF
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type ADR
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type REFINEMENT
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/story_status.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/approve_refinement.py --id REFINEMENT-0001 --reviewer "Seu Nome"   # só o humano
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean
```

Legacy ID types `FIX` and `RFC` remain supported for repositories with V1 history.

- `next_id.py` reads existing names and prints the next four-digit ID without writing.
- `validate_artifacts.py` validates names, metadata, owners and lifecycle; it also validates the V2 `SPECKIT_HANDOFF` contract and keeps compatibility checks for V1 FIX artifacts.
- `refinement_rules.py` holds the `STORY_REFINEMENT` checks used by `validate_artifacts.py`: required sections, ambiguity register vocabulary, `open_questions` counter, handoff cross-reference, and — for `READY_FOR_SPECKIT` — human review, no blocking open question, AC origin, guardrail proof and AC/GR/SLICE traceability.
- `sync_index.py` is the only writer of `INDEX.md`; identical inputs produce identical output and now indexes handoffs separately.
- `approve_refinement.py` is **human-only** (the agent hook denies it): moves `READY_FOR_REVIEW` → `READY_FOR_SPECKIT`, records reviewer/date and seals the content with `approval_digest`. It re-validates and changes nothing on failure.
- When the knowledge base sits at `<repo>/.github/copilot-knowledge`, `validate_artifacts.py` also checks evidence: cited `file:line`, `EXISTING_TEST` files/tests and artifact IDs must exist (errors for refinements, `WARNING` for handoffs).
- `story_status.py` is read-only: it lists handoffs and refinements with status, open questions and the next `/legacy.*` command. Used by `/legacy.status`, `/legacy.help`, `/legacy.story` and `/legacy.branch`.
- `archive_skill_artifacts.py` archives only skill-generated artifacts (`.github/copilot-knowledge/` and `.github/legacy-discovery/installation.json`) to a zip outside the repository by default, and can optionally clean them from the working tree.

The required order after artifact changes is: validate artifacts, rebuild the index, validate again. Never hand-edit the generated index.
