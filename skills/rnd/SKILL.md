---
description: Think a task through to a plan-ready brief via CLARIFY then EXPLORE - narrow an under-specified task, compare real approaches, record the decision - the tracked-task entry point. Use to shape a fuzzy task, feature idea, or open question before planning.
argument-hint: "[task | tracker key | question]"
---

# /nxs:rnd

Think a task through to a plan-ready brief and stop. The tracked-task entry point. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: a task description, a feature idea, a tracker key / URL / pasted ticket, or an open question. With nothing given, work with the current session context.

## STANCE (BRAINSTORM ONLY, HAND OFF)

- Brainstorm produces the brief and stops. It does not write a plan or implementation code, run the build, or change behavior.
- Two phases run in order: CLARIFY (remove misunderstanding) then EXPLORE (compare approaches). Both scale by complexity - a clear task collapses CLARIFY to 0 questions and EXPLORE to the single obvious approach; a fuzzy / risky / architectural one expands both.
- The next step is `/nxs:plan` (turn the brief into a plan). For a bug rather than a task, route to `/nxs:bug` instead of brainstorming.

## INTAKE

- If the input is a tracker key, URL, or pasted ticket, run the `intake` background skill first to parse structure and separate facts from assumptions, then continue here.
- Gather context before asking: read the relevant code, existing patterns, dependencies, integration points, and project memory (delegate to an explorer subagent (`nxs:explorer` or the built-in Explore) or inspect directly). Ask only about what the code does not answer. Do not over-read.
- When a domain term is fuzzy or ambiguous, stop and clarify it before EXPLORE rather than guessing its meaning.

## CLARIFY

Remove misunderstanding before proposing approaches. Throughout, separate facts from assumptions - state what the input and code establish versus what you are inferring.

- Internal coverage scan first: check the task across uncertainty categories - scope and explicit out-of-scope; data / model / migrations; integrations and external dependencies; edge cases and failure handling; terminology; testability / acceptance criteria. Mark each Clear / Partial / Missing. This is internal reasoning, not user-facing output, and it scales with complexity - a trivial task collapses it.
- Pick questions from Partial / Missing categories by Impact * Uncertainty - spend the budget on the highest-value unknowns, not whatever comes to mind first.
- Up to 3 questions total (hard limit), exactly one at a time. Do not dump a list. 0 questions is a normal and frequent outcome - if the task is clear from the input and the code, pass silently.
- Every question is hard-won: it changes the decision or removes a real ambiguity, not a routine survey for appearances. Prefer multiple choice (2-4 options) with a recommended answer and rationale; open-ended only when a choice is unnatural.
- If the answer is visible in the code, read the code instead of asking.
- After each answer, revise the understanding and derive the next question from the updated model - do not prepare a list in advance, do not reopen a closed point without new information.
- Surface acceptance / readiness criteria: pull them from the input, or formulate and confirm them.
- The limit of 3 is a budget for removing uncertainty, not a target to fill. Categories still Partial / Missing after the budget - record them in the brief as `[NEEDS CLARIFICATION: <specific question>]` markers (the same marker convention the `plan-conventions` background skill uses), not as prose; do not push further. Surface this remainder to the user only when it is non-empty; full coverage produces no summary.

## EXPLORE

Compare approaches, do not jump into the first one.

- Lay out 2-4 real approaches with explicit pros / cons for each. Do not present the first idea that comes to mind as the only option; show alternatives and trade-offs.
- Give a recommendation with a rationale (have an opinion), but leave the choice to the user.
- DRY and YAGNI: the recommended approach is the minimal viable one, building on how the task is already solved in the project. If there really is one reasonable approach, say so directly - do not stretch artificial alternatives.
- Validate the design with the user and record the selected approach.
- Record a significant design decision through the `decision-log` background skill - it applies the ADR gate and decides whether the decision is worth recording and where it lives (ADR / brief section / note / skip).

## ARTIFACT

Write a brief:

```
docs/briefs/YYYYMMDD-<slug>.md
```

It captures: the task / question; context; options; trade-offs; the chosen approach; the next step; and a link to the tracker ticket / task if there is one. A brief can be short for a simple task and detailed for a complex one.

Add a clarifications log only when at least one CLARIFY question was asked:

```markdown
## CLARIFICATIONS

### Session YYYY-MM-DD

- Q: <question> -> A: <accepted answer>
```

The accepted answer is integrated into the main brief text; the log records decision traceability. An answer that invalidates earlier brief text replaces it - contradicting stale wording must not remain.

Optional durable writes - only after explicit user approval: an ADR via the `decision-log` gate; a personal note if the user asks. Nothing durable is written from CLARIFY without approval.

## RULES

- Brainstorm produces the brief and stops - no plan, no code.
- Separate facts from assumptions throughout.
- Questions are hard-won and one at a time - 3 is a budget for removing uncertainty, not a target to fill; 0 is a normal outcome.
- Show 2-4 real approaches with trade-offs before recommending one; do not stretch artificial alternatives.
- Durable writes (ADR, note) happen only on explicit user approval.

## DIFFERENTIATION

- `/nxs:rnd` - two phases, CLARIFY (remove scope / terminology ambiguity) + EXPLORE (compare approaches) - open task shaping.
- `/nxs:dialectic` - compare two specific approaches head to head.
- `/nxs:wrong` - stop the current approach and find an alternative.

## NEXT

Brief written -> `/nxs:plan` turns it into a plan following the `plan-conventions` contract, then `/nxs:exec` to implement. For a bug rather than a task -> `/nxs:bug`. For a plain-language statement of the brief -> `/nxs:explain`.
