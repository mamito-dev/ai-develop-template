# Documentation Skill

## Purpose

Keep project documentation synchronized with requirements, architecture, APIs, development procedures, and implementation behavior.

## When to Use

Use this Skill when:

- requirements change;
- architecture changes;
- APIs change;
- configuration changes;
- development procedures change;
- implementation changes documented behavior.

## Inputs

- Issue;
- implementation;
- existing documentation;
- architecture;
- API contracts.

## Preconditions

Before changing documentation:

1. Identify the affected Source of Truth.
2. Determine whether the change is documentation-only or caused by implementation.
3. Check for duplicate information.

## Workflow

### Step 1: Identify Documentation Impact

Check:

- requirements;
- business rules;
- architecture;
- API;
- setup;
- build;
- test;
- troubleshooting.

### Step 2: Update Source of Truth

Update the document that owns the information.

Do not duplicate the same information across multiple documents.

### Step 3: Check Consistency

Verify that related documentation does not contradict the changed Source of Truth.

### Step 4: Check Implementation Consistency

Verify that documentation matches the actual implementation.

### Step 5: Check Links

Verify:

- internal links;
- referenced files;
- commands;
- paths.

### Step 6: Review

Check whether:

- outdated information remains;
- duplicated information exists;
- TODO/TBD remains where it should be resolved.

## Rules

One piece of information should have one primary Source of Truth.

## Prohibited Actions

- copying the same specification into multiple documents;
- documenting unimplemented behavior as implemented;
- silently resolving specification conflicts;
- changing requirements merely to match incorrect implementation.

## Completion Criteria

- relevant documentation is updated;
- Source of Truth is clear;
- implementation and documentation are consistent;
- links and commands are valid.

## Output

Provide:

- changed documents;
- reason for each change;
- consistency results;
- unresolved documentation issues.
