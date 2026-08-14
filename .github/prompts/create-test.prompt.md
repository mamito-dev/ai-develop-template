# Create Test Prompt

このPromptは、既存機能または新機能に対するTestを追加するための標準手順を定義する。

## 目的

- Requirement / Behavior に対応する意味のあるTestを追加する
- 既存のTest基盤、Test Pattern、Repository Rulesに従って検証を強化する

## Promptの責務

- このPromptは **How to design / implement / validate tests** を補助する
- `.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` を上書きしない
- Specification / Architecture / API Contract と矛盾する場合はそちらを優先する

## 作業前確認

1. Requirement / 対象Behavior
2. 関連Issueまたは仕様
3. Repository Rules
4. 既存Test
5. Test Pattern
6. 変更対象コードと影響範囲

情報が不足している場合は、推測で仕様を追加しない。

## 必須フロー

Requirement確認
↓
対象Behavior確認
↓
Existing Test調査
↓
Test Pattern確認
↓
Test Case設計
↓
Test実装
↓
Test実行

## Test Case検討

必要に応じて以下を検討する。

- 正常系
- 異常系
- Boundary
- Invalid Input
- Error
- Regression
- State Transition

意味のないTest Caseは増やさない。

## Test設計原則

Testは可能な限り以下を満たす。

- Deterministic
- 独立
- 明確なFailure Message
- Behavior Based

## 調査手順

- Requirementと対象Behaviorを分解する
- 既存Testの対象範囲と不足分を確認する
- 同種の既存Testから命名、構成、アサーション方針を確認する

## 禁止事項

以下を目的としたTestを作成しない。

- Coverage数字だけを上げる
- Implementation Detailを過剰に固定する
- 実装を変更しないと成立しないTest
- 意味のない重複Test

## 実行手順

- 既存のTestスタイル、命名、セットアップ方法を確認する
- 外部から観測可能なBehaviorを対象にTestを設計する
- 必要最小限のTest追加・更新にとどめる
- 追加したTestが失敗すべき条件で失敗することを確認する

## 検証

- 追加 / 更新したTestの実行
- 必要に応じて関連Testの実行
- 必要に応じて Build / Lint / Format の確認

実行していない検証を `PASS` と報告してはいけない。

## 完了報告

以下の形式で報告する。

```md
## Summary
## Target Behavior
## Test Cases
## Validation
- Tests: PASS / FAIL / NOT RUN / BLOCKED
- Lint: PASS / FAIL / NOT RUN / BLOCKED
- Build: PASS / FAIL / NOT RUN / BLOCKED
## Risks
## Remaining Work
```
