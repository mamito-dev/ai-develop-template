# Fix Bug Prompt

このPromptは、Bugの原因を特定し、Regression Testを追加したうえで修正するための標準手順を定義する。

## 目的

- Bugを再現し、Root Causeを特定したうえで最小修正を行う
- 同じBugが再発した場合に失敗するRegression Testを可能な限り追加する

## Promptの責務

- このPromptは **How to investigate / fix / test / report** を補助する
- `.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` を上書きしない
- Specification / Architecture / API Contract と矛盾する場合はそちらを優先する

## 作業前確認

1. Bugの内容
   - 期待される動作
   - 実際の動作
   - 再現条件
   - 影響範囲
2. Repository Rules
3. 関連Specification / Architecture / API Contract
4. 関連コード
5. 関連Test

情報が不足している場合は、推測で修正方針を決めず確認を求める。

## 必須フロー

Bug確認
↓
再現
↓
Root Cause特定
↓
最小修正
↓
Regression Test追加
↓
関連Test
↓
Build
↓
Diff Review

## 修正原則

AIは症状を隠すだけの修正を行わない。以下は禁止。

- Errorを無視する
- Exceptionを握りつぶす
- Testを削除する
- TestをSkipする
- Validationを無効化する
- Timeoutを不当に延長する
- 常に成功を返す

## 調査手順

- Bugを再現し、入力・状態・環境条件を整理する
- EvidenceにもとづいてRoot Causeを特定する
- 既存の責務境界・呼び出し元・副作用を確認する
- 修正範囲を最小に保つ

## 実行手順

- Root Causeに直接対応する最小修正を行う
- 可能な限りRegression Testを追加する
- 既存Testを弱めて成功させない
- 実装後に差分を確認し、Issue外の変更を除去する

## 検証

- Bug再現手順の再確認
- Regression Test
- 関連Test
- Build
- 必要に応じて Lint / Format

実行していないものを `PASS` と報告してはいけない。

## 完了報告

以下の形式で報告する。

```md
## Bug
## Root Cause
## Fix
## Regression Test
## Validation
- Tests:
- Lint:
- Build:
## Risks
## Remaining Issues
```
