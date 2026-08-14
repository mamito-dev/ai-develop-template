# Test

## Validation（バリデーション）

このテンプレートリポジトリのテストは、バリデーションスクリプトとして提供される。

### 全バリデーション実行

```bash
./scripts/validate.sh
```

### 個別バリデーション

```bash
# リポジトリ構造の検証
./scripts/validate.sh repository

# ドキュメントの検証（Markdown 構造・Broken Link）
./scripts/validate.sh docs

# API Contract の検証
./scripts/validate.sh contracts
```

### 期待される結果

```
========================================================
✅ All Validations: PASS
========================================================
```

---

## Unit Test

このテンプレートリポジトリはアプリケーションコードを持たないため、Unit Test は存在しない。

実際のプロジェクトへの適用時は、以下のテンプレートをベースに記述すること。

```bash
# TODO: プロジェクト固有の Unit Test コマンドを記述する
# 例:
# npm test
# go test ./...
# pytest
```

## Integration Test

```bash
# TODO: プロジェクト固有の Integration Test コマンドを記述する
```

## Full Test Suite

```bash
# TODO: 全テストを実行するコマンドを記述する
```

## Lint

```bash
# TODO: プロジェクト固有の Lint コマンドを記述する
# 例:
# npm run lint
# golangci-lint run
# flake8
```

## Format

```bash
# TODO: プロジェクト固有のフォーマットコマンドを記述する
# 例:
# npm run format
# gofmt -w .
# black .
```

## CI Equivalent

ローカルでの全バリデーション実行は、CI と同等の結果を提供する。

```bash
./scripts/validate.sh
```
