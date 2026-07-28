---
description: The plan authoring and checking contract - required plan structure, development approaches, per-task well-formedness, TDD and vertical-slice discipline - load when writing or checking an implementation plan. Background knowledge, not a user command.
user-invocable: false
---

# PLAN CONVENTIONS

Shared by `/nxs:plan`, `/nxs:plancheck`, `/nxs:exec`, `/nxs:rnd`.

A plan is the source of truth for execution: it has a concrete structure, is updated when scope changes, and is reviewable. Unclear task scope, missing files, missing tests, or missing verification means it is not ready.

## DEVELOPMENT APPROACH

The plan records the approach in one line right after Acceptance Criteria. `/nxs:exec` branches on it. Allowed values:

- **default** - ordinary implementation; tests are written together with the code for each task.
- **TDD** - for each narrow behavior write a failing test first, then minimal code, then refactor while green. Full discipline: `reference/tdd.md`.
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
- **SOURCE ARTIFACTS** - the tracker key or URL this plan derives from, so review can trace scope. The brief is a sibling in the same story directory and needs no pointer. Nothing to point at, no section.
- **ACCEPTANCE CRITERIA** - verifiable readiness criteria for the whole plan. Task verification checks a step; AC checks the plan as a whole, and `/nxs:exec` checks against AC rather than checkboxes alone.
- **DEVELOPMENT APPROACH** - one line, right after Acceptance Criteria (see above).
- **CONVENTIONS** - optional; the rules and shared steps every task follows: code style and naming for this work, a procedure repeated per task, standing preferences the user stated for this effort. Detail specific to one task stays in that task. No such rules, no section. `/nxs:exec` passes this section to every worker, so what is missing here does not reach the code.
- **Implementation** - each task well-formed (see below).
- **COMPLEXITY TRACKING** - only when the plan deviates from these conventions (see below).

Full skeleton and scaling of Acceptance Criteria: `reference/plan-template.md`. `/nxs:plan` states where the file goes; after completion the whole story directory moves to `docs/nxs/stories/completed/`, separately, on explicit user confirmation.

## PER-TASK WELL-FORMEDNESS

Each task is one atomic, independently verifiable logical change (one function, one endpoint, one component) and contains:

- **title** - a concrete name, not "Implementation", "Core logic", or "Setup".
- **Files block** - mandatory, exact Create / Modify paths. Without it the plan is incomplete and `/nxs:exec` stops on the task.
- **Test cases** - for a task with behavioral code changes, a `**Test cases:**` block right after the Files block: concrete checks with expected outcome, describing the contract, separate from how the tests are written. A behavioral task without them is incomplete.
- **checklist** - steps as `- [ ]`, marked `- [x]` when done. Tests are separate items, never bundled with the implementation.
- **success criteria** - an observable outcome of the task.
- **verification** - a final item: run tests / lint / typecheck / acceptance check.

Exemption: a config-only / settings / dotfiles / declarative task with no behavioral code to assert needs no Test cases block; verification is that the change takes effect. Review does not flag it.

Full task template, Test-cases scaling, and success-criteria forms by task type: `reference/plan-template.md`.

## TASK SIZING, DECOMPOSITION, SEQUENCING

- Target size ~5 checkboxes per task. Too large (> 8) - split; too small (1-2) - merge into the same logical unit; logically atomic - keep even if larger.
- Tasks are by default thin vertical slices, not thick horizontal layers. Definition, good and bad examples, and the allowed exceptions: `reference/vertical-slice.md`. Each exception is justified in COMPLEXITY TRACKING.
- Sequence tasks by dependency: groundwork a later slice needs comes first.
- `➕` prefixes a task added mid-execution; `⚠️` prefixes a blocker. The final plan state matches the work actually done.

### NEEDS CLARIFICATION markers

An open decision is marked in the artifact itself instead of a plausible guess:

```
[NEEDS CLARIFICATION: <specific question>]
```

- Mark only if the answer changes the decision; trivia stays unmarked.
- A marker resolved in conversation is edited out of the file in the same turn - a stale marker causes a false block.
- A plan with open markers is valid but not ready for execution: `/nxs:plancheck` and `/nxs:exec` both run `rg "NEEDS CLARIFICATION" <plan>` before execution starts.

## COMPLEXITY TRACKING

A plan that deviates from these conventions records every deviation in one table - horizontal slicing, a task over the size guideline, skipped tests, and similar:

```markdown
## COMPLEXITY TRACKING

| deviation | why needed | why simpler alternative rejected |
|---|---|---|
| horizontal "create all models" task | migration has no working intermediate state | vertical slice impossible until schema exists |
```

One row per deviation. An empty "why simpler alternative rejected" cell makes the justification incomplete. This table is the single justification location; no deviations, no section.

## REFERENCE

- `reference/plan-template.md` - full plan skeleton, strict task template, scaling of Acceptance Criteria / Test cases / success criteria, scope-change markers.
- `reference/tdd.md` - RED -> GREEN -> REFACTOR discipline, rules, anti-patterns, when not to use TDD, plan-level framing.
- `reference/vertical-slice.md` - vertical-slice definition, good vs bad examples, rules, when vertical does not fit.
