---
description: "Implement a GitHub Issue following project rules, specifications, architecture, contracts, tests, and validation requirements."
---

# Implement Issue

## Objective

Implement the requested GitHub Issue while preserving the project's requirements, architecture, contracts, and existing behavior.

## Phase 1: Understand the Issue

Read:

1. GitHub Issue
2. Acceptance Criteria
3. Related Requirements
4. Related Business Rules
5. Related Architecture
6. Related API/Data Contract

Determine:

- required behavior
- affected components
- expected outputs
- constraints
- explicit non-goals

Do not implement yet.

## Phase 2: Investigate Existing Code

Search for:

- related components
- similar implementations
- existing services
- existing repositories
- existing utilities
- API clients
- related tests

Prefer existing patterns when they satisfy the requirement.

Do not create duplicate abstractions without justification.

## Phase 3: Define the Implementation Plan

Before editing code, identify:

1. files to change
2. files to add
3. files to remove, if any
4. implementation approach
5. test strategy
6. validation commands

If the plan requires an architectural or contract change, stop and report it before implementation.

Before modifying files:

1. Determine the Issue scope.
2. Classify planned changes.
3. Check `.github/policies/change-safety-policy.md`.
4. Do not perform Restricted changes without explicit scope or approval.
5. Do not perform Forbidden changes.
6. Stop when a required change is UNKNOWN.

## Phase 4: Implement

Implement the smallest change that satisfies the Issue.

Rules:

- preserve existing architecture
- preserve existing contracts
- avoid unrelated refactoring
- reuse existing abstractions
- maintain existing error handling conventions
- do not introduce speculative functionality

## Phase 5: Test

Add or update tests for the changed behavior.

Consider:

- happy path
- invalid input
- boundary conditions
- expected errors
- regression cases

## Phase 6: Validate

Run the relevant:

- tests
- lint
- formatter
- build
- contract validation

Only report a check as successful if it was actually executed.

## Phase 7: Review the Diff

Inspect the final diff.

Verify:

- all changes are related to the Issue
- no accidental files were changed
- no secrets were introduced
- no unrelated formatting changes exist
- no existing behavior was unintentionally removed

## Completion Report

Report:

### Summary

What was implemented.

### Changed Files

List the changed files.

### Tests

Commands executed and results.

### Build

Command executed and result.

### Lint / Format

Commands executed and results.

### Remaining Issues

Any unresolved problems or decisions.

### Scope

Confirm whether unrelated changes were avoided.

## Phase 8: Completion Gate

Before reporting the task as complete, run the Completion Gate defined in `docs/ai/completion-gate.md`.

Do not report `READY_FOR_REVIEW` when:

- required Acceptance Criteria are not satisfied;
- required validation has failed;
- required validation has not been run;
- an existing safety validation has failed;
- a blocking issue remains.

Report blockers and failures explicitly using the Completion Report format defined in `docs/ai/completion-gate.md`.
