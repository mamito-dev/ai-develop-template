# Build

このテンプレートリポジトリはアプリケーションコードを持たないため、ビルド手順は存在しない。

実際のプロジェクトへの適用時は、以下のテンプレートをベースにプロジェクト固有のビルド手順を記述すること。

---

## Development Build

```bash
# TODO: プロジェクト固有のビルドコマンドを記述する
# 例:
# npm run build
# go build ./...
# ./gradlew build
```

## Production Build

```bash
# TODO: プロジェクト固有のリリースビルドコマンドを記述する
# 例:
# npm run build:prod
# go build -ldflags="-s -w" ./...
```

## Expected Result

```
# TODO: 成功時の期待される出力を記述する
```

## Common Build Problems

### 問題: バリデーションスクリプトが Permission Denied になる

**原因:** スクリプトに実行権限がない

**解決方法:**

```bash
chmod +x scripts/validate.sh
chmod +x scripts/validate/*.sh
```
