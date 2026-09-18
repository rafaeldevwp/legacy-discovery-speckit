#!/usr/bin/env python3
"""PreToolUse governance hook for the legacy-discovery agent ("a fechadura").

Same protocol as the AgentQA hook: reads the tool call as JSON on stdin, prints a hookSpecificOutput
decision and exits 0 (allow) or 2 (deny). Fails closed.

Design rule, learned from AgentQA v3: deny only clear violations. A hook that blocks legitimate work gets
switched off, and then all governance is gone. Discovery keeps full freedom to read, search, build and test.

Denied:
  1. writes outside the skill trails (.github/copilot-knowledge/ and test projects);
  2. writes to Spec Kit (.specify/, specs/), to the skills, contracts, hook, agent, commands and INDEX.md;
  3. an agent recording human approval (READY_FOR_SPECKIT on a refinement, reviewed_by, approval_digest);
  4. running approve_refinement.py (approval is a human act) or archive-and-clean (deletion);
  5. destructive or publishing Git commands (push, reset, stash, rebase, merge, commit, add, ...);
  6. shell writes/deletes aimed at protected or skill paths (use the edit tools, which this hook can inspect);
  7. uninspectable execution (-EncodedCommand).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote

PROTECTED_PATHS = [
    (r"(^|/)\.specify(/|$)", "Spec Kit (.specify/) pertence ao Spec Kit"),
    (r"(^|/)specs(/|$)", "Spec Kit (specs/) pertence ao Spec Kit"),
    (r"(^|/)\.github/skills(/|$)", "as skills não se reescrevem"),
    (r"(^|/)\.github/skill-contracts(/|$)", "contratos e validador não podem ser alterados pelo agente"),
    (r"(^|/)\.github/hooks/legacy_governance\.py$", "a fechadura não pode ser alterada pelo agente"),
    (r"(^|/)\.github/agents/legacy-discovery\.agent\.md$", "o agente não pode alterar a própria configuração"),
    (r"(^|/)\.github/prompts/legacy\.[^/]+\.prompt\.md$", "os comandos /legacy.* não podem ser alterados pelo agente"),
    (r"(^|/)\.github/legacy-discovery(/|$)", "metadados da instalação"),
    (r"(^|/)\.github/copilot-knowledge/index\.md$", "INDEX.md só é escrito por sync_index.py"),
]
ALLOWED_WRITE_PATHS = [
    r"(^|/)\.github/copilot-knowledge/",
    r"(^|/)(tests?|[^/]*[._-]tests?|[^/]*tests)/",
    r"(^|/)[^/]*tests?\.(cs|vb|fs)$",
]
SKILL_TRAILS = r"\.github/(copilot-knowledge|skills|skill-contracts|hooks|agents|prompts|legacy-discovery)|\.specify|(^|[\s\"'/])specs/"

WRITE_TOOLS = {
    "create_file", "apply_patch", "edit_file", "editfile", "insert_edit_into_file", "replace_string_in_file",
    "multi_replace_string_in_file", "str_replace_editor", "str_replace", "apply_diff", "write_file", "writefile",
    "update_file", "modify_file", "save_file", "patch_file", "create_directory", "delete_file", "remove_file",
    "rename_file", "move_file", "edit_notebook_file", "create_new_jupyter_notebook",
}
WRITE_NAME_HINT = re.compile(r"(edit|write|patch|insert|replace|create|delete|remove|rename|move).*(file|notebook|directory)"
                             r"|(file|notebook|directory).*(edit|write|patch|insert|replace|create|delete|remove|rename|move)")
TERMINAL_TOOLS = {"run_in_terminal", "execute", "runinterminal", "terminal", "run_command", "shell", "bash", "powershell"}
NEW_CONTENT_KEYS = {"content", "newcontent", "new_string", "newstring", "newtext", "new_text", "text", "filecontents",
                    "file_contents", "code", "replacement", "insert", "patch", "diff"}
PATH_KEYS = {"path", "file", "files", "uri", "filename", "file_name", "target", "targetfile", "target_file",
             "destination", "directory", "dirpath", "dir_path"}

GIT_DENIED_VERBS = {"push", "reset", "stash", "rebase", "merge", "clean", "commit", "add", "rm", "restore",
                    "cherry-pick", "revert", "filter-branch", "update-ref", "switch", "checkout", "am", "apply"}
SHELL_WRITE = re.compile(
    r"\b(set-content|add-content|out-file|new-item|remove-item|copy-item|move-item|rename-item|clear-content|"
    r"rm|del|erase|rmdir|rd|mv|cp|move|copy|ren|tee|truncate)\b|>>?|\bsed\s+-i\b|\bopen\([^)]*['\"][wax+]|write_text|write_bytes|"
    r"shutil\.|os\.remove|unlink\("
)
REDIRECT_NOISE = re.compile(r"\d?>\s*&\s*\d|\d?>\s*(\$null|/dev/null|nul)\b|-gt\b|->|=>")


def _git_verb(segment: str) -> tuple[str, list[str]]:
    """First non-option token after `git`, skipping global options like -C <dir> and -c <k=v>."""
    tokens = segment.split()
    try:
        index = next(i for i, tok in enumerate(tokens) if re.fullmatch(r"[\"']?git(\.exe)?[\"']?", tok))
    except StopIteration:
        return "", []
    rest = tokens[index + 1:]
    while rest and rest[0].startswith("-"):
        takes_value = rest[0] in {"-c", "-C", "--git-dir", "--work-tree", "--namespace"}
        rest = rest[2:] if takes_value else rest[1:]
    return (rest[0] if rest else ""), rest[1:]


def allow() -> tuple[str, str]:
    return "allow", "legacy governance check passed"


def deny(reason: str) -> tuple[str, str]:
    return "deny", reason


def _walk(value, key: str = ""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from _walk(v, k)
    elif isinstance(value, list):
        for item in value:
            yield from _walk(item, key)
    elif isinstance(value, str):
        yield key, value


def _norm_path(value: str) -> str:
    value = unquote(value.strip())
    value = re.sub(r"^file:/+", "/", value)
    return value.replace("\\", "/").lower()


def _first(payload: dict, names: tuple[str, ...]) -> str:
    for key, value in _walk(payload):
        if key.lower() in names and value:
            return value
    return ""


def _added_lines(text: str) -> str:
    if "*** begin patch" in text.lower() or re.search(r"(?m)^@@", text):
        return "\n".join(line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++"))
    return text


def _patch_paths(text: str) -> list[str]:
    return re.findall(r"(?im)^\*\*\*\s+(?:add|update|delete)\s+file:\s*(.+?)\s*$", text)


def decide(raw: str) -> tuple[str, str]:
    if not raw.strip():
        return allow()
    payload = json.loads(raw)
    tool = _first(payload, ("toolname", "tool_name", "name")).lower()
    pairs = list(_walk(payload))

    command = _first(payload, ("command", "cmd", "commandline", "script"))
    new_content = "\n".join(_added_lines(v) for k, v in pairs
                            if k.lower() in NEW_CONTENT_KEYS or "*** begin patch" in v.lower())
    paths = [_norm_path(v) for k, v in pairs
             if (k.lower() in PATH_KEYS or k.lower().endswith("path")) and not k.lower().startswith("old") and v.strip()]
    for _, value in pairs:
        paths.extend(_norm_path(p) for p in _patch_paths(value))

    is_terminal = tool in TERMINAL_TOOLS or (bool(command) and not new_content)
    is_write = tool in WRITE_TOOLS or bool(WRITE_NAME_HINT.search(tool)) or (bool(new_content) and bool(paths) and not is_terminal)

    if is_write:
        if not paths:
            return deny("Escrita sem arquivo identificável; a fechadura falha fechada")
        for path in paths:
            for pattern, why in PROTECTED_PATHS:
                if re.search(pattern, path):
                    return deny(f"Escrita bloqueada em {path}: {why}")
            if not any(re.search(pattern, path) for pattern in ALLOWED_WRITE_PATHS):
                return deny(f"Escrita bloqueada em {path}: as skills só escrevem em .github/copilot-knowledge/ e em projetos de teste")
        if re.search(r"(?im)^\s*reviewed_by\s*:\s*(?!null\b)\S", new_content):
            return deny("Só o humano registra reviewed_by, via approve_refinement.py no próprio terminal")
        if re.search(r"(?im)^\s*approval_digest\s*:\s*(?!null\b)\S", new_content):
            return deny("approval_digest só é gravado por approve_refinement.py, executado pelo humano")
        if any("/refinements/" in p for p in paths) and re.search(r"(?im)^\s*status\s*:\s*ready_for_speckit\b", new_content):
            return deny("Refinamento só vira READY_FOR_SPECKIT pela aprovação humana (approve_refinement.py); use READY_FOR_REVIEW")
        return allow()

    if is_terminal and command:
        text = command.replace("\\", "/").lower()
        if "approve_refinement.py" in text:
            return deny("Aprovação é ato humano: rode você mesmo approve_refinement.py no seu terminal")
        if "archive_skill_artifacts.py" in text and "archive-and-clean" in text:
            return deny("Apagar artefatos é ato humano: rode você mesmo o archive-and-clean")
        if re.search(r"\b(powershell|pwsh)(\.exe)?\b", text) and re.search(r"\s-(e|ec|enc|encodedcommand)\s", text):
            return deny("Execução codificada não pode ser inspecionada pela fechadura")
        for segment in re.split(r"[;&|\n]+", command):
            verb, args = _git_verb(segment)
            lowered = [a.lower() for a in args]
            if verb.lower() in GIT_DENIED_VERBS or (verb.lower() == "branch" and any(a in {"-d", "-D".lower(), "-m", "--delete", "--move", "-f", "--force"} for a in lowered)) \
                    or (verb.lower() == "tag" and any(a in {"-d", "--delete"} for a in lowered)):
                return deny(f"Comando Git bloqueado (git {verb}): as skills não publicam nem reescrevem histórico; "
                            "a branch é criada só pelo create_feature_branch.py")
        cleaned = REDIRECT_NOISE.sub(" ", text)
        if SHELL_WRITE.search(cleaned) and re.search(SKILL_TRAILS, cleaned):
            return deny("Escrita/remoção via terminal em trilhas protegidas; use as ferramentas de edição, que a fechadura inspeciona")
    return allow()


def _log(decision: str, reason: str, tool: str) -> None:
    try:
        knowledge = Path(".github/copilot-knowledge")
        if not knowledge.is_dir():
            return
        folder = knowledge / "governance-log"
        folder.mkdir(exist_ok=True)
        line = f"[{datetime.now().isoformat(timespec='seconds')}] tool={tool} decision={decision} reason={reason}\n"
        with (folder / f"legacy-governance-{datetime.now():%Y-%m-%d}.log").open("a", encoding="utf-8") as handle:
            handle.write(line)
    except OSError:
        pass


def main() -> int:
    raw = sys.stdin.buffer.read().decode("utf-8", "replace")
    tool = ""
    try:
        try:
            tool = _first(json.loads(raw), ("toolname", "tool_name", "name")) if raw.strip() else ""
        except ValueError:
            tool = ""
        decision, reason = decide(raw)
    except Exception as exc:  # fail closed
        decision, reason = "deny", f"Legacy governance hook failed closed: {exc}"
    if decision == "deny":
        _log(decision, reason, tool)
    output = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": decision,
                                     "permissionDecisionReason": reason}}
    sys.stdout.write(json.dumps(output, ensure_ascii=True))
    return 0 if decision == "allow" else 2


if __name__ == "__main__":
    raise SystemExit(main())
