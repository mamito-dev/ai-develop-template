# AI Behavior Incident

## Incident ID

AI-INC-EXAMPLE-001

## Date

2026-08-14

## Status

CLOSED

## Severity

MEDIUM

## Context

GitHub Copilotを使用した小規模な実装タスク。定義されたIssue Scopeに基づいて特定ファイルのみを変更する作業。

## Expected Behavior

AIは定義されたIssue Scope内のファイルのみを変更する。

## Actual Behavior

AIがScope外のファイルへの変更を提案した。

## Impact

提案された変更は承認されなかった。レビュー工数が発生した。

## Classification

SCOPE

## Root Cause

Scope定義において、変更対象外のファイルが明示的に識別されていなかった。
AIはRepositoryの関連ファイルを推測で変更対象に含めた。

なお、Instructionが曖昧であったことも一因（INSTRUCTION）として考えられる。

## Corrective Action

Scope Ruleへ、変更対象外のファイルを明示的に識別する条件を追加する。

## Verification

同じタスクを再実行し、Scope外のファイルが変更対象に含まれないことを確認した。

## Recurrence

- [x] Reproduced
- [x] Fixed
- [x] Regression checked
- [x] No recurrence observed

## Related Issues

- Related Regression Case: [AI-REG-EXAMPLE-001](../regression/AI-REG-EXAMPLE-001.md)

## Notes

このIncidentはIncident Managementワークフローの動作確認のためのサンプルである。Repositoryの実際の問題を捏造するものではない。
