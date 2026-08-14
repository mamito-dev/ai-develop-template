# Requirements

## Product Purpose

本プロジェクト（`ai-develop-template`）は、GitHub Copilot などの AI エージェントを用いた開発を安定・再現可能にするためのテンプレートリポジトリである。

AI エージェントが仕様・アーキテクチャ・ルールを正しく理解した上で実装できるよう、以下の基盤を提供する。

- AI への行動指示（`.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/`）
- プロジェクトの Source of Truth ドキュメント群（`docs/`）
- AI の再利用可能なプロンプト（`.github/prompts/`）
- ローカル・CI での自動バリデーション（`scripts/validate/`）

## Scope

- AI エージェント向けのプロジェクト構造・ルールのテンプレートを提供する
- AI が参照する Source of Truth ドキュメントの整備
- ローカルおよび CI での Validation の仕組みの提供
- GitHub Copilot Coding Agent が利用するプロンプト・インストラクションの整備

## Non-Scope

- 特定のアプリケーションビジネスロジックの実装
- 本番環境へのデプロイ基盤
- データベースやバックエンドサービスの提供
- エンドユーザー向け UI の提供

## Functional Requirements

### FR-001

**Requirement:** AI エージェントへの行動指示の提供

**Description:**
GitHub Copilot および AI エージェントが、リポジトリ内の指示ファイルを参照することで、プロジェクト固有のルール・制約・作業手順に従って動作できる。

**Acceptance Criteria:**

- [ ] `.github/copilot-instructions.md` が存在し、AI の基本行動方針が定義されている
- [ ] `AGENTS.md` が存在し、AI エージェントの作業手順が定義されている
- [ ] `.github/instructions/` に個別ルールファイルが存在する

---

### FR-002

**Requirement:** Source of Truth ドキュメントの提供

**Description:**
AI エージェントが実装時に参照できる、仕様・アーキテクチャ・API Contract・開発手順のドキュメントが整備されている。

**Acceptance Criteria:**

- [ ] `docs/specifications/requirements.md` が存在し、要件が明文化されている
- [ ] `docs/specifications/business-rules.md` が存在し、ビジネスルールが明文化されている
- [ ] `docs/architecture/overview.md` が存在し、アーキテクチャが明文化されている
- [ ] `docs/api/api-contract.md` が存在し、API Contract が定義されている
- [ ] `docs/development/` 以下に setup / build / test / troubleshooting が存在する

---

### FR-003

**Requirement:** ローカル・CI での自動バリデーション

**Description:**
リポジトリ構造・ドキュメント構造・API Contract の整合性を、ローカルおよび CI で自動検証できる。

**Acceptance Criteria:**

- [ ] `./scripts/validate.sh` で全バリデーションが実行できる
- [ ] GitHub Actions CI で同等のバリデーションが実行される
- [ ] バリデーション失敗時に具体的なエラーメッセージが出力される

---

### FR-004

**Requirement:** 再利用可能なプロンプトの提供

**Description:**
AI エージェントが実装・調査・レビュー・バグ修正・テスト作成を行う際に利用できる、標準化されたプロンプトが提供される。

**Acceptance Criteria:**

- [ ] `.github/prompts/` に用途別のプロンプトファイルが存在する
- [ ] 各プロンプトが、AI の参照順序（Requirements → Architecture → Code）を遵守している

---

### FR-005

**Requirement:** 未確定事項の明示

**Description:**
仕様・アーキテクチャ・ルールが未確定の場合、AI が推測で判断しないよう、未確定事項を明示する仕組みが存在する。

**Acceptance Criteria:**

- [ ] 未確定事項は `TODO`、`OPEN`、`Open Questions` セクションで明示される
- [ ] AI が `TODO` を確定済み仕様として扱わないルールが `AGENTS.md` に記載されている

## Future Requirements

- FR-101: AI エージェントの作業ログ・監査証跡の仕組み
- FR-102: 複数プロジェクトへのテンプレート適用を支援するスクリプト
- FR-103: AI が生成したコードの品質スコアリング

## Out of Scope

- 特定のプログラミング言語・フレームワークへの依存
- 本番環境向けインフラ構成
- エンドユーザー向け機能の実装
