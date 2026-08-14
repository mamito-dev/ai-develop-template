# Non-Functional Requirements

## Performance

### NFR-001

**Requirement:** ローカルバリデーションの実行時間

**Description:** `./scripts/validate.sh` の実行が、標準的な開発マシンで 60 秒以内に完了すること。

**Measurement:** `time ./scripts/validate.sh` で計測

**Target:** 60 秒以内

---

### NFR-002

**Requirement:** CI バリデーションの実行時間

**Description:** GitHub Actions での CI バリデーションが、1 つのワークフローで 5 分以内に完了すること。

**Measurement:** GitHub Actions のジョブ実行時間

**Target:** 5 分以内

---

## Reliability

### NFR-010

**Requirement:** バリデーションの冪等性

**Description:** `./scripts/validate.sh` は同じリポジトリ状態に対して、何度実行しても同じ結果を返すこと（冪等性）。

**Measurement:** 同一コミットに対して複数回実行し、結果が一致することを確認

**Target:** 100% 一致

---

### NFR-011

**Requirement:** ドキュメントの整合性

**Description:** `docs/` 内のすべての Markdown ファイルが、バリデーションスクリプトを通過すること。

**Target:** バリデーションエラー 0 件

---

## Security

### NFR-020

**Requirement:** 秘密情報の非混入

**Description:** リポジトリに API キー・トークン・パスワード等の秘密情報が含まれないこと。

**Target:** シークレットスキャンで検出 0 件

---

### NFR-021

**Requirement:** AI エージェントによる秘密情報の非コミット

**Description:** AI エージェントが生成・提案するコードに、秘密情報が含まれないこと。

**Target:** すべての PR でシークレットスキャンが実行され、検出 0 件

---

## Accessibility

### NFR-030

**Requirement:** ドキュメントの可読性

**Description:** `docs/` 内のドキュメントが、日本語で読める開発者にとって理解しやすい構造であること。

**Target:** 定量指標なし（定性的評価）。ただし、各セクションに目的・具体例が含まれること。

---

## Compatibility

### NFR-040

**Requirement:** GitHub Copilot との互換性

**Description:** `.github/copilot-instructions.md`、`.github/instructions/`、`.github/prompts/` が、GitHub Copilot の仕様に従った形式であること。

**Target:** GitHub Copilot が各ファイルを正常に読み込めること

---

### NFR-041

**Requirement:** シェルスクリプトの互換性

**Description:** `scripts/` 内のスクリプトが、`bash` 4.x 以上で動作すること。

**Target:** Ubuntu 22.04 以上の標準 bash で動作確認済み

---

## Observability

### NFR-050

**Requirement:** バリデーションの出力

**Description:** バリデーションスクリプトが、成功・失敗・警告を明確に区別して出力すること。

**Target:**
- 成功: `✅` プレフィックス
- 失敗: `❌` プレフィックス + 具体的なエラー内容
- 警告: `::warning::` プレフィックス（GitHub Actions 対応）

---

## Maintainability

### NFR-060

**Requirement:** バリデーションスクリプトの拡張性

**Description:** プロジェクト固有のバリデーション（Lint・Build・Test など）を `scripts/validate.sh` に追加できる構造であること。

**Target:** `scripts/validate/` に新しいスクリプトを追加し、`validate.sh` に 1 行追加するだけで組み込めること

---

### NFR-061

**Requirement:** ドキュメントの更新容易性

**Description:** 各ドキュメントのセクション構造が一貫しており、新しい情報を追記しやすい構造であること。

**Target:** 定量指標なし（定性的評価）
