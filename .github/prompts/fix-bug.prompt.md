---
description: "Diagnose and fix a bug while preserving existing behavior and adding regression coverage."
---

# Fix Bug

## Objective

Identify the root cause of the reported bug, implement the smallest safe fix, and add regression coverage.

## Phase 1: Reproduce

Determine:

- reproduction steps
- expected result
- actual result
- environment
- relevant input/state

Attempt to reproduce the issue.

If reproduction is impossible, clearly state that.

## Phase 2: Investigate

Trace the relevant execution path.

Inspect:

- input
- validation
- state
- transformations
- dependencies
- persistence
- external calls
- error handling

## Phase 3: Identify Root Cause

Distinguish:

- symptom
- direct cause
- root cause

Do not implement a workaround without understanding why the bug occurs unless an explicit emergency workaround is required.

## Phase 4: Plan

Define:

- files to change
- root cause
- proposed fix
- regression test
- validation steps

## Phase 5: Implement

Implement the smallest fix that resolves the root cause.

Avoid unrelated refactoring.

## Phase 6: Regression Test

Add or update a test that fails before the fix and passes after the fix whenever practical.

Also verify relevant existing tests.

## Phase 7: Validate

Run:

- regression test
- related tests
- full test suite when appropriate
- lint
- build

## Completion Report

Report:

### Bug

### Root Cause

### Fix

### Regression Test

### Tests Executed

### Build / Lint

### Remaining Risks
