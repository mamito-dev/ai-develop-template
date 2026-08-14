#!/usr/bin/env bash
# validate-repository.sh
# Repositoryの基本構造（必須ファイル・ディレクトリ・禁止ファイル）を検証するスクリプト
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ERRORS=0

error() {
  echo "::error::$*" >&2
  ERRORS=$((ERRORS + 1))
}

info() {
  echo "[INFO] $*"
}

# ──────────────────────────────────────────────
# 1. 必須ファイルの存在確認
# ──────────────────────────────────────────────
REQUIRED_FILES=(
  "AGENTS.md"
  ".github/copilot-instructions.md"
  "README.md"
  ".gitignore"
)

info "=== 必須ファイルの検証 ==="
for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "$REPO_ROOT/$f" ]]; then
    info "  OK: $f"
  else
    error "必須ファイルが存在しません: $f"
  fi
done

# ──────────────────────────────────────────────
# 2. 必須ディレクトリの存在確認
# ──────────────────────────────────────────────
REQUIRED_DIRS=(
  ".github/instructions"
  "docs"
  "docs/development"
  "docs/architecture"
  "scripts/validate"
)

info "=== 必須ディレクトリの検証 ==="
for d in "${REQUIRED_DIRS[@]}"; do
  if [[ -d "$REPO_ROOT/$d" ]]; then
    info "  OK: $d"
  else
    error "必須ディレクトリが存在しません: $d"
  fi
done

# ──────────────────────────────────────────────
# 3. 禁止ファイルの検出（Secret候補ファイル）
# ──────────────────────────────────────────────
FORBIDDEN_PATTERNS=(
  ".env"
  ".env.local"
  ".env.production"
  ".env.staging"
  "*.pem"
  "*.key"
  "credentials.*"
  "secrets.*"
  "secret.*"
)

info "=== 禁止ファイルの検出 ==="
FORBIDDEN_ERRORS=0
for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
  # find で禁止パターンのファイルを検索（.git は除外）
  while IFS= read -r found; do
    error "禁止ファイルが検出されました: $found"
    FORBIDDEN_ERRORS=$((FORBIDDEN_ERRORS + 1))
  done < <(find "$REPO_ROOT" -not -path "*/.git/*" -name "$pattern" 2>/dev/null)
done
if [[ $FORBIDDEN_ERRORS -eq 0 ]]; then
  info "  OK: 禁止ファイルは検出されませんでした"
fi

# ──────────────────────────────────────────────
# 4. AI Instructions ファイルの存在確認
# ──────────────────────────────────────────────
info "=== AI Instructions の検証 ==="
INSTRUCTIONS_DIR="$REPO_ROOT/.github/instructions"
if [[ -d "$INSTRUCTIONS_DIR" ]]; then
  md_count=$(find "$INSTRUCTIONS_DIR" -name "*.md" -not -name ".gitkeep" 2>/dev/null | wc -l)
  if [[ "$md_count" -gt 0 ]]; then
    info "  OK: $md_count 件の instructions ファイルが存在します"
  else
    error ".github/instructions/ に *.md ファイルが存在しません"
  fi
else
  error ".github/instructions/ ディレクトリが存在しません"
fi

# ──────────────────────────────────────────────
# 結果サマリー
# ──────────────────────────────────────────────
echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "✅ Repository Validation: PASS"
  exit 0
else
  echo "❌ Repository Validation: FAIL ($ERRORS エラー)"
  echo ""
  echo "Action:"
  echo "  上記のエラーを修正してから再実行してください。"
  exit 1
fi
