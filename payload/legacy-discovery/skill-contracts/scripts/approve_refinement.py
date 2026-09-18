#!/usr/bin/env python3
"""Human-only approval of a STORY_REFINEMENT.

Run it yourself, in your own terminal. The legacy-discovery governance hook denies this script to the agent,
so an approval recorded here is a human act. It moves READY_FOR_REVIEW -> READY_FOR_SPECKIT, records the
reviewer, and seals the content with approval_digest: any later edit invalidates the approval.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from artifact_lib import parse_artifact
from refinement_rules import approval_digest, check_refinement, repo_root_for


def set_field(text: str, key: str, value: str) -> str:
    lines = text.split("\n")
    end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    for index in range(1, end):
        if re.match(rf"{re.escape(key)}\s*:", lines[index]):
            lines[index] = f"{key}: {value}"
            return "\n".join(lines)
    lines.insert(end, f"{key}: {value}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Aprovação humana de um STORY_REFINEMENT (somente humano).")
    parser.add_argument("--root", default=".github/copilot-knowledge")
    parser.add_argument("--id", required=True, help="REFINEMENT-NNNN")
    parser.add_argument("--reviewer", required=True, help="Seu nome, como revisor")
    parser.add_argument("--confirm", help="Repita o ID para confirmar sem pergunta interativa")
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    root = Path(args.root)
    if not root.exists():
        print(f"artifact root not found: {root}", file=sys.stderr)
        return 2
    reviewer = args.reviewer.strip()
    if not reviewer or reviewer.lower() in {"null", "none", "-", "agent", "copilot", "claude"}:
        print("NOT_APPROVED: informe o nome de uma pessoa como revisor.", file=sys.stderr)
        return 1

    artifacts = [parse_artifact(p) for p in sorted(root.rglob("*.md")) if p.name != "INDEX.md"]
    target = next((a for a in artifacts if a.metadata.get("artifact_type") == "STORY_REFINEMENT"
                   and a.metadata.get("id") == args.id), None)
    if target is None:
        print(f"NOT_APPROVED: {args.id} não encontrado em {root}", file=sys.stderr)
        return 1
    if target.metadata.get("status") != "READY_FOR_REVIEW":
        print(f"NOT_APPROVED: {args.id} está {target.metadata.get('status')}; só READY_FOR_REVIEW pode ser aprovado.",
              file=sys.stderr)
        return 1

    confirmation = args.confirm
    if confirmation is None:
        if not sys.stdin.isatty():
            print("NOT_APPROVED: rode em um terminal interativo ou use --confirm <ID>.", file=sys.stderr)
            return 1
        try:
            confirmation = input(f"Aprovar {args.id} como '{reviewer}'? Digite o ID para confirmar: ").strip()
        except EOFError:
            print("\nNOT_APPROVED: confirmação não recebida.", file=sys.stderr)
            return 1
    if confirmation != args.id:
        print("NOT_APPROVED: confirmação não confere.", file=sys.stderr)
        return 1

    original = target.path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    revision = int(target.metadata.get("revision", "0") or 0) + 1
    updated = original
    for key, value in (("status", "READY_FOR_SPECKIT"), ("reviewed_by", f'"{reviewer}"'), ("reviewed_at", now),
                       ("updated_at", now), ("revision", str(revision)), ("block_reason", "null")):
        updated = set_field(updated, key, value)
    updated = set_field(updated, "approval_digest", approval_digest(updated))

    target.path.write_text(updated, encoding="utf-8", newline="\n")
    handoffs = {a.metadata.get("id", ""): a for a in artifacts if a.metadata.get("artifact_type") == "SPECKIT_HANDOFF"}
    known_ids = {a.metadata.get("id", "") for a in artifacts if a.metadata.get("id")}
    errors = check_refinement(parse_artifact(target.path), handoffs, known_ids, repo_root_for(root))
    if errors:
        target.path.write_text(original, encoding="utf-8", newline="\n")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"NOT_APPROVED: {len(errors)} erro(s); nada foi alterado.", file=sys.stderr)
        return 1

    print(f"APPROVED: {args.id} revisão {revision} por {reviewer} em {now}")
    print("Selado com approval_digest: qualquer edição posterior invalida a aprovação.")
    print("Próximo: python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge")
    print("         depois /legacy.branch <descrição>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
