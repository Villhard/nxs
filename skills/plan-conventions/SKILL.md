---
description: The plan authoring and checking contract - required plan structure, development approaches, per-task well-formedness, TDD and vertical-slice discipline - load when writing or checking an implementation plan. Background knowledge, not a user command.
user-invocable: false
---

# PLAN CONVENTIONS

Load when writing or checking an implementation plan. Workflow rules, not a user-invocable command. Shared by `/nxs:plan`, `/nxs:plancheck`, `/nxs:exec`, `/nxs:rnd`.

A plan is the source of truth for execution: it has a concrete structure, is updated when scope changes, and must be reviewable. If a plan is not reviewable (unclear task scope, missing files, missing tests, missing verification), it is not ready.

## DEVELOPMENT APPROACH

The plan records the approach in one line right after Acceptance Criteria. `/nxs:exec` branches on it. Allowed values:

- **default** - ordinary implementation; tests are written together with the code for each task.
- **TDD** - for each narrow behavior write a failing test first, then minimal code, then refactor while green. See `reference/tdd.md`.
- **tracer-bullet** - first a thin end-to-end path through all layers for UX / feasibility; tests as the slice expands.
- **spike / investigation** - the goal is an answer to a question, not shippable code; the artifact is findings / a brief, not a feature.

Default is `default`. TDD is chosen deliberately: clear observable behavior, a stable public interface, and tests give design feedback. Spike / tracer-bullet when uncertainty must be removed before shipping a feature.

One-line form in the plan:

```markdown
## DEVELOPMENT APPROACH

TDD - each behavior as RED -> GREEN -> REFACTOR through the HTTP level.
```

## PLAN STRUCTURE

Required sections, in order:

- **Overview** - what the plan does and why.
- **Context / source artifacts** - the brief, ticket, or diagnosis this plan derives from, so review can trace scope.
- **ACCEPTANCE CRITERIA** - verifiable readiness criteria for the whole plan, right after Overview. Separate from per-task verification: task verification checks a step, AC checks the plan as a whole. `/nxs:exec` auto checks against AC, not only checkboxes.
- **DEVELOPMENT APPROACH** - one line, right after Acceptance Criteria (see above).
- **Implementation tasks** - each task well-formed (see below).
- **COMPLEXITY TRACKING** - only when the plan deviates from these conventions (see below); no deviations, no section.

Full skeleton and scaling of Acceptance Criteria: `reference/plan-template.md`. Default location: `docs/plans/yyyymmdd-<task-name>.md`; move to `docs/plans/completed/` after completion, separately, on explicit user confirmation.

## PER-TASK WELL-FORMEDNESS

Each task is one atomic, independently verifiable logical change (one function, one endpoint, one component) and contains:

- **title** - a concrete name, not "Implementation", "Core logic", or "Setup".
- **Files block** - mandatory, exact Create / Modify paths. Without it the plan is incomplete (BLOCK).
- **Test cases** - for a task with behavioral code changes, a `**Test cases:**` block right after the Files block: concrete checks with expected outcome, describing what we check (the contract), separate from how the tests are written. Missing Test cases on a behavioral task is a BLOCK.
- **checklist** - steps as `- [ ]`, marked `- [x]` when done. Tests are separate items, never bundled with the implementation.
- **success criteria** - an observable outcome of the task.
- **verification** - a final item: run tests / lint / typecheck / acceptance check.

Exemption: a config-only / settings / dotfiles / declarative task with no behavioral code to assert needs no Test cases block; verification is that the change takes effect. The testing lens does not flag it.

Full task template, Test-cases scaling, and success-criteria forms by task type: `reference/plan-template.md`.

## TASK SIZING, DECOMPOSITION, SEQUENCING

- Target size ~5 checkboxes per task. Too large (> 8) - split; too small (1-2) - merge into the same logical unit; logically atomic - keep even if larger.
- Tasks are by default thin vertical slices, not thick horizontal layers (see below).
- Sequence tasks by dependency: groundwork a later slice needs comes first.
- `➕` prefixes a task added mid-execution; `⚠️` prefixes a blocker. The final plan state must match the work actually done.

### NEEDS CLARIFICATION markers

An open decision is marked in the artifact itself instead of a plausible guess:

```
[NEEDS CLARIFICATION: <specific question>]
```

- Mark only if the answer changes the decision; do not mark trivia.
- A marker resolved in conversation is edited out of the file in the same turn - a stale marker causes a false auto block.
- A plan with open markers is valid but not ready for auto execution: `/nxs:plancheck` flags open markers as BLOCK for auto modes, and `/nxs:exec` auto runs `rg "NEEDS CLARIFICATION" <plan>` before starting.

## TDD LOOP (essence)

When the approach is TDD, per narrow behavior: **RED** (one failing test through the public interface) -> **GREEN** (minimal code to pass) -> **REFACTOR** (improve structure while green). One behavior, one test, one cycle - not all tests first. Test through the public interface, not private internals. Never refactor while RED. A TDD task is framed through behavior, its Test cases describe observable cases, and its checklist has explicit RED / GREEN / REFACTOR steps per behavior. Full discipline, anti-patterns, and when-not-TDD: `reference/tdd.md`.

## VERTICAL SLICE (essence)

A task is by default a vertical slice: one narrow observable behavior across all the layers it needs and only those, independently verifiable, delivering a working end-to-end path. Prefer many thin slices to a few thick ones; the Files block usually touches several layers at once, which is normal. Horizontal-by-layer tasks ("create all models", then "all services", then "all tests") are an exception, allowed only for pure scaffolding, a migration / refactor with a non-functional intermediate state, or shared groundwork without which no slice runs - and each such exception is justified in COMPLEXITY TRACKING. `/nxs:plancheck` flags unjustified horizontal slicing as BLOCK. Detail and examples: `reference/vertical-slice.md`.

## COMPLEXITY TRACKING

A plan that deviates from these conventions records every deviation in one table:

```markdown
## COMPLEXITY TRACKING

| deviation | why needed | why simpler alternative rejected |
|---|---|---|
```

- Filled only on deviation: horizontal slicing, a task larger than the size guideline, skipped tests, and similar. No deviations - no section.
- One deviation per row. An empty "why simpler alternative rejected" cell makes the justification incomplete.
- This table is the single justification location; deviations are not justified by prose elsewhere.

## REFERENCE

- `reference/plan-template.md` - full plan skeleton, strict task template, scaling of Acceptance Criteria / Test cases / success criteria, scope-change markers.
- `reference/tdd.md` - full RED -> GREEN -> REFACTOR discipline, rules, anti-patterns, when not to use TDD, plan-level framing.
- `reference/vertical-slice.md` - vertical-slice definition, good vs bad examples, rules, when vertical does not fit.
