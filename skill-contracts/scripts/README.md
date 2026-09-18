# Contract scripts

Stdlib-only utilities. Run from the repository root:

```text
python .github/skill-contracts/scripts/next_id.py --root .github/copilot-knowledge --type FIX
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
```

- `next_id.py` reads existing names and prints the next four-digit ID without writing.
- `validate_artifacts.py` fails closed on invalid names, metadata, owners, lifecycle states, FIX identity, DESIGN gates, or TASK traceability.
- `sync_index.py` is the only writer of `INDEX.md`; identical inputs produce identical output.

The required order after artifact changes is: validate artifacts, rebuild the index, validate again. Never hand-edit the generated index.
