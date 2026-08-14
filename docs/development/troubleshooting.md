# Troubleshooting

## Problem: バリデーションスクリプトが Permission Denied になる

### Symptom

```
bash: ./scripts/validate.sh: Permission denied
```

### Cause

スクリプトファイルに実行権限が付与されていない。

### Resolution

```bash
chmod +x scripts/validate.sh
chmod +x scripts/validate/*.sh
```

### Prevention

Git リポジトリでスクリプトの実行権限を保持する。

```bash
git update-index --chmod=+x scripts/validate.sh
git update-index --chmod=+x scripts/validate/*.sh
```

---

## Problem: Code Fence が閉じられていないエラーが出る

### Symptom

```
::error::Code Fence が閉じられていません: docs/example.md
```

### Cause

Markdown ファイル内の ` ``` ` の開始・終了が対応していない。

### Resolution

対象ファイルを開き、` ``` ` の開始と終了が正しく対応しているか確認する。

ネストされたコードブロックや、コメントアウト内の ` ``` ` も検出されることがある。

### Prevention

Markdown エディタ（VS Code 等）のプレビューでコードブロックが正しく表示されることを確認してからコミットする。

---

## Problem: Broken Link エラーが出る

### Symptom

```
::error::Broken Link: docs/architecture/overview.md -> components.md
```

### Cause

Markdown ファイル内の相対リンクが指すファイルが存在しない。

### Resolution

1. リンク先のファイルが正しいパスに存在するか確認する
2. リンクのパスを修正する（相対パスに注意する）

### Prevention

ファイルを移動・削除する際は、そのファイルへのリンクを含む Markdown を検索して更新する。

```bash
grep -r "filename.md" docs/
```

---

## Problem: CI でのみバリデーションが失敗する

### Symptom

ローカルでは `./scripts/validate.sh` が PASS するが、GitHub Actions でのみ失敗する。

### Cause

- ローカルと CI の bash バージョンが異なる
- ファイルの改行コードが CRLF になっている（Windows 環境でのコミット）

### Resolution

改行コードを確認・修正する。

```bash
# 改行コードの確認
file scripts/validate.sh

# LF に変換（Git の設定）
git config core.autocrlf false
git rm --cached -r scripts/
git checkout -- scripts/
```

### Prevention

`.gitattributes` にシェルスクリプトの改行コードを指定する。

```
scripts/**/*.sh text eol=lf
```

---

## Problem: AI エージェントがドキュメントを参照しない

### Symptom

AI エージェントが、`docs/` 内のドキュメントを無視して実装する。

### Cause

`.github/copilot-instructions.md` または `AGENTS.md` にドキュメント参照の指示が不足している。

### Resolution

`AGENTS.md` の「作業開始」セクションに、ドキュメント参照ステップが明記されているか確認する。

また、Issue の説明・コメントで、AI に参照すべきドキュメントを明示する。

### Prevention

`AGENTS.md` に明確な参照順序を定義し、最新の状態を維持する。
