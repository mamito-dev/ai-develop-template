---
applyTo: "**/*"
---

# Testing Instructions

このファイルは、AIが変更したBehaviorをTestで検証し、問題を隠すためのTest変更を防ぐための個別ルールを定義する。

## このファイルの責務

- Test追加・更新の判断基準
- Test観点
- 既存Test変更時の制約
- Test品質の基準

実装方針は `coding.instructions.md`、API契約の検証は `api.instructions.md` を参照すること。

## 基本方針

Behavior変更に対して、必要に応じて以下をテストする。

- 正常系
- 異常系
- 境界値
- Invalid Input
- Error Handling
- Regression

既存のTest基盤がある場合はそれに従い、基盤がない場合はIssueの範囲を超えて新しいTest手段を持ち込まない。

## Existing Test

AIは以下を行ってはいけない。

- Test削除によるBuild/Test成功
- Assertionを弱くする
- TestをSkipする
- Test条件を不当に緩める
- 実装に合わせるためだけにTestを書き換える

## Specificationとの関係

既存Testが仕様を表している場合、Testを変更する前に以下を確認する。

- なぜ変更が必要なのか
- 新しい仕様は何か
- 何を保証するTestになるのか

不明な場合は、推測でTestを変更しない。

## Test品質

Testは可能な限り以下を重視する。

- deterministic
- 独立性
- 明確な失敗理由
- 外部から観測可能なBehavior

Implementation Detailだけをテストすることは避ける。
