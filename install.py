#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone

BUNDLE_VERSION = "1.4.1"
LEGACY_DISCOVERY_VERSION = "2.4"
DEFAULT_SPECKIT_VERSION = "1.0.1"
ACTIVE_SKILLS = (
    "analyze-legacy-solution",
    "investigate-legacy-bug",
    "analyze-change-impact",
    "prepare-speckit-context",
    "prepare-feature-branch",
    "refine-user-story",
)
LEGACY_V1_SKILLS = ("coordinate-fix", "execute-fix-plan", "run-solution-regression")
COMMAND_PREFIX = "legacy."
GOVERNANCE_FILES = (
    ("hooks/legacy_governance.py", ".github/hooks/legacy_governance.py"),
    ("agents/legacy-discovery.agent.md", ".github/agents/legacy-discovery.agent.md"),
)


def say(msg: str = "") -> None:
    print(msg, flush=True)


def run(cmd: list[str], cwd: Path | None = None) -> None:
    say("  > " + " ".join(cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def copy_path(src: Path, dst: Path) -> None:
    if src.is_dir():
        dst.mkdir(parents=True, exist_ok=True)
        for item in src.iterdir():
            copy_path(item, dst / item.name)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def backup_if_exists(target: Path, backup_root: Path, relative: str) -> None:
    src = target / relative
    if not src.exists():
        return
    dst = backup_root / relative
    say(f"Backup: {relative}")
    copy_path(src, dst)


def ensure_git_info_exclude(target: Path) -> None:
    """Keep skill-generated artifacts local without affecting tracked project files."""
    exclude = target / ".git" / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    existing = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
    marker_start = "# legacy-discovery-speckit-v4 local-only artifacts (managed)"
    marker_end = "# end legacy-discovery-speckit-v4 local-only artifacts"
    block = (
        f"{marker_start}\n"
        ".github/copilot-knowledge/\n"
        ".github/legacy-discovery/installation.json\n"
        f"{marker_end}\n"
    )
    if marker_start in existing and marker_end in existing:
        start = existing.index(marker_start)
        end = existing.index(marker_end) + len(marker_end)
        rebuilt = existing[:start] + block + existing[end:]
    else:
        prefix = existing if not existing or existing.endswith("\n") else existing + "\n"
        rebuilt = prefix + ("\n" if prefix and not prefix.endswith("\n\n") else "") + block
    exclude.write_text(rebuilt, encoding="utf-8", newline="\n")


def detect_uv() -> str | None:
    return shutil.which("uv")


def install_speckit(version: str) -> str:
    uv = detect_uv()
    package = f"specify-cli=={version}"
    if uv:
        say(f"\n[1/4] Instalando Spec Kit oficial {version} com uv...")
        run([uv, "tool", "install", "--force", package])
        return "uv"

    if sys.version_info < (3, 11):
        raise RuntimeError(
            "Python 3.11+ é necessário. Instale Python 3.11+ ou uv e execute novamente."
        )
    say(f"\n[1/4] uv não encontrado. Instalando Spec Kit oficial {version} com pip...")
    run([sys.executable, "-m", "pip", "install", "--user", "--upgrade", package])
    return "pip"


def init_speckit(target: Path, version: str, method: str | None) -> None:
    say("\n[2/4] Inicializando Spec Kit para GitHub Copilot no repositório legado...")
    args = ["init", "--here", "--force", "--non-interactive", "--integration", "copilot", "--ignore-agent-tools"]
    specify = shutil.which("specify")
    if specify:
        run([specify, *args], cwd=target)
        return
    uvx = shutil.which("uvx")
    if method == "uv" and uvx:
        run([uvx, "--from", f"specify-cli=={version}", "specify", *args], cwd=target)
        return
    run([sys.executable, "-m", "specify_cli", *args], cwd=target)


def archive_legacy_v1(target: Path, keep: bool) -> list[str]:
    found: list[str] = []
    skills_root = target / ".github" / "skills"
    archive_root = target / ".github" / "legacy-workflow-v1"
    for name in LEGACY_V1_SKILLS:
        src = skills_root / name
        if not src.exists():
            continue
        found.append(name)
        if keep:
            continue
        archive_root.mkdir(parents=True, exist_ok=True)
        dst = archive_root / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.move(str(src), str(dst))
        say(f"Arquivado workflow V1: .github/skills/{name} -> .github/legacy-workflow-v1/{name}")
    return found


def bundle_commands(bundle_root: Path) -> list[str]:
    prompts = bundle_root / "payload" / "legacy-discovery" / "prompts"
    return sorted(p.name for p in prompts.glob(f"{COMMAND_PREFIX}*.prompt.md"))


def install_commands(bundle_root: Path, target: Path) -> list[str]:
    """Copy only the bundle's legacy.*.prompt.md files; other prompts are never touched."""
    source = bundle_root / "payload" / "legacy-discovery" / "prompts"
    destination = target / ".github" / "prompts"
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    for name in bundle_commands(bundle_root):
        shutil.copy2(source / name, destination / name)
        installed.append(name)
    say(f"Comandos instalados: {len(installed)} (/legacy.*) em .github/prompts/")
    return installed


def install_governance(bundle_root: Path, target: Path) -> None:
    """Copy only the legacy-discovery hook and agent; other hooks/agents (e.g. AgentQA) are never touched."""
    payload = bundle_root / "payload" / "legacy-discovery"
    for source, destination in GOVERNANCE_FILES:
        dst = target / destination
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(payload / source, dst)
    say("Fechadura instalada: agente legacy-discovery + hook .github/hooks/legacy_governance.py")


def install_discovery(bundle_root: Path, target: Path, keep_legacy_v1: bool) -> None:
    say("\n[3/4] Instalando Legacy Discovery V" + LEGACY_DISCOVERY_VERSION + "...")
    payload = bundle_root / "payload" / "legacy-discovery"
    target_skills = target / ".github" / "skills"
    target_contracts = target / ".github" / "skill-contracts"
    target_skills.mkdir(parents=True, exist_ok=True)
    target_contracts.mkdir(parents=True, exist_ok=True)

    for skill in ACTIVE_SKILLS:
        src = payload / "skills" / skill
        dst = target_skills / skill
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        say(f"Skill instalada: {skill}")

    if target_contracts.exists():
        shutil.rmtree(target_contracts)
    shutil.copytree(payload / "skill-contracts", target_contracts)

    archive_legacy_v1(target, keep_legacy_v1)
    install_commands(bundle_root, target)
    install_governance(bundle_root, target)

    docs = target / ".github" / "legacy-discovery"
    docs.mkdir(parents=True, exist_ok=True)
    for name in ("README-ORIGINAL.md", "README-INSTALL.md", "MIGRATION-V2.md", "CHANGELOG-V2.md"):
        src = payload / name
        if src.exists():
            shutil.copy2(src, docs / name.replace("README-ORIGINAL.md", "README.md"))

    knowledge = target / ".github" / "copilot-knowledge"
    for name in (
        "projects", "decisions", "deep-dives", "proposals", "investigations",
        "impact-analyses", "handoffs", "fix-plans", "refinements"
    ):
        (knowledge / name).mkdir(parents=True, exist_ok=True)
    index = knowledge / "INDEX.md"
    if not index.exists():
        index.write_text(
            "# Índice de conhecimento — Repositório\n\n"
            "> Gerado/atualizado pelas Legacy Discovery Skills. Não use a existência deste arquivo como prova de cobertura.\n\n"
            "**Última atualização dos artefatos:** UNKNOWN\n",
            encoding="utf-8",
            newline="\n",
        )

    ensure_git_info_exclude(target)


def write_install_metadata(target: Path, version: str, commands: list[str] | None = None) -> None:
    meta_dir = target / ".github" / "legacy-discovery"
    meta_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "bundle": "legacy-discovery-speckit-all-in-one",
        "bundle_version": BUNDLE_VERSION,
        "spec_kit_version": version,
        "integration": "copilot",
        "legacy_discovery_version": LEGACY_DISCOVERY_VERSION,
        "installed_at_utc": datetime.now(timezone.utc).isoformat(),
        "active_skills": list(ACTIVE_SKILLS),
        "commands": ["/" + name[: -len(".prompt.md")] for name in (commands or [])],
    }
    (meta_dir / "installation.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Instala Spec Kit oficial + Legacy Discovery V{LEGACY_DISCOVERY_VERSION} em um repositório existente."
    )
    parser.add_argument("--target", default=".", help="Raiz do repositório legado")
    parser.add_argument("--spec-kit-version", default=DEFAULT_SPECKIT_VERSION)
    parser.add_argument("--skip-speckit-install", action="store_true")
    parser.add_argument("--skip-speckit-init", action="store_true")
    parser.add_argument("--keep-legacy-v1", action="store_true")
    args = parser.parse_args()

    bundle_root = Path(__file__).resolve().parent
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        parser.error(f"Repositório não encontrado: {target}")
    if not (target / ".git").exists():
        parser.error(
            f"{target} não parece ser a raiz de um repositório Git (.git não encontrado). "
            "Abra/indique a raiz correta."
        )

    say("=" * 72)
    say(" Legacy Discovery + Spec Kit — instalador único")
    say("=" * 72)
    say(f"Repositório: {target}")
    say(f"Spec Kit:    {args.spec_kit_version}")
    say("Integração:  GitHub Copilot")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = bundle_root / "backups" / f"{target.name}-{stamp}"
    backup_root.mkdir(parents=True, exist_ok=True)
    say(f"\nBackup preventivo: {backup_root}")
    for rel in (
        ".specify",
        ".github/prompts",
        ".github/skill-contracts",
        ".github/skills/analyze-legacy-solution",
        ".github/skills/investigate-legacy-bug",
        ".github/skills/analyze-change-impact",
        ".github/skills/prepare-speckit-context",
        ".github/skills/prepare-feature-branch",
        ".github/skills/refine-user-story",
        ".github/hooks/legacy_governance.py",
        ".github/agents/legacy-discovery.agent.md",
        ".github/skills/coordinate-fix",
        ".github/skills/execute-fix-plan",
        ".github/skills/run-solution-regression",
    ):
        backup_if_exists(target, backup_root, rel)

    method: str | None = None
    if not args.skip_speckit_install:
        method = install_speckit(args.spec_kit_version)
    else:
        say("\n[1/4] Instalação do CLI ignorada por opção.")

    if not args.skip_speckit_init:
        init_speckit(target, args.spec_kit_version, method)
    else:
        say("\n[2/4] Inicialização do Spec Kit ignorada por opção.")

    install_discovery(bundle_root, target, args.keep_legacy_v1)
    write_install_metadata(target, args.spec_kit_version, bundle_commands(bundle_root))

    say("\n[4/4] Validando estrutura instalada...")
    missing = []
    for skill in ACTIVE_SKILLS:
        if not (target / ".github" / "skills" / skill / "SKILL.md").exists():
            missing.append(skill)
    if missing:
        raise RuntimeError("Skills ausentes após instalação: " + ", ".join(missing))
    if not (target / ".github" / "skill-contracts" / "scripts" / "validate_artifacts.py").exists():
        raise RuntimeError("skill-contracts não foram instalados corretamente")
    missing_commands = [n for n in bundle_commands(bundle_root) if not (target / ".github" / "prompts" / n).exists()]
    if missing_commands:
        raise RuntimeError("Comandos ausentes após instalação: " + ", ".join(missing_commands))
    missing_governance = [dst for _, dst in GOVERNANCE_FILES if not (target / dst).exists()]
    if missing_governance:
        raise RuntimeError("Fechadura ausente após instalação: " + ", ".join(missing_governance))

    say("\nINSTALAÇÃO CONCLUÍDA.")
    say("\nAgora abra a raiz do repositório no VS Code e use o Copilot em Agent Mode.")
    say("Comandos das skills: digite /legacy.help no chat do Copilot.")
    say("Primeiro uso recomendado:")
    say("  1) /speckit.constitution")
    say("  2) Peça: 'Use analyze-legacy-solution para iniciar o mapa deste legado.'")
    say("  3) Para uma US do PM: /legacy.story <história literal>")
    say("     Responda com /legacy.answer; /legacy.approve mostra o comando de aprovação que só você roda")
    say("  4) Acompanhe com /legacy.status")
    say("  5) Com o REFINEMENT em READY_FOR_SPECKIT: /legacy.branch <descrição>")
    say("  6) Depois execute /speckit.specify")
    say("  7) Para arquivar dados locais da skill: python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean")
    say("\nRevise o resultado com: git status / git diff")
    say(f"Backup: {backup_root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        say(f"\nERRO: comando falhou com código {exc.returncode}.")
        raise SystemExit(exc.returncode)
    except Exception as exc:
        say(f"\nERRO: {exc}")
        raise SystemExit(1)
