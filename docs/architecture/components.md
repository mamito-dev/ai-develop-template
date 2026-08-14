# Components

## Component: AI Instructions

### Purpose

AI エージェントに対して、プロジェクトの基本行動方針・作業手順・禁止事項を伝達する。

### Responsibilities

- AI の基本行動ルールの定義（`.github/copilot-instructions.md`）
- AI エージェントの作業手順の定義（`AGENTS.md`）
- 個別ルール（API・Architecture・Coding・Git・Testing）の定義（`.github/instructions/`）

### Non-Responsibilities

- 具体的な機能要件の定義（→ `docs/specifications/requirements.md` が担当）
- アーキテクチャの定義（→ `docs/architecture/` が担当）
- API Contract の定義（→ `docs/api/api-contract.md` が担当）

### Inputs

- プロジェクト固有のルール・制約・作業方針

### Outputs

- AI エージェントへの行動指示

### Dependencies

- なし（他のコンポーネントに依存しない）

### Lifecycle

- プロジェクト開始時に定義し、ルール変更時に更新する
- AI エージェントが参照するたびに読み込まれる

### Error Handling

- ルールに矛盾がある場合、AI は矛盾を報告し判断を求める

### Testing Strategy

- `scripts/validate/validate-repository.sh` で存在確認
- 内容の整合性はレビューによる確認

---

## Component: Specifications

### Purpose

プロジェクトの要件・ビジネスルール・非機能要件の Source of Truth を提供する。

### Responsibilities

- 機能要件の定義と識別子（FR-xxx）の付与
- ビジネスルールの定義と識別子（BR-xxx）の付与
- 非機能要件の定義と識別子（NFR-xxx）の付与
- 未確定事項（Open Questions）の明示

### Non-Responsibilities

- アーキテクチャの詳細定義（→ `docs/architecture/` が担当）
- API の詳細仕様（→ `docs/api/api-contract.md` が担当）
- 実装コードの管理

### Inputs

- プロダクトオーナー・ステークホルダーからの要求

### Outputs

- 各要件の識別子・説明・受け入れ基準
- AI が参照できる確定済み仕様

### Dependencies

- なし（他のドキュメントコンポーネントに依存しない）

### Lifecycle

- 要件確定時に更新する
- 未確定事項は `TODO`・`OPEN` で管理し、確定後に更新する

### Error Handling

- 要件間に矛盾がある場合、AI は矛盾を報告し判断を求める

### Testing Strategy

- `scripts/validate/validate-docs.sh` で構造確認
- 要件の整合性はレビューによる確認

---

## Component: Architecture Docs

### Purpose

プロジェクトのアーキテクチャ・コンポーネント責務・データフローの Source of Truth を提供する。

### Responsibilities

- システム全体のアーキテクチャ図・説明の定義（`overview.md`）
- 各コンポーネントの責務・非責務・依存関係の定義（`components.md`）
- 主要な処理フロー・データフローの定義（`data-flow.md`）
- アーキテクチャ上の制約・禁止パターンの定義

### Non-Responsibilities

- 機能要件の定義（→ `docs/specifications/` が担当）
- API の詳細仕様（→ `docs/api/api-contract.md` が担当）
- 実装コードの管理

### Inputs

- アーキテクチャ設計の意思決定

### Outputs

- AI がコードを追加する際の「どこに実装するか」の判断基準
- コンポーネント間の責務境界

### Dependencies

- `docs/specifications/` （要件に基づいてアーキテクチャを定義する）

### Lifecycle

- アーキテクチャ変更時に更新する
- 変更は承認済みの意思決定（Architectural Decision）として記録する

### Error Handling

- 既存コードとアーキテクチャドキュメントが矛盾する場合、AI は矛盾を報告し判断を求める

### Testing Strategy

- `scripts/validate/validate-docs.sh` で構造確認
- アーキテクチャの整合性はレビューによる確認

---

## Component: API Contract

### Purpose

API・データ Contract の Source of Truth を提供する。

### Responsibilities

- Endpoint・HTTP メソッド・リクエスト・レスポンス・エラーの定義
- 認証方式・バリデーション・後方互換性方針の定義
- Contract 変更時の影響範囲の記録

### Non-Responsibilities

- 実装コードの管理
- アーキテクチャの定義（→ `docs/architecture/` が担当）

### Inputs

- API 設計の意思決定・仕様確定

### Outputs

- 実装者（人・AI）が参照できる API の正式仕様
- 後方互換性の判断基準

### Dependencies

- `docs/specifications/` （要件に基づいて API を定義する）
- `docs/architecture/` （アーキテクチャに基づいて API を設計する）

### Lifecycle

- API 変更時に更新する
- 破壊的変更の場合は、バージョニング・互換期間を明示する

### Error Handling

- 実装と Contract が矛盾する場合、AI は矛盾を報告し判断を求める

### Testing Strategy

- `scripts/validate/validate-contracts.sh` で存在・構造確認
- Contract の整合性はレビューによる確認

---

## Component: Development Docs

### Purpose

開発者・AI エージェントが、セットアップ・ビルド・テスト・トラブルシューティングを実行できる手順を提供する。

### Responsibilities

- 開発環境のセットアップ手順（`setup.md`）
- ビルド手順（`build.md`）
- テスト実行手順（`test.md`）
- 既知の問題と解決方法（`troubleshooting.md`）
- CI 設定の説明（`ci.md`）

### Non-Responsibilities

- 機能要件の定義（→ `docs/specifications/` が担当）
- アーキテクチャの定義（→ `docs/architecture/` が担当）

### Inputs

- 実際に動作する開発コマンド・手順

### Outputs

- 開発者・AI が実行できる具体的なコマンド

### Dependencies

- `scripts/validate/`（バリデーションコマンドを参照する）

### Lifecycle

- 開発環境・ツールが変更された場合に更新する

### Error Handling

- 手順が動作しない場合は `troubleshooting.md` に記録する

### Testing Strategy

- 実際のコマンドを実行して動作確認する

---

## Component: Validation Scripts

### Purpose

リポジトリ構造・ドキュメント構造・API Contract の整合性を自動検証する。

### Responsibilities

- 必須ファイル・ディレクトリの存在確認
- Markdown の Code Fence・Broken Link の検証
- API Contract ファイルの存在確認
- GitHub Actions での CI 実行

### Non-Responsibilities

- アプリケーションコードの Lint・Build・Test（プロジェクト固有の追加が必要）
- ドキュメント内容の意味的正確性の検証（レビューによる確認が必要）

### Inputs

- リポジトリのファイル構造・Markdown ファイル

### Outputs

- PASS / FAIL の結果とエラーメッセージ

### Dependencies

- bash 4.x 以上

### Lifecycle

- CI での自動実行（GitHub Actions）
- ローカルでの手動実行（`./scripts/validate.sh`）

### Error Handling

- エラー発生時は具体的なファイルパス・行番号・対処方法を出力する

### Testing Strategy

- 必須ファイルを削除した状態でスクリプトを実行し、エラーが検出されることを確認する
