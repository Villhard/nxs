---
description: Investigate a bug to a confirmed root cause - the tracked-bug entry point. Use when handed a bug report, a tracker bug key/URL, stack trace, log, or observed misbehavior, before any fix is proposed.
argument-hint: "[tracker key | bug description | path]"
---

# /nxs:bug

Bug investigation entry point. Reach a confirmed root cause, then stop. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: tracker key / URL, pasted bug text, observed behavior, stack trace / log, or a path.

Example: /nxs:bug PROJ-4213

## STANCE (READ-ONLY INVESTIGATION)

- /nxs:bug confirms the root cause with reproducible evidence. It does not write the fix.
- The investigation runs in the main context: you read code and logs, run repro and existing tests, and build minimal probes. Nothing here mutates the repo.
- No fix, patch, or code change here. No exceptions. The fix goes through `/nxs:plan` (fix plan) and `/nxs:exec` (execution).
- No solution before the root cause is confirmed. Do not narrow to the first plausible explanation - stay skeptical.

## INTAKE

- If the input is a tracker key, URL, or pasted ticket, run the `intake` background skill first to parse structure and separate facts from assumptions, then continue here.
- When a domain term in the bug report is fuzzy or ambiguous, stop and clarify it before running 5-Why rather than guessing its meaning.

## DIAGNOSIS LOOP

A disciplined engineering cycle: build a cheap feedback loop, reproduce the exact symptom, minimize, form ranked falsifiable hypotheses with predictions, instrument one at a time, confirm with facts. Guess-based fixes are the main source of regressions; without a reproducible symptom any fix is a lottery; without a minimized repro the investigation drowns in noise; without predictions a hypothesis is a story, not a theory; parallel variable changes destroy the signal.

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

0. Feedback loop - build a cheap cycle from the list above before any hypotheses.
1. Reproduce - reproduce exactly the symptom the user reports, not an adjacent failure.
2. Minimize - reduce the repro to a minimum of steps, data, and dependencies.
3. Hypotheses - formulate 3-5 ranked falsifiable hypotheses before any probes.
4. Predictions - for each: "if X is the cause, then change / observation Y produces Z". A hypothesis without a prediction is dropped.
5. Instrument - test one hypothesis at a time: one probe, one changed parameter, one added log.
6. 5-Why - when a probe confirms a hypothesis, run the 5-Why chain (below) on that confirmed hypothesis, not on the original guess.
7. Confirm - root cause only when the predictions held and the evidence is reproducible.
8. Fix direction - stated only after the cause is confirmed.
9. Regression test - propose a test at the right seam: the nearest layer where the cause reproduces cheaply and stably.
10. Cleanup - remove debug logs, delete or mark the throwaway harness, record evidence and probes in the brief. Debug tools do not ship to main.

## FIVE-WHY

For each observation ask "why is this happening?" and get a cause from a deeper layer. Repeat ~5 times (typically 3-7) until reaching a layer that can actually be fixed. The real number is: until an actionable cause. Trivial bugs need only 1-2 steps. Each step relies on evidence, not guesses; if no evidence, mark it an assumption and verify. Cross-check each step against facts - a "story" is not a chain. Do not stop at the first bad answer, and do not dig past the actionable layer. If it drifts to "not our area" or to social/political causes, record it as a known limitation and return to the layer above. For technical bugs, stop at the technical boundary.

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

Enabled automatically when key evidence is unavailable to the agent, or on explicit request ("ask me for evidence"). List the specific evidence needed to build or validate the feedback loop (production logs, metrics, runtime access, manual-check results, fixtures, captured traces) and ask targeted questions.

- Adaptivity: before asking, scan the repo for observability and test config (`docker-compose*.yml`, `infra/`, `deploy/`, `.env.example`, `README`, `Makefile`, test runner, fixtures). If an observability stack is visible (Graylog / Kibana / Grafana / Sentry / custom), the question names the query (where, which filter, period, metric). If a test runner is visible, ask about an available fixture / replay payload. If nothing is visible, give a short phrasing and offer to expand.
- If the user replies "I don't know where to get it", switch to detailed mode: go back to what the repo showed and explain step by step; if the repo has nothing on the topic, ask for minimal context (logging stack, capturable trace).
- Boundary: ask only at key points where without input the loop cannot be built or a hypothesis cannot be distinguished from a guess. Not a constant dialogue. Answers become Confirmed evidence in hypotheses and in the 5-Why chain.

## STOP CONDITIONS

- If reproduction fails, mark it an assumption and continue carefully, recording the missing evidence explicitly.
- If several plausible causes exist, describe all, pick the more likely one with justification, and mark the rest as rejected with a reason.
- When the user cannot provide requested evidence, work with what is available and mark the unavailable evidence as an assumption.

## ARTIFACT

Write a root-cause brief:

```
docs/nxs/briefs/YYYYMMDD-<slug>-bug.md
```

When intake extracted a tracker identifier, include it in the name - `docs/nxs/briefs/YYYYMMDD-<KEY>-<slug>-bug.md` - so the brief stays navigable by the key, as the `intake` contract promises.

It captures: symptom; feedback loop / repro method; minimized repro; evidence; ranked hypotheses; tested probes; 5-Why chain; confirmed root cause; assumptions; fix direction; regression test idea; verification plan.

## RULES

- Loop before hypotheses - without a feedback loop the investigation is vibes.
- Reproduce the exact symptom, not a "similar" bug.
- Falsifiable or drop - a hypothesis without a prediction is not tested.
- One probe at a time - parallel changes destroy the signal.
- Evidence-backed 5-Why - the chain sits on top of a confirmed hypothesis.
- No solution before the root cause. Clean up debug tools before finishing.

## NEXT

Root cause confirmed -> `/nxs:plan` for the fix plan, then `/nxs:exec` to implement.
