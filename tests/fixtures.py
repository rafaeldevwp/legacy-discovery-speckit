"""Knowledge-base fixtures shared by the bundle tests."""

from __future__ import annotations

from pathlib import Path


def front(**fields: str) -> str:
    lines = ["---", "schema_version: 1"]
    lines += [f"{key}: {value}" for key, value in fields.items()]
    return "\n".join(lines + ["---", ""])


TS = "2026-09-18T12:00:00Z"

HANDOFF_BODY = """# Handoff para Spec Kit — Timeout na consulta

## Request

Tratar timeout na consulta de veículos.

## Knowledge Coverage

| Dimension | Status | Basis |
|---|---|---|
| STRUCTURE | COVERED | PROJECT-consulta |

## Current Behavior

Consulta síncrona sem retry.

## Compatibility Constraints

- contrato SOAP mantido.

## Impact Surface

- relatório diário.

## External Boundaries

- serviço PBH.

## Evidence

- PROJECT-consulta.

## Unknowns

### Blocking

- NONE

### Non-blocking

- volume em produção.

## Explicitly Not Decided

- arquitetura TO-BE.

## Spec Kit Handoff

### Target flow

`SDD`
"""


def handoff(status: str = "READY_FOR_SPECKIT", ident: str = "HANDOFF-0001") -> str:
    return front(
        artifact_type="SPECKIT_HANDOFF", id=ident, status=status, owner_skill="prepare-speckit-context",
        created_at=TS, updated_at=TS, request='"tratar timeout"', target_flow="SDD", confidence="HIGH",
        source_access="NONE",
    ) + HANDOFF_BODY


REFINEMENT_BODY = """# Refinamento — Timeout na consulta de veículos

## Story (verbatim)

> Como atendente, quero que a consulta de veículos não perca o último estado quando der timeout.

## Story Quality Assessment

| Critério | Resultado | Observação |
|---|---|---|
| Testable | OK | - |

## AS-IS Basis

- `FACT` — consulta síncrona — HANDOFF-0001

## Scope

### In scope
- timeout da consulta.

### Out of scope
- retry automático.

## Ambiguity Register

| ID | Question | Why it matters | Source | Status | Blocking | Evidence / Answer |
|---|---|---|---|---|---|---|
| AMB-01 | Hoje há retry? | define AC | KNOWLEDGE | RESOLVED_BY_EVIDENCE | NO | HANDOFF-0001 § Current Behavior |
| AMB-02 | Quanto tempo o último estado vale? | regra de negócio | HUMAN | {amb2_status} | YES | {amb2_answer} |

## Human Decisions Required

{human}

## Acceptance Criteria

| ID | Given / When / Then | Origin |
|---|---|---|
| AC-01 | Dado timeout, quando consultar, então exibe o último estado | STORY |
| AC-02 | Dado estado com mais de 24h, quando exibir, então sinaliza desatualizado | HUMAN:AMB-02 |

## Regression Guardrails

| ID | Preserved behavior | Evidence | Proof |
|---|---|---|---|
| GR-01 | contrato SOAP inalterado | HANDOFF-0001 § Compatibility Constraints | CHARACTERIZATION_TEST_REQUIRED |

## Risks and Dependencies

- serviço PBH instável — HANDOFF-0001.

## Execution Plan

| Slice | Goal | AC | GR | Toolchain | Depends on |
|---|---|---|---|---|---|
| SLICE-01 | Rede de proteção + caminho feliz | AC-01 | GR-01 | /speckit.specify → /speckit.implement | - |
| SLICE-02 | Sinalizar estado antigo | AC-02 | GR-01 | /speckit.specify → /speckit.implement | SLICE-01 |

### Non-binding technical considerations

- nenhuma.

## Explicitly Not Decided

- arquitetura TO-BE.

## Next Steps

1. prepare-feature-branch.
"""


def refinement(
    status: str = "READY_FOR_SPECKIT",
    handoff_ref: str = "HANDOFF-0001",
    amb2_status: str = "ANSWERED_BY_HUMAN",
    amb2_answer: str = '"24 horas" — PM, 2026-09-18',
    open_questions: str | None = None,
    reviewed_by: str = '"Ana PO"',
    reviewed_at: str = TS,
    block_reason: str = "null",
    body_replace: tuple[tuple[str, str], ...] = (),
    ident: str = "REFINEMENT-0001",
) -> str:
    if open_questions is None:
        open_questions = "1" if amb2_status == "OPEN_HUMAN" else "0"
    human = "### AMB-02 — validade do último estado (BLOQUEANTE)" if amb2_status == "OPEN_HUMAN" else "NONE"
    body = REFINEMENT_BODY.format(amb2_status=amb2_status, amb2_answer=amb2_answer, human=human)
    for old, new in body_replace:
        assert old in body, old
        body = body.replace(old, new)
    return front(
        artifact_type="STORY_REFINEMENT", id=ident, status=status, owner_skill="refine-user-story",
        created_at=TS, updated_at=TS, story_ref='"US-1234"', handoff=handoff_ref, revision="1",
        decision_owner='"PM"', open_questions=open_questions, source_access="NONE",
        reviewed_by=reviewed_by, reviewed_at=reviewed_at, block_reason=block_reason,
    ) + body


def write(root: Path, relative: str, text: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def legacy_v2_knowledge(root: Path) -> None:
    """A realistic V2/V1 knowledge base with no refinements, including invalid artifacts."""
    write(root, "SOLUTION-OVERVIEW.md", front(
        artifact_type="SOLUTION_OVERVIEW", id="SOLUTION-OVERVIEW", status="CURRENT",
        owner_skill="analyze-legacy-solution", created_at=TS, updated_at=TS,
        solution_name="Atlas", solution_path="Atlas.sln") + "# Visão\n")
    write(root, "projects/PROJECT-consulta.md", front(
        artifact_type="PROJECT", id="PROJECT-consulta", status="CURRENT", owner_skill="analyze-legacy-solution",
        created_at=TS, updated_at=TS, project_name="Consulta", depth="STRUCTURAL",
        source_modified_at=TS) + "# Projeto Consulta\n\nVer [handoff](../handoffs/HANDOFF-0001-timeout.md).\n")
    write(root, "handoffs/HANDOFF-0001-timeout.md", handoff())
    write(root, "handoffs/HANDOFF-0002-sem-blocking.md", handoff(ident="HANDOFF-0002").replace("- NONE", "- falta contrato"))
    write(root, "decisions/ADR-0001-soap.md", front(
        artifact_type="ADR", id="ADR-0001", status="INFERRED", owner_skill="analyze-legacy-solution",
        created_at=TS, updated_at="2026-09-19T08:00:00Z") + "# SOAP | legado\n")
    write(root, "investigations/INVESTIGATION-20260901-timeout.md", front(
        artifact_type="INVESTIGATION", id="INVESTIGATION-20260901-timeout", status="CONFIRMED",
        owner_skill="investigate-legacy-bug", created_at=TS, updated_at=TS, symptom="timeout",
        confidence="HIGH", confirmed_test="null") + "# Inv\n")
    write(root, "impact-analyses/IMPACT-20260902-consulta.md", front(
        artifact_type="IMPACT_ANALYSIS", id="IMPACT-20260902-consulta", status="COMPLETE",
        owner_skill="wrong-owner", created_at=TS, updated_at="not-a-date", target="Consulta",
        risk="MEDIUM", investigation="INVESTIGATION-20260901-timeout") + "# Impacto\n[x](missing.md)\n")
    write(root, "fix-plans/FIX-0001-antigo/SPEC-FIX-0001.md", front(
        artifact_type="FIX_SPEC", id="SPEC-FIX-0001", status="APPROVED", owner_skill="coordinate-fix",
        created_at=TS, updated_at=TS, fix_id="FIX-0001") + "# Spec\n")
    write(root, "impact-analyses/IMPACT-20260903-sem-investigacao.md", front(
        artifact_type="IMPACT_ANALYSIS", id="IMPACT-20260903-sem-investigacao", status="PARTIAL",
        owner_skill="analyze-change-impact", created_at=TS, updated_at=TS, target="X", risk="LOW") + "# I\n")
    write(root, "projects/PROJECT-profundo.md", front(
        artifact_type="PROJECT", id="PROJECT-profundo", status="CURRENT", owner_skill="analyze-legacy-solution",
        created_at=TS, updated_at=TS, project_name="P", depth="DEEP", source_modified_at=TS) + "# P\n")
    write(root, "handoffs/HANDOFF-0003-incompleto.md", handoff(status="PARTIAL", ident="HANDOFF-0003")
          .replace("target_flow: SDD", "target_flow: XYZ").replace("## External Boundaries", "## Fronteiras"))
    write(root, "fix-plans/FIX-0002-sem-rastreio/TASKS-FIX-0002.md", front(
        artifact_type="FIX_TASKS", id="TASKS-FIX-0002", status="READY_FOR_APPROVAL", owner_skill="coordinate-fix",
        created_at=TS, updated_at=TS, fix_id="FIX-0002") + "# Tasks\n")
    write(root, "notes/random.md", "# sem frontmatter\n")
    write(root, "proposals/RFC-0003-x.md", front(
        artifact_type="UNKNOWN_KIND", id="RFC-0003", status="DRAFT", owner_skill="x",
        created_at=TS, updated_at=TS) + "# RFC\n")
