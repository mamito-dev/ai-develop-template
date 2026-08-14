#!/usr/bin/env bash
# validate.sh
# ローカルで CI 相当の Validation を実行するエントリポイント
#
# Usage:
#   ./scripts/validate.sh               # 全 Validation を実行
#   ./scripts/validate.sh repository    # Repository 構造のみ
#   ./scripts/validate.sh docs          # Documentation のみ
#   ./scripts/validate.sh contracts     # API Contract のみ
#   ./scripts/validate.sh all           # 全 Validation（デフォルトと同じ）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET="${1:-all}"
TOTAL_ERRORS=0

run_validate() {
  local name="$1"
  local script="$SCRIPT_DIR/validate/$2"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "▶ $name"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  if bash "$script"; then
    echo "✅ $name: PASS"
  else
    echo "❌ $name: FAIL"
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
  fi
}

echo "========================================================"
echo "  Local Validation"
echo "  Repository: $REPO_ROOT"
echo "  Target: $TARGET"
echo "========================================================"

case "$TARGET" in
  repository)
    run_validate "Repository Validation" "validate-repository.sh"
    ;;
  docs)
    run_validate "Documentation Validation" "validate-docs.sh"
    ;;
  contracts)
    run_validate "Contract Validation" "validate-contracts.sh"
    ;;
  all | *)
    run_validate "Repository Validation"    "validate-repository.sh"
    run_validate "Documentation Validation" "validate-docs.sh"
    run_validate "Contract Validation"      "validate-contracts.sh"

    # ──────────────────────────────────────────────────────────
    # プロジェクト固有の Validation をここに追加してください
    # 例:
    #   run_validate "Format Check"  "validate-format.sh"
    #   run_validate "Lint"          "validate-lint.sh"
    #   run_validate "Unit Test"     "validate-test.sh"
    #   run_validate "Build"         "validate-build.sh"
    # ──────────────────────────────────────────────────────────
    ;;
esac

echo ""
echo "========================================================"
if [[ $TOTAL_ERRORS -eq 0 ]]; then
  echo "✅ All Validations: PASS"
  exit 0
else
  echo "❌ Validations: FAIL ($TOTAL_ERRORS 件のエラー)"
  echo ""
  echo "CI と同じ Validation をローカルで実行することで、"
  echo "Push 前に問題を検出できます。"
  echo ""
  echo "上記エラーを修正してから再実行してください:"
  echo "  ./scripts/validate.sh"
  exit 1
fi
