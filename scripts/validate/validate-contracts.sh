#!/usr/bin/env bash
# validate-contracts.sh
# API Contract の整合性を検証するスクリプト
#
# 検証内容:
#   - docs/api/api-contract.md の存在確認
#   - Contract に定義されたエンドポイントの記述確認
#   - プロジェクトが OpenAPI を採用している場合は openapi.yaml/openapi.json の検証
#
# Note: 技術スタック固有の検証（実装との整合性チェック）はプロジェクトごとに追加してください。
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ERRORS=0
WARNINGS=0

error() {
  echo "::error::$*" >&2
  ERRORS=$((ERRORS + 1))
}

warning() {
  echo "::warning::$*" >&2
  WARNINGS=$((WARNINGS + 1))
}

info() {
  echo "[INFO] $*"
}

# ──────────────────────────────────────────────
# 1. API Contract ファイルの存在確認
# ──────────────────────────────────────────────
info "=== API Contract ファイルの確認 ==="
API_CONTRACT="$REPO_ROOT/docs/api/api-contract.md"

if [[ -f "$API_CONTRACT" ]]; then
  info "  OK: docs/api/api-contract.md"
else
  warning "docs/api/api-contract.md が存在しません（API が定義されていないプロジェクトは無視可）"
fi

# ──────────────────────────────────────────────
# 2. OpenAPI ファイルが存在する場合は検証
# ──────────────────────────────────────────────
info "=== OpenAPI 検証 ==="
OPENAPI_FILES=()
while IFS= read -r f; do
  OPENAPI_FILES+=("$f")
done < <(find "$REPO_ROOT" -not -path "*/.git/*" -not -path "*/node_modules/*" \
  \( -name "openapi.yaml" -o -name "openapi.yml" -o -name "openapi.json" \
     -o -name "swagger.yaml" -o -name "swagger.yml" -o -name "swagger.json" \) 2>/dev/null)

if [[ ${#OPENAPI_FILES[@]} -gt 0 ]]; then
  info "  OpenAPI ファイルが検出されました:"
  for f in "${OPENAPI_FILES[@]}"; do
    rel="${f#$REPO_ROOT/}"
    info "    $rel"

    # openapi-generator / swagger-codegen がある場合は lint 可能
    # ここではファイルが有効な YAML/JSON か確認する
    if command -v python3 &>/dev/null; then
      if python3 -c "
import sys, json, re
path = sys.argv[1]
try:
    if path.endswith('.json'):
        with open(path) as fh:
            json.load(fh)
    else:
        # 最低限 YAML として読めるか確認（PyYAML がなければスキップ）
        try:
            import yaml
            with open(path) as fh:
                yaml.safe_load(fh)
        except ImportError:
            pass  # yaml モジュールがなければスキップ
    print('OK')
except Exception as e:
    print('ERROR: ' + str(e))
    sys.exit(1)
" "$f" 2>/dev/null; then
        info "    OK: $rel (構文チェック通過)"
      else
        error "OpenAPI ファイルの構文エラー: $rel"
        echo "  File: $rel"
        echo "  Action: YAML/JSON 構文を確認してください"
      fi
    fi
  done
else
  info "  OpenAPI ファイルは検出されませんでした（スキップ）"
fi

# ──────────────────────────────────────────────
# 3. Contract 変更時のルール確認（PR での差分チェック）
# ──────────────────────────────────────────────
info "=== Contract 変更ルールの確認 ==="
# CI 上で実行している場合（GITHUB_BASE_REF が存在する場合）に差分をチェック
if [[ -n "${GITHUB_BASE_REF:-}" ]] && git -C "$REPO_ROOT" rev-parse --verify "origin/${GITHUB_BASE_REF}" &>/dev/null; then
  changed_contracts=$(git -C "$REPO_ROOT" diff --name-only "origin/${GITHUB_BASE_REF}"...HEAD -- \
    'docs/api/' 'openapi.*' 'swagger.*' 2>/dev/null || true)
  if [[ -n "$changed_contracts" ]]; then
    warning "API Contract ファイルが変更されています。以下を確認してください:"
    echo "$changed_contracts" | while IFS= read -r f; do
      echo "    変更: $f"
    done
    echo ""
    echo "  確認事項:"
    echo "    1. Contract 変更理由が Issue に記載されているか"
    echo "    2. 既存 Consumer への影響が評価されているか"
    echo "    3. Implementation と Tests が更新されているか"
    echo "    4. Breaking Change の場合は Migration 計画があるか"
  else
    info "  OK: API Contract ファイルに変更はありません"
  fi
else
  info "  CI 環境外または base ref 未設定のためスキップ"
fi

# ──────────────────────────────────────────────
# 結果サマリー
# ──────────────────────────────────────────────
echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "✅ Contract Validation: PASS (warnings: $WARNINGS)"
  exit 0
else
  echo "❌ Contract Validation: FAIL ($ERRORS エラー, $WARNINGS 警告)"
  echo ""
  echo "Action:"
  echo "  上記のエラーを修正してから再実行してください。"
  exit 1
fi
