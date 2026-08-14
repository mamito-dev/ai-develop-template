# AI Behavior Regression Suite

## Purpose

AI Behavior Regression Suiteは、過去に発生したAIの問題や重要なAI Ruleが現在も守られているかを継続的に確認するための仕組みである。

アプリケーションの動作を検証するUnit / Integration / E2E Testとは異なり、**AIの開発行動そのもの**を対象とする。

---

## Regression SuiteとCompletion Gateの違い

| 仕組み | 目的 |
|--------|------|
| Completion Gate | 現在のTaskが完了条件を満たしているか確認する |
| AI Regression Suite | AIの過去の問題が再発していないか確認する |

---

## Regression SuiteとIncidentの違い

| 仕組み | 目的 |
|--------|------|
| Incident | 実際に発生した問題を記録する |
| Regression Case | その問題が再発しないか確認する |
| Regression Suite | 複数のRegression Caseをまとめて確認する |

---

## Regression Catalog

[`docs/ai/regression/catalog.md`](regression/catalog.md) を参照すること。

---

## Suite Structure

```text
AI Regression Suite
│
├── Scope (AI-REG-001)
│   └── Scope Boundary
│
├── Validation (AI-REG-002)
│   └── Required Validation
│
├── Completion (AI-REG-003)
│   └── Completion Gate
│
├── Safety (AI-REG-004)
│   └── Change Safety
│
└── Instruction (AI-REG-005)
    └── Repository Rules
```

---

## Result Status

| Status | 説明 |
|--------|------|
| `PASS` | Caseが期待通りに通過した |
| `FAIL` | Caseが失敗した（期待動作が確認できなかった） |
| `BLOCKED` | 環境やToolの理由で実行できなかった |
| `NOT_RUN` | 実行されていない |

**NOT_RUNをPASSとして扱ってはいけない。**

**BLOCKEDをAIが推測によってPASSに変更してはいけない。**

---

## Suite Result Rules

- 1件でもCritical / Required Regression CaseがFAILした場合、Suite = FAILとして扱う。
- NOT_RUNが存在する場合、Suite = FAILとして扱う（BLOCKEDを除く）。
- Regression Suite FAILの状態でAI Rule変更を正常完了扱いにしない。

---

## Execution

### Targeted Regression

特定の変更に関連するCaseのみを実行する。

| 変更対象 | 実行対象 |
|----------|----------|
| `AGENTS.md` / `.instructions.md` / `copilot-instructions.md` | INSTRUCTION関連: AI-REG-005 |
| Scope Rules | SCOPE関連: AI-REG-001 |
| Validation Rules | VALIDATION関連: AI-REG-002 |
| Safety Rules | SAFETY関連: AI-REG-004 |
| Completion Rules | COMPLETION関連: AI-REG-003 |

### Full Regression

以下の場合は全Regression Caseを実行する。

- Major AI Rule変更
- Safety変更
- Completion変更
- 大量のPrompt変更

---

## Regression Suite実行手順

1. 変更内容に基づき、Targeted または Full を選択する。
2. 対象CaseをCatalog（[`docs/ai/regression/catalog.md`](regression/catalog.md)）で確認する。
3. 各Caseの Verification 手順に従って確認を実施する。
4. 結果をReport Template（[`docs/ai/regression/report-template.md`](regression/report-template.md)）へ記録する。
5. FAILが存在する場合は Failure Handling を参照する。

Prompt経由で実行する場合は `.github/prompts/run-regression.prompt.md` を利用する。

---

## Failure Handling

1. FAILしたCaseの Expected Behavior と Actual Behavior を記録する。
2. Test Caseを変更してPASSにしてはいけない（Failure隠蔽の禁止）。
3. Root Causeを調査する。
4. 新しいAI Behavior Incidentが必要な場合は [`docs/ai/ai-behavior-incidents.md`](ai-behavior-incidents.md) に従ってIncidentを作成する。
5. Corrective Actionを実施し、再度Regressionを実行する。

```text
Regression FAIL
↓
Root Cause確認
↓
AI Behavior Incident（必要な場合）
↓
Corrective Action
↓
Re-run Regression
↓
PASS
```

---

## Regression Case追加基準

Regression Caseは数を増やすことを目的にしない。重要なAI Behaviorを保護することを目的とする。

既存ルールの単純な重複テストは追加しない。

新規Case追加基準は [`docs/ai/ai-behavior-incidents.md`](ai-behavior-incidents.md) の「Regression」セクションを参照すること。

---

## Regression Case変更・廃止

- Regression Caseは原則として削除しない。
- 仕様変更によって不要になった場合のみ、理由を記録して廃止とする。
- Caseを変更する場合は Why / What Changed / Expected Impact を記録する。
- Critical Caseの変更は関連Incidentも確認する。

---

## References

- Regression Catalog: [`docs/ai/regression/catalog.md`](regression/catalog.md)
- Regression Report Template: [`docs/ai/regression/report-template.md`](regression/report-template.md)
- AI Behavior Incidents: [`docs/ai/ai-behavior-incidents.md`](ai-behavior-incidents.md)
- Completion Gate: [`docs/ai/completion-gate.md`](completion-gate.md)
- Change Safety Policy: [`.github/policies/change-safety-policy.md`](../../.github/policies/change-safety-policy.md)
- Run Regression Prompt: [`.github/prompts/run-regression.prompt.md`](../../.github/prompts/run-regression.prompt.md)
