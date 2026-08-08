---
description: Think a request through to a plan-ready brief - the entry point for new work. Use to shape a fuzzy request, feature idea, or open question before planning.
argument-hint: "[request | tracker key | question]"
---

# /nxs:rnd

Think a request through to a plan-ready brief and stop. The entry point for new work.

Accepted input: a request in words, a feature idea, a tracker key / URL / pasted ticket, or an open question. With nothing given, work from the current session context.

Example: /nxs:rnd add rate limiting to the public API

## STANCE

- Produce the brief and stop. The plan, the code, and any behavior change belong to the commands that own them.
- Three steps in order: clarify, explore, stress-test. All three scale with the request - a clear one collapses to zero questions, one obvious approach, and no stress pass.
- Full collapse makes the brief ceremony. Say so out loud and offer to route straight to `/nxs:plan` instead.
- For a bug rather than a request, route to `/nxs:bug`.

## CLARIFY

Read the relevant code, patterns, and integration points first - directly or through the built-in Explore agent. Ask only about what the code does not answer. Do not over-read. Clarify a fuzzy domain term before anything else.

Ask one question at a time, 2-4 concrete options with a recommendation, open-ended only where a choice is unnatural. After each answer, revise the understanding and derive the next question from the updated picture.

Stop as soon as the next question would not change a decision. Zero questions is a normal and frequent outcome.

Separate facts from assumptions throughout: state what the input and the code establish versus what you are inferring. Surface the acceptance criteria - pull them from the input or formulate and confirm them.

An axis deliberately left open goes into the brief as `[NEEDS CLARIFICATION: <specific question>]`, not as prose.

## EXPLORE

Lay out 2-4 real approaches with pros and cons, and show the trade-offs. Give a recommendation with a rationale and leave the choice to the user.

The recommended approach is the minimal viable one, built on how the project already solves this. If there is genuinely one reasonable approach, say so - a stretched alternative is worse than none.

## STRESS

Pressure-test the recommended approach before writing it down:

1. **Assumptions** - what must hold for it to survive, stated explicitly.
2. **Premortem** - assume it already failed, then trace the path: which assumption broke, which edge case hit, which cost was underestimated.
3. **Kill criteria** - the observable signal that says stop or scope this down, decided now rather than defended later.
4. **Verdict** - `holds` | `fails` | `holds only when ...`.

Every concern carries a concrete justification. If the approach clearly survives, say so. A fatal finding sends you back once - to explore if the approach must change, to clarify if a new uncertainty opened. After that single loop the brief is frozen.

## ARTIFACT

The brief is one file inside a story - one story is one whole unit of work, one directory:

```
docs/nxs/stories/YYYYMMDD-<slug>/brief.md
```

`YYYYMMDD` is the day the story is created and does not change on later writes into it. `<slug>` is two to four lowercase english words from the request, hyphenated. A tracker key names the directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/`. The files inside keep their fixed names.

Create the story when the request has none yet; write into the one the input names when it does.

Keep the headings stable - `/nxs:plan` reads the brief by them:

```markdown
# Brief: <title>

- Date: YYYY-MM-DD
- Tracker: <key / URL - drop the line if there is none>

## Request

## Context (facts from the code)

## Acceptance criteria

## Options

<2-4 options as `### O<n>. <name> - recommended | rejected: <reason>`, each with pros and cons>

## Chosen approach

<the selected approach with the answers integrated, plus "Explicitly not doing: ..." for what is out of scope>

## Stress

<assumptions, failure modes, kill criteria, verdict - only when the stress step actually ran>
```

Sections scale with the request, empty ones are dropped, headings keep their names. Add a `## Clarifications` log only when at least one question was asked, as `- Q: <question> -> A: <answer>`. The answer is integrated into the brief text; an answer that invalidates earlier wording replaces it.

Nothing durable is written before the user approves it.

## NEXT

Brief written -> `/nxs:plan` turns it into a plan, then `/nxs:exec` implements it.
