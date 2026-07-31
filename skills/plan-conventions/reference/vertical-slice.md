# VERTICAL SLICE (reference)

Loaded on demand from `plan-conventions` when checking whether tasks are sliced correctly.

## DEFINITION

A vertical slice is a task that:

- delivers one complete observable capability (a use case, an endpoint contract, a UI action);
- goes through all the layers that capability needs, and only those layers;
- can be executed and verified independently of neighboring slices;
- leaves the project in a working state - the tree builds and the suite passes at the task boundary.

A horizontal task is organized by layers ("create all models", "add all services", "wire everything") - an anti-pattern when a vertical slice is actually possible.

## GOOD - COMPLETE VERTICAL SLICES

```
Task 1: a visitor registers with an email and lands in the database
  - migration + user model with a unique email constraint
  - service.Register: normalize, persist, return ErrEmailTaken on a duplicate
  - POST /api/users: 201 on success, 409 on duplicate, 422 on an invalid format
  - repository test for the constraint
  - HTTP tests for all three outcomes

Task 2: a registered user signs in and receives a session token
  - sessions table + token issuing
  - service.Login against the stored credential
  - POST /api/sessions: 200 with a token, 401 on a bad credential
  - HTTP tests for both outcomes
```

Two tasks, not five: they change different public contracts and release independently, which is what earns the boundary.

## BAD - HORIZONTAL LAYERS

```
Task 1: create all models (users, sessions, tokens)
Task 2: create all services
Task 3: create all endpoints
Task 4: write all tests
```

Not demoable until the very end, design errors show up late, the review is gigantic, rolling back each part is expensive.

## BAD - ONE CAPABILITY SPLIT BY STEP

```
Task 1: registration happy path
Task 2: registration rejects a duplicate email
Task 3: registration rejects an invalid email format
```

One endpoint contract, one verification strategy, nothing releasable on its own - so this is Task 1 of the GOOD example, split three ways. Each boundary costs a worker launch with a cold context, a verify run, a review round, and a commit, and buys nothing back.

## RULES

- As few slices as the split criteria in `plan-conventions` justify, and no fewer than correctness needs.
- Each slice is independently verifiable; test cases describe exactly the capability of that slice.
- The Files block of a vertical slice usually touches several layers at once - this is normal, and it is not a reason to split the task.
- If a task does not reduce to a slice - justify it in the plan in one line (COMPLEXITY TRACKING).

## REVIEWABILITY CHECK

A slice is the right size when a reviewer reading that task alone can answer, without opening a later task:

- what capability was added;
- how it is verified;
- what public contracts changed;
- what risk remains.

Cannot answer the first from one task - the slice is too thin and belongs with its neighbor. Cannot hold the last two in one pass - it is too thick and splits on a criterion, not on a layer.

## WHEN VERTICAL DOES NOT FIT

- pure scaffolding without observable behavior (repo, base configs, types);
- migration / refactor with a fundamentally non-working intermediate state;
- shared groundwork without which no slice runs (split out as a separate minimal task);
- spike / investigation - the goal is findings, not behavior.

In these cases a narrow horizontal task is acceptable as an exception, explicitly justified in the plan.
