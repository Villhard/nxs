---
description: Shape a feature or open question when explicitly asked to use /dev:rnd. Save an agreed spec and one or more tickets, without implementation tasks or code. Use /dev:bug for a reported failure and the client's /plan for an already clear task.
argument-hint: "[request | spec path | tracker key | question]"
disable-model-invocation: true
---

# /dev:rnd

Think a request through to a spec and its tickets, then stop. The entry point for new work.

Accepted input: a request in words, a feature idea, a spec path, a tracker key / URL / pasted ticket, or an open question. With nothing given, work from the current session context.

Before reading input, read [feature directory](../../references/feature-directory.md): it owns tracker input, external specs, domain documents, the feature location and local storage.

Example: /dev:rnd add rate limiting to the public API

Suggest the next command at a handoff; never start it automatically.

## STANCE

- Produce the spec and the tickets and stop. The plan, the code, and any behavior change belong to the client's plan mode.
- Four steps in order: clarify, explore, stress-test, slice. A clear request may need zero questions, one obvious approach and no stress pass. After agreement, slice always runs, even when it yields one ticket.
- Full collapse makes the spec ceremony. Say so out loud and offer to describe the task straight to `/plan` in Claude Code or Codex instead.
- For a bug rather than a request, route to `/dev:bug`.

## EXISTING INPUT

Read an explicit spec path before shaping; a missing or unreadable file stops, never becomes a new request. Inspect its decisions, exclusions, testing requirements, answers and open questions regardless of its producer or ready label. Check them against relevant code. An approved spec with no unresolved decision enters ARTIFACT and SLICE directly: do not repeat settled clarification, explore or stress steps. New contradictory evidence reopens only the affected decision; show the evidence and ask before changing it. An unresolved spec follows CLARIFY and cannot produce tickets while a material question remains open.

A source spec follows EXTERNAL SPEC from feature directory.

Remote input follows TRACKER INPUT from feature directory. Preserve its evidence in the spec's existing sections. With unknown or unmapped blockers, an authorized draft records the missing evidence as a clarification and produces no tickets.

## CLARIFY

Read the relevant code, patterns, and integration points first - directly or through the built-in Explore agent. Scale the reading to the request: trace the current behavior and likely change points, look for reusable code, and check affected consumers and tests for a migration. Before discussing approaches, show a short account of those findings with repository-relative paths and symbol names where applicable. If no suitable implementation was found, say where you looked; do not invent an analogue. Ask only about what the code does not answer. Do not over-read. Clarify a fuzzy domain term before anything else.

Apply DOMAIN DOCUMENTS from feature directory before asking: use the glossary's terms in the spec and tickets, and ask only about a term it leaves undefined or the request contradicts. Name a missing term or a decision worth recording in the reply.

Ask one question at a time, 2-4 concrete options with a recommendation, open-ended only where a choice is unnatural. After each answer, revise the understanding and derive the next question from the updated picture.

Stop as soon as the next question would not change a decision. Zero questions is a normal and frequent outcome.

Separate facts from assumptions throughout: state what the input and the code establish versus what you are inferring. Surface the acceptance criteria - pull them from the input or formulate and confirm them. They become the checkboxes on the tickets.

An axis deliberately left open goes into the spec as `[NEEDS CLARIFICATION: <specific question>]`, not as prose.

## EXPLORE

Lay out 2-4 real approaches with pros and cons, and show the trade-offs. Give a recommendation with a rationale and leave the choice to the user.

The recommended approach is the minimal viable one, built on how the project already solves this. If there is genuinely one reasonable approach, say so - a stretched alternative is worse than none.

Mark an approach that contradicts a recorded project decision as such, with the record's path and what it would reopen. The user decides whether to reopen it; never drop the approach or the record silently.

## STRESS

Pressure-test the recommended approach before writing it down:

1. **Assumptions** - what must hold for it to survive, stated explicitly.
2. **Premortem** - assume it already failed, then trace the path: which assumption broke, which edge case hit, which cost was underestimated.
3. **Kill criteria** - the observable signal that says stop or scope this down, decided now rather than defended later.
4. **Verdict** - `holds` | `fails` | `holds only when ...`.

Every concern needs concrete evidence or an explicitly named assumption. A fatal finding sends you back once: to explore for another approach, or to clarify for missing information. If it still fails after that loop, stop with the unresolved decision. A loop limit never turns a failed approach into an agreed spec.

## ARTIFACT

One feature is one local directory, holding the spec, one file per ticket and any saved research:

```
.scratch/<feature-slug>/spec.md
.scratch/<feature-slug>/issues/NN-<slug>.md
.scratch/<feature-slug>/research/<topic>.<json|md>
.scratch/<feature-slug>/research/<topic>/
```

Everything research saves goes under `research/`, including files written by agents or workflows this command launches: one topic's result as `research/<topic>.json` or `.md`, and the scripts, probes, downloads and raw outputs behind it in `research/<topic>/`. `<topic>` is one to three lowercase english words, hyphenated, shared by the result and its folder. Give each launched agent or workflow its `research/<topic>/` path as its output location. `## Implementation Decisions` cites results by their path inside the feature. The feature root holds only `spec.md`, `root-cause.md`, `review.md` and the `issues/` and `research/` directories.

The directory follows LOCATION and LOCAL STORAGE from feature directory. Leave a `root-cause.md` already sitting there untouched, and never replace an existing `spec.md` without approval of that concrete revision. Decision documents, including tickets carrying a bare or Markdown-bold `Type:` field, supply context for a distinct implementation deliverable; never convert them in place.

Before writing the spec, read [assets/spec.md](assets/spec.md), resolved relative to this installed skill directory. It lists the seven permitted `##` headings in order. Keep Problem Statement and Solution; omit any other section only when it has no content. Do not invent other `##` headings.

`## Solution` holds the chosen approach with the answers integrated. `## Implementation Decisions` holds the findings that influenced the approach, with their code references, and the decisions every ticket inherits, each with a brief reason, including applicable recorded project decisions with their paths; keep assumptions distinguishable from confirmed facts. `## Testing Decisions` holds the relevant test findings and chosen checks. `## Out of Scope` names what is explicitly not being done. `## Further Notes` takes the options with their rejection reasons, the stress verdict when the stress step ran, and a `- Q: <question> -> A: <answer>` log when at least one question was asked. Sections scale with the request, an empty one is dropped, headings keep their names.

Before the first durable write, show the proposed spec and ticket breakdown. Obtain approval unless the user has already approved that content or explicitly authorized writing it from the agreed decisions. Reuse that authorization. Material unanswered decisions still block ready tickets; permission to save a draft does not answer them or start `/plan`.

## SLICE

Inspect every existing `issues/*.md` before proposing a breakdown. Match existing scope and dependencies; preserve file names, ticket IDs, blockers, statuses, checked criteria, plans and Comments/execution notes byte-for-byte on a repeat. Existing tickets that cover the spec are the output, not files to regenerate. General permission to save tickets does not authorize replacing their history. If changed scope or dependencies cannot preserve the existing graph, show the affected files and decisions and stop for a concrete revision decision; reuse only authorization that covers that revision. Never renumber, reset or silently replace existing work, including ready tickets.

Cut genuinely new authorized work into tickets under `issues/`. Each ticket is one vertical slice: end-to-end behavior a user or an API can exercise, demoable on its own, sized to fit one fresh context window. Never a layer - not the schema, then the service, then the route. A wide refactor is the exception: expand, migrate in batches, contract, one ticket per batch, with passing checks after each ticket. If only final integration can pass, ask for a compatible breakdown instead of promising execution with failing intermediate tickets. One ticket is the normal outcome for small work and gets no ceremony - same file, same shape.

Before writing tickets, read [ticket](../../references/ticket.md): it owns the template, numbering, fields and statuses. Show each proposed ticket's `**Branch:**` line in the breakdown before writing.

## NEXT

Return the spec path, created or preserved ticket paths and any unresolved clarification. Suggest `/plan <ticket-path>` in Claude Code or Codex for the first `ready-for-agent` implementation ticket that has no bare or Markdown-bold `Type:` field and whose local blockers are `resolved`. An incomplete spec or unknown/unmapped remote blocker has no ready handoff; existing tickets do not become new work on a repeat. Do not invoke another command.
