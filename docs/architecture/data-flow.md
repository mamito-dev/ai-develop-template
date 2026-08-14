# Data Flow

## Primary Flow

AI エージェントが Issue に基づいて実装を行う際の基本的なデータフローを定義する。

```text
GitHub Issue
    ↓
AI エージェントが Issue を確認
    ↓
AI Instructions 参照
(.github/copilot-instructions.md / AGENTS.md / .github/instructions/)
    ↓
Source of Truth ドキュメント参照
(docs/specifications/ → docs/architecture/ → docs/api/)
    ↓
既存コード・テスト参照
    ↓
影響範囲の確認
    ↓
実装
    ↓
テスト実行
    ↓
バリデーション実行 (./scripts/validate.sh)
    ↓
PR 作成・レビュー
    ↓
CI 実行 (GitHub Actions)
    ↓
マージ
```

---

## Flow: AI エージェントの参照フロー

### Trigger

AI エージェントが Issue を受け取り、実装を開始する。

### Step 1: AI Instructions の確認

AI エージェントは最初に以下を確認する。

- `.github/copilot-instructions.md`（基本行動方針）
- `AGENTS.md`（作業手順）
- `.github/instructions/`（個別ルール）

### Step 2: Source of Truth の確認

Issue に関連する範囲で以下を順番に確認する。

1. `docs/specifications/requirements.md`（機能要件）
2. `docs/specifications/business-rules.md`（ビジネスルール）
3. `docs/architecture/overview.md`（アーキテクチャ）
4. `docs/architecture/components.md`（コンポーネント責務）
5. `docs/architecture/data-flow.md`（データフロー）
6. `docs/api/api-contract.md`（API Contract）

### Step 3: 既存コード・テストの確認

ドキュメントを確認した後、既存コード・テストを参照する。

### Step 4: 矛盾の検出

ドキュメントと既存コードに矛盾がある場合、実装を開始せずに矛盾を報告する。

### Step 5: 実装

Issue のスコープ内で最小限の変更を実装する。

### Error Flow

- 仕様が未確定（`TODO`、`OPEN`）の場合 → 推測せず確認を求める
- ドキュメントとコードが矛盾する場合 → 矛盾を報告し判断を求める
- Issue スコープ外の変更が必要になった場合 → 無承認で実装せず確認を求める

---

## Flow: バリデーション実行フロー

### Trigger

開発者または CI が `./scripts/validate.sh` を実行する。

### Step 1: Repository Validation

`scripts/validate/validate-repository.sh` が実行される。

- 必須ファイルの存在確認（`AGENTS.md`、`.github/copilot-instructions.md` 等）
- 必須ディレクトリの存在確認
- 禁止ファイルの検出
- AI Instructions ファイルの確認

### Step 2: Documentation Validation

`scripts/validate/validate-docs.sh` が実行される。

- `docs/` ディレクトリ構造の確認
- Markdown の Code Fence 検証
- Broken Link 検証
- 必須ドキュメントの内容チェック

### Step 3: Contract Validation

`scripts/validate/validate-contracts.sh` が実行される。

- `docs/api/api-contract.md` の存在確認
- OpenAPI ファイルの検証（存在する場合）
- Contract 変更ルールの確認（CI 環境のみ）

### Error Flow

- 検証エラーが発生した場合 → エラーメッセージとファイルパスを出力し、exit code 1 で終了
- CI でエラーが発生した場合 → PR のマージをブロック

---

## Flow: ドキュメント更新フロー

### Trigger

実装・アーキテクチャ・API の変更が発生する。

### Step 1: 変更の影響範囲の特定

変更によって影響を受けるドキュメントを特定する。

| 変更の種類 | 更新が必要なドキュメント |
|---|---|
| 機能要件の変更 | `docs/specifications/requirements.md` |
| ビジネスルールの変更 | `docs/specifications/business-rules.md` |
| アーキテクチャの変更 | `docs/architecture/overview.md`、`components.md`、`data-flow.md` |
| API の変更 | `docs/api/api-contract.md` |
| 開発手順の変更 | `docs/development/` 内の該当ファイル |

### Step 2: ドキュメントの更新

実装と同じ PR でドキュメントを更新する。

### Step 3: バリデーション実行

`./scripts/validate.sh` でドキュメントの整合性を確認する。

### Error Flow

- ドキュメントの更新漏れがある場合 → レビューで指摘し、更新を求める
