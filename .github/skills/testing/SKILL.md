# Testing Skill

## Purpose

Design, implement, and validate meaningful tests for changed behavior.

## When to Use

Use this Skill when:

- adding functionality;
- fixing bugs;
- changing existing behavior;
- increasing test coverage;
- validating regressions.

## Inputs

- Issue;
- Requirements;
- Business Rules;
- implementation;
- existing tests.

## Preconditions

Before writing tests:

1. Understand expected behavior.
2. Inspect existing tests.
3. Identify project testing conventions.
4. Identify reusable fixtures and helpers.

## Workflow

### Step 1: Identify Behavior

Determine:

- expected behavior;
- invalid behavior;
- error behavior;
- boundary conditions.

### Step 2: Inspect Existing Tests

Search for:

- similar tests;
- test helpers;
- fixtures;
- mocks;
- integration tests.

### Step 3: Define Scenarios

Consider:

```text
Happy Path
Error Path
Boundary
Invalid Input
Regression
Compatibility
```

Only add scenarios relevant to the behavior.

### Step 4: Implement Tests

Tests should:

- be deterministic;
- be readable;
- test observable behavior;
- follow project conventions;
- avoid unnecessary implementation coupling.

### Step 5: Execute

Run:

1. newly added tests;
2. related tests;
3. broader test suite where appropriate.

### Step 6: Validate

Check that:

- tests pass;
- no existing tests were weakened;
- expected errors are correctly validated;
- regression coverage exists where needed.

## Rules

Prefer behavior-based testing over implementation-detail testing.

## Prohibited Actions

- deleting tests to make builds pass;
- weakening assertions without justification;
- adding meaningless coverage;
- introducing flaky timing-dependent tests unnecessarily.

## Completion Criteria

- relevant scenarios are covered;
- tests pass;
- regression risks are addressed;
- coverage gaps are documented.

## Output

Provide:

- scenarios tested;
- files changed;
- commands executed;
- results;
- remaining gaps.
