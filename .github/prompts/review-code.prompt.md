---
description: "Review code against requirements, architecture, contracts, correctness, security, maintainability, and tests."
---

# Review Code

## Objective

Review the requested changes and identify correctness, design, security, testing, and maintainability problems.

Do not modify code unless explicitly requested.

## Phase 1: Understand the Change

Read:

1. Issue
2. Acceptance Criteria
3. Requirements
4. Business Rules
5. Architecture
6. API/Data Contract

Determine what the change is supposed to accomplish.

## Phase 2: Inspect the Diff

Check:

- changed files
- added files
- deleted files
- configuration changes
- dependency changes
- generated files

Identify unrelated changes.

Compare Expected Changes vs Actual Changed Files and verify:

- scope compliant
- no unauthorized dependency/API/database/configuration changes
- no security regression
- no destructive operation

## Phase 3: Review Correctness

Check:

- expected behavior
- edge cases
- error handling
- state transitions
- concurrency where relevant
- compatibility
- regression risks

## Phase 4: Review Architecture

Check:

- component responsibilities
- dependency direction
- abstraction boundaries
- duplication
- inappropriate coupling
- unnecessary architectural changes

## Phase 5: Review API / Contract

Check:

- request compatibility
- response compatibility
- field semantics
- error contract
- versioning
- backward compatibility

## Phase 6: Review Security

Check for:

- secret exposure
- unsafe input handling
- authentication issues
- authorization issues
- insecure storage
- sensitive information leakage

## Phase 7: Review Tests

Check:

- meaningful coverage
- happy path
- failure path
- boundary conditions
- regression coverage
- test quality

Do not require tests that provide no meaningful value.

## Severity

Classify findings as:

### Critical

Must be fixed before merge.

### High

Strongly recommended before merge.

### Medium

Should be addressed unless there is a documented reason not to.

### Low

Improvement that does not materially block the change.

### Informational

Observation or optional suggestion.

## Completion Report

For each finding provide:

- severity
- file
- location
- problem
- impact
- recommendation

If no issue is found, explicitly state what was checked.
