#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY=""
if command -v python3 >/dev/null 2>&1; then PY=python3; elif command -v python >/dev/null 2>&1; then PY=python; fi
if [[ -z "$PY" ]]; then
  echo "ERRO: Python 3.11+ não encontrado."
  exit 1
fi
exec "$PY" "$SCRIPT_DIR/install.py" --target "$TARGET"
