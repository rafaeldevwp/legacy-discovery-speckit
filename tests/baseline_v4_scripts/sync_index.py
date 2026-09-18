#!/usr/bin/env python3
"""Rebuild INDEX.md deterministically from artifact frontmatter."""

from __future__ import annotations

import argparse
from pathlib import Path

from artifact_lib import Artifact, escape_cell, parse_artifact, title_of


GROUPS = [
    ("Visão da solution", {"SOLUTION_OVERVIEW"}),
    ("Projetos", {"PROJECT"}),
    ("Decisões arquiteturais", {"ADR"}),
    ("Propostas", {"RFC"}),
    ("Aprofundamentos", {"DEEP_DIVE"}),
    ("Investigações", {"INVESTIGATION"}),
    ("Análises de impacto", {"IMPACT_ANALYSIS"}),
    ("Handoffs para Spec Kit", {"SPECKIT_HANDOFF"}),
    ("Histórico V1 — planos e execução de correções", {"FIX_SPEC", "FIX_DESIGN", "FIX_TASKS", "FIX_EXECUTION", "FIX_REGRESSION", "FIX_VERIFICATION"}),
]


def row(root: Path, artifact: Artifact) -> str:
    relative = artifact.path.relative_to(root).as_posix()
    meta = artifact.metadata
    return "| {id} | {title} | {status} | {updated} | [{path}](./{path}) |".format(
        id=escape_cell(meta.get("id", artifact.path.stem)),
        title=escape_cell(title_of(artifact)),
        status=escape_cell(meta.get("status", "UNKNOWN")),
        updated=escape_cell(meta.get("updated_at", "UNKNOWN")),
        path=relative,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".github/copilot-knowledge")
    args = parser.parse_args()
    root = Path(args.root)
    root.mkdir(parents=True, exist_ok=True)

    artifacts = []
    for path in root.rglob("*.md"):
        if path.name == "INDEX.md":
            continue
        artifact = parse_artifact(path)
        if artifact.metadata.get("artifact_type"):
            artifacts.append(artifact)

    artifacts.sort(key=lambda item: (item.metadata.get("artifact_type", ""), item.metadata.get("id", ""), item.path.as_posix()))
    latest = max((item.metadata.get("updated_at", "") for item in artifacts), default="UNKNOWN")
    solution = next((item for item in artifacts if item.metadata.get("artifact_type") == "SOLUTION_OVERVIEW"), None)
    name = solution.metadata.get("solution_name", "Repositório") if solution else "Repositório"

    lines = [
        f"# Índice de conhecimento — {name}",
        "",
        "> Gerado por `.github/skill-contracts/scripts/sync_index.py`. Não editar manualmente.",
        "",
        f"**Última atualização dos artefatos:** {latest}",
    ]
    grouped_types: set[str] = set()
    for heading, types in GROUPS:
        grouped_types.update(types)
        selected = [item for item in artifacts if item.metadata.get("artifact_type") in types]
        if not selected:
            continue
        lines.extend(["", f"## {heading}", "", "| ID | Título | Status | Atualizado em | Arquivo |", "|---|---|---|---|---|"])
        lines.extend(row(root, item) for item in selected)

    unknown = [item for item in artifacts if item.metadata.get("artifact_type") not in grouped_types]
    if unknown:
        lines.extend(["", "## Tipos não registrados", "", "| ID | Título | Status | Atualizado em | Arquivo |", "|---|---|---|---|---|"])
        lines.extend(row(root, item) for item in unknown)

    (root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"indexed {len(artifacts)} artifact(s): {root / 'INDEX.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
