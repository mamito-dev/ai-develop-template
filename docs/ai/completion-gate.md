# Completion Gate

## Purpose

AIが作業完了を報告する前に実行する最終確認。

実装の完了（Implementation Completed）とタスクの完了（Task Completed）を明確に分離し、
既存のValidation・Safety・Instructionsの結果を統合して最終判定を行う。

既存のルール体系（Instructions / Prompts / Skills / Change Safety Policy / Validation）を
再定義するものではなく、それらの結果を「作業完了直前に必ず確認するGate」として統合する。

## Checks

Completion Gateは以下の順序で確認を行う。

```text
1. Acceptance Criteria Verification
2. Existing Validation（Test / Lint / Build 等）
3. Existing Change Safety（.github/policies/change-safety-policy.md）
4. Remaining Blockers / Unresolved Issues
5. Completion Status Decision
```

## Status

| Status | 条件 |
|--------|------|
| `READY_FOR_REVIEW` | 全Acceptance Criteria確認済み / 必須Validation通過 / Safety Policy通過 / Blockerなし |
| `BLOCKED` | 環境・外部依存等により確認・実行できない項目が存在する |
| `FAILED` | 実装またはValidationが明確に失敗している |

未確認の状態を `PASS` として扱わない。

## Rules

- Required ValidationがNOT_RUNの場合、`READY_FOR_REVIEW` として報告しない。
- Required ValidationがFAILの場合、`READY_FOR_REVIEW` として報告しない。
- Change Safety PolicyでFORBIDDEN / VIOLATIONが検出された場合、Completionを停止する。
- Acceptance Criteriaが未達の場合、`READY_FOR_REVIEW` として報告しない。
- 未確認事項を推測によってPASSに変更しない。
- Issue Scope外の改善点はOut-of-Scope Findingsとして記録し、現在のIssueのCompletionを妨げない。

詳細なルールは以下を参照すること。

- Validation Rules: `.github/policies/change-safety-policy.md`
- Change Categories: `.github/change-safety.yml`
- Instructions: `.github/instructions/`
- Prompts: `.github/prompts/`

## Completion Report Format

### READY_FOR_REVIEW

```markdown
## Completion Report

### Status

READY_FOR_REVIEW

### Acceptance Criteria

- AC-01: PASS
- AC-02: PASS

### Validation

- Test: PASS
- Lint: PASS
- Build: PASS

### Change Safety

PASS

### Remaining Issues

None

### Out-of-Scope Findings

None

### Summary

Implementation is complete and ready for review.
```

### BLOCKED

```markdown
## Completion Report

### Status

BLOCKED

### Acceptance Criteria

- AC-01: PASS
- AC-02: BLOCKED

### Validation

- Test: PASS
- Lint: PASS
- Build: BLOCKED

### Change Safety

PASS

### Blockers

- Required external environment is unavailable.

### Remaining Work

- Run the blocked validation.
- Re-evaluate AC-02.

### Summary

The implementation cannot be considered complete until the blocker is resolved.
```

### FAILED

```markdown
## Completion Report

### Status

FAILED

### Acceptance Criteria

- AC-01: PASS
- AC-02: FAIL

### Validation

- Test: FAIL
- Lint: PASS
- Build: NOT_RUN

### Change Safety

PASS

### Failure

The required test suite failed.

### Remaining Work

- Fix the failing test.
- Re-run validation.

### Summary

The task is not complete.
```

## Machine-Readable Configuration

Completion Gateの設定は `.github/change-safety.yml` の `completion` セクションで管理する。

詳細は `.github/change-safety.yml` を参照すること。

## References

- Change Safety Policy: `.github/policies/change-safety-policy.md`
- Machine-Readable Safety Config: `.github/change-safety.yml`
- AI Documentation Manifest: `.github/ai-docs.yml`
- Implementation Skill: `.github/skills/implementation/SKILL.md`
- Implement Issue Prompt: `.github/prompts/implement-issue.prompt.md`
- Coding Instructions: `.github/instructions/coding.instructions.md`
