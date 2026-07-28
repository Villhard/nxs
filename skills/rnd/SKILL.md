---
description: Think a task through to a plan-ready brief - the task entry point. Use to shape a fuzzy task, feature idea, or open question before planning.
argument-hint: "[task | tracker key | question]"
---

# /nxs:rnd

Think a task through to a plan-ready brief and stop. The task entry point. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: a task description, a feature idea, a tracker key / URL / pasted ticket, or an open question. With nothing given, work with the current session context.

Example: /nxs:rnd add rate limiting to the public API

## STANCE (BRAINSTORM ONLY, HAND OFF)

- /nxs:rnd produces the brief and stops. It does not write a plan or implementation code, run the build, or change behavior.
- Three phases run in order: CLARIFY (remove misunderstanding), then EXPLORE (compare approaches), then STRESS (pressure-test the recommended approach). All scale by complexity - a clear task collapses CLARIFY to 0 questions, EXPLORE to the single obvious approach, and STRESS to ~0; a fuzzy / risky / architectural one expands all three.
- Full collapse (CLARIFY 0 questions, EXPLORE the single obvious approach, STRESS ~0) makes the brief ceremony. Do not write it silently and do not skip it silently - offer the user the choice: route straight to `/nxs:plan`, or write a short brief for decision traceability.
- The next step is `/nxs:plan` (turn the brief into a plan). For a bug rather than a task, route to `/nxs:bug` instead of brainstorming.

## CONTEXT

- Gather context before asking: read the relevant code, existing patterns, dependencies, integration points, and project memory (delegate to the built-in Explore agent or inspect directly). Ask only about what the code does not answer. Do not over-read.
- When a domain term is fuzzy or ambiguous, stop and clarify it before EXPLORE rather than guessing its meaning.

## CLARIFY

Remove misunderstanding before proposing approaches. Throughout, separate facts from assumptions - state what the input and code establish versus what you are inferring.

- Internal coverage scan first: check the task across uncertainty categories - scope and explicit out-of-scope; data / model / migrations; integrations and external dependencies; edge cases and failure handling; terminology; testability / acceptance criteria. Mark each Clear / Partial / Missing. This is internal reasoning, not user-facing output, and it scales with complexity - a trivial task collapses it.
- Pick questions from Partial / Missing categories by Impact * Uncertainty - prioritize the highest-value unknowns, not whatever comes to mind first.
- Stop rule: ask while the next question changes the decision AND a Missing (or Partial) category with high Impact * Uncertainty remains; stop as soon as either fails. Exactly one at a time. Do not dump a list. 0 questions is a normal and frequent outcome - if the task is clear from the input and the code, pass silently.
- Every question is hard-won: it changes the decision or removes a real ambiguity, not a routine survey for appearances. Prefer multiple choice (2-4 options) with a recommended answer and rationale; open-ended only when a choice is unnatural.
- If the answer is visible in the code, read the code instead of asking.
- After each answer, revise the understanding and derive the next question from the updated model - do not prepare a list in advance, do not reopen a closed point without new information.
- Surface acceptance / readiness criteria: pull them from the input, or formulate and confirm them.
- Categories still Partial / Missing once the stop rule fires - axes deliberately left open - record them in the brief as `[NEEDS CLARIFICATION: <specific question>]` markers (the same marker convention the `plan-conventions` background skill uses), not as prose; do not push further. Surface this remainder to the user only when it is non-empty; full coverage produces no summary.

## EXPLORE

Compare approaches, do not jump into the first one.

- Lay out 2-4 real approaches with explicit pros / cons for each. Do not present the first idea that comes to mind as the only option; show alternatives and trade-offs.
- Give a recommendation with a rationale (have an opinion), but leave the choice to the user.
- DRY and YAGNI: the recommended approach is the minimal viable one, building on how the task is already solved in the project. If there really is one reasonable approach, say so directly - do not stretch artificial alternatives.
- Validate the design with the user and record the selected approach in the brief's `## Chosen approach` section, including what is explicitly not being done.

## STRESS

Pressure-test the approach EXPLORE recommended before writing it into the brief.

- Run four steps on the recommended approach: **assumptions inventory** (what must hold for it to survive, stated explicitly and separated from what is already established) -> **premortem** (assume it has already failed, then trace the concrete path from chosen to wrong: which assumption broke, which edge case hit, which cost was underestimated) -> **kill-criteria** (the observable signal that says stop or scope this down, decided in advance rather than defended after the fact) -> **verdict** (`holds` | `fails` | `holds only when ...`).
- Be honest: if the approach clearly survives, say so instead of manufacturing doubt. Every concern needs a concrete justification, not an abstraction.
- Scale by complexity like CLARIFY and EXPLORE: a trivial / clear idea collapses STRESS to ~0 (skip to ARTIFACT); a risky / architectural one runs all four steps.
- One bounded loop-back only: a fatal finding or a met kill-criterion returns once - to EXPLORE if the approach must change, or to CLARIFY if a new uncertainty axis opened. After that single iteration the brief is frozen; STRESS does not loop again. Preserve the standing stance - produce the brief and stop, the loop-back is one iteration, not open-ended.

## ARTIFACT

Write a brief:

```
docs/nxs/briefs/YYYYMMDD-<slug>-rnd.md
```

When the input carries a tracker key, include it in the name - `docs/nxs/briefs/YYYYMMDD-<KEY>-<slug>-rnd.md` - so the brief stays navigable by the key.

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

A brief can be short for a simple task and detailed for a complex one: sections scale in depth, empty ones are dropped, headings are not renamed. Acceptance criteria surfaced in CLARIFY land in their own section - `/nxs:plan` pulls them from here. The CLARIFICATIONS and STRESS sections are appended only under their own conditions below.

Add a clarifications log only when at least one CLARIFY question was asked:

```markdown
## CLARIFICATIONS

### Session YYYY-MM-DD

- Q: <question> -> A: <accepted answer>
```

The accepted answer is integrated into the main brief text; the log records decision traceability. An answer that invalidates earlier brief text replaces it - contradicting stale wording must not remain.

Add a STRESS block only when STRESS actually ran - a trivial task where STRESS collapsed to ~0 does not add it. Capture the assumptions inventory, the failure modes, the kill-criteria, and the verdict.

Nothing durable is written from CLARIFY without approval.

## RULES

- /nxs:rnd produces the brief and stops - no plan, no code. On full collapse the user chooses: route to `/nxs:plan` or a short brief.
- Separate facts from assumptions throughout.
- Questions are hard-won and one at a time - ask only while the next question still changes the decision; 0 is a normal outcome.
- Show 2-4 real approaches with trade-offs before recommending one; do not stretch artificial alternatives.

## NEXT

Brief written -> `/nxs:plan` turns it into a plan following the `plan-conventions` contract, then `/nxs:exec` to implement. For a bug rather than a task -> `/nxs:bug`.
