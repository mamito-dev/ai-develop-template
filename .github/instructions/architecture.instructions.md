---
applyTo: "**/*"
---

# Architecture Instructions

このファイルは、AIが既存ArchitectureとComponent責務を壊さずに実装するための個別ルールを定義する。

## このファイルの責務

- 既存Architectureの尊重
- Component責務と依存方向の維持
- 新Component追加時の判断基準
- Architecture変更として扱う範囲の明確化

実装手順は `AGENTS.md`、Repository全体の行動原則は `.github/copilot-instructions.md` を参照すること。

## Architectureの基本原則

AIは以下を優先する。

1. 既存Architectureを優先する
2. 既存の責務境界を尊重する
3. 既存の依存方向を維持する
4. 既存の抽象化を優先的に利用する
5. 同じ責務を持つ新しい仕組みを勝手に作らない

## 新しいComponentを作成する場合

新Componentを追加する前に、以下を確認する。

1. 既存Componentで対応できないか
2. 新Componentの責務は明確か
3. 他Componentとの依存方向は適切か
4. Lifecycleは明確か
5. Test可能な構造になっているか

いずれかを説明できない場合は、実装前に確認を求めること。

## Architecture変更として扱うもの

以下はArchitecture変更として扱う。

- Module構成変更
- Layer構成変更
- Dependency方向変更
- Data ownership変更
- Persistence方式変更
- Networking境界変更
- Authentication境界変更
- Shared infrastructure変更
- 複数Componentが利用するPublic Interface変更

これらはAIが独断で変更してはいけない。

## Architecture変更が必要な場合の行動

Architecture変更が必要になった場合は、実装を開始せずに以下を整理して確認を求める。

- 現在の構成
- 変更が必要な理由
- 影響を受けるComponent
- 依存方向への影響
- 代替案の有無
- 承認が必要な変更点
