# ai-develop-template

AI開発標準テンプレート

GitHub Copilot などの AI を活用した開発を安定・一貫して行うための Repository 標準テンプレート。

---

## AI エージェントの方へ

作業を開始する前に、以下の順序でドキュメントを参照してください。

```text
1. AGENTS.md                            ← 作業手順・基本方針（必読）
2. .github/copilot-instructions.md      ← AI 共通ルール（必読）
3. .github/instructions/                ← タスク別ルール（必要に応じて）
4. docs/ai/completion-gate.md           ← 完了判定ゲート（必読）
5. .github/policies/change-safety-policy.md  ← 変更安全ポリシー（必読）
```

**入口は `AGENTS.md` です。**

---

## ドキュメント構成

### AI 開発ルール

| ファイル | 役割 |
|----------|------|
| `AGENTS.md` | AIエージェント向け作業手順・基本方針 |
| `.github/copilot-instructions.md` | AI 共通ルール・禁止事項 |
| `.github/instructions/` | タスク別ルール（API / Architecture / Coding / Git / Testing） |
| `.github/prompts/` | 再利用可能な Prompt |
| `.github/skills/` | AI スキル定義 |

### 完了・安全管理

| ファイル | 役割 |
|----------|------|
| `docs/ai/completion-gate.md` | Completion Gate 定義・Report フォーマット |
| `.github/policies/change-safety-policy.md` | 変更安全ポリシー |
| `.github/change-safety.yml` | 変更安全設定（機械可読） |
| `.github/ai-docs.yml` | AI ドキュメント Manifest |

### AI 行動管理

| ファイル | 役割 |
|----------|------|
| `docs/ai/ai-behavior-incidents.md` | AI Behavior Incident 管理 |
| `docs/ai/regression-suite.md` | Regression Suite 定義 |
| `docs/ai/regression/catalog.md` | Regression Case カタログ |
| `docs/ai/integration.md` | AI 開発基盤 最終統合サマリー |

### プロジェクトドキュメント

| ディレクトリ | 内容 |
|--------------|------|
| `docs/specifications/` | 要件・ビジネスルール |
| `docs/architecture/` | アーキテクチャ |
| `docs/api/` | API Contract |
| `docs/development/` | 開発ガイド（ビルド / テスト / CI） |

---

## AI 開発ワークフロー

```text
Issue / User Request
       ↓
AI Instructions 確認（AGENTS.md → copilot-instructions.md）
       ↓
Scope 定義
       ↓
Implementation
       ↓
Validation（./scripts/validate.sh）
       ↓
Change Safety 確認
       ↓
Completion Gate（docs/ai/completion-gate.md）
       ↓
Completion Report 出力
       ↓
Human Review
```

---

## Validation

```bash
# 全 Validation を実行
./scripts/validate.sh

# AI ドキュメント Validation のみ
./scripts/validate.sh ai-docs
```

詳細は `docs/development/` を参照してください。
