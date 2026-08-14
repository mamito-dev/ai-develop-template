---
applyTo: "**/*"
---

# Coding Instructions

このファイルは、AIがコードを実装するときの品質・可読性・保守性・変更範囲に関する個別ルールを定義する。

## このファイルの責務

- 実装時の基本原則
- 禁止する実装パターン
- Error Handlingの扱い
- Dependency追加時の判断基準

Architecture判断は `architecture.instructions.md`、Test設計は `testing.instructions.md` を参照すること。

## 基本ルール

AIは以下を優先する。

1. 既存プロジェクトの実装パターン
2. 明確な責務
3. 可読性
4. テスト容易性
5. シンプルさ
6. 必要最小限の変更

## 禁止事項

以下を無条件に行わない。

- 不要な抽象化
- 過剰な汎用化
- 将来のためだけの機能追加
- Issueと無関係なリファクタリング
- 同じ責務を持つUtilityの重複作成
- エラーの握りつぶし
- 不要なGlobal State
- 不要な依存ライブラリ追加

## Error Handling

- Errorを無視しない
- Error contextを失わない
- 意図しないfallbackを作らない
- Broad catchを安易に使用しない
- Errorを隠すことでBuild/Testを成功させない

## Dependency

新しいDependencyを追加する前に、以下を確認する。

1. 既存コードで対応できないか
2. Framework / Standard Libraryで対応できないか
3. 既存Dependencyで対応できないか
4. 新Dependencyの必要性がIssueにあるか

上記を満たせない場合は、追加前に確認を求めること。

## Completion Gate

作業完了を報告する前に、`docs/ai/completion-gate.md` に定義されたCompletion Gateを実行すること。

`READY_FOR_REVIEW` の判定条件、および Blocker / Failure の報告形式は `docs/ai/completion-gate.md` を Source of Truth とする。
