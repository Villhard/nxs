---
description: Create an implementation plan that becomes the source of truth for execution - decompose a task, brief, or tracker input into sequenced, verifiable vertical-slice tasks. Use before executing non-trivial work, after a brainstorm or diagnosis, or whenever you need a reviewable plan.
argument-hint: "[task | story path | tracker key]"
---

# /nxs:plan

Turn a task, brief, or tracker input into a well-formed implementation plan and stop. The plan becomes the source of truth for execution.

Accepted input: a task description, a story directory (`docs/nxs/stories/`) holding a brainstorm or root-cause brief, or a tracker key / URL / pasted ticket. A plan can be made with or without a brief - with no input, gather it here first.

Example: /nxs:plan docs/nxs/stories/20260711-auth-refactor

## STANCE (PLAN ONLY, HAND OFF)

- /nxs:plan produces the plan document and stops, leaving implementation code, the build, and any behavior change to `/nxs:exec`.
- The plan is a proposal: read-only until the user approves it.
- If the task is small and single-step, no plan is needed - route to `/nxs:exec` or a direct edit instead of ceremony.

## CONTEXT

- When a domain term in the task is fuzzy or ambiguous, clarify it before encoding it into the plan.
- Inspect project context before decomposing: read the relevant files, patterns, and dependencies (delegate to the built-in Explore agent or inspect directly). Do not over-read.

## PROCEDURE

1. Understand scope. Parse intent - feature, bug fix, refactor, migration, or generic. Pull acceptance criteria from the tracker / brief / root-cause brief; if none exist, formulate them.
2. Resolve open questions. Ask one at a time, multiple-choice where possible. For several viable approaches, propose 2-3 with trade-offs and a recommendation, and ask once.
3. Choose the development approach - `default` / `TDD` / `tracer-bullet` / `spike`. Evaluate on complexity, risk, and future flexibility; pick the one that minimizes risk and preserves flexibility, and record it in the plan. Definitions and selection criteria are in `plan-conventions`.
4. Decompose into the fewest vertical slices the split criteria justify - each a complete observable capability through all the layers it needs and only those, independently verifiable. A technical step in one layer is not a task, and neither is a file boundary. Counts, split criteria, and the horizontal-layer exception are in `plan-conventions`.
5. Sequence tasks by dependency - groundwork a later slice needs comes first.
6. Make each task well-formed - a concrete title, a Files block (Create / Modify), Test cases for behavioral tasks, a `- [ ]` checklist with tests as separate items, success criteria, and a final verification step. Follow `plan-conventions` for the exact structure and per-task well-formedness. Every task earns its place; DRY and YAGNI, cut the excess.
7. Write the plan file (see ARTIFACT). When scope changes during planning, update the plan explicitly and add COMPLEXITY TRACKING on any deviation from the conventions. A significant design decision surfaced while planning goes into the plan itself, as a short `## Decision: <title>` section with what was decided, why, and what is explicitly not being done.

## PLAN STRUCTURE

Follow the `plan-conventions` background skill for the required sections, development-approach values, the per-task template, TDD and vertical-slice discipline, NEEDS CLARIFICATION markers, and COMPLEXITY TRACKING.

Mark an open decision that would change the plan with `[NEEDS CLARIFICATION: <specific question>]` in the plan itself instead of a plausible guess. A plan with open markers is valid but not ready for execution; the marker convention and its effect on review and execution are detailed in `plan-conventions`.

## ARTIFACT

Write the plan into the story directory the input names, creating the directory when the input is a bare task with no prior brief:

```
docs/nxs/stories/YYYYMMDD-<slug>/plan.md
```

When the input carries a tracker key (from the story directory or the ticket), it names the directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/` - so the story stays navigable by the key.

With a tracker key or URL to record, add a `## SOURCE ARTIFACTS` section - the brief is a sibling in the same directory and needs no pointer. No tracker, no section:

```markdown
## SOURCE ARTIFACTS

Tracker: <ticket URL or key>
```

## NEXT

Plan written -> `/nxs:plancheck` to review it before execution, then `/nxs:exec` to implement.
