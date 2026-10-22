---
description: Investigate a reported failure when explicitly asked to use it (/dev:bug in Claude Code, $dev:bug in Codex, /dev/bug in OpenCode). Save reproducible evidence and a confirmed root cause with one fix ticket for /plan, or the evidence still missing and no ticket. Do not implement a fix.
argument-hint: "[tracker key | bug description | path]"
disable-model-invocation: true
---

# /dev:bug

Investigate the reported symptom and save the conclusion, plus a fix ticket when the cause is confirmed, then stop. A confirmed cause and an incomplete investigation are different outcomes.

Accepted input: a tracker key / URL, pasted bug text, observed behavior, a stack trace or log, or a path.

Before reading input, read [feature directory](../../references/feature-directory.md): it owns tracker input, domain documents, the feature location and local storage.

Example: /dev:bug PROJ-4213

Suggest the next command at a handoff; never start it automatically.

## STANCE

- Confirm the cause with reproducible evidence and leave the fix to the ticket this command writes. No patch, no product-code change here.
- The investigation runs in the main context: read code and logs, run the repro and the existing tests, build minimal probes. Probes, debug logs, and a throwaway harness are temporary and come out at the end. The root cause and, once confirmed, the fix ticket are the only files that stay.
- Stay skeptical of the first plausible explanation. Clarify a fuzzy term in the report before running the 5-Why.
- Apply DOMAIN DOCUMENTS from feature directory to the report's terms and the suspect behavior. Behavior a recorded decision establishes is evidence with its path, not a defect by itself: say so and let the user decide whether the decision is the problem.

## THE LOOP

1. **Build the cheapest feedback loop** that reproduces the real symptom, not an adjacent failure. Scan the repo for what is already there - test runner, fixtures, local server - and pick the fastest: a failing test, a curl script against the API, a CLI invocation with a fixture, a replay of a captured trace, a throwaway wrapper around the suspect function, or a good-versus-broken differential run. A structured script for the user to run by hand is the last resort, for when the runtime is out of your reach.
2. **Reproduce** exactly the symptom the report describes.
3. **Minimize** it to the fewest steps, the least data, the fewest dependencies.
4. **Form ranked hypotheses**, each with a prediction: "if X is the cause, then change or observation Y produces Z". As many as there are checkable alternatives and no more - one, when a probe has already confirmed it. A hypothesis without a prediction is dropped.
5. **Instrument one at a time** - one probe, one changed parameter, one added log. Parallel changes destroy the signal.
6. **Run the 5-Why** on the hypothesis a probe confirmed, not on the original guess.
7. **Confirm** - a root cause only once the predictions held and the evidence reproduces. Then, and only then, name the fix direction and propose a regression test at the nearest layer where the cause reproduces cheaply and stably.
8. **Clean up** - remove debug logs, delete the throwaway harness, record the evidence and the probes in the root cause.

When key evidence is out of your reach, ask for it specifically. Scan the repo for its observability and test setup first (`docker-compose*.yml`, `infra/`, `.env.example`, `Makefile`, the test runner, fixtures) and name what you need: which log query with which filter and period, which fixture, which captured payload. Ask only where the loop cannot be built or a hypothesis cannot be told apart from a guess without it.

## FIVE-WHY

For each observation ask "why is this happening?" and get a cause from a deeper layer. Repeat until you reach a layer that can actually be fixed - typically 3-7 steps, 1-2 for a trivial bug, and always past a bad first answer. Each step stands on evidence; without it, mark the step an assumption and verify it. A chain drifting to "not our area" or to social causes is recorded as a known limitation and returns to the layer above.

```
Symptom: <observable behavior>

5-Why:
1. Why <symptom>? -> <cause>
   Evidence: <log / code / repro>
N. Why <cause from N-1>? -> <root cause>
   Evidence: ...

Root cause: <statement>
Fix direction: <what to actually fix>
```

Example: a request with `limit=0` returns ten records. The minimized test reproduces it; the parser uses `limit or 10`; a probe shows that testing for `None` preserves zero. This confirms default substitution as the cause. It does not establish increased traffic or justify redesigning the request pipeline.

## WHEN IT WILL NOT CONFIRM

| Evidence | Conclusion and next action |
| --- | --- |
| The reported symptom reproduces and a discriminating probe supports the cause | Record the confirmed cause, smallest supported fix direction and regression check. |
| Reproduction fails or required evidence is unavailable | State that the cause is unconfirmed. Record attempted checks, hypotheses and the specific missing evidence. |
| Several causes still fit | Keep them open and rank them with reasons. State the next probe that distinguishes them; reject a cause only when evidence disproves it. |

For an unconfirmed result, `## Fix direction` and `## Regression test` say that they are pending confirmation. Conditional ideas may be recorded as hypotheses, never as an approved implementation direction. Save the incomplete investigation and stop for the missing evidence; write no ticket and do not hand it off as ready.

## ARTIFACT

The root cause is one file at the root of a feature directory - one feature is one directory:

```
.scratch/<feature-slug>/root-cause.md
```

The directory follows LOCATION from feature directory. The file name is fixed.

Reproduction scripts, probes and raw outputs the investigation saves go under `.scratch/<feature-slug>/research/<topic>/`, `<topic>` being one to three lowercase english words, hyphenated; `root-cause.md` cites them by that path. Nothing else goes at the feature root.

Create the feature directory when the report has none yet; write into the one the input names when it does. Before overwriting an existing `root-cause.md`, apply the repeat rule under FIX TICKET. A `spec.md` already sitting there is left untouched - a bug that grew into a feature carries both documents side by side.

Keep the headings stable - the fix ticket's executor reads the root cause by them:

```markdown
# Root cause: <title>

- Tracker: <key / URL, or the path to the ticket this fix implements - drop the line if there is none>

## Symptom

## Repro

<the feedback loop that was built, and the minimized repro with the exact steps to run it>

## Evidence

## Hypotheses

<ranked, each with its prediction and probe result; untested alternatives say "not tested" and name the next probe>

## 5-Why

<the chain in the format above>

## Root cause

## Assumptions

<what could not be verified - drop the section when everything held>

## Fix direction

## Regression test
```

Every other heading stays even when the investigation fell short: an unconfirmed cause is stated as unconfirmed under `## Root cause`, not left out.

## FIX TICKET

Write one fix ticket only for a confirmed cause, after `root-cause.md` is saved. An unconfirmed cause, or several causes still open, gets no ticket.

Before writing, read [ticket](../../references/ticket.md): it owns the template, numbering, fields and statuses. Write the ticket into `issues/` of the same feature directory as `.scratch/<feature-slug>/issues/NN-<slug>.md`.

- `**What to build:**` the corrected behavior from the user's side, naming `root-cause.md` as its source.
- Acceptance criteria: the reported symptom no longer reproduces through the minimized repro, and the check from `## Regression test` exists and passes. Add a criterion only for a further requirement `## Fix direction` states.
- `**Blocked by:**` `None (can start immediately)` unless an existing ticket of this feature must land first; then its number.
- `**Branch:**` by the rule in the reference, with `<type>` `fix`.

On a repeat, check the tickets in `issues/` that already name this `root-cause.md`. An open one - any status but `resolved` and `wontfix` - is the fix ticket:

| Existing ticket | Action |
| --- | --- |
| Open, same confirmed cause | Leave `root-cause.md` and the ticket unchanged, and write no second ticket. Report a wrong line reference or another correction in the answer. |
| Open, new confirmed cause | Stop before rewriting `root-cause.md` or the ticket. Ask whether to update the ticket's What to build and criteria for the new cause, or to close it. After the answer, save `root-cause.md`. Update keeps the ticket's number, `**Status:**` and `**Branch:**`; close sets its `**Status:**` to `wontfix` as the user's decision and writes the next number by NUMBERING. |
| Only `resolved` or `wontfix` | Write the next number by NUMBERING. |

## NEXT

Return the root-cause path and state whether the cause is confirmed or unconfirmed. A confirmed result names the evidence, returns the fix ticket path and its `**Branch:**`, and suggests `/plan <ticket-path>` in Claude Code, Codex or OpenCode; an unconfirmed result names the missing evidence or next discriminating probe. Do not invoke another command.
