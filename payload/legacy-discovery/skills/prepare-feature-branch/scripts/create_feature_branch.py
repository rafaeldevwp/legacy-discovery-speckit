\
#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


def run(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], check=check)


def out(*args: str) -> str:
    return git(*args).stdout.strip()


def fail(code: str, message: str, **extra: object) -> int:
    payload = {"status": code, "message": message, **extra}
    print(json.dumps(payload, ensure_ascii=False))
    return 2


def normalize_slug(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value


def ref_exists(ref: str) -> bool:
    return git("show-ref", "--verify", "--quiet", ref, check=False).returncode == 0


def main() -> int:
    p = argparse.ArgumentParser(description="Cria branch feature/mmYYYY/slug com baseline segura em main.")
    p.add_argument("--slug", required=True, help="Descrição curta, por exemplo tratar-timeout-pbh")
    p.add_argument("--base", default="main", help="Branch base; padrão e política oficial deste bundle: main")
    args = p.parse_args()

    slug = normalize_slug(args.slug)
    if not slug or len(slug) < 3:
        return fail("INVALID_SLUG", "Slug vazio ou curto demais após normalização.")
    if args.base != "main":
        return fail("INVALID_BASE", "Este workflow exige base main.", base=args.base)

    if git("rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
        return fail("NOT_A_GIT_REPOSITORY", "Execute na raiz ou dentro do repositório Git.")

    dirty = out("status", "--porcelain")
    if dirty:
        return fail("WORKTREE_DIRTY", "Existem alterações locais. Faça commit/stash manual antes de continuar.")

    origin = git("remote", "get-url", "origin", check=False)
    if origin.returncode != 0 or not origin.stdout.strip():
        return fail("ORIGIN_MISSING", "Remote origin não encontrado.")
    origin_url = origin.stdout.strip()

    fetch = git("fetch", "origin", check=False)
    if fetch.returncode != 0:
        return fail("FETCH_FAILED", fetch.stderr.strip() or "git fetch origin falhou.", origin_url=origin_url)

    if not ref_exists("refs/heads/main"):
        return fail("LOCAL_MAIN_MISSING", "Branch local main não existe.")
    if not ref_exists("refs/remotes/origin/main"):
        return fail("REMOTE_MAIN_MISSING", "origin/main não existe.")

    sw = git("switch", "main", check=False)
    if sw.returncode != 0:
        return fail("SWITCH_MAIN_FAILED", sw.stderr.strip() or "Não foi possível mudar para main.")

    pull = git("pull", "--ff-only", "origin", "main", check=False)
    if pull.returncode != 0:
        return fail("MAIN_DIVERGED", pull.stderr.strip() or "main não pôde ser atualizada por fast-forward.")

    local_main = out("rev-parse", "main")
    remote_main = out("rev-parse", "origin/main")
    if local_main != remote_main:
        return fail("MAIN_NOT_SYNCED", "main local e origin/main divergem após pull --ff-only.", local=local_main, remote=remote_main)

    branch = f"feature/{datetime.now().strftime('%m%Y')}/{slug}"
    if ref_exists(f"refs/heads/{branch}") or ref_exists(f"refs/remotes/origin/{branch}"):
        return fail("BRANCH_EXISTS", "A branch já existe local ou remotamente.", branch=branch)

    create = git("switch", "-c", branch, "main", check=False)
    if create.returncode != 0:
        return fail("BRANCH_CREATE_FAILED", create.stderr.strip() or "Falha ao criar branch.", branch=branch)

    payload = {
        "status": "BRANCH_READY",
        "branch": branch,
        "base_branch": "main",
        "base_commit": local_main,
        "origin_url": origin_url,
    }
    print(json.dumps(payload, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
