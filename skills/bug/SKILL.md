---
description: Investigate a bug to a confirmed root cause - the bug entry point. Use when handed a bug report, a tracker bug key/URL, stack trace, log, or observed misbehavior, before any fix is proposed.
argument-hint: "[tracker key | bug description | path]"
---

# /nxs:bug

Bug investigation entry point. Reach a confirmed root cause, then stop.

Accepted input: tracker key / URL, pasted bug text, observed behavior, stack trace / log, or a path.

Example: /nxs:bug PROJ-4213

## STANCE (INVESTIGATE, DO NOT FIX)

- /nxs:bug confirms the root cause with reproducible evidence and leaves the fix to `/nxs:plan` and `/nxs:exec`. No patch, no product-code change here, no exceptions.
- The investigation runs in the main context: you read code and logs, run repro and existing tests, and build minimal probes. Probes, debug logs, and a throwaway harness are temporary and come out in Cleanup; the brief is the only file that stays.
- Stay skeptical of the first plausible explanation - the root cause is confirmed before any solution is named.
- When a domain term in the bug report is fuzzy or ambiguous, clarify it before running 5-Why.

## DIAGNOSIS LOOP

Build a cheap feedback loop, reproduce the exact symptom, minimize, form ranked falsifiable hypotheses with predictions, instrument one at a time, confirm with facts.

### Feedback loop - choice

Before any hypotheses, build the cheapest cycle that reproduces the real symptom (not a similar failure). Scan the repo (test runner, fixtures, local server) and pick the fastest available:

1. failing test - unit / integration that reproduces the symptom;
2. curl / HTTP script - for an HTTP API;
3. CLI invocation with fixture - for CLI / job runner / batch;
4. replay captured trace / log / payload - replay a real request / event;
5. throwaway harness - a short wrapper around the suspect function;
6. differential loop - run good vs broken in parallel (version, env, input);
7. HITL structured script - last resort, only when the runtime is not available to the agent.

### Phases in order

0. Feedback loop - from the list above, before any hypotheses.
1. Reproduce - reproduce exactly the symptom the user reports, not an adjacent failure.
2. Minimize - reduce the repro to a minimum of steps, data, and dependencies.
3. Hypotheses - formulate 3-5 ranked falsifiable hypotheses before any probes.
4. Predictions - for each: "if X is the cause, then change / observation Y produces Z". A hypothesis without a prediction is dropped.
5. Instrument - test one hypothesis at a time: one probe, one changed parameter, one added log. Parallel variable changes destroy the signal.
6. 5-Why - when a probe confirms a hypothesis, run the 5-Why chain (below) on that confirmed hypothesis, not on the original guess.
7. Confirm - root cause only when the predictions held and the evidence is reproducible.
8. Fix direction - stated only after the cause is confirmed.
9. Regression test - propose a test at the right seam: the nearest layer where the cause reproduces cheaply and stably.
10. Cleanup - remove debug logs, delete or mark the throwaway harness, record evidence and probes in the brief. Debug tools stay out of main.

## FIVE-WHY

For each observation ask "why is this happening?" and get a cause from a deeper layer. Repeat until reaching a layer that can actually be fixed - typically 3-7 steps, 1-2 for a trivial bug, and always past a bad first answer. Each step stands on evidence; without it, mark the step an assumption and verify. A chain drifting to "not our area" or to social / political causes is recorded as a known limitation and returns to the layer above: for technical bugs, stop at the technical boundary.

Example - symptom: "API returns 500 on payment".

1. Why 500? -> Unhandled exception in the payment handler.
2. Why unhandled? -> No catch for a timeout from the payment provider.
3. Why no catch? -> The provider used to never time out, so it was not accounted for.
4. Why does it time out now? -> Order volume grew, the provider responds slower.
5. Why did we hit their latency? -> Sync call instead of async; RPS grew.

Root cause: sync coupling with an external provider under increased RPS. The fix is not "add a catch" (symptomatic) but "rework to async / queue".

Output format for the chain:

```
Symptom: <observable behavior>

5-Why:
1. Why <symptom>? -> <cause>
   Evidence: <log / code / repro>
2. Why <cause from 1>? -> <deeper cause>
   Evidence: ...
N. Why <cause from N-1>? -> <root cause>
   Evidence: ...

Root cause: <root cause statement>
Fix direction: <what to actually fix>
```

## EVIDENCE REQUEST MODE

Enabled automatically when key evidence is unavailable to the agent, or on explicit request ("ask me for evidence"). Name the specific evidence needed to build or validate the feedback loop - production logs, metrics, runtime access, manual-check results, fixtures, captured traces.

- Adapt the question to the repo: scan for observability and test config (`docker-compose*.yml`, `infra/`, `deploy/`, `.env.example`, `README`, `Makefile`, test runner, fixtures). An observability stack in sight (Graylog / Kibana / Grafana / Sentry / custom) -> name the query: where, which filter, period, metric. A test runner in sight -> ask about an available fixture / replay payload. Nothing in sight -> a short phrasing, with an offer to expand.
- "I don't know where to get it" -> detailed mode: go back to what the repo showed and explain step by step; if the repo has nothing on the topic, ask for minimal context (logging stack, capturable trace).
- Ask only where without input the loop cannot be built or a hypothesis cannot be distinguished from a guess. Answers become Confirmed evidence in hypotheses and in the 5-Why chain.

## STOP CONDITIONS

- Reproduction fails -> mark it an assumption and continue carefully, recording the missing evidence explicitly.
- Several plausible causes -> describe all, pick the more likely one with justification, and mark the rest as rejected with a reason.
- Requested evidence unavailable -> work with what is available and mark the unavailable evidence as an assumption.

## ARTIFACT

Write a root-cause brief:

```
docs/nxs/stories/YYYYMMDD-<slug>/root-cause.md
```

When the input carries a tracker key, it names the story directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/` - so the story stays navigable by the key. The files inside keep their fixed names.

It captures: symptom; feedback loop / repro method; minimized repro; evidence; ranked hypotheses; tested probes; 5-Why chain; confirmed root cause; assumptions; fix direction; regression test idea; verification plan.

## NEXT

Root cause confirmed -> `/nxs:plan` for the fix plan, then `/nxs:exec` to implement.
