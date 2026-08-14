# API Contract

## Version

v1.0.0（このテンプレートリポジトリはアプリケーション API を持たないため、バリデーション API のみを定義する）

## 概要

`ai-develop-template` はアプリケーション API を提供しない。

本ドキュメントは、**AI エージェントが参照する Source of Truth としての API Contract のテンプレート構造**を定義する。

実際のプロジェクトへの適用時は、このテンプレートをベースに具体的な Endpoint・リクエスト・レスポンスを定義すること。

---

## テンプレート: Endpoint 定義

以下はテンプレートの Endpoint 定義例である。実際のプロジェクトでは、この構造に従って具体的な Endpoint を記述する。

### `GET /example`

#### Purpose

リソース一覧を取得する。

#### Authentication

要認証。 ヘッダーにトークンを指定する。（方式はプロジェクト適用時に決定）

#### Request

```json
{}
```

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | ページ番号（デフォルト: 1） |
| per_page | integer | No | 1ページあたりの件数（デフォルト: 20） |

#### Response 200

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 0
  }
}
```

#### Errors

| Status | Code | Meaning |
|--------|------|---------|
| 400 | INVALID_PARAMETER | リクエストパラメータが不正 |
| 401 | UNAUTHORIZED | 認証トークンが無効または期限切れ |
| 403 | FORBIDDEN | リソースへのアクセス権限がない |
| 500 | INTERNAL_ERROR | サーバー内部エラー |

#### Compatibility

- このエンドポイントは後方互換性を維持する
- フィールドの追加は非破壊的変更として扱う
- フィールドの削除・型変更は破壊的変更として扱い、バージョンアップが必要

---

## Contract 変更ルール

### 非破壊的変更（承認不要）

- レスポンスへの新しいフィールドの追加
- 任意パラメータの追加
- ドキュメントの補足・修正

### 破壊的変更（承認必要）

- フィールドの削除・リネーム
- フィールドの型変更
- Required / Optional の変更
- エラーコードの変更
- HTTP ステータスコードの変更
- Endpoint URL の変更
- HTTP メソッドの変更

### 破壊的変更の手順

1. 影響を受ける Consumer を特定する
2. 互換期間・マイグレーション方法を決定する
3. バージョニング方針を決定する
4. 承認を得る
5. 実装する
6. 本ドキュメントを更新する

---

## Authentication

### 方式

プロジェクト適用時に決定する。（例: ****** Key、OAuth 2.0 など）

### ヘッダー

```
Authorization: ******
```

### 未認証時のレスポンス

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required"
  }
}
```

---

## Validation

- リクエストパラメータのバリデーションは、サーバーサイドで必ず実施する
- バリデーションエラーは HTTP 400 で返す
- エラーレスポンスには、どのフィールドが不正かを含める

---

## Compatibility

- 本 Contract で定義されたすべての Endpoint は、後方互換性を維持することを基本方針とする
- 破壊的変更が必要な場合は、前述の「破壊的変更の手順」に従う

---

## Open Questions

### OQ-001

**Question:** 実際のプロジェクトで API を追加する場合、どの Endpoint から先に定義するか？

**Status:** OPEN（プロジェクト適用時に決定）

**Decision:** TODO
