# PLAN TEMPLATE (reference)

Loaded on demand from `plan-conventions` when authoring or checking the concrete shape of a plan.

## PLAN SKELETON

```markdown
# <Plan title>

## Overview

<what this plan does and why, in a few lines>

## Context / source artifacts

<links or paths to the brief / ticket / diagnosis this plan derives from>

## ACCEPTANCE CRITERIA

<verifiable readiness criteria for the whole plan>

## DEVELOPMENT APPROACH

<one of: default | TDD | tracer-bullet | spike / investigation> - <one line>

## CONVENTIONS

<rules and shared steps every task in this plan follows - omit the section when there are none>

## Implementation

### Task 1: <concrete title>
...

### Task 2: <concrete title>
...

## COMPLEXITY TRACKING

<only if the plan deviates from conventions>
```

## STRICT TASK TEMPLATE

Each task follows this shape:

```markdown
### Task 1: Add password hashing utility

**Files:**
- Create: src/auth/hash
- Create: src/auth/hash_test

**Test cases:**
- HashPassword(valid_input) -> returns 60-char bcrypt string
- HashPassword(empty_string) -> returns ErrEmptyPassword
- VerifyPassword(correct_hash, password) -> returns true
- VerifyPassword(correct_hash, wrong_password) -> returns false

- [ ] create `src/auth/hash` with HashPassword and VerifyPassword functions
- [ ] implement bcrypt-based hashing with configurable cost
- [ ] write tests from Test cases above (HashPassword)
- [ ] write tests from Test cases above (VerifyPassword)
- [ ] run tests - must pass before task 2
```

Rules for the template:

- **Title** - specific and descriptive. Bad: "Implementation", "Core changes", "Setup".
- **Files block** - mandatory Create / Modify with exact paths. Without it the plan is incomplete.
- **Checklist** - tests are separate items, never bundled with implementation:
  - Good: `- [ ] write tests for HashPassword (error cases)`
  - Bad: `- [ ] implement HashPassword and write tests`
- **Verification** - the final checklist item runs tests / lint / typecheck / manual repro / e2e.

## ACCEPTANCE CRITERIA SCALING

The whole-plan AC scale with the change:

- refactor / single-step edit - one line ("existing behaviour unchanged, tests still pass");
- bug fix - repro stops reproducing + regression test passes;
- feature - list of observable outcomes (what the user / API / system can now do);
- migration - verification for both old and new path.

## TEST CASES SCALING

Per-task Test cases scale too:

- trivial refactor - one line "existing tests still pass";
- bug fix - a repro test is mandatory;
- feature - the full list of observable cases;
- config-only / settings / dotfiles / declarative change with no behavioral code to assert - no Test cases item required; verification is that the change takes effect. The testing lens does not flag this.

When the change only alters behavior of already-covered code, prefer updating or parametrizing existing tests over inventing new ones (`- [ ] update / parametrize tests for cases above`); reserve new tests for genuinely new behavior or a new branch.

## SUCCESS CRITERIA BY TASK TYPE

Turn a vague request into verifiable outcomes:

- feature -> acceptance check: what the user / API / system can now do;
- bug -> a repro or test that shows the bug, then passes after the fix;
- refactor -> checks before / after to confirm no behavior change;
- migration -> verification for old and new path, rollback note if needed.

Weak criteria like "make it work" are insufficient for execution.

## SCOPE CHANGES DURING EXECUTION

If scope changes while executing:

- update the plan;
- add new tasks with the prefix `➕`;
- mark blockers with the prefix `⚠️`;
- the final state of the plan must match the work actually done.

Task completion is tracked by flipping checkboxes `- [ ]` -> `- [x]` inside the plan file; `/nxs:exec` updates them after a task is done. Moving the plan to `docs/nxs/plans/completed/` happens separately, after explicit user confirmation - not automatically on the last checkbox.

## COMPLEXITY TRACKING TABLE

```markdown
## COMPLEXITY TRACKING

| deviation | why needed | why simpler alternative rejected |
|---|---|---|
| horizontal "create all models" task | migration has no working intermediate state | vertical slice impossible until schema exists |
```

One row per deviation. An empty "why simpler alternative rejected" cell makes the justification incomplete. This table is the single justification location.
