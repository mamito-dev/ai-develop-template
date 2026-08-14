# Implement Issue Prompt

このPromptは、GitHub Issueに記載された機能追加・改善を実装するための標準手順を定義する。

## 目的

- Issueの **What / Why / Acceptance Criteria** を確認したうえで、最小変更で実装する
- Repository Rules、Specification、Architecture、API Contractと矛盾しない形で変更する

## Promptの責務

- このPromptは **How to investigate / implement / test / report** を補助する
- **Issue = What**、**Prompt = How** として扱う
- `.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` を上書きしない
- Project Specification / Architecture / API Contract と矛盾する場合はそちらを優先する

## 作業前確認

以下を順番に確認する。

1. Issue
   - Background
   - Purpose
   - Scope
   - Non-scope
   - Requirements
   - Constraints
   - Acceptance Criteria
2. Repository Rules
   - `.github/copilot-instructions.md`
   - `AGENTS.md`
   - 関連する `.github/instructions/`
3. Project Documents
   - `docs/specifications/`
   - `docs/architecture/`
   - `docs/api/`
   - 必要に応じて `docs/development/`
4. Existing Code / Tests
   - 関連Component
   - 関連Service
   - 関連Model
   - 関連Test
   - 呼び出し元
5. 変更範囲
   - 影響するファイル
   - 影響するモジュール
   - 依存先 / 利用者

情報が不足している場合は、推測で仕様を補完せず確認を求める。

## 必須フロー

Issue確認
↓
Requirements確認
↓
Architecture確認
↓
既存実装調査
↓
既存Test調査
↓
影響範囲確認
↓
実装計画
↓
Implementation
↓
Test追加・変更
↓
Test
↓
Lint / Format
↓
Build
↓
Diff Review
↓
完了報告

## 調査手順

- Acceptance Criteriaを満たすために必要な最小変更を特定する
- 既存の責務境界・依存方向・API Contractを確認する
- 既存の実装パターンと既存Testの書き方を確認する
- 変更の副作用と未変更でよい範囲を明確にする

## 実行手順

- 最小の変更でAcceptance Criteriaを満たす
- Issue外の改善、不要なRefactoring、不要なDependency追加を行わない
- 既存Architecture / Contract / Test方針を壊さない
- 必要な場合のみTestを追加または更新する
- 実装後は変更ファイルと差分を確認し、意図しない変更を除去する

## 検証

変更内容に応じて必要な検証を実行する。

- Unit Test
- Integration Test
- UI Test
- Lint
- Format
- Build
- API Contract Validation

実行していないものを `PASS` と報告してはいけない。実行できなかった場合は `NOT RUN` または `BLOCKED` と報告する。

## 完了報告

以下の形式で報告する。

```md
## Summary
## Changed Files
## Validation
- Tests: PASS / FAIL / NOT RUN / BLOCKED
- Lint: PASS / FAIL / NOT RUN / BLOCKED
- Build: PASS / FAIL / NOT RUN / BLOCKED
## Scope Review
## Risks
## Remaining Work
```
