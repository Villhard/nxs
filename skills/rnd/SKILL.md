---
description: Think a task through to a plan-ready brief - the task entry point. Use to shape a fuzzy task, feature idea, or open question before planning.
argument-hint: "[task | tracker key | question]"
---

# /nxs:rnd

Think a task through to a plan-ready brief and stop. The task entry point.

Accepted input: a task description, a feature idea, a tracker key / URL / pasted ticket, or an open question. With nothing given, work with the current session context.

Example: /nxs:rnd add rate limiting to the public API

## STANCE (BRAINSTORM ONLY, HAND OFF)

- /nxs:rnd produces the brief and stops. It leaves the plan, the implementation code, the build, and any behavior change to the skills that own them.
- Three phases run in order: CLARIFY (remove misunderstanding), then EXPLORE (compare approaches), then STRESS (pressure-test the recommended approach).
- **All three scale by complexity.** A clear task collapses CLARIFY to 0 questions, EXPLORE to the single obvious approach, and STRESS to ~0; a fuzzy / risky / architectural one expands all three. This scaling rule holds in every phase below.
- Full collapse makes the brief ceremony. Offer the user the choice out loud: route straight to `/nxs:plan`, or write a short brief for decision traceability.
- For a bug rather than a task, route to `/nxs:bug` instead of brainstorming.

## CONTEXT

- Gather context before asking: read the relevant code, existing patterns, dependencies, integration points, and project memory (delegate to the built-in Explore agent or inspect directly). Ask only about what the code does not answer. Do not over-read.
- When a domain term is fuzzy or ambiguous, clarify it before EXPLORE.

## CLARIFY

Remove misunderstanding before proposing approaches. Throughout, separate facts from assumptions - state what the input and code establish versus what you are inferring.

- Internal coverage scan first: check the task across uncertainty categories - scope and explicit out-of-scope; data / model / migrations; integrations and external dependencies; edge cases and failure handling; terminology; testability / acceptance criteria. Mark each Clear / Partial / Missing. This stays internal reasoning, not user-facing output.
- Pick questions from Partial / Missing categories by Impact * Uncertainty - the highest-value unknowns, not whatever comes to mind first.
- Stop rule: ask while the next question changes the decision AND a Missing (or Partial) category with high Impact * Uncertainty remains; stop as soon as either fails. Exactly one question at a time. 0 questions is a normal and frequent outcome - if the task is clear from the input and the code, pass silently.
- Prefer multiple choice (2-4 options) with a recommended answer and rationale; open-ended only when a choice is unnatural.
- After each answer, revise the understanding and derive the next question from the updated model - each question comes from the current state, and a closed point reopens only on new information.
- Surface acceptance / readiness criteria: pull them from the input, or formulate and confirm them.
- Categories still Partial / Missing once the stop rule fires - axes deliberately left open - go into the brief as `[NEEDS CLARIFICATION: <specific question>]` markers (the same marker convention `plan-conventions` uses), not as prose. Surface this remainder to the user only when it is non-empty.

## EXPLORE

- Lay out 2-4 real approaches with explicit pros / cons for each, and show the trade-offs between them.
- Give a recommendation with a rationale (have an opinion), but leave the choice to the user.
- DRY and YAGNI: the recommended approach is the minimal viable one, building on how the task is already solved in the project. If there really is one reasonable approach, say so directly - a stretched alternative is worse than none.
- Validate the design with the user and record the selected approach in the brief's `## Chosen approach` section, including what is explicitly not being done.

## STRESS

Pressure-test the approach EXPLORE recommended before writing it into the brief.

- Four steps on the recommended approach: **assumptions inventory** (what must hold for it to survive, stated explicitly and separated from what is already established) -> **premortem** (assume it has already failed, then trace the concrete path from chosen to wrong: which assumption broke, which edge case hit, which cost was underestimated) -> **kill-criteria** (the observable signal that says stop or scope this down, decided in advance rather than defended after the fact) -> **verdict** (`holds` | `fails` | `holds only when ...`).
- If the approach clearly survives, say so. Every concern carries a concrete justification, not an abstraction.
- One bounded loop-back only: a fatal finding or a met kill-criterion returns once - to EXPLORE if the approach must change, or to CLARIFY if a new uncertainty axis opened. After that single iteration the brief is frozen.

## ARTIFACT

Write a brief:

```
docs/nxs/stories/YYYYMMDD-<slug>/brief.md
```

When the input carries a tracker key, it names the story directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/` - so the story stays navigable by the key. The files inside keep their fixed names.

Keep the section skeleton stable - `/nxs:plan` consumes the brief by these headings:

```markdown
# Brief: <title>

- Date: YYYY-MM-DD
- Status: ready for `/nxs:plan`
- Tracker: <key / URL - omit the line if none>

## Task

## Context (facts from the code)

## Acceptance criteria

## Options

<2-4 options as `### O<n>. <name> - recommended | rejected: <reason>`, each with pros / cons>

## Chosen approach

<the selected approach with integrated answers, plus "Explicitly not doing: ..." for out-of-scope>

## Next
```

Sections scale in depth with the task, empty ones are dropped, headings keep their names. Acceptance criteria surfaced in CLARIFY land in their own section - `/nxs:plan` pulls them from here.

Add a clarifications log only when at least one CLARIFY question was asked:

```markdown
## CLARIFICATIONS

### Session YYYY-MM-DD

- Q: <question> -> A: <accepted answer>
```

The accepted answer is integrated into the main brief text; the log records decision traceability. An answer that invalidates earlier brief text replaces it, so the stale wording goes.

Add a STRESS block only when STRESS actually ran, capturing the assumptions inventory, the failure modes, the kill-criteria, and the verdict.

Nothing durable is written from CLARIFY without approval.

## NEXT

Brief written -> `/nxs:plan` turns it into a plan following the `plan-conventions` contract, then `/nxs:exec` to implement.
