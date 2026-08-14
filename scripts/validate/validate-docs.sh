#!/usr/bin/env bash
# validate-docs.sh
# Markdown の Syntax・Broken Link・必須ドキュメント構造を検証するスクリプト
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
# 1. docs/ ディレクトリ構造の検証
# ──────────────────────────────────────────────
info "=== docs/ 構造の検証 ==="
REQUIRED_DOC_DIRS=(
  "docs/development"
)
for d in "${REQUIRED_DOC_DIRS[@]}"; do
  if [[ -d "$REPO_ROOT/$d" ]]; then
    info "  OK: $d"
  else
    error "必須 docs ディレクトリが存在しません: $d"
  fi
done

# ci.md の存在確認
if [[ -f "$REPO_ROOT/docs/development/ci.md" ]]; then
  info "  OK: docs/development/ci.md"
else
  error "docs/development/ci.md が存在しません"
fi

# ──────────────────────────────────────────────
# 2. Markdown の Code Fence クローズ検証
# ──────────────────────────────────────────────
info "=== Markdown Code Fence 検証 ==="
while IFS= read -r md_file; do
  fence_opens=0
  line_num=0
  while IFS= read -r line; do
    line_num=$((line_num + 1))
    if echo "$line" | grep -qE '^\s*```'; then
      fence_opens=$((fence_opens + 1))
    fi
  done < "$md_file"

  if (( fence_opens % 2 != 0 )); then
    rel="${md_file#$REPO_ROOT/}"
    error "Code Fence が閉じられていません: $rel"
    echo "  File: $rel"
    echo "  Action: \`\`\` の対応を確認してください"
  fi
done < <(find "$REPO_ROOT" -not -path "*/.git/*" -name "*.md" 2>/dev/null)

if [[ $ERRORS -eq 0 ]]; then
  info "  OK: Code Fence は正常です"
fi

# ──────────────────────────────────────────────
# 3. Broken Link 検証（Markdownの相対リンク）
# ──────────────────────────────────────────────
info "=== Broken Link 検証 ==="
broken_links=0
while IFS= read -r md_file; do
  md_dir="$(dirname "$md_file")"
  # [text](path) 形式の相対リンクを抽出（http/https/mailto は除外）
  while IFS= read -r link; do
    # アンカー部分を除去
    path_part="${link%%#*}"
    [[ -z "$path_part" ]] && continue
    # 絶対URLはスキップ
    [[ "$path_part" == http://* || "$path_part" == https://* || "$path_part" == mailto:* ]] && continue

    # リンクが指すファイルを解決
    if [[ "$path_part" == /* ]]; then
      target="$REPO_ROOT$path_part"
    else
      target="$md_dir/$path_part"
    fi

    if [[ ! -e "$target" ]]; then
      rel="${md_file#$REPO_ROOT/}"
      error "Broken Link: $rel -> $link"
      echo "  File: $rel"
      echo "  Link: $link"
      echo "  Action: リンク先ファイルが存在するか確認してください"
      broken_links=$((broken_links + 1))
    fi
  done < <(grep -oE '\]\([^)]+\)' "$md_file" 2>/dev/null | sed 's/^](//; s/)$//')
done < <(find "$REPO_ROOT" -not -path "*/.git/*" -name "*.md" 2>/dev/null)

if [[ $broken_links -eq 0 ]]; then
  info "  OK: Broken Link は検出されませんでした"
fi

# ──────────────────────────────────────────────
# 4. 必須ドキュメントの内容チェック（TODO のみでないか）
# ──────────────────────────────────────────────
info "=== 必須ドキュメント内容の検証 ==="
CRITICAL_DOCS=(
  "docs/development/ci.md"
)
for doc in "${CRITICAL_DOCS[@]}"; do
  if [[ -f "$REPO_ROOT/$doc" ]]; then
    # ファイルが TODO だけでないか確認
    non_todo_lines=$(grep -v '^\s*$' "$REPO_ROOT/$doc" | grep -Ecv '^#|TODO' || true)
    if [[ "$non_todo_lines" -lt 3 ]]; then
      warning "$doc の内容が不足しています（TODO のみの可能性があります）"
    else
      info "  OK: $doc"
    fi
  fi
done

# ──────────────────────────────────────────────
# 結果サマリー
# ──────────────────────────────────────────────
echo ""
if [[ $ERRORS -eq 0 ]]; then
  echo "✅ Documentation Validation: PASS (warnings: $WARNINGS)"
  exit 0
else
  echo "❌ Documentation Validation: FAIL ($ERRORS エラー, $WARNINGS 警告)"
  echo ""
  echo "Action:"
  echo "  上記のエラーを修正してから再実行してください。"
  exit 1
fi
