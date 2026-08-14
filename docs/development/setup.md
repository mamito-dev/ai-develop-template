# Development Setup

## Prerequisites

以下の環境が必要である。

- OS: Linux / macOS / Windows（WSL2 推奨）
- Git 2.x 以上
- bash 4.x 以上

## Required Tools

| Tool | Version | Notes |
|------|---------|-------|
| Git | 2.x 以上 | バージョン管理 |
| bash | 4.x 以上 | バリデーションスクリプトの実行 |

このテンプレートリポジトリは、アプリケーションコードを持たないため、追加のランタイム（Node.js・Python 等）は不要である。

## Installation

```bash
# リポジトリをクローン
git clone https://github.com/mamito-dev/ai-develop-template.git
cd ai-develop-template
```

## Configuration

特別な設定は不要である。

クローン後すぐにバリデーションスクリプトを実行できる。

## Environment Variables

このテンプレートリポジトリでは、環境変数は不要である。

実際のプロジェクトに適用する場合は、プロジェクト固有の環境変数をここに記載すること。

| Variable | Required | Description |
|----------|----------|-------------|
| （なし） | - | - |

## Run Locally

### バリデーションの実行

```bash
# すべてのバリデーションを実行
./scripts/validate.sh

# または個別に実行
./scripts/validate.sh repository   # リポジトリ構造の検証
./scripts/validate.sh docs         # ドキュメント検証
./scripts/validate.sh contracts    # API Contract 検証
```

### 期待される結果

```
========================================================
  Local Validation
  Repository: /path/to/ai-develop-template
  Target: all
========================================================
✅ Repository Validation: PASS
✅ Documentation Validation: PASS
✅ Contract Validation: PASS
========================================================
✅ All Validations: PASS
```
