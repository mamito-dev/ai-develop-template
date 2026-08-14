# Review Code Prompt

このPromptは、Pull Request、Issue実装、AI生成コードなどをレビューするための標準手順を定義する。

## 目的

- 要件、Architecture、Contract、Test、Security、Scopeの観点から変更を評価する
- 個人的な好みではなく、根拠のある指摘のみを報告する

## Promptの責務

- このPromptは **How to review / report** を補助する
- `.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` を上書きしない
- Specification / Architecture / API Contract と矛盾する場合はそちらを優先する

## 作業前確認

1. 対象Issue / PRの目的
2. Acceptance Criteria
3. 関連Specification / Architecture / API Contract
4. 変更差分
5. 関連コード
6. 関連Test

## 必須フロー

Issue / PR確認
↓
Requirements確認
↓
Diff確認
↓
関連コード調査
↓
関連Test調査
↓
観点別レビュー
↓
指摘レベル分類
↓
レビュー結果報告

## 調査手順

- 対象Issue / PRの要求と差分を照合する
- 関連コード、関連Test、影響範囲を確認する
- 変更前提と実装意図が差分から読み取れるかを確認する

## レビュー項目

### Functional Correctness

- Requirementsを満たしているか
- Acceptance Criteriaを満たしているか
- Edge Caseに問題がないか

### Architecture

- Architectureに違反していないか
- Component責務が適切か
- Dependency方向が適切か

### API / Data

- Contract違反がないか
- Breaking Changeがないか
- Data Integrityに問題がないか

### Testing

- 必要なTestが存在するか
- Testが十分か
- Testを弱めていないか

### Security

- Secret Leakage
- Authorization
- Input Validation
- Unsafe Data Handling

### Scope

- Issue外の変更がないか
- 不要なRefactoringがないか
- 不要なDependencyがないか

## 指摘レベル

- `BLOCKER`: Merge前に必ず修正が必要
  - 例: Security vulnerability、Data corruption、Major functional failure、Architecture violation
- `HIGH`: 重大な問題
- `MEDIUM`: 修正を推奨する問題
- `LOW`: 改善提案

単なる個人的な好みは問題として報告しない。

## 実行手順

- 指摘には根拠、影響、必要であれば再現条件を含める
- 明確な根拠がない懸念は `NEEDS INVESTIGATION` として扱う
- Positive Findings があれば簡潔に記録する

## 検証

- Diffと要求の突合
- Contract / Architecture / Test / Security観点の確認
- 必要な追加検証の有無を整理

実施していない確認を断定的に成功扱いしない。

## 完了報告

レビュー結果は以下の形式で報告する。

```md
## Summary
## BLOCKER
## HIGH
## MEDIUM
## LOW
## Positive Findings
## Recommendation
- APPROVE
- REQUEST CHANGES
- NEEDS INVESTIGATION
```
