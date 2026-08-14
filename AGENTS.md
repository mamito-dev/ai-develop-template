# AGENTS.md

本ドキュメントは、このリポジトリで作業するAIエージェント向けの作業手順・基本方針を定義する。

AIエージェントは作業開始前に本ドキュメントおよび `.github/copilot-instructions.md` を必ず参照すること。

---

## 1. 作業開始

作業を開始する前に、以下の順序で情報を確認する。

```text
Issue確認
↓
仕様確認（docs/specifications/）
↓
Architecture確認（docs/architecture/）
↓
既存コード調査
↓
既存テスト調査
↓
影響範囲確認
```

不明点がある場合は、この段階で確認を求めること。推測で進めない。

---

## Context Loading

AIエージェントは **progressive context loading** を行い、必要な情報だけを順序付きで読み込む。

### Context Hierarchy（Level 0〜5）

```text
Level 0: Global Rules
    - .github/copilot-instructions.md
Level 1: Repository Rules
    - AGENTS.md
Level 2: Task Rules
    - .github/instructions/
    - .github/prompts/
    - .github/skills/
Level 3: Domain Documentation
    - docs/specifications/
    - docs/architecture/
    - docs/api/
    - docs/development/
Level 4: Existing Implementation
    - 関連Source Code
Level 5: Tests / Validation
    - 関連Test
    - Build / Lint / CI設定
```

### Required Order

1. Issue
2. Repository rules
3. Task-specific instructions
4. Relevant skills/prompts
5. Relevant documentation
6. Relevant source code
7. Relevant tests

関連しないファイルを網羅目的で読まないこと。

### Task Classification

```text
FEATURE
BUG
REFACTOR
TEST
DOCUMENTATION
ARCHITECTURE
API
CONFIGURATION
SECURITY
UNKNOWN
```

### TaskごとのContext Matrix

| Task | Requirements | Architecture | API | Tests | Documentation |
| ---- | ------------ | ------------ | --- | ----- | ------------- |
| Feature | 必須 | 必須 | 必要時 | 必須 | 必要時 |
| Bug | 必須 | 必要時 | 必要時 | 必須 | 必要時 |
| Refactor | 必要 | 必須 | 必要時 | 必須 | 必要時 |
| Test | 必要 | 必要時 | 必要時 | 必須 | 必要時 |
| Documentation | 必要時 | 必要時 | 必要時 | 必要時 | 必須 |
| Architecture | 必須 | 必須 | 必要時 | 必要時 | 必須 |
| API | 必須 | 必須 | 必須 | 必須 | 必須 |
| Configuration | 必要時 | 必要時 | 必要時 | 必要時 | 必須 |
| Security | 必須 | 必須 | 必要時 | 必須 | 必須 |

### Context Loading Algorithm

```text
START
  ↓
Read Issue
  ↓
Classify Task
  ↓
Read Global Rules
  ↓
Read Repository Rules
  ↓
Identify Required Instructions
  ↓
Identify Required Skills / Prompt
  ↓
Identify Relevant Documentation
  ↓
Identify Relevant Source Code
  ↓
Identify Relevant Tests
  ↓
Check for Conflicts / Unknowns
  ↓
Create Work Plan
  ↓
Begin Work
```

### Context Loadingの停止条件

以下が満たされた時点で停止してよい。

- [ ] Task scope is understood
- [ ] Acceptance criteria are understood
- [ ] Applicable rules are known
- [ ] Relevant architecture is understood
- [ ] Relevant contracts are understood
- [ ] Affected components are identified
- [ ] Test strategy is understood
- [ ] No unresolved critical conflict exists

### 追加ロード条件

作業中に以下が見つかった場合のみ追加で読む。

- New Component: component責務と関連architecture
- API Change: API contract・API documentation・関連tests
- Database Change: schema・migration rules・persistence layer
- Security Impact: security rules・authn/authz rules・影響コード

### Conflict Detection / Unknown Handling

以下を検出したら停止して確認を求める（黙って解決しない）。

- Issue vs Documentation conflict
- Documentation vs Implementation conflict
- Architecture conflict
- API/Data Contract conflict
- Unknown（仕様確定に必要な情報不足）

Assumptionを置く場合は、Assumptionであることを明示する。

### Context Priority / Budget

```text
Critical
  ↓
Required
  ↓
Relevant
  ↓
Optional
```

- 無関係なContextを読まない
- 同一情報の重複記載・重複読込を避ける
- Repository全体の無差別読込を禁止する

### Skills / Promptsとの関係

```text
Context Loading
       ↓
Applicable Skills Identification
       ↓
Skill / Prompt Execution
```

例:

- Feature: `issue-analysis` → `implementation` → `testing` → `documentation`
- Bug: `investigate-issue.prompt.md` / `fix-bug.prompt.md` + `implementation` + `testing`

### 既存Instructionsとの重複整理方針

`.github/instructions/` の既存ファイル（api / architecture / coding / testing / git）をTask RuleのSource of Truthとして使用し、同等内容の新規Instructionを重複作成しない。

### Context Loading Report（大きなIssue向け）

必要に応じて作業開始前に以下を簡潔に出力する。

```markdown
## Context Loading Report

### Task Type
- FEATURE / BUG / ...

### Loaded Rules
- `.github/copilot-instructions.md`
- `AGENTS.md`
- relevant task instructions

### Loaded Skills / Prompts
- relevant skills/prompts

### Loaded Documentation
- relevant requirements / architecture / API contract

### Loaded Code
- relevant components

### Loaded Tests
- relevant tests

### Additional Context Required
- None / details

### Conflicts
- None / details
```

---

## 2. 実装

確認が完了したら、以下の方針で実装を行う。

```text
最小変更を選択
↓
実装
↓
テスト追加・更新
```

### 実装の原則

- Issue のスコープを超えた変更を行わない
- 既存のコード規約・スタイルに従う
- 変更は最小限にとどめる
- テストを削除・弱体化させない
- 秘密情報をコードに含めない

---

## 3. 検証

実装が完了したら、以下の検証を行う。

```text
Test（テスト実行）
↓
Lint / Format（コードスタイル確認）
↓
Build（ビルド確認）
↓
Diff確認（意図しない変更がないか確認）
↓
Completion Gate（docs/ai/completion-gate.md）
```

> TODO: プロジェクト固有のコマンドが確定次第、ここに記載すること。

---

## 4. 完了報告

作業完了を報告する前に、**必ず `docs/ai/completion-gate.md` に定義された Completion Gate を実行すること**。

Completion Gate を通過していない状態で `READY_FOR_REVIEW` として報告してはいけない。

作業完了時には、以下の項目を明示して報告する。

| 項目 | 内容 |
| ---- | ---- |
| 変更内容 | 何を・なぜ変更したか |
| 変更ファイル | 変更したファイルの一覧 |
| Test 結果 | テストの実行結果（Pass / Fail / Skip） |
| Build 結果 | ビルドの成否 |
| Lint 結果 | Lint チェックの結果 |
| 未解決事項 | 判断できなかった点・確認が必要な点 |
| 注意事項 | レビュアーへの申し送り事項 |

Completion Report は `docs/ai/completion-gate.md` に定義された形式で出力すること。

`READY_FOR_REVIEW` は Human Review の完了を意味しない。

---

## 5. 参照ドキュメント

| 種別 | 場所 |
| ---- | ---- |
| Copilot 共通ルール | `.github/copilot-instructions.md` |
| Architecture | `docs/architecture/` |
| 仕様 | `docs/specifications/` |
| API Contract | `docs/api/` |
| 開発ガイド | `docs/development/` |
| Change Safety Policy | `.github/policies/change-safety-policy.md` |
| 個別ルール | `.github/instructions/` |
| 再利用可能Prompt | `.github/prompts/` |
| Completion Gate | `docs/ai/completion-gate.md` |

---

> TODO: プロジェクト固有の設定・制約が確定次第、本ドキュメントに追記すること。
