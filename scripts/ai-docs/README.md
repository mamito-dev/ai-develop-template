# AI Documentation Validator

AI向けDocumentation / Instructions / Skills / Promptsの整合性を自動検証するツールです。

## 概要

このツールは、AIが参照するドキュメント基盤が壊れていないことを機械的に確認します。

```text
AIが正しいか → Human / AI Review で確認
AIが参照する基盤が壊れていないか → このツールで確認
```

## ファイル構成

```text
scripts/ai-docs/
├── validate.py    # バリデーター本体
├── rules.py       # ルールID・定数定義
└── README.md      # このファイル
```

## 実行方法

### ローカル実行

```bash
python scripts/ai-docs/validate.py
```

### JSON出力

```bash
python scripts/ai-docs/validate.py --json
```

### validate.sh から実行

```bash
./scripts/validate.sh ai-docs
```

### リポジトリルートを指定して実行

```bash
python scripts/ai-docs/validate.py --repo-root /path/to/repo
```

## 依存関係

- Python 3.8 以上
- PyYAML（オプション。未インストールの場合 YAML 検証がスキップされます）

```bash
pip install pyyaml
```

## Exit Code

| Code | 意味 |
|------|------|
| 0 | PASS（ERROR なし。WARNING のみの場合も 0） |
| 1 | ERROR（1件以上の ERROR が検出された） |
| 2 | INVALID_CONFIGURATION（設定ファイルに問題がある） |

## Validation Level

| Level | 意味 | CI への影響 |
|-------|------|-------------|
| ERROR | 修正必須 | CIをFailさせる |
| WARNING | 問題の可能性あり | CIをFailさせない |
| INFO | 参考情報 | CIに影響なし |

## Rule ID 一覧

| ID | 説明 |
|----|------|
| AI001 | Required file missing |
| AI002 | Broken internal link |
| AI003 | Invalid path reference |
| AI004 | Invalid Skill structure |
| AI005 | Invalid Prompt structure |
| AI006 | Invalid Instruction structure |
| AI007 | Missing required section |
| AI008 | Missing referenced Skill |
| AI009 | Missing referenced Prompt |
| AI010 | Deprecated document reference |
| AI011 | Source of Truth conflict |
| AI012 | Invalid metadata |
| AI013 | Invalid manifest |
| AI014 | Invalid naming convention |
| AI015 | Invalid change safety policy |

## 検証内容

### 1. 必須ファイル確認 (AI001)

`.github/ai-docs.yml` の `required` に定義されたファイルの存在を確認します。

### 2. ディレクトリ構造 / 命名規則 (AI014)

- Instructions: `*.instructions.md`
- Prompts: `*.prompt.md`
- Skills: `<skill-name>/SKILL.md`

### 3. 内部リンク (AI002)

Markdown内の内部リンクが実際に存在するファイルを指しているか確認します。
アンカー（`#heading`）についても可能な範囲で検証します。

### 4. Pathリファレンス (AI003)

Markdown本文中に記載された `.github/`, `docs/`, `scripts/` で始まるパスが
実際に存在するか確認します。

### 5. Skill必須セクション (AI007)

Skillファイルに以下のセクションが存在することを確認します：
- Purpose
- When to Use
- Workflow
- Rules
- Validation
- Completion Criteria
- Output

### 6. Prompt必須セクション (AI007)

Promptファイルに以下のセクションが存在することを確認します：
- Objective（または Purpose）
- Completion Report（または Output）

### 7. Skill参照 (AI008)

PromptのFront Matterで宣言された `skills` が実際に存在するか確認します。

### 8. Deprecated参照 (AI010)

`status: deprecated` なドキュメントへの参照をWARNINGとして検出します。

### 9. Manifest検証 (AI013)

`.github/ai-docs.yml` のYAML構文・必須フィールドを検証します。

### 10. Change Safety Policy検証 (AI015)

`.github/change-safety.yml` の以下を検証します。

- YAML syntax
- `version` フィールド
- サポートされたカテゴリのみを使用
- Policy Value（`allowed` / `restricted` / `forbidden`）の妥当性
- 必須カテゴリの充足

## Manifest設定

`.github/ai-docs.yml` でValidation対象と設定を管理します。

```yaml
version: 1

required:
  - .github/copilot-instructions.md
  - AGENTS.md

optional:
  - .github/instructions/
  - .github/prompts/
  - .github/skills/

source_of_truth:
  requirements: docs/specifications/
  architecture: docs/architecture/
  api: docs/api/
  development: docs/development/

validation:
  markdown: true
  links: true
  paths: true
  structure: true
  source_of_truth: true
  naming_convention: true
  metadata: true
```

## Front Matter

Prompt / Skill に Front Matter を設定することでメタデータ検証が有効になります。

### Prompt

```markdown
---
name: implement-issue
type: prompt
skills:
  - issue-analysis
  - implementation
  - testing
  - documentation
---
```

### Skill

```markdown
---
name: implementation
type: skill
requires:
  - issue-analysis
---
```

### Documentation

```markdown
---
domain: api
source_of_truth: true
status: active
---
```

## Deprecated Document

Deprecated なドキュメントには以下のメタデータを設定します：

```markdown
---
status: deprecated
replacement: docs/api/users-v2.md
---
```

このドキュメントへの参照は WARNING として検出されます。

## CI統合

GitHub Actions での実行は `.github/workflows/ai-docs-validation.yml` を参照してください。

## 設計原則

このツールは「AIの賢さ」を検証しません。

**検証対象**:
- ファイルの存在
- リンクの有効性
- パスの存在
- 構造の完全性
- メタデータの有効性
- 依存関係の存在
- Manifestの有効性

**Human / AI Reviewの対象**:
- 要件の正しさ
- Architectureの正しさ
- Business Ruleの正しさ
- Promptの効果
- Skillの効果
