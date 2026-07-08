---
description: Create an implementation plan that becomes the source of truth for execution - decompose a task, brief, or tracker input into sequenced, verifiable vertical-slice tasks. Use before executing non-trivial work, after a brainstorm or diagnosis, or whenever you need a reviewable plan.
argument-hint: "[task | brief path | tracker key]"
---

# /nxs:plan

Turn a task, brief, or tracker input into a well-formed implementation plan and stop. The plan becomes the source of truth for execution. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: a task description, a brainstorm brief (`docs/briefs/`), a root-cause brief from `/nxs:bug`, or a tracker key / URL / pasted ticket. A plan can be made with or without a brief - with no input, gather it here first.

## STANCE (PLAN ONLY, HAND OFF)

- dev-plan produces the plan document and stops. It does not write implementation code, run the build, or change behavior.
- The plan is a proposal: read-only until the user approves it. Review is a separate step (`/nxs:plancheck`); execution is a separate step (`/nxs:exec`).
- If the task is small and single-step, no plan is needed - route to `/nxs:exec` or a direct edit instead of ceremony.

## INTAKE

- If the input is a tracker key, URL, or pasted ticket, run the `intake` background skill first to parse structure and separate facts from assumptions, then continue here.
- When a domain term in the task is fuzzy or ambiguous, stop and clarify it before encoding it into the plan rather than guessing its meaning.
- Inspect project context before decomposing: read the relevant files, patterns, and dependencies (delegate to an explorer subagent (`nxs:explorer` or the built-in Explore) or inspect directly). Do not over-read.

## PROCEDURE

1. Understand scope. Parse intent - feature, bug fix, refactor, migration, or generic. Pull acceptance criteria from the tracker / brief / root-cause brief; if none exist, formulate them.
2. Resolve open questions. Ask one at a time, multiple-choice where possible. For several viable approaches, propose 2-3 with trade-offs and a recommendation, and ask once.
3. Choose the development approach - `default` / `TDD` / `tracer-bullet` / `spike`. Evaluate on complexity, risk, and future flexibility; pick the one that minimizes risk and preserves flexibility, and record it in the plan. Definitions and selection criteria are in `plan-conventions`.
4. Decompose into thin vertical-slice tasks - each a narrow observable behavior through all the layers it needs and only those, independently verifiable. Horizontal-by-layer tasks are a justified exception, not the default.
5. Sequence tasks by dependency - groundwork a later slice needs comes first.
6. Make each task well-formed - a concrete title, a Files block (Create / Modify), Test cases for behavioral tasks, a `- [ ]` checklist with tests as separate items, success criteria, and a final verification step. Follow `plan-conventions` for the exact structure and per-task well-formedness; do not invent tasks to pad the count.
7. Record any significant design decision surfaced while planning through the `decision-log` background skill - it applies the ADR gate and decides whether the decision is worth recording and where it lives.
8. Write the plan file (see ARTIFACT). When scope changes during planning, update the plan explicitly and add COMPLEXITY TRACKING on any deviation from the conventions.

## PLAN STRUCTURE

Follow the `plan-conventions` background skill for the required sections, development-approach values, the per-task template, TDD and vertical-slice discipline, NEEDS CLARIFICATION markers, and COMPLEXITY TRACKING. Do not restate that contract here - reference it and apply it.

Mark an open decision that would change the plan with `[NEEDS CLARIFICATION: <specific question>]` in the plan itself instead of a plausible guess. A plan with open markers is valid but not ready for auto execution; the marker convention and its effect on review and execution are detailed in `plan-conventions`.

## ARTIFACT

Write the plan to:

```
docs/plans/YYYYMMDD-<slug>.md
```

If source artifacts exist, add a `## SOURCE ARTIFACTS` section referencing only those that actually exist - no empty placeholders:

```markdown
## SOURCE ARTIFACTS

Tracker: <ticket URL or key>
Briefs: <path(s) to brief files>
Root-cause brief: <path to root-cause brief>
```

## RULES

- The plan is the source of truth for execution - keep it reviewable and current.
- Do not invent tasks for the sake of count - DRY and YAGNI, cut the excess.
- Produce the plan and stop; do not execute it.

## NEXT

Plan written -> `/nxs:plancheck` to review it before execution, then `/nxs:exec` to implement. For a plain-language statement of what the plan does -> `/nxs:explain`.
