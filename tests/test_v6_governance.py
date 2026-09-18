"""V6 suite: the lock (hook), human-only approval with seal, evidence checks and release hygiene."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fixtures as fx  # noqa: E402

BUNDLE = Path(__file__).resolve().parents[1]
PAYLOAD = BUNDLE / "payload" / "legacy-discovery"
SCRIPTS = PAYLOAD / "skill-contracts" / "scripts"
HOOK = PAYLOAD / "hooks" / "legacy_governance.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = load("legacy_governance", HOOK)


SCRATCH = Path(tempfile.mkdtemp(prefix="ldsk6cwd-"))


def run(script: Path, *args: str, stdin: str = "", cwd: Path | None = None) -> subprocess.CompletedProcess:
    """stdin is never inherited (no accidental tty) and cwd is never the bundle (no stray files)."""
    return subprocess.run([sys.executable, str(script), *args], input=stdin, capture_output=True, text=True,
                          encoding="utf-8", cwd=str(cwd or SCRATCH))


def call(tool: str, **tool_input) -> tuple[str, str]:
    return hook.decide(json.dumps({"hookEventName": "PreToolUse", "toolName": tool, "toolInput": tool_input}))


K = ".github/copilot-knowledge"


class HookAllowsLegitimateWork(unittest.TestCase):
    """A lock that blocks real work gets switched off. These must stay allowed."""

    def assertAllowed(self, result) -> None:
        self.assertEqual(result[0], "allow", result[1])

    def test_reading_and_searching_anything(self) -> None:
        self.assertAllowed(call("read_file", filePath="src/Consulta/PbhClient.cs"))
        self.assertAllowed(call("grep_search", query="reviewed_by", includePattern="**/*.md"))
        self.assertAllowed(call("read_file", filePath=".github/skill-contracts/scripts/validate_artifacts.py"))

    def test_writing_knowledge_artifacts(self) -> None:
        self.assertAllowed(call("create_file", filePath=f"{K}/handoffs/HANDOFF-0001-x.md",
                                content="---\nstatus: READY_FOR_SPECKIT\n---\n"))
        self.assertAllowed(call("create_file", filePath=f"{K}/refinements/REFINEMENT-0001-x.md",
                                content="---\nstatus: READY_FOR_REVIEW\nreviewed_by: null\n---\n"))
        self.assertAllowed(call("replace_string_in_file", filePath=f"{K}/refinements/REFINEMENT-0001-x.md",
                                oldString="status: READY_FOR_SPECKIT", newString="status: READY_FOR_REVIEW"))

    def test_windows_absolute_and_uri_paths(self) -> None:
        self.assertAllowed(call("create_file", filePath="C:\\Projetos\\Repo\\.github\\copilot-knowledge\\projects\\PROJECT-x.md",
                                content="x"))
        self.assertAllowed(call("create_file", uri="file:///c%3A/Projetos/Repo/.github/copilot-knowledge/x.md", content="x"))

    def test_writing_regression_test_in_test_project(self) -> None:
        self.assertAllowed(call("create_file", filePath="src/Consulta.Tests/PbhClientTests.cs", content="class T {}"))
        self.assertAllowed(call("create_file", filePath="tests/Consulta/TimeoutTests.cs", content="class T {}"))

    def test_contract_scripts_and_read_only_commands(self) -> None:
        for command in (
            f"python .github/skill-contracts/scripts/validate_artifacts.py --root {K} 2>&1",
            f"python .github/skill-contracts/scripts/sync_index.py --root {K}",
            "python .github/skill-contracts/scripts/story_status.py > $null",
            "python .github/skill-contracts/scripts/next_id.py --type REFINEMENT",
            'python .github/skills/prepare-feature-branch/scripts/create_feature_branch.py --slug "timeout-pbh"',
            "git status", "git log --oneline -5", "git -C src diff", "git fetch origin", "git merge-base main HEAD",
            f"grep -rn reviewed_by {K}", "grep -e umpadraobemlongosemespacos1234 src",
            "dotnet build Atlas.sln", "dotnet test tests/Consulta.Tests",
            'Get-ChildItem -Recurse -Filter *.csproj | Select-String "PackageReference"',
        ):
            self.assertAllowed(call("run_in_terminal", command=command, explanation="x"))

    def test_empty_input_and_unrelated_keys(self) -> None:
        self.assertEqual(hook.decide("")[0], "allow")
        self.assertAllowed(call("run_in_terminal", command="git status", profile="pwsh"))


class HookDeniesViolations(unittest.TestCase):
    def assertDenied(self, result, fragment: str = "") -> None:
        self.assertEqual(result[0], "deny", result[1])
        if fragment:
            self.assertIn(fragment, result[1])

    def test_production_code(self) -> None:
        self.assertDenied(call("create_file", filePath="src/Consulta/PbhClient.cs", content="x"), "só escrevem")
        self.assertDenied(call("replace_string_in_file", filePath="src/Consulta/VeiculoController.cs",
                               oldString="a", newString="b"))
        self.assertDenied(call("apply_patch", input="*** Begin Patch\n*** Update File: src/A.cs\n@@\n-a\n+b\n*** End Patch"))

    def test_spec_kit_territory(self) -> None:
        self.assertDenied(call("create_file", filePath="specs/001-timeout/spec.md", content="x"), "Spec Kit")
        self.assertDenied(call("create_file", filePath=".specify/memory/constitution.md", content="x"), "Spec Kit")

    def test_tooling_cannot_be_weakened(self) -> None:
        """Each rule is proven by its own reason, not only by the generic 'outside the trails' fallback."""
        for path, reason in ((".github/skill-contracts/scripts/validate_artifacts.py", "contratos e validador"),
                             (".github/skills/refine-user-story/SKILL.md", "as skills não se reescrevem"),
                             (".github/hooks/legacy_governance.py", "a fechadura não pode"),
                             (".github/agents/legacy-discovery.agent.md", "própria configuração"),
                             (".github/prompts/legacy.approve.prompt.md", "comandos /legacy.*"),
                             (f"{K}/INDEX.md", "sync_index.py"),
                             (".github/legacy-discovery/installation.json", "metadados da instalação")):
            self.assertDenied(call("replace_string_in_file", filePath=path, oldString="a", newString="b"), reason)

    def test_agent_cannot_approve(self) -> None:
        ref = f"{K}/refinements/REFINEMENT-0001-x.md"
        self.assertDenied(call("create_file", filePath=ref, content="---\nstatus: READY_FOR_SPECKIT\n---\n"), "READY_FOR_REVIEW")
        self.assertDenied(call("replace_string_in_file", filePath=ref, oldString="reviewed_by: null",
                               newString='reviewed_by: "Rafael"'), "reviewed_by")
        self.assertDenied(call("replace_string_in_file", filePath=ref, oldString="x",
                               newString="approval_digest: abc123"), "approval_digest")
        self.assertDenied(call("apply_patch", input=f"*** Begin Patch\n*** Update File: {ref}\n@@\n-status: READY_FOR_REVIEW\n"
                                                    "+status: READY_FOR_SPECKIT\n*** End Patch"))
        self.assertDenied(call("run_in_terminal", command="python .github/skill-contracts/scripts/approve_refinement.py "
                                                          "--id REFINEMENT-0001 --reviewer Rafael --confirm REFINEMENT-0001"),
                          "ato humano")

    def test_destructive_git(self) -> None:
        for command in ("git push", "git push --force origin x", "git -C . push", "git commit -m x", "git add -A",
                        "git reset --hard", "git stash", "git checkout main", "git switch -c x", "git branch -D x",
                        "git rebase main", "git merge feature", "git clean -fd", "cd src && git push",
                        "git -c user.name=x commit -m y", '"git.exe" push'):
            self.assertDenied(call("run_in_terminal", command=command), "Git")

    def test_shell_writes_into_protected_trails(self) -> None:
        for command in (
            f"Set-Content {K}/refinements/REFINEMENT-0001-x.md 'status: READY_FOR_SPECKIT'",
            f"echo x > {K}/INDEX.md",
            f"python -c \"import pathlib; pathlib.Path('{K}/refinements/x.md').write_text('x')\"",
            "Remove-Item .github/skills/refine-user-story -Recurse",
            "sed -i s/x/y/ .github/skill-contracts/scripts/refinement_rules.py",
            f"python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean",
        ):
            self.assertDenied(call("run_in_terminal", command=command))

    def test_uninspectable_execution(self) -> None:
        self.assertDenied(call("run_in_terminal", command="powershell -EncodedCommand SQBFAFgAIAAoACcAeAAnACkA"))
        self.assertDenied(call("run_in_terminal", command="pwsh -enc SQBFAFgA"))

    def test_write_without_identifiable_file_fails_closed(self) -> None:
        self.assertDenied(call("create_file", content="x"), "falha fechada")


class HookProtocol(unittest.TestCase):
    def test_allow_and_deny_follow_agentqa_protocol(self) -> None:
        allowed = run(HOOK, stdin=json.dumps({"toolName": "read_file", "toolInput": {"filePath": "x.cs"}}))
        denied = run(HOOK, stdin=json.dumps({"toolName": "run_in_terminal", "toolInput": {"command": "git push"}}))
        self.assertEqual(allowed.returncode, 0)
        self.assertEqual(json.loads(allowed.stdout)["hookSpecificOutput"]["permissionDecision"], "allow")
        self.assertEqual(denied.returncode, 2)
        output = json.loads(denied.stdout)["hookSpecificOutput"]
        self.assertEqual((output["hookEventName"], output["permissionDecision"]), ("PreToolUse", "deny"))

    def test_output_is_encoding_proof(self) -> None:
        denied = run(HOOK, stdin=json.dumps({"toolName": "create_file", "toolInput": {"filePath": "src/A.cs", "content": "x"}}))
        denied.stdout.encode("ascii")
        self.assertIn("só escrevem", json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_hook_never_creates_folders_to_log(self) -> None:
        empty = Path(tempfile.mkdtemp(prefix="ldsk6e-"))
        try:
            run(HOOK, stdin=json.dumps({"toolName": "run_in_terminal", "toolInput": {"command": "git push"}}), cwd=empty)
            self.assertEqual(list(empty.iterdir()), [])
        finally:
            shutil.rmtree(empty, ignore_errors=True)

    def test_malformed_input_fails_closed(self) -> None:
        result = run(HOOK, stdin="{not json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("failed closed", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecisionReason"])

    def test_agent_wires_the_hook(self) -> None:
        agent = (PAYLOAD / "agents" / "legacy-discovery.agent.md").read_text(encoding="utf-8")
        self.assertIn("name: legacy-discovery", agent)
        self.assertIn("PreToolUse:", agent)
        self.assertIn(".github/hooks/legacy_governance.py", agent)


class RepoCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ldsk6-"))
        self.repo = self.tmp / "repo"
        self.kb = self.repo / ".github" / "copilot-knowledge"
        fx.write(self.kb, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        fx.write(self.repo, "src/Consulta/PbhClient.cs", "\n".join(f"// line {i}" for i in range(1, 51)) + "\n")
        fx.write(self.repo, "tests/Consulta.Tests/PbhClientTests.cs", "public void Envelope_Mantem_Contrato() {}\n")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def refinement(self, **kwargs) -> Path:
        path = self.kb / "refinements" / "REFINEMENT-0001-timeout.md"
        fx.write(self.kb, "refinements/REFINEMENT-0001-timeout.md", fx.refinement(**kwargs))
        return path

    def validate(self) -> subprocess.CompletedProcess:
        return run(SCRIPTS / "validate_artifacts.py", "--root", str(self.kb))

    def approve(self, *extra: str) -> subprocess.CompletedProcess:
        return run(SCRIPTS / "approve_refinement.py", "--root", str(self.kb), "--id", "REFINEMENT-0001", *extra)


REVIEW = dict(status="READY_FOR_REVIEW", reviewed_by="null", reviewed_at="null")


class HumanApprovalAndSeal(RepoCase):
    def test_ready_for_review_is_valid_before_approval(self) -> None:
        self.refinement(**REVIEW)
        self.assertEqual(self.validate().returncode, 0, self.validate().stderr)

    def test_approval_records_reviewer_and_seals(self) -> None:
        path = self.refinement(**REVIEW)
        result = self.approve("--reviewer", "Rafael Lima", "--confirm", "REFINEMENT-0001")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("APPROVED", result.stdout)
        text = path.read_text(encoding="utf-8")
        self.assertIn("status: READY_FOR_SPECKIT", text)
        self.assertIn('reviewed_by: "Rafael Lima"', text)
        self.assertIn("revision: 2", text)
        self.assertRegex(text, r"approval_digest: [0-9a-f]{64}")
        validated = self.validate()
        self.assertEqual(validated.returncode, 0, validated.stderr)
        self.assertNotIn("WARNING", validated.stderr)

    def test_edit_after_approval_breaks_the_seal(self) -> None:
        path = self.refinement(**REVIEW)
        self.approve("--reviewer", "Rafael Lima", "--confirm", "REFINEMENT-0001")
        path.write_text(path.read_text(encoding="utf-8").replace("24h", "48h"), encoding="utf-8", newline="\n")
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("changed after approval", result.stderr)

    def test_only_ready_for_review_can_be_approved(self) -> None:
        path = self.refinement(status="AWAITING_HUMAN", amb2_status="OPEN_HUMAN", amb2_answer="-",
                               reviewed_by="null", reviewed_at="null")
        before = path.read_bytes()
        result = self.approve("--reviewer", "Rafael Lima", "--confirm", "REFINEMENT-0001")
        self.assertEqual(result.returncode, 1)
        self.assertIn("só READY_FOR_REVIEW", result.stderr)
        self.assertEqual(path.read_bytes(), before)

    def test_confirmation_is_required(self) -> None:
        path = self.refinement(**REVIEW)
        before = path.read_bytes()
        self.assertEqual(self.approve("--reviewer", "Rafael Lima", "--confirm", "REFINEMENT-0009").returncode, 1)
        not_tty = self.approve("--reviewer", "Rafael Lima")
        self.assertEqual(not_tty.returncode, 1)
        self.assertRegex(not_tty.stderr, "terminal interativo|confirmação não recebida")
        self.assertEqual(path.read_bytes(), before)

    def test_reviewer_must_be_a_person(self) -> None:
        self.refinement(**REVIEW)
        for name in ("copilot", "agent", "null", " "):
            self.assertEqual(self.approve("--reviewer", name, "--confirm", "REFINEMENT-0001").returncode, 1, name)

    def test_failed_approval_changes_nothing(self) -> None:
        path = self.refinement(status="READY_FOR_REVIEW", reviewed_by="null", reviewed_at="null",
                               body_replace=(("## Explicitly Not Decided", "## Talvez"),))
        before = path.read_bytes()
        result = self.approve("--reviewer", "Rafael Lima", "--confirm", "REFINEMENT-0001")
        self.assertEqual(result.returncode, 1)
        self.assertIn("nada foi alterado", result.stderr)
        self.assertEqual(path.read_bytes(), before)

    def test_v5_approval_without_seal_is_a_warning(self) -> None:
        self.refinement()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARNING", result.stderr)
        self.assertIn("approval_digest", result.stderr)

    def test_review_fields_only_after_approval(self) -> None:
        self.refinement(status="READY_FOR_REVIEW")
        result = self.validate()
        self.assertEqual(result.returncode, 1)
        self.assertIn("must not carry reviewed_by", result.stderr)

    def test_awaiting_without_questions_points_to_ready_for_review(self) -> None:
        self.refinement(status="AWAITING_HUMAN", reviewed_by="null", reviewed_at="null")
        self.assertIn("use READY_FOR_REVIEW", self.validate().stderr)

    def test_status_shows_next_command(self) -> None:
        self.refinement(**REVIEW)
        out = run(SCRIPTS / "story_status.py", "--root", str(self.kb)).stdout
        self.assertIn("/legacy.approve REFINEMENT-0001", out)


def cite(old: str, new: str) -> dict:
    return dict(body_replace=((old, new),), **REVIEW)


AS_IS = "- `FACT` — consulta síncrona — HANDOFF-0001"
GR_PROOF = "| CHARACTERIZATION_TEST_REQUIRED |"


class EvidenceChecks(RepoCase):
    def assertEvidence(self, fragment: str | None, **kwargs) -> None:
        self.refinement(**kwargs)
        result = self.validate()
        if fragment is None:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertIn(fragment, result.stderr)

    def test_real_citation_passes(self) -> None:
        self.assertEvidence(None, **cite(AS_IS, AS_IS + " — `src/Consulta/PbhClient.cs:41`"))
        self.assertEvidence(None, **cite(AS_IS, AS_IS + " — `src/Consulta/PbhClient.cs:40-50`"))

    def test_line_beyond_file(self) -> None:
        self.assertEvidence("has only 50 line(s)", **cite(AS_IS, AS_IS + " — `src/Consulta/PbhClient.cs:99`"))

    def test_missing_file(self) -> None:
        self.assertEvidence("does not exist in the repository", **cite(AS_IS, AS_IS + " — `src/Nada/Fantasma.cs:3`"))

    def test_path_outside_repository(self) -> None:
        self.assertEvidence("does not exist in the repository", **cite(AS_IS, AS_IS + " — `../../fora.cs:1`"))

    def test_existing_test_must_exist_and_contain_the_test(self) -> None:
        ok = "| EXISTING_TEST:tests/Consulta.Tests/PbhClientTests.cs::Envelope_Mantem_Contrato |"
        self.assertEvidence(None, **cite(GR_PROOF, ok))
        self.assertEvidence("does not contain Teste_Que_Nao_Existe",
                            **cite(GR_PROOF, "| EXISTING_TEST:tests/Consulta.Tests/PbhClientTests.cs::Teste_Que_Nao_Existe |"))
        self.assertEvidence("EXISTING_TEST tests/Nada.cs does not exist", **cite(GR_PROOF, "| EXISTING_TEST:tests/Nada.cs |"))

    def test_cited_artifact_must_exist(self) -> None:
        self.assertEvidence("cites IMPACT-20260915-historico, which does not exist",
                            **cite(AS_IS, AS_IS + " — IMPACT-20260915-historico"))

    def test_story_verbatim_is_not_checked(self) -> None:
        self.assertEvidence(None, **cite("> Como atendente", "> Ver `src/Qualquer/Coisa.cs:9` e IMPACT-20990101-x. Como atendente"))

    def test_handoff_bad_citation_is_only_a_warning(self) -> None:
        fx.write(self.kb, "handoffs/HANDOFF-0001-timeout.md",
                 fx.handoff().replace("- PROJECT-consulta.", "- `src/Fantasma.cs:10`."))
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARNING", result.stderr)
        self.assertIn("src/Fantasma.cs", result.stderr)

    def test_outside_a_repository_file_checks_are_skipped(self) -> None:
        loose = self.tmp / "solta"
        fx.write(loose, "handoffs/HANDOFF-0001-timeout.md", fx.handoff())
        fx.write(loose, "refinements/REFINEMENT-0001-timeout.md",
                 fx.refinement(**cite(AS_IS, AS_IS + " — `src/Nada.cs:1`")))
        self.assertEqual(run(SCRIPTS / "validate_artifacts.py", "--root", str(loose)).returncode, 0)


class InstallerGovernance(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="ldsk6i-"))
        self.repo = self.tmp / "repo"
        (self.repo / ".git" / "info").mkdir(parents=True)
        self.installer = load("bundle_install_v6", BUNDLE / "install.py")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_lock_installed_without_touching_agentqa(self) -> None:
        agentqa = {".github/hooks/qa-governance.ps1": "# AgentQA hook\n",
                   ".github/agents/qa-delivery.agent.md": "---\nname: Enterprise QA Lead\n---\n"}
        for relative, text in agentqa.items():
            fx.write(self.repo, relative, text)
        self.installer.install_discovery(BUNDLE, self.repo, False)
        self.installer.install_discovery(BUNDLE, self.repo, False)
        for relative, text in agentqa.items():
            self.assertEqual((self.repo / relative).read_text(encoding="utf-8"), text, relative)
        for source, destination in self.installer.GOVERNANCE_FILES:
            self.assertEqual((self.repo / destination).read_bytes(), (PAYLOAD / source).read_bytes(), destination)

    def test_installed_hook_runs_from_repo_root(self) -> None:
        self.installer.install_discovery(BUNDLE, self.repo, False)
        result = run(self.repo / ".github" / "hooks" / "legacy_governance.py", cwd=self.repo,
                     stdin=json.dumps({"toolName": "run_in_terminal", "toolInput": {"command": "git push"}}))
        self.assertEqual(result.returncode, 2)
        log = list((self.repo / ".github" / "copilot-knowledge" / "governance-log").glob("*.log"))
        self.assertEqual(len(log), 1)
        self.assertIn("decision=deny", log[0].read_text(encoding="utf-8"))
        validated = run(self.repo / ".github" / "skill-contracts" / "scripts" / "validate_artifacts.py",
                        "--root", str(self.repo / ".github" / "copilot-knowledge"))
        self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_versions_agree(self) -> None:
        bundle = json.loads((BUNDLE / "bundle.json").read_text(encoding="utf-8"))
        self.assertEqual(bundle["bundle_version"], self.installer.BUNDLE_VERSION)
        self.assertEqual(bundle["legacy_discovery"]["version"], self.installer.LEGACY_DISCOVERY_VERSION)


class ReleaseHygiene(unittest.TestCase):
    def test_package_matches_its_checksums_and_has_no_leftovers(self) -> None:
        release = load("build_release", BUNDLE / "tools" / "build_release.py")
        self.assertEqual(release.check(), [])

    def test_order_is_the_same_on_every_os(self) -> None:
        """Found by CI: Windows sorted paths case-insensitively, Linux did not, so the zip differed by OS."""
        names = [line.split(None, 1)[1] for line in (BUNDLE / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(names, sorted(names))
        self.assertLess(names.index("./payload/legacy-discovery/skills/refine-user-story/SKILL.md"),
                        names.index("./payload/legacy-discovery/skills/refine-user-story/references/ambiguity-protocol.md"))

    def test_release_build_is_clean_and_reproducible(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="ldsk6r-"))
        try:
            copy = tmp / BUNDLE.name
            shutil.copytree(BUNDLE, copy, ignore=shutil.ignore_patterns("__pycache__"))
            (copy / "backups").mkdir()
            refused = run(copy / "tools" / "build_release.py", "--out-dir", str(tmp / "out"))
            self.assertEqual(refused.returncode, 1)
            self.assertIn("backups", refused.stderr)
            (copy / "backups").rmdir()
            first = run(copy / "tools" / "build_release.py", "--out-dir", str(tmp / "out"))
            self.assertEqual(first.returncode, 0, first.stderr)
            zip_path = tmp / "out" / f"{BUNDLE.name}.zip"
            digest_one = zip_path.read_bytes()
            run(copy / "tools" / "build_release.py", "--out-dir", str(tmp / "out"))
            self.assertEqual(zip_path.read_bytes(), digest_one)
            with zipfile.ZipFile(zip_path) as archive:
                names = {n.split("/", 1)[1] for n in archive.namelist()}
            files = {p.relative_to(copy).as_posix() for p in copy.rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts}
            self.assertEqual(names, files)
            self.assertEqual(run(copy / "tools" / "build_release.py", "--check").returncode, 0)
            verified = run(copy / "tools" / "build_release.py", "--verify-zip", str(zip_path))
            self.assertEqual(verified.returncode, 0, verified.stderr)
            (copy / "README.md").write_text("adulterado\n", encoding="utf-8")
            tampered = run(copy / "tools" / "build_release.py", "--verify-zip", str(zip_path))
            self.assertEqual(tampered.returncode, 1)
            self.assertIn("conteúdo diferente no zip", tampered.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
