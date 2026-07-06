---
description: Find architectural friction and deepening opportunities in a subsystem - scan structure, propose 3-5 candidates each with problem, cost, proposed deepening, benefits, risks, and a recommendation strength, then a top pick and open questions. Read-only. Use to surface structural friction without running code or changing it.
argument-hint: "[subsystem | scope]"
---

# /nxs:rnd-architecture

Analyze structural friction in a subsystem and propose deepening opportunities. Read-only: it reads code and structure, identifies friction, and proposes candidates - it does not change code and does not write a plan. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: a subsystem or scope (path / area), or nothing (analyze the current session context or the repo, narrowing scope with one question if too broad).

## STANCE (ARCHITECTURE ONLY)

- Analyze structure, not runtime behavior and not a specific bug. This is static reasoning over names, boundaries, dependency directions, and contracts - nothing is executed.
- Read-only. Do not change code, do not create `docs/plans/*`, do not run a refactor. The deliverable is a set of candidates and a recommendation.
- Not a code review: do not hunt for bugs or flag security findings. Structural friction only.
- 3-5 candidates, never padded to 10. If there are fewer real ones, give fewer.
- If the user wants a plan for a chosen refactor, route to `/nxs:dev-plan`; this skill stops at the recommendation.

## VOCABULARY (architecture-depth, inlined)

One canonical set of words for the analysis - no parallel synonyms within a session. If the project's `docs/.ai/domain-language.md` defines its own term for the same concept, respect the project canonical and do not impose your own.

- module - a unit of code with an explicit boundary (package / directory / namespace / class) that has a name and a public surface.
- interface - the public contract of a module: the operations it promises to support, what clients see. In code: functions / methods / types exported outward.
- implementation - the internal realization hidden behind the interface; changeable without clients' consent.
- depth - the ratio of functionality provided through the interface to how narrow that interface is. High depth = a lot of functionality behind a small surface.
- shallow module - interface almost as large as implementation; it does not hide complexity, it passes it along. Anti-pattern: thin wrappers, getter / setter chains, 1:1 wrappers.
- deep module - narrow interface, substantial implementation behind it; hides complexity, gives the client a simple contract.
- seam - a point where you can swap the implementation or wedge in without changing client code (interface, factory, dependency injection, port). A good seam is where the split is natural.
- adapter - an implementation of someone else's contract via existing code; connects external systems (HTTP, DB, queue) through a stable internal seam.
- locality - related changes stay in one place. High locality = editing one behavior touches one module; low locality = the edit is smeared around.
- leverage - how far one change scales. High leverage = one edit safely has an effect in many places; low leverage = every improvement requires individual work.
- deletion test - a thought experiment: what breaks or gets simpler if this module / abstraction / parameter / flag is deleted. If the answer is "nothing important", it is a candidate for deletion, not deepening. Keep it a short item in the report, not a chapter.

Signals to scan for: shallow modules, leaky interfaces, missing or premature seams, low leverage, broken locality, deletion-test candidates.

Anti-patterns to name honestly:

- term-creep - adding "your own" term alongside the canonical one.
- spotted abstraction - a module presented as deep but with loud name and trivial internals - no real depth.
- premature seam - a seam added "just in case", without a second real client.
- shallow re-wrap - renaming a shallow module without increasing its depth.

Shallow / deep are evaluative labels: always explain in what exactly the interface is wider than the implementation, or vice versa.

## PROCEDURE

1. Read project AI context if it exists: `docs/.ai/index.md`, `docs/.ai/domain-language.md`, plus discoverable ADR / project docs.
2. Determine scope - a specific subsystem / code area, or the whole repo, from the input. If the scope is too broad to analyze usefully, narrow it with one question.
3. Scan the code area statically: names, module boundaries, dependency directions, contracts, tests. Do not run anything.
4. Identify friction points through the VOCABULARY signals above - where depth is low, seams are missing or premature, locality is broken, leverage is thin, or an abstraction fails the deletion test.
5. Produce 3-5 candidates. Each candidate reports:
   - files / modules involved;
   - problem - the structural friction, in vocabulary terms;
   - why it hurts - the concrete cost (churn, low locality, leaky contract, forced individual work);
   - proposed deepening - the structural change that would raise depth / restore locality / add or remove a seam;
   - benefits - in locality / leverage / testability;
   - risks - what the change threatens, cost, blast radius;
   - recommendation strength: Strong / Worth exploring / Speculative.
6. Finish with a top recommendation and open questions - which candidate to explore further.
7. If the user picks a candidate, move into a design conversation, one question at a time:
   - one question with a recommended answer and rationale, not a list;
   - use the VOCABULARY consistently, no parallel synonyms; on term ambiguity, stop and clarify;
   - a new or clarified project term is written to `docs/.ai/domain-language.md` only after approval (see REFS);
   - a significant architectural decision goes through the `decision-log` gate (see REFS) - only after approval.
8. Do not change code. Do not create a plan. If the user wants a plan, recommend `/nxs:dev-plan`.

## RULES

- Read-only: no code changes, no `docs/plans/*`, no refactor execution.
- 3-5 candidates, each with a recommendation strength; fewer if fewer are real, never padded.
- Evaluative labels (shallow / deep) always come with an explanation of where the interface and implementation diverge.
- Design phase: one question at a time, each with a recommended answer.
- Durable writes (glossary term, ADR, brief) happen only after explicit user approval.
- Respect the project canonical term when `docs/.ai/domain-language.md` defines one.

## ARTIFACT

By default - a chat report, no durable file. The report carries:

- scope analyzed;
- 3-5 candidates, each with files / modules, problem, why it hurts, proposed deepening, benefits, risks, recommendation strength;
- top recommendation;
- open questions.

Only when the user explicitly asks to save the result, propose a brief and write it after approval:

```text
docs/briefs/YYYYMMDD-<slug>-architecture-review.md
```

Fields: scope, candidates with the report fields above, top recommendation, open questions. This skill does not create a plan - if the user wants one, route to `/nxs:dev-plan`.

## REFS

- Resolve a fuzzy or ambiguous domain term through the `domain-language` background skill before analysis; stop on ambiguity rather than guessing, and respect the project canonical.
- Record a significant architectural decision through the `decision-log` background skill - it applies the ADR gate and decides whether the decision is worth recording and where it lives (ADR / brief / note / skip). Only after approval.

## ROUTING / DIFFERENTIATION

- `/nxs:rnd-architecture` - structural friction analyzed statically, without running code.
- `/nxs:rnd-prototype` - a question about runtime behavior that reading code cannot settle.
- `/nxs:dev-diagnose` - a specific bug.
- `/nxs:rnd-dialectic` - comparing two specific approaches head to head.
- `/nxs:dev-review` - finding problems in a diff.

## NEXT

Candidate chosen and worth implementing -> `/nxs:dev-plan` turns the refactor into a plan, then `/nxs:dev-exec`. Decision deserves an ADR -> `decision-log`. A runtime question surfaced instead -> `/nxs:rnd-prototype`.
