"""Bundle regression suite. Run from the bundle root: python -m unittest discover -s tests -v"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixtures as fx  # noqa: E402

BUNDLE = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE / "payload" / "legacy-discovery"
SCRIPTS = PAYLOAD / "skill-contracts" / "scripts"
BASELINE = Path(__file__).resolve().parent / "baseline_v4_scripts"


def run_script(scripts: Path, name: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(scripts / name), *args], capture_output=True, text=True, encoding="utf-8",
    )


def load_installer():
    spec = importlib.util.spec_from_file_location("bundle_install", BUNDLE / "install.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TempDirCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ldsk-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class DifferentialRegressionTests(TempDirCase):
    """Without refinements, V5 scripts must behave byte-for-byte like the frozen V4 scripts."""

    def kb(self, name: str) -> Path:
        root = self.tmp / name
        fx.legacy_v2_knowledge(root)
        return root

    def test_validate_is_identical_on_v2_knowledge(self) -> None:
        old = run_script(BASELINE, "validate_artifacts.py", "--root", str(self.kb("a")))
        new = run_script(SCRIPTS, "validate_artifacts.py", "--root", str(self.kb("a")))
        self.assertEqual(old.returncode, 1, old.stderr)
        self.assertEqual((old.returncode, old.stdout, old.stderr), (new.returncode, new.stdout, new.stderr))

    def test_validate_is_identical_on_clean_knowledge(self) -> None:
        root = self.tmp / "clean"
        fx.write(root, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        old = run_script(BASELINE, "validate_artifacts.py", "--root", str(root))
        new = run_script(SCRIPTS, "validate_artifacts.py", "--root", str(root))
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertEqual((old.returncode, old.stdout, old.stderr), (new.returncode, new.stdout, new.stderr))

    def test_validate_missing_root_is_identical(self) -> None:
        missing = str(self.tmp / "nope")
        old = run_script(BASELINE, "validate_artifacts.py", "--root", missing)
        new = run_script(SCRIPTS, "validate_artifacts.py", "--root", missing)
        self.assertEqual((old.returncode, old.stdout, old.stderr), (new.returncode, new.stdout, new.stderr))

    def test_index_is_identical_on_v2_knowledge(self) -> None:
        a, b = self.kb("a"), self.kb("b")
        run_script(BASELINE, "sync_index.py", "--root", str(a))
        run_script(SCRIPTS, "sync_index.py", "--root", str(b))
        self.assertEqual((a / "INDEX.md").read_bytes(), (b / "INDEX.md").read_bytes())

    def test_next_id_is_identical_for_existing_types(self) -> None:
        root = self.kb("a")
        for kind in ("HANDOFF", "ADR", "FIX", "RFC"):
            old = run_script(BASELINE, "next_id.py", "--root", str(root), "--type", kind)
            new = run_script(SCRIPTS, "next_id.py", "--root", str(root), "--type", kind)
            self.assertEqual((old.returncode, old.stdout), (new.returncode, new.stdout), kind)


class RefinementContractTests(TempDirCase):
    def validate(self, refinement_text: str, handoff_status: str | None = "READY_FOR_SPECKIT",
                 relative: str = "refinements/REFINEMENT-0001-timeout.md") -> subprocess.CompletedProcess:
        root = self.tmp / "kb"
        if handoff_status:
            fx.write(root, "handoffs/HANDOFF-0001-timeout.md", fx.handoff(status=handoff_status))
        fx.write(root, relative, refinement_text)
        return run_script(SCRIPTS, "validate_artifacts.py", "--root", str(root))

    def assertValid(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stderr)

    def assertRejected(self, result: subprocess.CompletedProcess, fragment: str) -> None:
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(fragment, result.stderr)

    # Valid shapes
    def test_ready_refinement_passes(self) -> None:
        self.assertValid(self.validate(fx.refinement()))

    def test_awaiting_human_passes_with_open_question(self) -> None:
        self.assertValid(self.validate(fx.refinement(
            status="AWAITING_HUMAN", amb2_status="OPEN_HUMAN", amb2_answer="-",
            reviewed_by="null", reviewed_at="null")))

    def test_blocked_without_handoff_passes_with_reason(self) -> None:
        self.assertValid(self.validate(fx.refinement(
            status="BLOCKED", handoff_ref="NONE", block_reason="HANDOFF_MISSING",
            reviewed_by="null", reviewed_at="null")))

    def test_ready_with_nonblocking_open_question_passes(self) -> None:
        text = fx.refinement(open_questions="1", body_replace=((
            "| AMB-01 | Hoje há retry? | define AC | KNOWLEDGE | RESOLVED_BY_EVIDENCE | NO | HANDOFF-0001 § Current Behavior |",
            "| AMB-01 | Texto do aviso? | UX | HUMAN | OPEN_HUMAN | NO | - |"),))
        self.assertValid(self.validate(text))

    def test_no_existing_behavior_marker_passes(self) -> None:
        text = fx.refinement(body_replace=(
            ("| GR-01 | contrato SOAP inalterado | HANDOFF-0001 § Compatibility Constraints | CHARACTERIZATION_TEST_REQUIRED |",
             "NO_EXISTING_BEHAVIOR_AFFECTED — tela nova, sem consumidor (HANDOFF-0001 § Impact Surface)"),
            ("| AC-01 | GR-01 |", "| AC-01 | - |"), ("| AC-02 | GR-01 |", "| AC-02 | - |")))
        self.assertValid(self.validate(text))

    # Human-in-the-loop guardrails
    def test_ready_with_blocking_open_question_is_rejected(self) -> None:
        text = fx.refinement(amb2_status="OPEN_HUMAN", amb2_answer="-")
        self.assertRejected(self.validate(text), "blocking open questions: AMB-02")

    def test_ac_from_unanswered_question_is_rejected(self) -> None:
        text = fx.refinement(amb2_status="OPEN_HUMAN", amb2_answer="-")
        self.assertRejected(self.validate(text), "AC-02 derives from AMB-02, which has no human answer")

    def test_ready_without_human_review_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(reviewed_by="null")), "requires human reviewed_by")

    def test_answered_without_answer_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(amb2_answer="-")), "AMB-02 lacks the recorded human answer")

    def test_awaiting_without_open_question_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(status="AWAITING_HUMAN")),
                            "AWAITING_HUMAN requires at least one OPEN_HUMAN")

    def test_open_questions_counter_must_match(self) -> None:
        self.assertRejected(self.validate(fx.refinement(open_questions="3")),
                            "open_questions is 3 but register has 0 OPEN_HUMAN")

    def test_evidence_resolution_cannot_come_from_human(self) -> None:
        text = fx.refinement(body_replace=(("| KNOWLEDGE | RESOLVED_BY_EVIDENCE |", "| HUMAN | RESOLVED_BY_EVIDENCE |"),))
        self.assertRejected(self.validate(text), "AMB-01 resolved by evidence cannot have Source HUMAN")

    def test_evidence_resolution_requires_evidence(self) -> None:
        text = fx.refinement(body_replace=(("| NO | HANDOFF-0001 § Current Behavior |", "| NO | - |"),))
        self.assertRejected(self.validate(text), "AMB-01 resolved by evidence lacks evidence")

    def test_invalid_register_values_are_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| KNOWLEDGE | RESOLVED_BY_EVIDENCE | NO |", "| GUESS | RESOLVED_BY_EVIDENCE | MAYBE |"),))
        result = self.validate(text)
        self.assertRejected(result, "AMB-01 invalid Source GUESS")
        self.assertIn("AMB-01 Blocking must be YES or NO", result.stderr)

    # AS-IS precondition
    def test_ready_requires_ready_handoff(self) -> None:
        self.assertRejected(self.validate(fx.refinement(), handoff_status="PARTIAL"),
                            "requires HANDOFF-0001 to be READY_FOR_SPECKIT (is PARTIAL)")

    def test_ready_without_handoff_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(handoff_ref="NONE"), handoff_status=None),
                            "READY_FOR_SPECKIT requires an existing handoff")

    def test_dangling_handoff_reference_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(handoff_ref="HANDOFF-0009")),
                            "handoff HANDOFF-0009 not found")

    def test_blocked_requires_reason(self) -> None:
        self.assertRejected(self.validate(fx.refinement(status="BLOCKED")), "BLOCKED refinement lacks block_reason")

    # Traceability and regression guardrails
    def test_ac_without_valid_origin_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("último estado | STORY |", "último estado | ACHISMO |"),))
        self.assertRejected(self.validate(text), "AC-01 has invalid Origin ACHISMO")

    def test_ac_not_covered_by_slice_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| Sinalizar estado antigo | AC-02 |", "| Sinalizar estado antigo | AC-01 |"),))
        self.assertRejected(self.validate(text), "AC-02 is not covered by any SLICE")

    def test_guardrail_not_covered_by_slice_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| AC-01 | GR-01 |", "| AC-01 | - |"), ("| AC-02 | GR-01 |", "| AC-02 | - |")))
        self.assertRejected(self.validate(text), "GR-01 is not covered by any SLICE")

    def test_missing_guardrails_are_rejected(self) -> None:
        text = fx.refinement(body_replace=(
            ("| GR-01 | contrato SOAP inalterado | HANDOFF-0001 § Compatibility Constraints | CHARACTERIZATION_TEST_REQUIRED |", ""),
            ("| AC-01 | GR-01 |", "| AC-01 | - |"), ("| AC-02 | GR-01 |", "| AC-02 | - |")))
        self.assertRejected(self.validate(text), "requires GR-NN rows or NO_EXISTING_BEHAVIOR_AFFECTED")

    def test_invalid_guardrail_proof_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| CHARACTERIZATION_TEST_REQUIRED |", "| confia |"),))
        self.assertRejected(self.validate(text), "GR-01 has invalid Proof confia")

    def test_slice_dependency_cycle_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| GR-01 | /speckit.specify → /speckit.implement | - |",
                                            "| GR-01 | /speckit.specify → /speckit.implement | SLICE-02 |"),))
        self.assertRejected(self.validate(text), "dependency cycle")

    def test_slice_referencing_unknown_ac_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("| Sinalizar estado antigo | AC-02 |", "| Sinalizar estado antigo | AC-02, AC-09 |"),))
        self.assertRejected(self.validate(text), "SLICE-02 references unknown AC-09")

    def test_missing_section_is_rejected(self) -> None:
        text = fx.refinement(body_replace=(("## Explicitly Not Decided", "## Talvez"),))
        self.assertRejected(self.validate(text), "missing section ## Explicitly Not Decided")

    # Shared contracts still apply to the new type
    def test_wrong_owner_is_rejected(self) -> None:
        text = fx.refinement().replace("owner_skill: refine-user-story", "owner_skill: prepare-speckit-context")
        self.assertRejected(self.validate(text), "owner prepare-speckit-context must be refine-user-story")

    def test_wrong_directory_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(), relative="handoffs/REFINEMENT-0001-timeout.md"),
                            "STORY_REFINEMENT must be stored under refinements")

    def test_non_canonical_name_is_rejected(self) -> None:
        self.assertRejected(self.validate(fx.refinement(), relative="refinements/REFINEMENT-0001-Timeout-FINAL.md"),
                            "non-canonical filename for STORY_REFINEMENT")


class RefinementToolingTests(TempDirCase):
    def test_next_id_supports_refinement(self) -> None:
        root = self.tmp / "kb"
        self.assertEqual(run_script(SCRIPTS, "next_id.py", "--root", str(root), "--type", "REFINEMENT").stdout.strip(), "0001")
        fx.write(root, "refinements/REFINEMENT-0007-x.md", "x")
        fx.write(root, "handoffs/HANDOFF-0012-x.md", "x")
        self.assertEqual(run_script(SCRIPTS, "next_id.py", "--root", str(root), "--type", "REFINEMENT").stdout.strip(), "0008")
        self.assertEqual(run_script(SCRIPTS, "next_id.py", "--root", str(root), "--type", "HANDOFF").stdout.strip(), "0013")

    def test_index_lists_refinements_in_own_group_after_handoffs(self) -> None:
        root = self.tmp / "kb"
        fx.write(root, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        fx.write(root, "refinements/REFINEMENT-0001-timeout.md", fx.refinement())
        self.assertEqual(run_script(SCRIPTS, "sync_index.py", "--root", str(root)).returncode, 0)
        index = (root / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("## Refinamentos de histórias (PO)", index)
        self.assertLess(index.index("## Handoffs para Spec Kit"), index.index("## Refinamentos de histórias (PO)"))
        self.assertNotIn("Tipos não registrados", index)
        self.assertEqual(run_script(SCRIPTS, "validate_artifacts.py", "--root", str(root)).returncode, 0)


def _probe_module() -> None:
    """Expose refinement_rules for the vocabulary test without polluting sys.path globally."""
    spec = importlib.util.spec_from_file_location("refinement_rules_probe", SCRIPTS / "refinement_rules.py")
    sys.path.insert(0, str(SCRIPTS))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules["refinement_rules_probe"] = module


class SkillDocumentationTests(unittest.TestCase):
    """The skill documentation and the validator must speak the same vocabulary."""

    @classmethod
    def setUpClass(cls) -> None:
        _probe_module()
        cls.rules = sys.modules["refinement_rules_probe"]
        cls.skill = PAYLOAD / "skills" / "refine-user-story"
        cls.format = (cls.skill / "references" / "refinement-format.md").read_text(encoding="utf-8")

    def test_skill_files_exist_with_frontmatter(self) -> None:
        text = (self.skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: refine-user-story\ndescription: "))
        for ref in ("refinement-format.md", "ambiguity-protocol.md", "story-quality-checklist.md", "execution-planning.md"):
            self.assertTrue((self.skill / "references" / ref).exists(), ref)
            self.assertIn(ref, text)

    def test_format_documents_every_required_section(self) -> None:
        for section in self.rules.REQUIRED_SECTIONS:
            self.assertIn(section, self.format)

    def test_format_documents_every_register_value(self) -> None:
        for value in self.rules.AMB_SOURCES | self.rules.AMB_STATUSES:
            self.assertIn(value, self.format)

    def test_skill_never_claims_speckit_or_git_ownership(self) -> None:
        text = (self.skill / "SKILL.md").read_text(encoding="utf-8")
        for forbidden in ("git commit", "git push", "git add"):
            self.assertNotIn(forbidden, text)


class CommandTests(unittest.TestCase):
    """The /legacy.* prompt files must be well-formed and only point at things that exist."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir = PAYLOAD / "prompts"
        cls.files = sorted(cls.dir.glob("legacy.*.prompt.md"))
        cls.names = {f.name[: -len(".prompt.md")] for f in cls.files}

    def test_expected_commands_exist(self) -> None:
        expected = {"help", "story", "analyze", "bug", "impact", "handoff", "refine", "answer",
                    "approve", "branch", "status", "validate", "archive"}
        self.assertEqual({n.split(".", 1)[1] for n in self.names}, expected)

    def test_frontmatter_is_valid(self) -> None:
        for f in self.files:
            text = f.read_text(encoding="utf-8")
            match = re.match(r"---\n(.*?)\n---\n", text, re.S)
            self.assertIsNotNone(match, f.name)
            head = match.group(1)
            self.assertRegex(head, r'(?m)^description: ".+"$', f.name)
            self.assertRegex(head, r"(?m)^agent: legacy-discovery$", f.name)
            for section in ("## Objetivo", "## Entradas Mínimas", "## Passos", "## Saída Obrigatória", "## Regras"):
                self.assertIn(section, text, f"{f.name} {section}")

    def test_skill_links_resolve(self) -> None:
        for f in self.files:
            for target in re.findall(r"\]\((\.\./skills/[^)]+)\)", f.read_text(encoding="utf-8")):
                resolved = PAYLOAD / "skills" / target.replace("../skills/", "")
                self.assertTrue(resolved.exists(), f"{f.name} -> {target}")

    def test_every_active_skill_has_a_command(self) -> None:
        installer = load_installer()
        joined = "\n".join(f.read_text(encoding="utf-8") for f in self.files)
        for skill in installer.ACTIVE_SKILLS:
            self.assertIn(f"../skills/{skill}/SKILL.md", joined, skill)

    def test_scripts_referenced_by_commands_exist(self) -> None:
        joined = "\n".join(f.read_text(encoding="utf-8") for f in self.files)
        for script in set(re.findall(r"scripts/([a-z_]+\.py)", joined)):
            self.assertTrue((SCRIPTS / script).exists(), script)

    def test_every_mentioned_legacy_command_exists(self) -> None:
        sources = list(self.files) + [self.dir / "README.md", BUNDLE / "README.md",
                                      PAYLOAD / "skills" / "refine-user-story" / "SKILL.md",
                                      SCRIPTS / "story_status.py", BUNDLE / "install.py"]
        for source in sources:
            for command in set(re.findall(r"/(legacy\.[a-z]+)", source.read_text(encoding="utf-8"))):
                self.assertIn(command, self.names, f"{source.name} mentions /{command}")

    def test_commands_do_not_collide_with_speckit(self) -> None:
        for name in self.names:
            self.assertTrue(name.startswith("legacy."))
            self.assertNotIn("speckit", name)

    def test_no_command_lets_the_agent_approve(self) -> None:
        approve = (self.dir / "legacy.approve.prompt.md").read_text(encoding="utf-8")
        self.assertIn("Você nunca executa `approve_refinement.py`", approve)
        for f in self.files:
            text = f.read_text(encoding="utf-8")
            self.assertNotIn("`reviewed_by`, `reviewed_at` (agora", text, f.name)
            self.assertNotRegex(text, r"(?im)^\d+\.\s+grave[^\n]*READY_FOR_SPECKIT", f.name)


class StoryStatusTests(TempDirCase):
    def status(self, *extra: str) -> str:
        result = run_script(SCRIPTS, "story_status.py", "--root", str(self.tmp), *extra)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_empty_knowledge(self) -> None:
        self.assertIn("/legacy.story", self.status())

    def test_missing_root(self) -> None:
        result = run_script(SCRIPTS, "story_status.py", "--root", str(self.tmp / "nope"))
        self.assertEqual(result.returncode, 2)

    def test_next_command_per_state(self) -> None:
        fx.write(self.tmp, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        fx.write(self.tmp, "handoffs/HANDOFF-0002-outro.md", fx.handoff(ident="HANDOFF-0002"))
        fx.write(self.tmp, "handoffs/HANDOFF-0003-parcial.md", fx.handoff(status="PARTIAL", ident="HANDOFF-0003"))
        fx.write(self.tmp, "refinements/REFINEMENT-0001-timeout.md", fx.refinement(
            status="AWAITING_HUMAN", amb2_status="OPEN_HUMAN", amb2_answer="-", reviewed_by="null", reviewed_at="null"))
        out = self.status()
        self.assertIn("/legacy.answer REFINEMENT-0001", out)
        self.assertIn("| HANDOFF-0002 |", out)
        self.assertIn("/legacy.refine", out)
        self.assertIn("/legacy.handoff (fechar lacunas", out)
        self.assertNotIn("| HANDOFF-0001 |", out)

    def test_ready_and_blocked(self) -> None:
        fx.write(self.tmp, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        fx.write(self.tmp, "refinements/REFINEMENT-0001-timeout.md", fx.refinement())
        fx.write(self.tmp, "refinements/REFINEMENT-0002-sem.md", fx.refinement(
            ident="REFINEMENT-0002", status="BLOCKED", handoff_ref="NONE", block_reason="HANDOFF_MISSING",
            reviewed_by="null", reviewed_at="null"))
        out = self.status()
        self.assertIn("/legacy.branch -> /speckit.specify", out)
        self.assertRegex(out, r"REFINEMENT-0002 .*\| /legacy\.handoff \|")
        only = self.status("--id", "REFINEMENT-0002")
        self.assertNotIn("REFINEMENT-0001", only)

    def test_status_is_read_only(self) -> None:
        fx.write(self.tmp, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        before = sorted((p.as_posix(), p.read_bytes()) for p in self.tmp.rglob("*") if p.is_file())
        self.status()
        after = sorted((p.as_posix(), p.read_bytes()) for p in self.tmp.rglob("*") if p.is_file())
        self.assertEqual(before, after)


class InstallerTests(TempDirCase):
    def setUp(self) -> None:
        super().setUp()
        self.installer = load_installer()
        self.repo = self.tmp / "repo"
        (self.repo / ".git" / "info").mkdir(parents=True)

    def install(self, keep_v1: bool = False) -> None:
        self.installer.install_discovery(BUNDLE, self.repo, keep_v1)
        self.installer.write_install_metadata(self.repo, "1.0.1", self.installer.bundle_commands(BUNDLE))

    def test_commands_installed_without_touching_other_prompts(self) -> None:
        prompts = self.repo / ".github" / "prompts"
        foreign = {
            "speckit.specify.prompt.md": "---\nagent: speckit.specify\n---\nSpec Kit\n",
            "meu-prompt.prompt.md": "# meu prompt\n",
        }
        for name, text in foreign.items():
            fx.write(prompts, name, text)
        self.install()
        self.install()
        for name, text in foreign.items():
            self.assertEqual((prompts / name).read_text(encoding="utf-8"), text, name)
        commands = self.installer.bundle_commands(BUNDLE)
        self.assertGreaterEqual(len(commands), 13)
        for name in commands:
            self.assertEqual((prompts / name).read_bytes(), (PAYLOAD / "prompts" / name).read_bytes(), name)
        self.assertFalse((prompts / "README.md").exists())
        meta = json.loads((self.repo / ".github" / "legacy-discovery" / "installation.json").read_text(encoding="utf-8"))
        self.assertIn("/legacy.refine", meta["commands"])
        self.assertIn("/legacy.approve", meta["commands"])

    def test_every_previous_skill_is_still_active(self) -> None:
        previous = {"analyze-legacy-solution", "investigate-legacy-bug", "analyze-change-impact",
                    "prepare-speckit-context", "prepare-feature-branch"}
        self.assertTrue(previous <= set(self.installer.ACTIVE_SKILLS))
        self.assertIn("refine-user-story", self.installer.ACTIVE_SKILLS)

    def test_bundle_manifest_matches_installer(self) -> None:
        bundle = json.loads((BUNDLE / "bundle.json").read_text(encoding="utf-8"))
        self.assertEqual(bundle["legacy_discovery"]["active_skills"], list(self.installer.ACTIVE_SKILLS))
        self.assertEqual(bundle["bundle_version"], self.installer.BUNDLE_VERSION)
        self.assertEqual(bundle["legacy_discovery"]["version"], self.installer.LEGACY_DISCOVERY_VERSION)

    def test_install_places_all_skills_and_knowledge_dirs(self) -> None:
        self.install()
        for skill in self.installer.ACTIVE_SKILLS:
            self.assertTrue((self.repo / ".github" / "skills" / skill / "SKILL.md").exists(), skill)
        knowledge = self.repo / ".github" / "copilot-knowledge"
        for name in ("projects", "decisions", "deep-dives", "proposals", "investigations",
                     "impact-analyses", "handoffs", "fix-plans", "refinements"):
            self.assertTrue((knowledge / name).is_dir(), name)
        self.assertTrue((self.repo / ".github" / "skill-contracts" / "scripts" / "refinement_rules.py").exists())
        meta = json.loads((self.repo / ".github" / "legacy-discovery" / "installation.json").read_text(encoding="utf-8"))
        self.assertIn("refine-user-story", meta["active_skills"])

    def test_upgrade_preserves_existing_knowledge_and_local_only_policy(self) -> None:
        knowledge = self.repo / ".github" / "copilot-knowledge"
        fx.write(knowledge, "INDEX.md", "# meu índice\n")
        fx.write(knowledge, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        exclude = self.repo / ".git" / "info" / "exclude"
        exclude.write_text("*.log\n", encoding="utf-8")
        self.install()
        self.install()
        self.assertEqual((knowledge / "INDEX.md").read_text(encoding="utf-8"), "# meu índice\n")
        self.assertEqual((knowledge / "handoffs/HANDOFF-0001-timeout.md").read_text(encoding="utf-8"), fx.handoff())
        excluded = exclude.read_text(encoding="utf-8")
        self.assertTrue(excluded.startswith("*.log\n"))
        self.assertEqual(excluded.count(".github/copilot-knowledge/"), 1)
        installed = self.repo / ".github" / "skill-contracts" / "scripts"
        self.assertEqual(run_script(installed, "validate_artifacts.py", "--root", str(knowledge)).returncode, 0)

    def test_v1_skills_are_still_archived(self) -> None:
        fx.write(self.repo / ".github" / "skills" / "coordinate-fix", "SKILL.md", "v1")
        self.install()
        self.assertFalse((self.repo / ".github" / "skills" / "coordinate-fix").exists())
        self.assertTrue((self.repo / ".github" / "legacy-workflow-v1" / "coordinate-fix" / "SKILL.md").exists())

    def test_v1_skills_kept_on_request(self) -> None:
        fx.write(self.repo / ".github" / "skills" / "coordinate-fix", "SKILL.md", "v1")
        self.install(keep_v1=True)
        self.assertTrue((self.repo / ".github" / "skills" / "coordinate-fix" / "SKILL.md").exists())

    def test_existing_skill_payloads_are_unchanged(self) -> None:
        """Every file of the five V4 skills and of the archived V1 workflow is byte-identical to V4."""
        baseline = BUNDLE / "tests" / "baseline_v4_skill_digests.json"
        digests = json.loads(baseline.read_text(encoding="utf-8"))
        import hashlib
        for relative, digest in digests.items():
            current = hashlib.sha256((PAYLOAD / relative).read_bytes()).hexdigest()
            self.assertEqual(current, digest, f"{relative} changed; update baseline only with a reviewed change")


if __name__ == "__main__":
    unittest.main()
