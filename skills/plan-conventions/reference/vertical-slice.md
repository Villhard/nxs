# VERTICAL SLICE (reference)

Loaded on demand from `plan-conventions` when checking whether tasks are sliced correctly.

## DEFINITION

A vertical slice is a task that:

- contains one concrete observable behavior (one use case, one endpoint contract, one UI action);
- goes through all the layers this behavior needs, and only those layers;
- can be executed and verified independently of neighboring slices;
- delivers a working end-to-end path, even if the behavior is narrow.

A horizontal task is organized by layers ("create all models", "add all services", "wire everything") - an anti-pattern when a vertical slice is actually possible. Horizontal-by-layer tasks produce a lot of code without working behavior and postpone the first rollback-able green build; design errors surface later and more expensively.

## GOOD - THIN VERTICAL SLICES

```
Task 1: registration accepts valid email and creates user
  - DB column + minimal model
  - service.Register happy path
  - POST /api/users happy path
  - HTTP test for happy path

Task 2: registration rejects duplicate email
  - unique constraint
  - service returns ErrEmailTaken
  - HTTP 409 mapping
  - test for duplicate

Task 3: registration rejects invalid email format
  - validation
  - HTTP 422 mapping
  - test for validation
```

Each task is a narrow behavior across all layers, separately verifiable and demoable.

## BAD - HORIZONTAL LAYERS

```
Task 1: create all models (users, sessions, tokens)
Task 2: create all services
Task 3: create all endpoints
Task 4: write all tests
```

Not demoable until the very end, design errors show up late, the review is gigantic, rolling back each part is expensive.

## RULES

- By default - many thin vertical slices, not a few thick ones.
- Each slice is independently verifiable; test cases describe exactly the behavior of that slice.
- The Files block of a vertical slice usually touches several layers at once - this is normal.
- If a task does not reduce to a slice - justify it in the plan in one line (COMPLEXITY TRACKING).
- Slice size is bounded by task sizing (~5 checkboxes per task).

## WHEN VERTICAL DOES NOT FIT

- pure scaffolding without observable behavior (repo, base configs, types);
- migration / refactor with a fundamentally non-working intermediate state;
- shared groundwork without which no slice runs (split out as a separate minimal task);
- spike / investigation - the goal is findings, not behavior.

In these cases a narrow horizontal task is acceptable as an exception, explicitly justified in the plan.
