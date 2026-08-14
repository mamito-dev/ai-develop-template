---
applyTo: "**/*"
---

# API Instructions

このファイルは、AIによるAPI / Data Contractの意図しない破壊を防止するための個別ルールを定義する。

## このファイルの責務

- Contractとして扱う対象の明確化
- 無承認で変更してはいけない項目の定義
- Contract変更時の進め方
- Backward Compatibilityの考え方

実装手順は `AGENTS.md`、変更管理は `git.instructions.md` を参照すること。

## Contract対象

以下をContractとして扱う。

- Endpoint
- HTTP Method
- Request
- Response
- Field Name
- Field Type
- Required / Optional
- Error Response
- Status Code
- Serialized Data
- Event / Message
- Shared DTO / Model

## 禁止事項

AIは明示的な仕様変更なしに、以下を行わない。

- Field Rename
- Field削除
- Field Type変更
- Required / Optional変更
- Error形式変更
- Status Code変更
- Endpoint変更
- Request形式変更
- Response形式変更

## Contract変更

API変更が必要になった場合は、以下の順序で扱う。

Current Contract
↓
Affected Consumers
↓
Compatibility Impact
↓
Approved Change
↓
Implementation
↓
Tests

仕様・利用者・互換性影響を説明できない場合は、実装前に確認を求めること。

## Backward Compatibility

既存Consumerが存在する場合、破壊的変更を避ける。

破壊的変更が必要な場合は、少なくとも以下を明確にする。

- Migration
- Versioning
- Compatibility period
