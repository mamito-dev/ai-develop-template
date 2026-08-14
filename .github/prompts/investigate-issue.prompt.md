---
description: "Investigate a GitHub Issue or technical problem without modifying implementation unless explicitly requested."
---

# Investigate Issue

## Objective

Investigate the requested problem and identify facts, causes, affected areas, and possible solutions.

Do not modify implementation unless explicitly requested.

## Phase 1: Understand

Read:

1. Issue
2. Requirements
3. Business Rules
4. Architecture
5. API/Data Contract
6. Relevant documentation

Identify:

- expected behavior
- actual behavior
- constraints
- reproduction conditions

## Phase 2: Trace

Trace the relevant execution path.

Inspect:

- entry point
- state changes
- data transformations
- dependencies
- external calls
- persistence
- error handling

## Phase 3: Compare Expected vs Actual

Document:

### Expected

What should happen.

### Actual

What currently happens.

### Difference

Where the behavior diverges.

## Phase 4: Identify Root Cause

Do not stop at the first symptom.

Determine:

- direct cause
- underlying cause
- contributing factors

Clearly distinguish facts from hypotheses.

## Phase 5: Evaluate Solutions

If appropriate, provide:

- recommended solution
- alternative solutions
- advantages
- disadvantages
- affected files/components
- architectural impact
- testing requirements

Do not implement a solution unless explicitly requested.

## Completion Report

Report:

### Findings

### Reproduction

### Root Cause

### Evidence

### Affected Components

### Recommended Solution

### Alternatives

### Risks

### Required Tests
