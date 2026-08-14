---
description: "Create meaningful tests for existing or newly implemented behavior."
---

# Create Test

## Objective

Create tests that verify observable behavior and protect against regressions.

## Phase 1: Understand the Behavior

Read:

1. Issue
2. Requirements
3. Business Rules
4. Relevant Architecture
5. Existing implementation
6. Existing tests

Determine the behavior that must be protected.

## Phase 2: Inspect Existing Tests

Search for:

- related test files
- similar test cases
- shared fixtures
- test helpers
- mocks
- test utilities

Reuse existing test patterns.

## Phase 3: Identify Scenarios

Consider:

- happy path
- invalid input
- boundary values
- expected errors
- state transitions
- regression scenarios

Only add scenarios relevant to the behavior.

## Phase 4: Implement Tests

Tests should:

- have clear names
- be deterministic
- test observable behavior
- minimize unnecessary implementation coupling
- follow existing project conventions

Do not create tests that merely reproduce private implementation details.

## Phase 5: Run Tests

Run the newly created tests.

Then run relevant existing tests.

## Phase 6: Validate

Confirm:

- test passes
- test fails for the expected reason when the protected behavior is intentionally broken, where practical
- no unrelated tests were weakened

## Completion Report

Report:

### Test Objective

### Scenarios Covered

### Files Changed

### Commands Executed

### Results

### Remaining Coverage Gaps
