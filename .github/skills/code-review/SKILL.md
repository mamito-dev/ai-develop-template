# Code Review Skill

## Purpose

Evaluate implementation quality against project requirements, architecture, contracts, security, and testing standards.

## When to Use

Use this Skill when:

- reviewing a Pull Request;
- reviewing local changes;
- validating an implementation before merge.

## Inputs

- Issue;
- Acceptance Criteria;
- diff;
- Requirements;
- Architecture;
- API/Data Contract;
- tests.

## Preconditions

Before review:

1. Understand the Issue.
2. Read acceptance criteria.
3. Inspect the complete diff.
4. Identify affected components.

## Workflow

### Step 1: Scope Review

Confirm that changes are related to the Issue.

### Step 2: Correctness Review

Check:

- expected behavior;
- edge cases;
- errors;
- state handling;
- compatibility.

### Step 3: Architecture Review

Check:

- responsibilities;
- dependency direction;
- coupling;
- duplication;
- abstraction quality.

### Step 4: Contract Review

Check:

- API;
- data structures;
- compatibility;
- error responses;
- versioning.

### Step 5: Security Review

Check:

- secrets;
- authentication;
- authorization;
- input validation;
- sensitive data;
- unsafe operations.

### Step 6: Test Review

Check:

- meaningful coverage;
- regression protection;
- failure scenarios;
- test quality.

### Step 7: Maintainability Review

Check:

- readability;
- complexity;
- naming;
- duplication;
- unnecessary abstractions.

### Step 8: Classify Findings

Use:

- Critical;
- High;
- Medium;
- Low;
- Informational.

## Rules

Review the implementation against project requirements, not personal preference.

## Prohibited Actions

- changing code during review unless explicitly requested;
- requesting unnecessary refactoring;
- treating personal style preference as a defect.

## Validation

Review is not complete until all categories (correctness, architecture, contract, security, tests, maintainability) have been evaluated and all findings are classified.

## Completion Criteria

Every significant risk is:

- identified;
- explained;
- assigned a severity;
- linked to a concrete recommendation.

## Output

Provide:

### Summary

### Findings

### Positive Aspects

### Risks

### Recommendation
