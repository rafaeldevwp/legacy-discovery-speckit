#!/usr/bin/env python3
"""Validate canonical names, ownership, lifecycle metadata, and FIX contracts."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

from artifact_lib import parse_artifact
from refinement_rules import check_evidence, check_refinement, repo_root_for


COMMON = {"schema_version", "artifact_type", "id", "status", "owner_skill", "created_at", "updated_at"}
OWNERS = {
    "SOLUTION_OVERVIEW": "analyze-legacy-solution", "PROJECT": "analyze-legacy-solution",
    "ADR": "analyze-legacy-solution", "RFC": "analyze-legacy-solution", "DEEP_DIVE": "analyze-legacy-solution",
    "INVESTIGATION": "investigate-legacy-bug", "IMPACT_ANALYSIS": "analyze-change-impact",
    "SPECKIT_HANDOFF": "prepare-speckit-context", "STORY_REFINEMENT": "refine-user-story",
    "FIX_SPEC": "coordinate-fix", "FIX_DESIGN": "coordinate-fix", "FIX_TASKS": "coordinate-fix",
    "FIX_EXECUTION": "execute-fix-plan", "FIX_REGRESSION": "run-solution-regression", "FIX_VERIFICATION": "coordinate-fix",
}
STATUSES = {
    "SOLUTION_OVERVIEW": {"CURRENT", "STALE", "BLOCKED"}, "PROJECT": {"CURRENT", "STALE", "BLOCKED"},
    "DEEP_DIVE": {"CURRENT", "STALE", "BLOCKED"}, "ADR": {"INFERRED", "CONFIRMED", "SUPERSEDED", "BLOCKED"},
    "RFC": {"DRAFT", "READY_FOR_REVIEW", "ACCEPTED", "REJECTED", "SUPERSEDED"},
    "INVESTIGATION": {"STATIC_HYPOTHESIS", "CONFIRMED", "REFUTED", "BLOCKED"},
    "IMPACT_ANALYSIS": {"COMPLETE", "PARTIAL", "BLOCKED"},
    "SPECKIT_HANDOFF": {"READY_FOR_SPECKIT", "PARTIAL", "BLOCKED"},
    "STORY_REFINEMENT": {"READY_FOR_SPECKIT", "READY_FOR_REVIEW", "AWAITING_HUMAN", "BLOCKED"},
    "FIX_REGRESSION": {"PASSED", "FAILED", "UNSTABLE", "BLOCKED"},
    "FIX_SPEC": {"DRAFT", "READY_FOR_APPROVAL", "APPROVED", "BLOCKED"},
    "FIX_DESIGN": {"DRAFT", "READY_FOR_APPROVAL", "APPROVED", "BLOCKED"},
    "FIX_TASKS": {"DRAFT", "READY_FOR_APPROVAL", "APPROVED", "BLOCKED"},
    "FIX_EXECUTION": {"IN_PROGRESS", "BLOCKED"},
    "FIX_VERIFICATION": {"VERIFIED", "BLOCKED"},
}
NAME_PATTERNS = {
    "SOLUTION_OVERVIEW": r"SOLUTION-OVERVIEW\.md", "PROJECT": r"PROJECT-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "ADR": r"ADR-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md", "RFC": r"RFC-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "DEEP_DIVE": r"DEEP-DIVE-[a-z0-9]+(?:-[a-z0-9]+)+\.md", "INVESTIGATION": r"INVESTIGATION-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "IMPACT_ANALYSIS": r"IMPACT-\d{8}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "SPECKIT_HANDOFF": r"HANDOFF-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "STORY_REFINEMENT": r"REFINEMENT-\d{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md",
    "FIX_SPEC": r"SPEC-FIX-\d{4}\.md", "FIX_DESIGN": r"DESIGN-FIX-\d{4}\.md", "FIX_TASKS": r"TASKS-FIX-\d{4}\.md",
    "FIX_EXECUTION": r"EXECUTION-FIX-\d{4}\.md", "FIX_REGRESSION": r"REGRESSION-FIX-\d{4}\.md", "FIX_VERIFICATION": r"VERIFICATION-FIX-\d{4}\.md",
}
FIX_TYPES = {"FIX_SPEC", "FIX_DESIGN", "FIX_TASKS", "FIX_EXECUTION", "FIX_REGRESSION", "FIX_VERIFICATION"}
FIX_PREFIX = {"FIX_SPEC": "SPEC", "FIX_DESIGN": "DESIGN", "FIX_TASKS": "TASKS", "FIX_EXECUTION": "EXECUTION", "FIX_REGRESSION": "REGRESSION", "FIX_VERIFICATION": "VERIFICATION"}
DIRECTORIES = {
    "SOLUTION_OVERVIEW": ".", "PROJECT": "projects", "ADR": "decisions", "RFC": "proposals",
    "DEEP_DIVE": "deep-dives", "INVESTIGATION": "investigations", "IMPACT_ANALYSIS": "impact-analyses",
    "SPECKIT_HANDOFF": "handoffs", "STORY_REFINEMENT": "refinements",
}
REQUIRED_BY_KIND = {
    "SOLUTION_OVERVIEW": {"solution_name", "solution_path"},
    "PROJECT": {"project_name", "depth", "source_modified_at"},
    "INVESTIGATION": {"symptom", "confidence", "confirmed_test"},
    "IMPACT_ANALYSIS": {"target", "risk", "investigation"},
    "SPECKIT_HANDOFF": {"request", "target_flow", "confidence", "source_access"},
    "STORY_REFINEMENT": {"story_ref", "handoff", "revision", "decision_owner", "open_questions", "source_access", "reviewed_by", "reviewed_at", "block_reason"},
    "FIX_DESIGN": {"solution_path", "build_configuration", "build_command", "regression_command", "regression_scope"},
    "FIX_EXECUTION": {"branch", "remote_url", "base_commit", "base_build", "solution_path", "spec_digest", "design_digest", "tasks_digest", "block_reason"},
    "FIX_REGRESSION": {"branch", "tested_commit", "solution_path", "build_command", "regression_command", "block_reason"},
    "FIX_VERIFICATION": {"spec", "design", "tasks", "execution", "regression", "verified_commit"},
}


def expected_id(kind: str, path: Path) -> str:
    stem = path.stem
    if kind in {"ADR", "RFC"}:
        return "-".join(stem.split("-")[:2])
    if kind in {"SPECKIT_HANDOFF", "STORY_REFINEMENT"}:
        return "-".join(stem.split("-")[:2])
    return stem


def valid_iso8601(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".github/copilot-knowledge")
    args = parser.parse_args()
    root = Path(args.root)
    errors: list[str] = []
    artifacts = []
    ids: dict[str, Path] = {}

    if not root.exists():
        print(f"artifact root not found: {root}", file=sys.stderr)
        return 2

    for path in sorted(root.rglob("*.md")):
        if path.name == "INDEX.md":
            continue
        artifact = parse_artifact(path)
        artifacts.append(artifact)
        meta = artifact.metadata
        missing = sorted(COMMON - set(meta))
        if missing:
            errors.append(f"{path}: missing frontmatter keys: {', '.join(missing)}")
            continue
        kind = meta["artifact_type"]
        if meta["schema_version"] != "1":
            errors.append(f"{path}: unsupported schema_version {meta['schema_version']}")
        if kind not in OWNERS:
            errors.append(f"{path}: unregistered artifact_type {kind}")
            continue
        if meta["owner_skill"] != OWNERS[kind]:
            errors.append(f"{path}: owner {meta['owner_skill']} must be {OWNERS[kind]}")
        if meta["status"] not in STATUSES[kind]:
            errors.append(f"{path}: invalid {kind} status {meta['status']}")
        if not re.fullmatch(NAME_PATTERNS[kind], path.name):
            errors.append(f"{path}: non-canonical filename for {kind}")
        if meta["id"] != expected_id(kind, path):
            errors.append(f"{path}: id {meta['id']} does not match filename")
        if meta["id"] in ids:
            errors.append(f"{path}: duplicate id {meta['id']} also used by {ids[meta['id']]}")
        else:
            ids[meta["id"]] = path
        for key in ("created_at", "updated_at"):
            if not valid_iso8601(meta[key]):
                errors.append(f"{path}: {key} is not ISO-8601")
        for key in sorted(REQUIRED_BY_KIND.get(kind, set())):
            if key not in meta or meta[key] == "":
                errors.append(f"{path}: {kind} missing {key}")

        if kind in DIRECTORIES:
            relative_parent = path.parent.relative_to(root).as_posix() or "."
            if relative_parent != DIRECTORIES[kind]:
                errors.append(f"{path}: {kind} must be stored under {DIRECTORIES[kind]}")

        if kind in FIX_TYPES:
            fix_id = meta.get("fix_id", "")
            directory_match = re.fullmatch(r"FIX-(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*", path.parent.name)
            if not directory_match:
                errors.append(f"{path}: FIX artifact must be inside FIX-NNNN-slug")
            else:
                expected = f"FIX-{directory_match.group(1)}"
                if fix_id != expected or expected not in path.name or meta["id"] != f"{FIX_PREFIX[kind]}-{expected}":
                    errors.append(f"{path}: directory, filename, id and fix_id disagree")

        if kind == "FIX_TASKS":
            if not re.search(r"\bREQ-[A-Za-z0-9-]+\b", artifact.body) or not re.search(r"\bDESIGN-[A-Za-z0-9-]+\b", artifact.body):
                errors.append(f"{path}: TASKS lacks REQ/DESIGN traceability")
            if "Unit test gate:" not in artifact.body:
                errors.append(f"{path}: TASKS lacks explicit unit-test gate")
        if kind in {"FIX_SPEC", "FIX_DESIGN", "FIX_TASKS"} and meta["status"] not in {"DRAFT", "READY_FOR_APPROVAL", "BLOCKED"}:
            if not meta.get("approver") or meta.get("approver") == "null" or not meta.get("approved_at") or meta.get("approved_at") == "null":
                errors.append(f"{path}: approved plan artifact lacks approver/approved_at")
        if kind == "PROJECT" and meta.get("depth") not in {"STRUCTURAL", "COMPLETE"}:
            errors.append(f"{path}: PROJECT depth must be STRUCTURAL or COMPLETE")
        if kind == "INVESTIGATION" and meta["status"] == "CONFIRMED" and meta.get("confirmed_test") in {None, "", "null"}:
            errors.append(f"{path}: confirmed investigation lacks confirmed_test")
        if kind == "SPECKIT_HANDOFF":
            if meta.get("target_flow") not in {"SDD", "BUG"}:
                errors.append(f"{path}: SPECKIT_HANDOFF target_flow must be SDD or BUG")
            if meta.get("confidence") not in {"HIGH", "MEDIUM", "LOW"}:
                errors.append(f"{path}: SPECKIT_HANDOFF confidence must be HIGH, MEDIUM or LOW")
            if meta.get("source_access") not in {"NONE", "BOUNDED"}:
                errors.append(f"{path}: SPECKIT_HANDOFF source_access must be NONE or BOUNDED")
            required_sections = [
                "## Request", "## Knowledge Coverage", "## Current Behavior",
                "## Compatibility Constraints", "## Impact Surface",
                "## External Boundaries", "## Evidence", "## Unknowns",
                "## Explicitly Not Decided", "## Spec Kit Handoff",
            ]
            for section in required_sections:
                if section not in artifact.body:
                    errors.append(f"{path}: SPECKIT_HANDOFF missing section {section}")
            if meta["status"] == "READY_FOR_SPECKIT":
                blocking_match = re.search(r"### Blocking\s*(.*?)(?:\n### |\Z)", artifact.body, re.S)
                if not blocking_match or not re.search(r"\bNONE\b", blocking_match.group(1)):
                    errors.append(f"{path}: READY_FOR_SPECKIT must declare Blocking unknowns as NONE")

        for target in re.findall(r"\]\(([^)]+\.md(?:#[^)]+)?)\)", artifact.body):
            target = target.split("#", 1)[0]
            if "://" in target or target.startswith("/"):
                continue
            if not (path.parent / target).resolve().exists():
                errors.append(f"{path}: broken local Markdown link {target}")

    handoffs = {a.metadata.get("id", ""): a for a in artifacts if a.metadata.get("artifact_type") == "SPECKIT_HANDOFF"}
    known_ids = {a.metadata.get("id", "") for a in artifacts if a.metadata.get("id")}
    repo_root = repo_root_for(root)
    warnings: list[str] = []
    for refinement in artifacts:
        if refinement.metadata.get("artifact_type") == "STORY_REFINEMENT" and COMMON <= set(refinement.metadata):
            errors.extend(check_refinement(refinement, handoffs, known_ids, repo_root, warnings))
    if repo_root is not None:
        for handoff in handoffs.values():
            warnings.extend(check_evidence(handoff.path, handoff.body, repo_root, None))
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)

    for fix_dir in sorted(root.glob("fix-plans/FIX-[0-9][0-9][0-9][0-9]-*")):
        number = fix_dir.name[4:8]
        for prefix in ("SPEC", "DESIGN", "TASKS"):
            if not (fix_dir / f"{prefix}-FIX-{number}.md").exists():
                errors.append(f"{fix_dir}: missing required {prefix}-FIX-{number}.md")

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"validation passed: {len(artifacts)} artifact(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
