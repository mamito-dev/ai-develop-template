# Issue Analysis Skill

## Purpose

Analyze a GitHub Issue before implementation.

The goal is to understand what must be changed, what must not be changed, and what project rules constrain the implementation.

## When to Use

Use this Skill when:

- starting a new Issue;
- investigating an implementation task;
- preparing an implementation plan;
- determining affected components;
- identifying missing requirements.

## Inputs

- GitHub Issue
- Acceptance Criteria
- Related documentation
- Existing implementation

## Preconditions

Before analysis:

1. Read the Issue completely.
2. Identify the explicit scope.
3. Identify the acceptance criteria.
4. Locate relevant project documentation.

## Workflow

### Step 1: Understand the Issue

Identify:

- objective;
- required behavior;
- expected result;
- constraints;
- explicit non-goals.

### Step 2: Locate Source of Truth

Search:

- requirements;
- business rules;
- architecture;
- component responsibilities;
- data flow;
- API contracts.

Do not infer project-specific rules from generic knowledge.

### Step 3: Investigate Existing Code

Search for:

- related components;
- similar implementations;
- tests;
- dependencies;
- configuration.

### Step 4: Determine Impact

Identify:

- affected files;
- affected components;
- affected APIs;
- affected data;
- required tests;
- documentation impact.

### Step 5: Identify Risks

Consider:

- backward compatibility;
- regression;
- architecture violations;
- API compatibility;
- data migration;
- security;
- performance.

### Step 6: Identify Unknowns

Classify unresolved information as:

- Unknown;
- Conflict;
- Assumption;
- Decision Required.

Do not silently convert these into implementation decisions.

## Rules

- Do not modify code during analysis unless explicitly requested.
- Do not invent requirements.
- Do not expand Issue scope.
- Prefer existing project patterns.

## Prohibited Actions

- speculative implementation;
- unrelated refactoring;
- undocumented architecture changes;
- silently resolving specification conflicts.

## Validation

Confirm that:

- Issue scope is understood;
- affected components are identified;
- relevant documentation was checked;
- unknowns are documented.

## Completion Criteria

The Issue can be explained in terms of:

1. required behavior;
2. affected components;
3. constraints;
4. required changes;
5. tests;
6. risks;
7. unresolved decisions.

## Output

Provide an implementation-ready analysis.
