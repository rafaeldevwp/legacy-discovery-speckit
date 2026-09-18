#!/usr/bin/env python3
"""Print the next deterministic four-digit ID for active and legacy sequential artifacts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PATTERNS = {
    "HANDOFF": re.compile(r"(?:^|/)HANDOFF-(\d{4})(?:-|\.|$)"),
    "FIX": re.compile(r"(?:^|/)FIX-(\d{4})(?:-|/|$)"),
    "ADR": re.compile(r"(?:^|/)ADR-(\d{4})(?:-|\.|$)"),
    "RFC": re.compile(r"(?:^|/)RFC-(\d{4})(?:-|\.|$)"),
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".github/copilot-knowledge")
    parser.add_argument("--type", required=True, choices=sorted(PATTERNS))
    args = parser.parse_args()

    root = Path(args.root)
    found: set[int] = set()
    if root.exists():
        for path in root.rglob("*"):
            relative = path.relative_to(root).as_posix()
            for match in PATTERNS[args.type].finditer(relative):
                found.add(int(match.group(1)))

    next_value = max(found, default=0) + 1
    if next_value > 9999:
        raise SystemExit(f"{args.type} ID space exhausted")
    print(f"{next_value:04d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
