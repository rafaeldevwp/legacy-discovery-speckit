#!/usr/bin/env python3
"""STORY_REFINEMENT contract checks, used by validate_artifacts.py."""

from __future__ import annotations

import re
from datetime import datetime

from artifact_lib import Artifact


REQUIRED_SECTIONS = (
    "## Story (verbatim)", "## Story Quality Assessment", "## AS-IS Basis", "## Scope",
    "## Ambiguity Register", "## Human Decisions Required", "## Acceptance Criteria",
    "## Regression Guardrails", "## Risks and Dependencies", "## Execution Plan",
    "## Explicitly Not Decided", "## Next Steps",
)
AMB_SOURCES = {"STORY", "KNOWLEDGE", "CODE", "HUMAN"}
AMB_STATUSES = {"RESOLVED_BY_EVIDENCE", "OPEN_HUMAN", "ANSWERED_BY_HUMAN", "ASSUMPTION_ACCEPTED"}
HUMAN_STATUSES = {"OPEN_HUMAN", "ANSWERED_BY_HUMAN", "ASSUMPTION_ACCEPTED"}
EMPTY = {"", "-", "null", "none", "n/a"}
NO_GUARDRAIL_MARKER = "NO_EXISTING_BEHAVIOR_AFFECTED"


def _section(body: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}[ \t]*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return match.group(1) if match else ""


def _rows(text: str, id_pattern: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in re.split(r"(?<!\\)\|", line.strip("|"))]
        if cells and re.fullmatch(id_pattern, cells[0]):
            rows.append(cells)
    return rows


def _ids(text: str, prefix: str) -> list[str]:
    return re.findall(rf"\b{prefix}-\d{{2,}}\b", text)


def _is_empty(value: str | None) -> bool:
    return value is None or value.strip().lower() in EMPTY


def _iso(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def check_refinement(artifact: Artifact, handoffs: dict[str, Artifact]) -> list[str]:
    path, meta, body = artifact.path, artifact.metadata, artifact.body
    errors: list[str] = []
    status = meta.get("status", "")

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(section)}[ \t]*$", body, re.M):
            errors.append(f"{path}: STORY_REFINEMENT missing section {section}")

    if meta.get("source_access") not in {"NONE", "BOUNDED"}:
        errors.append(f"{path}: STORY_REFINEMENT source_access must be NONE or BOUNDED")
    if not re.fullmatch(r"[1-9]\d*", meta.get("revision", "")):
        errors.append(f"{path}: STORY_REFINEMENT revision must be a positive integer")
    if _is_empty(meta.get("decision_owner")):
        errors.append(f"{path}: STORY_REFINEMENT decision_owner must name who answers business decisions")

    handoff_ref = meta.get("handoff", "")
    handoff = None
    if handoff_ref != "NONE":
        if not re.fullmatch(r"HANDOFF-\d{4}", handoff_ref):
            errors.append(f"{path}: STORY_REFINEMENT handoff must be HANDOFF-NNNN or NONE")
        else:
            handoff = handoffs.get(handoff_ref)
            if handoff is None:
                errors.append(f"{path}: STORY_REFINEMENT handoff {handoff_ref} not found in knowledge base")

    # Ambiguity register
    ambiguities = _rows(_section(body, "## Ambiguity Register"), r"AMB-\d{2,}")
    amb_status: dict[str, str] = {}
    open_count = 0
    open_blocking: list[str] = []
    for cells in ambiguities:
        amb_id = cells[0]
        if len(cells) < 7:
            errors.append(f"{path}: {amb_id} must have 7 columns (ID, Question, Why it matters, Source, Status, Blocking, Evidence / Answer)")
            continue
        source, amb_state, blocking, evidence = cells[3], cells[4], cells[5], cells[6]
        if amb_id in amb_status:
            errors.append(f"{path}: duplicate ambiguity {amb_id}")
        amb_status[amb_id] = amb_state
        if source not in AMB_SOURCES:
            errors.append(f"{path}: {amb_id} invalid Source {source}")
        if amb_state not in AMB_STATUSES:
            errors.append(f"{path}: {amb_id} invalid Status {amb_state}")
        if blocking not in {"YES", "NO"}:
            errors.append(f"{path}: {amb_id} Blocking must be YES or NO")
        if amb_state == "RESOLVED_BY_EVIDENCE":
            if source == "HUMAN":
                errors.append(f"{path}: {amb_id} resolved by evidence cannot have Source HUMAN")
            if _is_empty(evidence):
                errors.append(f"{path}: {amb_id} resolved by evidence lacks evidence")
        if amb_state in HUMAN_STATUSES and source != "HUMAN":
            errors.append(f"{path}: {amb_id} with status {amb_state} must have Source HUMAN")
        if amb_state in {"ANSWERED_BY_HUMAN", "ASSUMPTION_ACCEPTED"} and _is_empty(evidence):
            errors.append(f"{path}: {amb_id} lacks the recorded human answer")
        if amb_state == "OPEN_HUMAN":
            open_count += 1
            if blocking == "YES":
                open_blocking.append(amb_id)

    if meta.get("open_questions", "") != str(open_count):
        errors.append(f"{path}: open_questions is {meta.get('open_questions')} but register has {open_count} OPEN_HUMAN")
    if status == "AWAITING_HUMAN" and open_count == 0:
        errors.append(f"{path}: AWAITING_HUMAN requires at least one OPEN_HUMAN ambiguity")
    if status == "BLOCKED" and _is_empty(meta.get("block_reason")):
        errors.append(f"{path}: BLOCKED refinement lacks block_reason")

    if status != "READY_FOR_SPECKIT":
        return errors

    # Readiness gate
    if handoff is None:
        errors.append(f"{path}: READY_FOR_SPECKIT requires an existing handoff")
    elif handoff.metadata.get("status") != "READY_FOR_SPECKIT":
        errors.append(f"{path}: READY_FOR_SPECKIT requires {handoff_ref} to be READY_FOR_SPECKIT (is {handoff.metadata.get('status')})")
    if open_blocking:
        errors.append(f"{path}: READY_FOR_SPECKIT with blocking open questions: {', '.join(open_blocking)}")
    if _is_empty(meta.get("reviewed_by")) or _is_empty(meta.get("reviewed_at")):
        errors.append(f"{path}: READY_FOR_SPECKIT requires human reviewed_by and reviewed_at")
    elif not _iso(meta["reviewed_at"]):
        errors.append(f"{path}: reviewed_at is not ISO-8601")
    if not _is_empty(meta.get("block_reason")):
        errors.append(f"{path}: READY_FOR_SPECKIT must not carry block_reason")

    criteria = _rows(_section(body, "## Acceptance Criteria"), r"AC-\d{2,}")
    ac_ids = {cells[0] for cells in criteria}
    if not criteria:
        errors.append(f"{path}: READY_FOR_SPECKIT requires at least one AC-NN")
    for cells in criteria:
        origin = cells[-1] if len(cells) >= 3 else ""
        human = re.fullmatch(r"HUMAN:(AMB-\d{2,})", origin)
        if human:
            if amb_status.get(human.group(1)) not in {"ANSWERED_BY_HUMAN", "ASSUMPTION_ACCEPTED"}:
                errors.append(f"{path}: {cells[0]} derives from {human.group(1)}, which has no human answer")
        elif origin != "STORY" and not re.fullmatch(r"AS-IS:\S.*", origin):
            errors.append(f"{path}: {cells[0]} has invalid Origin {origin or '(empty)'}")

    guardrail_text = _section(body, "## Regression Guardrails")
    guardrails = _rows(guardrail_text, r"GR-\d{2,}")
    gr_ids = {cells[0] for cells in guardrails}
    if not guardrails and NO_GUARDRAIL_MARKER not in guardrail_text:
        errors.append(f"{path}: READY_FOR_SPECKIT requires GR-NN rows or {NO_GUARDRAIL_MARKER} with justification")
    for cells in guardrails:
        proof = cells[-1] if len(cells) >= 4 else ""
        if not (proof == "CHARACTERIZATION_TEST_REQUIRED" or re.fullmatch(r"(EXISTING_TEST|MANUAL_CHECK):\S.*", proof)):
            errors.append(f"{path}: {cells[0]} has invalid Proof {proof or '(empty)'}")

    slices = _rows(_section(body, "## Execution Plan"), r"SLICE-\d{2,}")
    slice_ids = {cells[0] for cells in slices}
    if not slices:
        errors.append(f"{path}: READY_FOR_SPECKIT requires at least one SLICE-NN")
    covered_ac: set[str] = set()
    covered_gr: set[str] = set()
    for cells in slices:
        if len(cells) < 6:
            errors.append(f"{path}: {cells[0]} must have 6 columns (Slice, Goal, AC, GR, Toolchain, Depends on)")
            continue
        slice_ac, slice_gr, depends = set(_ids(cells[2], "AC")), set(_ids(cells[3], "GR")), set(_ids(cells[5], "SLICE"))
        if not slice_ac:
            errors.append(f"{path}: {cells[0]} covers no AC")
        for unknown in sorted(slice_ac - ac_ids):
            errors.append(f"{path}: {cells[0]} references unknown {unknown}")
        for unknown in sorted(slice_gr - gr_ids):
            errors.append(f"{path}: {cells[0]} references unknown {unknown}")
        for unknown in sorted(depends - slice_ids):
            errors.append(f"{path}: {cells[0]} depends on unknown {unknown}")
        if cells[0] in depends:
            errors.append(f"{path}: {cells[0]} depends on itself")
        covered_ac |= slice_ac
        covered_gr |= slice_gr
    graph = {cells[0]: set(_ids(cells[5], "SLICE")) for cells in slices if len(cells) >= 6}
    visiting: set[str] = set()
    done: set[str] = set()

    def has_cycle(node: str) -> bool:
        if node in visiting:
            return True
        if node in done or node not in graph:
            return False
        visiting.add(node)
        found = any(has_cycle(child) for child in graph[node])
        visiting.discard(node)
        done.add(node)
        return found

    if any(has_cycle(node) for node in sorted(graph)):
        errors.append(f"{path}: Execution Plan has a dependency cycle between slices")
    for missing in sorted(ac_ids - covered_ac):
        errors.append(f"{path}: {missing} is not covered by any SLICE")
    for missing in sorted(gr_ids - covered_gr):
        errors.append(f"{path}: {missing} is not covered by any SLICE")

    return errors
