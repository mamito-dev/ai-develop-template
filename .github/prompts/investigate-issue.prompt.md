# Investigate Issue Prompt

このPromptは、Bug、Unexpected Behavior、Performance問題などの調査を行うための標準手順を定義する。

## 目的

- 現象を再現し、EvidenceにもとづいてRoot Causeを特定する
- 調査と実装を分離し、明示的な依頼がない限りコード変更を行わない

## Promptの責務

- このPromptは **How to investigate / report** を補助する
- `.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` を上書きしない
- Specification / Architecture / API Contract と矛盾する場合はそちらを優先する

## 作業前確認

1. Issueの内容
   - 期待される動作
   - 観測された動作
   - 再現条件
   - スコープ / 非スコープ
2. Repository Rules
3. 関連Specification / Architecture / API Contract
4. 関連コード
5. 関連Test
6. 影響範囲

情報が不足している場合は、推測で仕様を作らず確認を求める。

## 必須フロー

Issue確認
↓
Expected Behavior確認
↓
Observed Behavior確認
↓
再現確認
↓
関連コード調査
↓
関連Test調査
↓
Data / State確認
↓
Root Cause特定
↓
Fix案作成

## 調査原則

以下の順番を守る。

Evidence
↓
Hypothesis
↓
Verification
↓
Root Cause

原因が分からないまま「とりあえず修正」は行わない。

## 調査手順

- Expected Behavior と Observed Behavior を明確に分離する
- 再現に必要な入力、状態、依存条件を確認する
- 関連コード、呼び出し元、状態遷移、データの流れを調査する
- 既存Testで保証されていること / 保証されていないことを確認する
- Evidenceで裏づけられたRoot Causeのみを報告する

## 実行手順

- 調査ログ、再現手順、確認したファイル、確認した挙動を整理する
- 必要であれば複数のFix案を比較する
- 実装依頼がない限りコード変更を行わない

## 検証

- 再現確認
- 仮説検証
- 既存Test確認
- 必要な追加Testの整理

実行していない確認を `PASS` と表現してはいけない。

## 完了報告

調査結果は以下の形式で報告する。

```md
## Expected Behavior
## Observed Behavior
## Reproduction
## Evidence
## Root Cause
## Affected Components
## Proposed Fix
## Risks
## Required Tests
```
