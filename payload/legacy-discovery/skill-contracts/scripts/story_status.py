#!/usr/bin/env python3
"""Print, without writing anything, where each story stands and which command comes next."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from artifact_lib import escape_cell, parse_artifact, title_of


def next_for_handoff(status: str) -> str:
    if status == "READY_FOR_SPECKIT":
        return "/legacy.refine"
    return "/legacy.handoff (fechar lacunas do handoff)"


def next_for_refinement(meta: dict[str, str], handoff_status: str | None) -> str:
    status = meta.get("status", "")
    if status == "AWAITING_HUMAN":
        return f"/legacy.answer {meta.get('id', '')}"
    if status == "BLOCKED":
        if meta.get("block_reason") == "HANDOFF_MISSING" or handoff_status is None:
            return "/legacy.handoff"
        return f"resolver {meta.get('block_reason', 'block_reason')} e depois /legacy.refine"
    if status == "READY_FOR_SPECKIT":
        if handoff_status != "READY_FOR_SPECKIT":
            return "/legacy.validate (handoff não está pronto)"
        return "/legacy.branch -> /speckit.specify"
    return "/legacy.validate"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".github/copilot-knowledge")
    parser.add_argument("--id", help="Mostrar somente um HANDOFF-NNNN ou REFINEMENT-NNNN")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = Path(args.root)
    if not root.exists():
        print(f"artifact root not found: {root}", file=sys.stderr)
        return 2

    handoffs: dict[str, dict[str, str]] = {}
    refinements: list[dict[str, str]] = []
    titles: dict[str, str] = {}
    for path in sorted(root.rglob("*.md")):
        if path.name == "INDEX.md":
            continue
        artifact = parse_artifact(path)
        kind = artifact.metadata.get("artifact_type")
        ident = artifact.metadata.get("id", path.stem)
        if kind == "SPECKIT_HANDOFF":
            handoffs[ident] = artifact.metadata
            titles[ident] = title_of(artifact)
        elif kind == "STORY_REFINEMENT":
            refinements.append(artifact.metadata)
            titles[ident] = title_of(artifact)

    refined = {meta.get("handoff", "") for meta in refinements}
    if args.id:
        refinements = [m for m in refinements if args.id in {m.get("id"), m.get("handoff")}]
        handoffs = {k: v for k, v in handoffs.items() if k == args.id or k in {m.get("handoff") for m in refinements}}

    lines = ["# Status das histórias", ""]
    if refinements:
        lines += ["## Refinamentos", "",
                  "| Refinamento | História | Status | Rev. | Handoff | Perguntas abertas | Próximo comando |",
                  "|---|---|---|---|---|---|---|"]
        for meta in sorted(refinements, key=lambda m: m.get("id", "")):
            handoff_ref = meta.get("handoff", "NONE")
            handoff_status = handoffs.get(handoff_ref, {}).get("status") if handoff_ref != "NONE" else None
            handoff_cell = f"{handoff_ref} ({handoff_status or 'não encontrado'})" if handoff_ref != "NONE" else "NONE"
            lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
                escape_cell(meta.get("id", "")), escape_cell(meta.get("story_ref", "") + " — " + titles.get(meta.get("id", ""), "")),
                escape_cell(meta.get("status", "")), escape_cell(meta.get("revision", "")), escape_cell(handoff_cell),
                escape_cell(meta.get("open_questions", "")), escape_cell(next_for_refinement(meta, handoff_status))))
        lines.append("")

    pending = {k: v for k, v in handoffs.items() if k not in refined}
    if pending:
        lines += ["## Handoffs sem refinamento", "",
                  "| Handoff | Pedido | Status | Próximo comando |", "|---|---|---|---|"]
        for ident in sorted(pending):
            meta = pending[ident]
            lines.append("| {} | {} | {} | {} |".format(
                escape_cell(ident), escape_cell(meta.get("request", titles.get(ident, ""))),
                escape_cell(meta.get("status", "")), escape_cell(next_for_handoff(meta.get("status", "")))))
        lines.append("")

    if not refinements and not pending:
        lines += ["Nenhuma história em andamento. Comece com `/legacy.story <história do PM>`.", ""]
    lines.append("> Somente leitura. Rode `/legacy.validate` para checar os contratos.")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
