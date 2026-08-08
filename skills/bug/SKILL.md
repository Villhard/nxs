---
description: Investigate a bug to a confirmed root cause - the bug entry point. Use when handed a bug report, a tracker bug key/URL, stack trace, log, or observed misbehavior, before any fix is proposed.
argument-hint: "[tracker key | bug description | path]"
---

# /nxs:bug

Reach a confirmed root cause, then stop. The bug entry point.

Accepted input: a tracker key / URL, pasted bug text, observed behavior, a stack trace or log, or a path.

Example: /nxs:bug PROJ-4213

## STANCE

- Confirm the cause with reproducible evidence and leave the fix to `/nxs:plan` and `/nxs:exec`. No patch, no product-code change here.
- The investigation runs in the main context: read code and logs, run the repro and the existing tests, build minimal probes. Probes, debug logs, and a throwaway harness are temporary and come out at the end. The root cause is the only file that stays.
- Stay skeptical of the first plausible explanation. Clarify a fuzzy term in the report before running the 5-Why.

## THE LOOP

1. **Build the cheapest feedback loop** that reproduces the real symptom, not an adjacent failure. Scan the repo for what is already there - test runner, fixtures, local server - and pick the fastest: a failing test, a curl script against the API, a CLI invocation with a fixture, a replay of a captured trace, a throwaway wrapper around the suspect function, or a good-versus-broken differential run. A structured script for the user to run by hand is the last resort, for when the runtime is out of your reach.
2. **Reproduce** exactly the symptom the report describes.
3. **Minimize** it to the fewest steps, the least data, the fewest dependencies.
4. **Form 3-5 ranked hypotheses**, each with a prediction: "if X is the cause, then change or observation Y produces Z". A hypothesis without a prediction is dropped.
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

Example. Symptom: the API returns 500 on payment. Unhandled exception in the payment handler -> no catch for a provider timeout -> the provider never used to time out -> order volume grew and it responds slower -> the call is synchronous and RPS grew. Root cause: synchronous coupling to an external provider under increased load. The fix is not "add a catch" but "move to a queue".

## WHEN IT WILL NOT CONFIRM

- Reproduction fails - mark it an assumption, continue carefully, record the missing evidence.
- Several plausible causes - describe them all, pick the more likely one with a justification, mark the rest rejected with a reason.
- Requested evidence unavailable - work with what is there and mark the gap as an assumption.

## ARTIFACT

The root cause is one file inside a story - one story is one whole unit of work, one directory:

```
docs/nxs/stories/YYYYMMDD-<slug>/root-cause.md
```

`YYYYMMDD` is the day the story is created and does not change on later writes into it. `<slug>` is two to four lowercase english words from the report, hyphenated. A tracker key names the directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/`. The files inside keep their fixed names.

Create the story when the report has none yet; write into the one the input names when it does.

Keep the headings stable - `/nxs:plan` reads the root cause by them:

```markdown
# Root cause: <title>

- Date: YYYY-MM-DD
- Tracker: <key / URL - drop the line if there is none>

## Symptom

## Repro

<the feedback loop that was built, and the minimized repro with the exact steps to run it>

## Evidence

## Hypotheses

<ranked, each with its prediction and the probe that confirmed or killed it>

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

Root cause confirmed -> `/nxs:plan` for the fix plan, then `/nxs:exec` to implement it.
