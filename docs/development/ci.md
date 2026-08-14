# CI / Automated Validation

## Purpose

このリポジトリでは GitHub Actions を利用して、AI が作成した Pull Request に対して自動 Validation を実行します。

CI は単なる情報提供ではなく、**Merge 判断のための品質ゲート**として機能します。

```text
AI Implementation
      ↓
Pull Request
      ↓
Automated Validation (GitHub Actions)
      ↓
   PASS / FAIL
      ↓
PASS → Review → Merge
FAIL → AI investigates → Fix → CI
```

---

## Validation 一覧

| Validation | ワークフロー | 目的 |
| --- | --- | --- |
| Repository Structure | `ci.yml` | 必須ファイル・ディレクトリの存在確認 |
| Documentation | `documentation.yml` | Markdown 構文・Broken Link・doc 構造 |
| Markdown | `documentation.yml` | Code Fence・見出し・リスト構文 |
| Broken Link | `documentation.yml` | 相対リンクが有効か検証 |
| Format Check | `ci.yml` | Formatter によるスタイル確認 |
| Lint | `ci.yml` | 構文エラー・コーディング規約違反 |
| Unit Test | `ci.yml` | ユニットテストの実行 |
| Build | `ci.yml` | ビルドの成否確認 |
| Secret Detection | `security.yml` | API Key・Token 等の混入検出 |
| Dependency 変更検出 | `security.yml` | 無承認の依存関係追加の検出 |
| API Contract | `ci.yml` | Contract ファイルの整合性確認 |

---

## Local Validation

CI と同じ Validation をローカルで実行できます。

```bash
# 全 Validation を実行
./scripts/validate.sh

# Repository 構造のみ
./scripts/validate.sh repository

# Documentation のみ
./scripts/validate.sh docs

# API Contract のみ
./scripts/validate.sh contracts
```

**原則として、`git push` 前にローカル Validation を実行してください。**

---

## Pull Request

Pull Request を作成すると、以下の Validation が自動で実行されます。

- Repository Validation
- Documentation Validation（Markdown・Broken Link）
- Format Check
- Lint
- Unit Test
- Build
- Secret Detection
- Dependency 変更検出
- API Contract Validation

全 Validation が PASS した場合に Review を依頼してください。

---

## Main Branch

`main` ブランチへの Push でも CI が実行されます。

Main Branch Protection として、以下を推奨します。

- CI PASS を Merge 条件にする
- Required Reviewer を設定する
- AI による直接 Push を禁止する

---

## Failure Handling

### CI が FAIL した場合

1. **原因確認**: GitHub Actions のログを確認する
2. **スコープ確認**: Issue の変更範囲と一致しているか確認する
3. **ローカル再現**: `./scripts/validate.sh` でローカル再現を試みる
4. **最小修正**: 最小限の変更で修正する
5. **再実行**: Push して CI を再実行する

### NG 対応

以下の対応は禁止されています。

- テストを削除して CI を通す
- Lint Rule を無効化する
- Security Scan を無効化する
- `continue-on-error: true` を無断で追加する
- Validation 対象からファイルを除外する

### CI Override

例外的に CI をオーバーライドする場合は、以下を記録してください。

- Override の理由
- 影響範囲
- 対応予定（Issue 番号）

---

## Override ルール

CI Override は原則として人間のレビュアーが判断します。

AI は以下の状況でも CI を回避しようとしてはいけません。

- マージ期限が迫っている
- 「些細な変更」だと判断した
- エラーの原因がわからない

---

## Architecture Validation

`docs/architecture/overview.md` に `Forbidden Dependencies` を定義することで、
Architecture ルールを CI で検証できます。

プロジェクト固有の Architecture Validation が必要な場合は、
`scripts/validate/` にスクリプトを追加し、`ci.yml` から呼び出してください。

---

## 技術スタック固有の Validation 追加方法

本 CI はテンプレートです。プロジェクトの技術スタックに応じて以下を追加してください。

### Format Check を追加する例

```yaml
# .github/workflows/ci.yml の format-lint ジョブに追加
- name: Format Check
  run: npm run format:check
```

### カスタム Validate スクリプトを追加する例

```bash
# scripts/validate/validate-lint.sh を作成
# scripts/validate.sh の "all" ケースに追加
run_validate "Lint" "validate-lint.sh"
```

---

## 参考

- [Repository Structure Validation](../../scripts/validate/validate-repository.sh)
- [Documentation Validation](../../scripts/validate/validate-docs.sh)
- [Contract Validation](../../scripts/validate/validate-contracts.sh)
- [Local Validation Entry Point](../../scripts/validate.sh)
- [CI Workflow](../../.github/workflows/ci.yml)
- [Documentation Workflow](../../.github/workflows/documentation.yml)
- [Security Workflow](../../.github/workflows/security.yml)
