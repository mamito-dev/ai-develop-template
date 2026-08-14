# AI Behavior Incidents

## Purpose

AI開発で発生した問題や改善点を記録し、今後のAIルール改善へつなげるための仕組み。

Incidentを記録する目的は「同じ問題を繰り返さない」ことであり、AIのミスを記録すること自体を目的にしない。

```text
AI Development
      ↓
AI Behavior Observation
      ↓
Incident
      ↓
Root Cause Analysis
      ↓
Corrective Action
      ↓
Regression Verification
      ↓
Repository Standard Improvement
      ↓
AI Development
```

---

## 記録基準

すべてのAI操作を記録する必要はない。

### 記録対象

- AIがRepositoryルールに違反した
- AIがScope外変更を行った
- AIがRequired Validationを実行しなかった
- AIがCompletion条件を誤判定した
- AIが既存仕様を壊した
- AIが重大な不要変更を行った
- 同じ問題が繰り返し発生した
- AIの挙動を改善するためにRepositoryルールを変更した

### 原則として記録不要

- 単純なタイプミス
- Human Reviewで容易に修正できる軽微なコードミス
- AIが通常のValidationによって自動的に検出・修正できた問題
- AIの挙動改善につながらない一時的な問題

---

## Classification

AIの問題を単に「AIが間違えた」で終わらせない。可能な範囲で原因を分類する。

| Classification | 説明 |
|----------------|------|
| `INSTRUCTION` | AIへのInstruction（`.instructions.md`等）に問題があった |
| `PROMPT` | Promptの内容や構造に問題があった |
| `SCOPE` | Scope定義が曖昧または不足していた |
| `VALIDATION` | Validationが不足またはスキップされた |
| `SAFETY` | Change Safety Ruleへの違反または不足 |
| `COMPLETION` | Completion条件の誤判定または未確認 |
| `CONTEXT` | AIへ与えられたContextが不足していた |
| `TOOL` | 使用したツールの問題 |
| `MODEL` | 特定のAI Modelでのみ発生する問題 |
| `HUMAN_INPUT` | IssueやPromptの指示が曖昧だった |
| `UNKNOWN` | 原因が特定できない |

AIだけを原因とする記録にならないよう、`HUMAN_INPUT` や `CONTEXT` も積極的に評価する。

---

## Severity

| Severity | 説明 | 例 |
|----------|------|----|
| `LOW` | 軽微な問題 | 不要なコメントを追加した、命名規則を一度だけ誤った |
| `MEDIUM` | Reviewや追加修正が必要 | Scope内だが不要なファイル変更、Required Validationを忘れた |
| `HIGH` | Repositoryや機能へ明確な影響 | Scope外の重要な変更、既存機能を壊す変更、Safety Rule違反 |
| `CRITICAL` | 重大なRepository破壊や安全上の問題 | 既存のSafety Policyの定義を優先する |

---

## Lifecycle

```text
OPEN → INVESTIGATING → FIXED → VERIFIED → CLOSED
```

| Status | 説明 |
|--------|------|
| `OPEN` | 問題が確認された状態 |
| `INVESTIGATING` | 原因を調査している状態 |
| `FIXED` | Corrective Actionを実施した状態（再発防止確認は未完了） |
| `VERIFIED` | 修正後の動作確認が完了した状態 |
| `CLOSED` | 必要な記録・検証が完了した状態 |

Incidentを `FIXED` だけで終了扱いしない。可能な限り `VERIFIED` まで確認する。

---

## Corrective Action の原則

同じ問題をAIに再び起こさせないための最小限の改善とする。

```text
Problem:
AIがScope外ファイルを変更

Bad Fix:
Repository全体のInstructionsを書き直す

Better Fix:
Scope Ruleへ不足していた明示的条件を追加
```

Incident対応によって既存ルールを変更する場合、どのRuleを変更したか・なぜ変更したかをIncidentへ記録する。

---

## Regression

再発防止が重要なIncidentについては、再発確認用のRegression Caseを残す。

Regression Caseの追加を優先する基準：

- HIGH以上
- 同じ問題が複数回発生した
- Repository Ruleの変更につながった
- Completion Gateの問題だった
- Scope制御の問題だった
- Safetyに関係する問題だった

配置場所：`docs/ai/regression/`

---

## 既存の仕組みとの関係

| 仕組み | 関係 |
|--------|------|
| Validation | ValidationのFAILはValidationで扱う。AI Behavior IncidentはValidationだけでは把握できないAI固有の挙動を記録するために使用する |
| Change Safety | 既存Change Safetyで検出された問題をIncidentとして記録する場合、既存Safety ResultとIncident Analysisとして扱う。Change Safety Policy自体をIncident Documentationへコピーしない |
| Completion Gate | Completion Gateが正常に動作した後も、Human ReviewでAIの問題が発見された場合は記録対象とする |

---

## Incident Template

新しいIncidentは `docs/ai/incidents/AI-INC-XXXX.md` として作成する。

```markdown
# AI Behavior Incident

## Incident ID

AI-INC-XXXX

## Date

YYYY-MM-DD

## Status

OPEN / INVESTIGATING / FIXED / VERIFIED / CLOSED

## Severity

LOW / MEDIUM / HIGH / CRITICAL

## Context

タスクと関連する状況を説明する。

## Expected Behavior

AIが本来すべきだった動作。

## Actual Behavior

AIが実際に行った動作。

## Impact

何が影響を受けたか。

## Classification

INSTRUCTION / PROMPT / SCOPE / VALIDATION / SAFETY / COMPLETION / CONTEXT / TOOL / MODEL / HUMAN_INPUT / UNKNOWN

## Root Cause

推定される根本原因を説明する。

## Corrective Action

再発防止のために行った変更を説明する。

## Verification

修正がどのように確認されたかを説明する。

## Recurrence

- [ ] Reproduced
- [ ] Fixed
- [ ] Regression checked
- [ ] No recurrence observed

## Related Issues

-

## Notes

-
```

---

## Regression Case Template

重要なIncidentについては `docs/ai/regression/AI-REG-XXXX.md` としてRegression Caseを作成する。

```markdown
# AI Behavior Regression Case

## Case ID

AI-REG-XXXX

## Purpose

保護対象の挙動は何か。

## Input / Context

どのようなタスクまたはContextを与えるか。

## Expected Behavior

AIが行うべき動作。

## Forbidden Behavior

AIが行ってはいけない動作。

## Verification

挙動をどのように確認するか。

## Related Incident

AI-INC-XXXX
```

---

## IncidentからIssueへの接続

AI Behavior IncidentによってRepository側の改善が必要になった場合、Incidentから改善Issueへ接続して追跡する。

```text
Incident
↓
Root Cause
↓
Improvement Issue
```

既存Issueで対応可能な場合は、新しい改善Issueを作成せず、`Related Issues` として既存Issueへ関連付ける。
