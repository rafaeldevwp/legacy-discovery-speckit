#!/usr/bin/env python3
"""Build a clean, reproducible release of this bundle.

1. refuses forbidden content (backups/, installation leftovers, compiled files outside __pycache__);
2. removes __pycache__ folders;
3. regenerates SHA256SUMS.txt for every file;
4. writes <bundle-folder>.zip next to the bundle (or --out-dir) with sorted entries and fixed timestamps.

Usage (from anywhere):  python tools/build_release.py [--out-dir DIR] [--check] [--verify-zip ZIP]
  --check           only verifies: no forbidden content and SHA256SUMS.txt matches every file. Writes nothing.
  --verify-zip ZIP  verifies that ZIP holds exactly this folder: same files, same order, same bytes.
                    (Compressed bytes may differ between OSes because zlib differs; the content may not.)
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

BUNDLE = Path(__file__).resolve().parents[1]
SUMS = "SHA256SUMS.txt"
FORBIDDEN_DIRS = {"backups", ".git", ".github", "node_modules", ".venv", "venv"}
FORBIDDEN_SUFFIXES = {".pyc", ".pyo", ".log", ".zip"}


def _key(path: Path) -> str:
    """Case-sensitive POSIX order: identical on Windows and Linux (Path sorting is not)."""
    return path.relative_to(BUNDLE).as_posix()


def release_files() -> list[Path]:
    return sorted(
        (p for p in BUNDLE.rglob("*")
         if p.is_file() and "__pycache__" not in p.relative_to(BUNDLE).parts and p.name != SUMS),
        key=_key,
    )


def forbidden() -> list[str]:
    problems = []
    for path in BUNDLE.rglob("*"):
        relative = path.relative_to(BUNDLE)
        if "__pycache__" in relative.parts:
            continue
        if path.is_dir() and path.name in FORBIDDEN_DIRS:
            problems.append(f"pasta proibida no pacote: {relative.as_posix()}/")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(f"arquivo proibido no pacote: {relative.as_posix()}")
        if path.is_file() and path.name == "installation.json":
            problems.append(f"metadado de instalação no pacote: {relative.as_posix()}")
    return problems


def sums_text() -> str:
    lines = []
    for path in release_files():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  ./{path.relative_to(BUNDLE).as_posix()}")
    return "\n".join(lines) + "\n"


def check() -> list[str]:
    problems = forbidden()
    sums_file = BUNDLE / SUMS
    if not sums_file.exists():
        return problems + [f"{SUMS} ausente"]
    listed = {}
    for line in sums_file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            listed[name.strip().removeprefix("./")] = digest
    actual = {p.relative_to(BUNDLE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in release_files()}
    for name in sorted(set(actual) - set(listed)):
        problems.append(f"arquivo fora do {SUMS}: {name}")
    for name in sorted(set(listed) - set(actual)):
        problems.append(f"{SUMS} lista arquivo inexistente: {name}")
    for name in sorted(set(actual) & set(listed)):
        if actual[name] != listed[name]:
            problems.append(f"checksum não confere: {name}")
    return problems


def verify_zip(zip_path: Path) -> list[str]:
    expected = [(f"{BUNDLE.name}/{_key(p)}", p) for p in release_files() + [BUNDLE / SUMS]]
    expected.sort(key=lambda item: item[0])
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        problems = []
        if names != [name for name, _ in expected]:
            missing = sorted(set(n for n, _ in expected) - set(names))
            extra = sorted(set(names) - set(n for n, _ in expected))
            problems.append(f"entradas do zip não são os arquivos da pasta na mesma ordem "
                            f"(faltando: {missing[:5]}, sobrando: {extra[:5]})")
            return problems
        for name, path in expected:
            if archive.read(name) != path.read_bytes():
                problems.append(f"conteúdo diferente no zip: {name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=BUNDLE.parent)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-zip", type=Path)
    args = parser.parse_args()
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    if args.verify_zip:
        problems = verify_zip(args.verify_zip)
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print("zip verificado: mesmos arquivos, mesma ordem, mesmos bytes" if not problems else "zip diverge da pasta")
        return 1 if problems else 0

    if args.check:
        problems = check()
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print("release check passed" if not problems else f"release check failed: {len(problems)} problem(s)")
        return 1 if problems else 0

    problems = forbidden()
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    for cache in list(BUNDLE.rglob("__pycache__")):
        shutil.rmtree(cache, ignore_errors=True)
    (BUNDLE / SUMS).write_text(sums_text(), encoding="utf-8", newline="\n")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = args.out_dir / f"{BUNDLE.name}.zip"
    files = release_files() + [BUNDLE / SUMS]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(files, key=_key):
            info = zipfile.ZipInfo(f"{BUNDLE.name}/{path.relative_to(BUNDLE).as_posix()}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    print(f"{SUMS}: {len(files) - 1} arquivo(s)")
    print(f"zip: {zip_path} ({zip_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
