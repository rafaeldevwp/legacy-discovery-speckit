#!/usr/bin/env python3
"""Archive and optionally clean skill-generated local artifacts.

This utility intentionally touches only skill artifacts:
- .github/copilot-knowledge/
- .github/legacy-discovery/installation.json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_PATHS = (
    Path(".github") / "copilot-knowledge",
    Path(".github") / "legacy-discovery" / "installation.json",
)


def collect_existing(root: Path) -> list[Path]:
    items: list[Path] = []
    for relative in SKILL_PATHS:
        target = root / relative
        if target.exists():
            items.append(target)
    return items


def default_archive_dir(root: Path) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", str(root)))
    return base / "legacy-discovery-speckit" / "archives" / root.name


def create_archive(root: Path, archive_dir: Path, items: list[Path]) -> tuple[Path, dict]:
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    bundle_name = f"skill-artifacts-{root.name}-{stamp}"
    staging = archive_dir / bundle_name
    staging.mkdir(parents=True, exist_ok=True)

    archived: list[str] = []
    for item in items:
        relative = item.relative_to(root)
        destination = staging / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if item.is_dir():
            shutil.copytree(item, destination)
        else:
            shutil.copy2(item, destination)
        archived.append(relative.as_posix())

    manifest = {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(root),
        "artifact_count": len(archived),
        "artifacts": archived,
    }
    (staging / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    zip_path = Path(shutil.make_archive(str(staging), "zip", root_dir=str(staging)))
    shutil.rmtree(staging)
    return zip_path, manifest


def clean_items(items: list[Path]) -> None:
    for item in items:
        if item.is_dir():
            shutil.rmtree(item)
        elif item.exists():
            item.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Archive local skill artifacts and optionally remove them from the repository working tree."
    )
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--mode",
        choices=("list", "archive", "archive-and-clean"),
        default="archive",
        help="Operation mode",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory where the archive zip will be written",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / ".git").exists():
        print(f"ERROR: {root} is not a Git repository root (.git not found)", file=sys.stderr)
        return 2

    items = collect_existing(root)
    if not items:
        print("NO_SKILL_ARTIFACTS_FOUND")
        return 0

    print("SKILL_ARTIFACTS")
    for item in items:
        print(f"- {item.relative_to(root).as_posix()}")

    if args.mode == "list":
        return 0

    archive_dir = Path(args.output_dir).resolve() if args.output_dir else default_archive_dir(root)
    zip_path, manifest = create_archive(root, archive_dir, items)

    if args.mode == "archive-and-clean":
        clean_items(items)
        action = "ARCHIVED_AND_CLEANED"
    else:
        action = "ARCHIVED"

    print(action)
    print(f"ARCHIVE_ZIP={zip_path}")
    print(f"ARTIFACT_COUNT={manifest['artifact_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
