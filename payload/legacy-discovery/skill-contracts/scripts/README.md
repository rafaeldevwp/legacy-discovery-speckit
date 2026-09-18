# Contract scripts

Stdlib-only utilities. Run from the repository root:

```text
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type HANDOFF
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type ADR
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
```

Legacy ID types `FIX` and `RFC` remain supported for repositories with V1 history.

- `next_id.py` reads existing names and prints the next four-digit ID without writing.
- `validate_artifacts.py` validates names, metadata, owners and lifecycle; it also validates the V2 `SPECKIT_HANDOFF` contract and keeps compatibility checks for V1 FIX artifacts.
- `sync_index.py` is the only writer of `INDEX.md`; identical inputs produce identical output and now indexes handoffs separately.

The required order after artifact changes is: validate artifacts, rebuild the index, validate again. Never hand-edit the generated index.
