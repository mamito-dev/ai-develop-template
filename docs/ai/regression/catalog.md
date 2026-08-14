# AI Behavior Regression Catalog

このCatalogは、Repositoryで管理されているAI Behavior Regression Caseの一覧を提供する。

Regression Caseの詳細は各ファイルを参照すること。

---

## Catalog

| ID | Category | Priority | Description | Related Incident |
|----|----------|----------|-------------|------------------|
| [AI-REG-001](AI-REG-001.md) | SCOPE | HIGH | AIがIssue Scopeで定義された変更対象外のファイルを変更しない | [AI-INC-EXAMPLE-001](../incidents/AI-INC-EXAMPLE-001.md) |
| [AI-REG-002](AI-REG-002.md) | VALIDATION | HIGH | AIがタスク完了前にRequired Validationを実行する | N/A |
| [AI-REG-003](AI-REG-003.md) | COMPLETION | CRITICAL | AIがCompletion Gate未通過のままタスクを完了扱いにしない | N/A |
| [AI-REG-004](AI-REG-004.md) | SAFETY | CRITICAL | AIがChange Safety PolicyのFORBIDDEN操作を行わない | N/A |
| [AI-REG-005](AI-REG-005.md) | INSTRUCTION | HIGH | AIがRepositoryルールの禁止事項を遵守する | N/A |

---

## Category

| Category | 説明 |
|----------|------|
| `SCOPE` | AIのScope制御に関するCase |
| `INSTRUCTION` | AIがRepositoryルールを遵守するかに関するCase |
| `PROMPT` | PromptやContext構造に関するCase |
| `VALIDATION` | Required Validationの実行に関するCase |
| `SAFETY` | Change Safety Policyの遵守に関するCase |
| `COMPLETION` | Completion Gateの正常動作に関するCase |
| `CONTEXT` | AIへのContext提供に関するCase |
| `TOOL` | 使用ツールの問題に関するCase |

## Priority

| Priority | 説明 |
|----------|------|
| `CRITICAL` | SafetyやCompletion誤判定など重大な問題を防ぐCase |
| `HIGH` | 開発品質や再発防止に重要なCase |
| `MEDIUM` | 再発すると開発効率に影響するCase |
| `LOW` | 軽微な挙動差異や将来的な改善Case |

---

## Regression Case追加基準

[AI Behavior Incidents](../ai-behavior-incidents.md) を参照すること。

新規Regression Caseは `docs/ai/regression/AI-REG-NNN.md` として作成し、このCatalogへ追記する。
