# Business Rules

## BR-001

### Rule

AI エージェントは、`.github/copilot-instructions.md`、`AGENTS.md`、`.github/instructions/` に定義されたルールを、他のどの情報よりも優先して遵守する。

### Reason

AI が独自の判断でルールを無視することを防ぎ、プロジェクトの一貫した開発フローを維持するため。

### Examples

- ルールにより「Architecture を無承認で変更してはいけない」と定義されている場合、AI は必ず確認を求める
- ルールに従い、Issue に記載のない機能を独断で追加しない

### Exceptions

- 明示的なユーザー指示がある場合は、ユーザー指示を優先する（ただし禁止事項は除く）

---

## BR-002

### Rule

AI エージェントは、ドキュメント（仕様・アーキテクチャ・API Contract）と既存コードが矛盾している場合、独断でどちらかを正解と判断してはならない。

### Reason

矛盾を放置したまま実装を進めると、仕様・コードの乖離が拡大し、将来的な保守コストが増大するため。

### Examples

- アーキテクチャドキュメントが `Service → Repository → Database` と定義されているが、既存コードが `Service → Database` の場合 → 矛盾を報告し、判断を求める
- API Contract が `POST /users` を定義しているが、実装が `POST /user` になっている場合 → 矛盾を報告し、判断を求める

### Exceptions

- ドキュメントに `TODO` や `OPEN` と明記されている未確定箇所については、既存コードを参考情報として報告してよい

---

## BR-003

### Rule

AI エージェントは、仕様が未確定（`TODO`、`TBD`、`OPEN`）の場合、推測で実装してはならない。

### Reason

推測による実装は、後から発覚した場合の修正コストが大きく、品質の予測可能性を損なうため。

### Examples

- `requirements.md` に `TODO` と書かれた要件は、確定仕様として扱わない
- `api-contract.md` に `TODO` と書かれた Endpoint は、実装対象としない

### Exceptions

- ユーザーが明示的に「TODO のまま仮実装してよい」と指示した場合のみ許可する

---

## BR-004

### Rule

AI エージェントは、Issue に記載されていない機能・リファクタリング・アーキテクチャ変更を、無承認で行ってはならない。

### Reason

スコープ外の変更は、レビューコスト増大・予期しないデグレードの原因となるため。

### Examples

- Issue が「バリデーションのエラーメッセージを修正する」である場合、無関係なファイルのフォーマットを変更しない
- Issue が「README を更新する」である場合、ソースコードを変更しない

### Exceptions

- Issue に直接起因するバグ・セキュリティ脆弱性は、スコープ内として対応してよい

---

## BR-005

### Rule

ドキュメントを変更する場合、変更内容と実装が一致していることを確認する。

### Reason

ドキュメントとコードの乖離は、AI が誤った情報を参照する原因となるため。

### Examples

- アーキテクチャを変更した場合、`docs/architecture/overview.md` を更新する
- API を変更した場合、`docs/api/api-contract.md` を更新する

### Exceptions

- 将来要件として明示している箇所は、実装前にドキュメントを先行して更新してよい

---

## Open Questions

### OQ-001

**Question:**
複数の AI エージェントが同時に同一リポジトリで作業する場合の競合解決ルールをどうするか？

**Status:** OPEN

**Decision:** TODO

---

### OQ-002

**Question:**
テンプレートをプロジェクトに適用する際、どのドキュメントをプロジェクト固有に書き換え必須とするか？

**Status:** OPEN

**Decision:** TODO
