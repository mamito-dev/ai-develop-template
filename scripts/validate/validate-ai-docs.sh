#!/usr/bin/env bash
# validate-ai-docs.sh
# AI Documentation Validation を実行するシェルスクリプトラッパー
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

VALIDATE_PY="$REPO_ROOT/scripts/ai-docs/validate.py"

if [[ ! -f "$VALIDATE_PY" ]]; then
  echo "ERROR: validate.py が見つかりません: $VALIDATE_PY" >&2
  exit 1
fi

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
  echo "ERROR: Python が見つかりません。Python 3.8 以上をインストールしてください。" >&2
  exit 1
fi

PYTHON=$(command -v python3 2>/dev/null || command -v python)

exec "$PYTHON" "$VALIDATE_PY" "$@"
