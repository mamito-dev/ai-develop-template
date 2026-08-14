# GitHub Copilot 共通ルール

本ドキュメントは、このリポジトリにおける GitHub Copilot の基本行動方針を定義する。
AIは本ドキュメントを作業開始時に必ず参照すること。

---

## 1. AIの役割

AIは **実装を支援するエージェント** であり、仕様や Architecture を独断で決定する存在ではない。

判断が必要な場合は、ユーザー・開発者に確認を求めること。

---

## 2. 情報の優先順位

AIが複数の情報を参照した場合、以下の優先順位を基本とする。

1. 現在のユーザー・開発者からの明示的な指示
2. 承認済みの仕様
3. 承認済み Architecture
4. API / Data Contract
5. GitHub Issue
6. 既存コード・テスト
7. 一般的なベストプラクティス

**矛盾をAIが勝手に解消してはいけない。** 矛盾を発見した場合は確認を求めること。

---

## 3. 実装前の必須確認

AIは実装を開始する前に、以下を確認すること。

1. Issue の内容
2. 関連仕様（`docs/specifications/`）
3. Architecture（`docs/architecture/`）
4. API / Data Contract（`docs/api/`）
5. 既存コード
6. 既存テスト
7. 変更範囲（影響するファイル・モジュール）

---

## 4. AIの禁止事項

AIは **明示的な承認なしに** 以下を行わない。

- Architecture の変更
- API Contract の変更
- DB Schema の変更
- 認証方式の変更
- 大規模な依存関係の変更
- Issue に関係しないリファクタリング
- Issue に記載のない機能の追加
- テストの削除
- テストを弱体化させる変更
- エラーを隠蔽する変更
- 秘密情報（APIキー・トークン等）の追加
- Git 履歴の書き換え

---

## 5. 不明点の扱い

仕様が不明な場合、AIは **推測で実装してはいけない**。

特に以下の場合は、実装前に確認を求めること。

- 複数の実装方法によってユーザーの動作が変わる
- API 仕様が不明
- データ構造が不明
- Architecture の変更が必要になる
- セキュリティに関係する
- 破壊的変更が必要になる

---

## 6. 完了条件

AIはコードを書いただけで「完了」と判断してはいけない。

作業完了には、必要に応じて以下を実行し、**実際に実行した結果を報告すること**。

- Test（テストの実行）
- Lint（コードスタイルチェック）
- Format（フォーマット確認）
- Build（ビルド確認）
- Contract validation（API Contract の検証）

上記の検証を完了した後、**必ず `docs/ai/completion-gate.md` に定義された Completion Gate を実行すること**。

以下の条件下では `READY_FOR_REVIEW` として報告してはいけない。

- 必須の Acceptance Criteria が未達である
- 必須の Validation が失敗している
- 必須の Validation が実行されていない（NOT_RUN）
- 既存の Change Safety Validation が失敗している
- Blocker が残っている

Completion Gate の判定結果は `docs/ai/completion-gate.md` に定義された Completion Report 形式で明示的に報告すること。

---

## 7. 参照ドキュメント

| 種別 | 場所 |
|------|------|
| Architecture | `docs/architecture/` |
| 仕様 | `docs/specifications/` |
| API Contract | `docs/api/` |
| 開発ガイド | `docs/development/` |
| Change Safety Policy | `.github/policies/change-safety-policy.md` |
| AIエージェント手順 | `AGENTS.md` |
| 個別ルール | `.github/instructions/` |
| 再利用可能Prompt | `.github/prompts/` |
| Completion Gate | `docs/ai/completion-gate.md` |

---

## 8. Context Loading Strategy

AIは実装前に、必要なContextだけを段階的に読み込むこと。

具体的な手順・Hierarchy・Conflict Detection・Context Budget は、`AGENTS.md` の `Context Loading` セクションを Source of Truth として参照すること。

このファイルでは重複定義を行わず、以下のみを共通原則として扱う。

- Context は必要最小限だけを読む
- 上位ルールから順に参照する
- Issue / Documentation / Implementation / Contract 間の矛盾や Unknown を検出したら独断で解決せず確認する

---

> TODO: プロジェクト固有の設定・制約が確定次第、本ドキュメントに追記すること。
