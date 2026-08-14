# Change Safety Policy

このドキュメントは、AI エージェントが Issue 対応時に変更してよい範囲と禁止操作を定義する。

## 1. Change Classification

変更は以下のカテゴリに分類する。

- CODE
- TEST
- DOCUMENTATION
- DEPENDENCY
- API
- DATABASE
- ARCHITECTURE
- CONFIGURATION
- SECURITY
- CI_CD
- INFRASTRUCTURE
- GENERATED
- GIT
- DESTRUCTIVE
- UNKNOWN

分類結果は `.github/change-safety.yml` の `changes` を Source of Truth とする。

## 2. Allowed Changes

Issue Scope 内で以下を許可する。

- Source Code の修正
- Test の追加・更新
- 実装に直接関連する Documentation 更新
- 必要最小限の Error Handling / Logging 補強

## 3. Restricted Changes

以下は AI が勝手に Scope 拡張して実施してはいけない。Issue に明示されている場合のみ実施可能。

- Dependency 追加・更新
- API / Data Contract 変更
- Database Schema / Migration 変更
- Architecture 変更
- Configuration 変更
- Security 関連変更
- CI/CD 変更
- Infrastructure 変更
- Generated File 変更
- Public Interface 変更
- 大規模 Refactor

## 4. Forbidden Changes

以下は原則として実施禁止。

- Secret / Credential の取得・出力・埋め込み
- Force Push / History Rewrite
- 破壊的 Git 操作（`git reset --hard`、`git clean -fd` 等）
- Repository 破壊操作（`rm -rf` など）
- 無関係な Scope 外の大規模変更
- Security 機構の無断無効化
- Test 削除や弱体化による不正な CI 通過

## 5. Approval Requirements

Restricted Change は以下の状態で管理する。

- NOT_REQUESTED
- REQUESTED
- APPROVED
- REJECTED

`NOT_REQUESTED` の Restricted Change は実施してはいけない。

## 6. Scope Expansion Rules

実装中に追加変更が必要な場合は次で判定する。

1. この変更は Issue 達成に必須か
2. 必須なら最小範囲で実施する
3. 必須でない改善は実施せず別 Issue として提案する
4. 判断不能（UNKNOWN）は停止して確認する

## 7. File Modification Rules

変更前に `Expected Files` を明確化し、変更後に `Actual Changed Files` と比較する。

- 期待外ファイルが含まれる場合は `Unexpected Changes Detected`
- 無関係なファイル変更は取り消す

## 8. Dependency Rules

Dependency 変更時は必ず以下を満たす。

1. 変更理由を明示
2. 既存依存で代替不可を確認
3. 追加/更新 Version を明示
4. Lockfile 更新有無を確認
5. Test / Build / Diff を実施

## 9. API Rules

API 変更時は以下を確認する。

- Request / Response
- Status Code
- Error Format
- Authentication / Authorization
- Versioning
- Backward Compatibility

Issue に API 変更が明示されない場合は変更しない。

## 10. Database Rules

Database 変更は Restricted とし、以下は原則禁止または明示承認必須。

- DROP TABLE / DROP DATABASE
- TRUNCATE
- 大量 DELETE
- 破壊的 Migration

## 11. Configuration Rules

Configuration 変更は Restricted とする。特に以下は慎重に扱う。

- Production Configuration
- Security Configuration
- Authentication Configuration

## 12. Security Rules

Security 変更は Restricted とする。Issue Scope に Security 修正が明示される場合のみ実施可能。

禁止例:

- 認証の無断無効化
- 認可の削除
- TLS 検証の無効化
- CORS の無制限化

## 13. Generated File Rules

Generated File は原則直接編集しない。

```text
Generator を修正
  ↓
再生成
  ↓
差分確認
```

## 14. Git Operation Rules

通常許可:

- `git status`
- `git diff`
- `git log`
- `git show`
- `git branch`

Restricted:

- `git commit`
- `git merge`
- `git rebase`
- `git cherry-pick`

Forbidden:

- `git push --force`
- `git reset --hard`
- `git clean -fd`
- history rewrite

## 15. Destructive Operation Rules

Issue Scope 外の破壊的操作は実施しない。

- mass file deletion
- mass rename
- database deletion
- history rewrite

必要時は明示承認を要求する。

## 16. Validation Requirements

### Pre-Change Check

- [ ] Issue Scope understood
- [ ] Expected files identified
- [ ] Change category identified
- [ ] Restricted areas identified
- [ ] Forbidden areas identified
- [ ] Required approvals identified
- [ ] Security impact considered
- [ ] Destructive operations avoided

### Post-Change Check

- [ ] Only expected files changed
- [ ] No unrelated files changed
- [ ] No unexpected dependency changes
- [ ] No unexpected API changes
- [ ] No unexpected database changes
- [ ] No unexpected configuration changes
- [ ] No secrets exposed
- [ ] No forbidden operation performed
- [ ] Tests / Validation executed

### Integration

- `.github/copilot-instructions.md` と `AGENTS.md` は本 Policy を参照する
- Prompt / Skill は実装前後で Change Safety Check を実施する
- AI Docs Validator は `.github/ai-docs.yml` 経由で本 Policy を検証対象に含める
- `change-safety.yml` は機械可読の Source of Truth として扱う
