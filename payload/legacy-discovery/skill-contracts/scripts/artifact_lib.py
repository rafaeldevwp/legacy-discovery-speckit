#!/usr/bin/env python3
"""Small stdlib-only helpers shared by artifact contract scripts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Artifact:
    path: Path
    metadata: dict[str, str]
    body: str


def parse_artifact(path: Path) -> Artifact:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    metadata: dict[str, str] = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body_start = index + 1
                break
            if not line or line[0].isspace() or ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"\'')
    return Artifact(path, metadata, "\n".join(lines[body_start:]))


def title_of(artifact: Artifact) -> str:
    if artifact.metadata.get("title"):
        return artifact.metadata["title"]
    for line in artifact.body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return artifact.metadata.get("id", artifact.path.stem)


def escape_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value).replace("|", "\\|").strip()
