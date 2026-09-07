---
description: Think a request through to a spec and a set of tickets - the entry point for new work. Use to shape a fuzzy request, feature idea, or open question before planning.
argument-hint: "[request | tracker key | question]"
disable-model-invocation: true
---

# /dev:rnd

Think a request through to a spec and its tickets, then stop. The entry point for new work.

Accepted input: a request in words, a feature idea, a tracker key / URL / pasted ticket, or an open question. With nothing given, work from the current session context.

A tracker key or URL is read before anything else - through the tracker when it is reachable, otherwise ask the user to paste the ticket. Never infer its content from the key.

Example: /dev:rnd add rate limiting to the public API

## STANCE

- Produce the spec and the tickets and stop. The plan, the code, and any behavior change belong to the commands that own them.
- Four steps in order: clarify, explore, stress-test, slice. The first three scale with the request - a clear one collapses to zero questions, one obvious approach, and no stress pass. The slice step always runs, even when it yields one ticket.
- Full collapse makes the spec ceremony. Say so out loud and offer to route straight to `/dev:plan` instead.
- For a bug rather than a request, route to `/dev:bug`.

## CLARIFY

Read the relevant code, patterns, and integration points first - directly or through the built-in Explore agent. Scale the reading to the request: trace the current behavior and likely change points, look for reusable code, and check affected consumers and tests for a migration. Before discussing approaches, show a short account of those findings with repository-relative paths and symbol names where applicable. If no suitable implementation was found, say where you looked; do not invent an analogue. Ask only about what the code does not answer. Do not over-read. Clarify a fuzzy domain term before anything else.

Ask one question at a time, 2-4 concrete options with a recommendation, open-ended only where a choice is unnatural. After each answer, revise the understanding and derive the next question from the updated picture.

Stop as soon as the next question would not change a decision. Zero questions is a normal and frequent outcome.

Separate facts from assumptions throughout: state what the input and the code establish versus what you are inferring. Surface the acceptance criteria - pull them from the input or formulate and confirm them. They become the checkboxes on the tickets.

An axis deliberately left open goes into the spec as `[NEEDS CLARIFICATION: <specific question>]`, not as prose.

## EXPLORE

Lay out 2-4 real approaches with pros and cons, and show the trade-offs. Give a recommendation with a rationale and leave the choice to the user.

The recommended approach is the minimal viable one, built on how the project already solves this. If there is genuinely one reasonable approach, say so - a stretched alternative is worse than none.

## STRESS

Pressure-test the recommended approach before writing it down:

1. **Assumptions** - what must hold for it to survive, stated explicitly.
2. **Premortem** - assume it already failed, then trace the path: which assumption broke, which edge case hit, which cost was underestimated.
3. **Kill criteria** - the observable signal that says stop or scope this down, decided now rather than defended later.
4. **Verdict** - `holds` | `fails` | `holds only when ...`.

Every concern carries a concrete justification. If the approach clearly survives, say so. A fatal finding sends you back once - to explore if the approach must change, to clarify if a new uncertainty opened. After that single loop the spec is frozen.

## ARTIFACT

One feature is one directory in the issue tracker, holding the spec and one file per ticket:

```
.scratch/<feature-slug>/spec.md
.scratch/<feature-slug>/issues/NN-<slug>.md
```

`<feature-slug>` is two to four lowercase english words from the request, hyphenated; a tracker key names the directory instead - `.scratch/<KEY>-<slug>/`. Write into the directory the input names when it has one, leave a `root-cause.md` already sitting there untouched, and never replace an existing `spec.md` without asking.

Never write into a `.scratch/<x>/` that holds a `map.md` - that directory belongs to `/wayfinder`. Pick another slug and say why in one line.

Before the first write into a NEW feature directory, resolve the tracker layout from the first line of `docs/agents/issue-tracker.md` in this repo, else the same relative path under the user's Claude config directory, else local markdown. `# Issue tracker: Local Markdown`, or no such file anywhere: proceed silently. GitHub or GitLab: name the tracker, say in one sentence that writing under `.scratch/` here leaves the shaping in local files while the issues live on that tracker, then let the user pick - write under `.scratch/` anyway, or stop and drive the tracker with `/to-spec` and `/to-tickets` and come back with the ticket path. Ask once; the answer holds for the session. Never invent a `gh` or `glab` call.

The spec carries these seven headings, in this order, and nothing else at `##`:

```markdown
# <Feature title>

## Problem Statement

## Solution

## User Stories

## Implementation Decisions

## Testing Decisions

## Out of Scope

## Further Notes
```

`## Solution` holds the chosen approach with the answers integrated. `## Implementation Decisions` holds the findings that influenced the approach, with their code references, and the decisions every ticket inherits, each with a brief reason; keep assumptions distinguishable from confirmed facts. `## Testing Decisions` holds the relevant test findings and chosen checks. `## Out of Scope` names what is explicitly not being done. `## Further Notes` takes the options with their rejection reasons, the stress verdict when the stress step ran, and a `- Q: <question> -> A: <answer>` log when at least one question was asked. Sections scale with the request, an empty one is dropped, headings keep their names.

Nothing durable is written before the user approves it.

## SLICE

Cut the chosen approach into tickets under `issues/`, numbered from `01` in dependency order so a blocker always carries a lower number than what it blocks. Each ticket is one vertical slice: end-to-end behavior a user or an API can exercise, demoable on its own, sized to fit one fresh context window. Never a layer - not the schema, then the service, then the route. A wide refactor is the exception: expand, migrate in batches, contract, one ticket per batch. One ticket is the normal outcome for small work and gets no ceremony - same file, same shape.

Write each one exactly like this:

```markdown
# <NN>: <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list>

**Blocked by:** <the numbers and titles of the tickets that gate this one, or "None (can start immediately)">

**Status:** ready-for-agent

- [ ] <acceptance criterion>
- [ ] <acceptance criterion>
```

Rules the template does not show:

- `**Status:**` is `needs-info` instead when an open `[NEEDS CLARIFICATION: ...]` marker sits in this ticket's own body. A marker still open in the spec gates the whole feature: write no tickets at all until it is answered.
- `**Blocked by:**` names numbers first - `01`, or `01, 03` - with a title optional after each number. `/dev:exec` resolves every leading number against `issues/NN-*.md`, so a line without a number costs it a lookup.
- The checkboxes here are acceptance criteria, flipped once by `/dev:exec` after the last task is green. The implementation checkboxes are a different set that `/dev:plan` appends to this same file under `## Implementation`. Never write a `### Task` heading or a checkbox of that second kind here.
- No `## Parent` section and no back-link: the local ticket template has none, and the shared feature directory is the whole link to the spec.

## NEXT

Spec and tickets written -> `/dev:plan` plans one ticket, then `/dev:exec` executes it and marks it resolved.
