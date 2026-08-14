# Implementation Skill

## Purpose

Implement an approved change while preserving project requirements, architecture, contracts, and existing behavior.

## When to Use

Use this Skill when implementing:

- new functionality;
- enhancements;
- approved refactoring;
- approved architectural changes.

## Inputs

- GitHub Issue;
- Issue Analysis;
- implementation plan;
- project documentation;
- existing code.

## Preconditions

Before implementation:

1. Understand the Issue.
2. Review relevant Requirements.
3. Review Business Rules.
4. Review Architecture.
5. Review API/Data Contracts.
6. Inspect existing implementation.
7. Define the implementation plan.

## Workflow

### Step 1: Confirm Scope

Identify:

- required changes;
- prohibited changes;
- affected files;
- affected components.

Classify planned changes using `.github/policies/change-safety-policy.md` and confirm that Restricted changes are explicitly in Issue scope.

### Step 2: Confirm Existing Patterns

Search for existing patterns before creating:

- new abstractions;
- utilities;
- services;
- repositories;
- helpers;
- configuration.

Reuse existing patterns when appropriate.

### Step 3: Implement

Implement the smallest change that satisfies the requirement.

Prefer:

- simple solutions;
- existing abstractions;
- existing conventions;
- explicit behavior.

### Step 4: Preserve Existing Behavior

Verify that unrelated behavior is not changed.

### Step 5: Add Tests

Add or update tests for changed behavior.

### Step 6: Update Documentation

If the implementation changes:

- public behavior;
- API contracts;
- architecture;
- setup;
- configuration;
- development procedures;

update the relevant documentation.

### Step 7: Validate

Run relevant:

- tests;
- lint;
- formatter;
- build;
- contract checks.

### Step 8: Review Diff

Check:

- scope;
- accidental changes;
- generated files;
- secrets;
- dependency changes.

Compare Expected Changes vs Actual Changed Files and report out-of-scope changes as a separate improvement proposal.

## Rules

- Make the smallest safe change.
- Follow existing architecture.
- Follow project coding conventions.
- Reuse existing abstractions.
- Do not add speculative functionality.

## Prohibited Actions

- unrelated refactoring;
- unnecessary dependency additions;
- architecture changes without approval;
- API changes without contract review;
- deleting tests to make validation pass.

## Validation

Implementation is not complete until relevant validation has been executed.

## Completion Criteria

- requirements satisfied;
- tests added/updated;
- relevant validation passed;
- documentation updated where required;
- final diff reviewed.

## Output

Provide:

- summary;
- changed files;
- tests;
- validation results;
- remaining risks.
