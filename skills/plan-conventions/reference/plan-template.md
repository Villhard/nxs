# PLAN TEMPLATE (reference)

Loaded on demand from `plan-conventions` when authoring or checking the concrete shape of a plan.

## Contents

- Plan skeleton
- Strict task template
- Acceptance criteria scaling
- Test cases scaling
- Success criteria by task type
- Scope changes during execution

## PLAN SKELETON

```markdown
# <Plan title>

## Overview

<what this plan does and why, in a few lines>

## SOURCE ARTIFACTS

<the tracker key or URL this plan derives from - the brief is a sibling, not a link>

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
### Task 1: A visitor registers with an email and lands in the database

**Files:**
- Create: migrations/0007_users.sql
- Create: src/auth/hash.go
- Create: src/auth/hash_test.go
- Modify: src/users/service.go
- Modify: src/users/service_test.go
- Modify: src/api/routes.go
- Create: src/api/users_test.go

**Test cases:**
- POST /api/users with a fresh email -> 201, the row holds a bcrypt hash, never the plaintext
- POST /api/users with an existing email -> 409, no second row
- POST /api/users with a malformed email -> 422

- [ ] add the users migration with a unique index on email
- [ ] add HashPassword in `src/auth/hash.go` (bcrypt, configurable cost)
- [ ] add service.Register: normalize, hash, persist, ErrEmailTaken on a duplicate
- [ ] wire POST /api/users to the service and map errors to 201 / 409 / 422
- [ ] write tests from Test cases above (the stored hash)
- [ ] write tests from Test cases above (the duplicate and malformed outcomes)
- [ ] run `go test ./...` and check against ACCEPTANCE CRITERIA

Success: a visitor registers through the public API, the credential round-trips, and a duplicate email is rejected with 409.
```

Required elements and their bar are in `plan-conventions` -> PER-TASK WELL-FORMEDNESS. The one that is easiest to get wrong is splitting tests out of the implementation step:

- Good: `- [ ] write tests for the duplicate-email path`
- Bad: `- [ ] implement service.Register and write tests`

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
- config-only / settings / dotfiles / declarative change with no behavioral code to assert - no Test cases item required; verification is that the change takes effect. Review does not flag this.

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

Task completion is tracked by flipping checkboxes `- [ ]` -> `- [x]` inside the plan file; `/nxs:exec` updates them after a task is done. Archiving the plan happens separately, after explicit user confirmation.
