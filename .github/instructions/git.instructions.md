---
applyTo: "**/*"
---

# Git Instructions

このファイルは、AIによる不要な変更・意図しないファイル変更・Git履歴破壊を防止するための個別ルールを定義する。

## このファイルの責務

- Issue単位の変更範囲管理
- Gitで禁止する操作の明確化
- Diff Reviewの手順
- Secret混入防止

Repository全体の禁止事項は `.github/copilot-instructions.md`、作業手順は `AGENTS.md` を参照すること。

## 基本ルール

AIは現在のIssueに必要な変更だけを行う。

- 変更対象はIssueに直接必要なファイルに限定する
- 作業中も差分を確認し、意図しない変更を広げない
- Lock FileやGenerated Fileは、Issue対応に必要で変更理由が説明できる場合のみ更新する

## 禁止事項

- Force Push
- History Rewrite
- Unrelated Revert
- Unrelated Formatting
- 不要なRename
- 無関係なFile変更
- 意図しないLock File変更
- 不要なGenerated File変更

## Diff Review

作業終了前に、以下の順序で確認する。

Changed Files
↓
Diff
↓
Unrelated Changes
↓
Remove Accidental Changes
↓
Final Validation

## Secrets

以下をGitへ追加してはいけない。

- API Key
- Access Token
- Password
- Private Key
- Credential
- Production Secret
- .env の実値
