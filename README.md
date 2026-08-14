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

## テンプレート適用直後の必須作業

このリポジトリの `docs/specifications/`、`docs/architecture/`、`docs/api/` は、**テンプレート自身** を説明する初期値です。

新規プロジェクトへ適用したら、AI が誤ってこのテンプレートの説明を実プロジェクトの Source of Truth として扱わないよう、最初に以下を実施してください。

1. `docs/specifications/` をプロジェクト固有の要件へ置き換える
2. `docs/architecture/` をプロジェクト固有の構成へ置き換える
3. `docs/api/` を実際の API / Data Contract へ置き換える
4. `docs/development/` を実際のセットアップ・Build・Test・CI 手順へ更新する
5. `.github/workflows/ci.yml` の `format-lint` / `test` / `build` プレースホルダーを実コマンドへ置き換える

特に 5 は必須です。テンプレート初期状態の CI は、Repository / Documentation / Contract Validation は実行しますが、Format / Lint / Test / Build はプレースホルダー通知のみです。

---

## Issue Template の使い分け

このテンプレートには、通常 issue 向けの 4 テンプレートと、軽量な subtask テンプレートが含まれます。

| テンプレート | 用途 |
|----------|------|
| `.github/ISSUE_TEMPLATE/feature.md` | 機能追加や仕様に基づく実装 |
| `.github/ISSUE_TEMPLATE/bug.md` | 不具合修正 |
| `.github/ISSUE_TEMPLATE/refactoring.md` | 既存 Behavior を維持する改善 |
| `.github/ISSUE_TEMPLATE/architecture.md` | Architecture / Public Interface に影響する変更 |
| `.github/ISSUE_TEMPLATE/subtask.md` | 親 issue から切り出した 1 コミット〜数ファイル単位の小さな作業 |

通常 issue では要件・背景・制約を十分に書き、subtask では親 issue を前提に最小限の実装境界だけを明示してください。

---

## AI が安全に進めやすい Issue の書き方

このテンプレートの AI ルールは、issue に書かれた情報を根拠に Scope 判定・Context Loading・Completion Gate を行います。

特に以下を明示すると、AI が不要な確認で止まりにくくなります。

### Scope / Non-Scope

- 何をやるかだけでなく、何をやらないかも書く
- 「ついでにやってよい改善」と「絶対に触らない箇所」を分けて書く
- `.github/policies/change-safety-policy.md` の Restricted Change 判定の前提になる

### Affected Components / Affected Files

- 分かる範囲でよいので、影響範囲を先に書く
- 粒度は「認証まわり」「API client 層」程度でもよい
- `Expected Files vs Actual Changed Files` の確認基準として使える

### Acceptance Criteria

- 曖昧な表現ではなく、検証可能な条件を checkbox で書く
- 例: 「ちゃんと動く」ではなく「X を入力したとき Y が返る」
- Completion Gate はここをそのまま完了条件として使う

### References

- 関連する `docs/specifications/`、`docs/architecture/`、`docs/api/` を明示する
- Progressive Context Loading により、関連リンクがあるほど AI が正確に必要箇所だけを読める

### Restricted Change の明示

- API / Data Contract / Architecture / Configuration / CI/CD などの Restricted Change を含む場合は issue に明記する
- 例: `この issue では API フィールド追加を含む`
- これがないと、AI は安全側に倒して実装を止めることがある

### Subtask での Notes for AI

- `subtask.md` では親 issue の文脈を短く要約する
- 親 issue の Requirements / Architecture / Constraints のうち、この subtask に必要な部分だけを抜粋する
- subtask 単体でも AI が安全に作業境界を理解しやすくなる

---

## ドキュメント構成

### AI 開発ルール

| ファイル | 役割 |
|----------|------|
| `AGENTS.md` | AIエージェント向け作業手順・基本方針 |
| `CLAUDE.md` | `AGENTS.md` へのポインタ（Claude Code 等向け） |
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

---

## 軽量モードでの導入

このテンプレートは、チーム開発や本番運用まで見据えたフル装備を含みます。

個人開発や小規模プロジェクトでは、まず以下を必須セットとして採用し、必要に応じて拡張できます。

- `AGENTS.md` / `.github/copilot-instructions.md` / `.github/instructions/`
- `docs/specifications/` / `docs/architecture/` / `docs/api/` の最小限の Source of Truth
- `docs/ai/completion-gate.md`
- 実プロジェクト向けに更新した Validation / CI

一方で、`docs/ai/regression-suite.md` や Incident 管理ドキュメントは、運用規模に応じて後から導入しても構いません。

重要なのは、**採用しない要素がある場合は README や関連 docs に明記し、実際の運用とドキュメントを一致させること**です。
