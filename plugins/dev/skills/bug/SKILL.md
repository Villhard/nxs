---
description: Investigate a reported failure when explicitly asked to use /dev:bug. Save reproducible evidence and a confirmed root cause, or the evidence still missing. Do not implement a fix; a confirmed cause can go to /dev:plan.
argument-hint: "[tracker key | bug description | path]"
disable-model-invocation: true
---

# /dev:bug

Investigate the reported symptom and save the conclusion, then stop. A confirmed cause and an incomplete investigation are different outcomes.

Accepted input: a tracker key / URL, pasted bug text, observed behavior, a stack trace or log, or a path.

A tracker key or URL is read before anything else - through the tracker when it is reachable, otherwise ask the user to paste the ticket. Never infer its content from the key.

Example: /dev:bug PROJ-4213

Run only when the user selects this command or directly asks to use it. Discussion, quotations, handoffs and mentions are not invocation. Suggest the next command at a handoff; never start it automatically.

## STANCE

- Confirm the cause with reproducible evidence and leave the fix to `/dev:plan` and `/dev:exec`. No patch, no product-code change here.
- The investigation runs in the main context: read code and logs, run the repro and the existing tests, build minimal probes. Probes, debug logs, and a throwaway harness are temporary and come out at the end. The root cause is the only file that stays.
- Stay skeptical of the first plausible explanation. Clarify a fuzzy term in the report before running the 5-Why.

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

For an unconfirmed result, `## Fix direction` and `## Regression test` say that they are pending confirmation. Conditional ideas may be recorded as hypotheses, never as an approved implementation direction. Save the incomplete investigation and stop for the missing evidence; do not hand it to plan as ready.

## ARTIFACT

The root cause is one file at the root of a feature directory - one feature is one directory:

```
.scratch/<feature-slug>/root-cause.md
```

`<feature-slug>` is two to four lowercase english words from the report, hyphenated. A tracker key names the directory - `.scratch/<KEY>-<slug>/`. The file name is fixed.

Create the feature directory when the report has none yet; write into the one the input names when it does. A `spec.md` already sitting there is left untouched - a bug that grew into a feature carries both documents side by side. Never write into a directory that holds a `map.md`: that one belongs to another tool's effort, so pick a different slug and say in one line why.

Write no ticket here. Once the cause is confirmed, `/dev:plan` selects or creates the fix ticket using its numbering rules.

Keep the headings stable - `/dev:plan` reads the root cause by them:

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

## NEXT

Return the root-cause path and state whether the cause is confirmed or unconfirmed. A confirmed result names the evidence and suggests `/dev:plan`; an unconfirmed result names the missing evidence or next discriminating probe. Do not invoke another command.
