---
description: Explain a target from zero - a diff, file, function, flow, or subsystem - in plain words, scaling depth to what you point at. Understanding only, not a review. With no argument, explains the current session context.
argument-hint: "[topic | path | branch | flow | subsystem]"
---

# /nxs:explain

Explain the target in plain language, from zero. One command, one axis: depth. It scales from a single artifact to a whole subsystem by inference, no mode word. Understanding only - it never hunts bugs. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:explain src/payments/webhook.ts

## FROM ZERO

Assume the reader has not read the plan, the diff, or the code, and is not familiar with this area - not because they are slow, but because they have not looked yet. Supply the missing context; never skip the introductory layer, never write as if they already reviewed it. Audience: a smart person outside this domain - no ELI5, no condescension.

## DEPTH BANDS (inferred, no mode word)

Pick the smallest band that covers what the target points at; escalate or narrow on the user's cue ("deeper", "the whole flow", "the whole subsystem", "just this function").

| band | target / ask | output |
|---|---|---|
| 1 thing | one artifact: diff, file, function, error, config, term, pasted snippet | plain breakdown: what it is, what it does, why it matters, which parts are involved |
| 2 flow | a path / branch / feature across several files; "how does X work", "walk the flow" | meaning-grouped map in reading order: the pieces and how they connect, start to end |
| 3 area | a subsystem / domain; "onboard me", "where do I start" | orientation map: load-bearing components with one-line roles, responsibilities and boundaries, how it is observed and operated, where to start |

## PROCEDURE

1. Determine the target. No argument -> current session context. Ask one narrowing question only if the scope is genuinely unclear.
2. Infer the band from the target and the ask. Default to band 1 when ambiguous and offer to widen.
3. Read the minimum needed: band 1 - the one artifact; band 2 - the path / diff; band 3 - a breadth-first skeleton (entry points, key types), drilling only where signal is. For a wide area, fan out read-only collection to `nxs:explorer` or the built-in Explore and synthesize in the main context. Do not over-read.
4. Emit at the chosen band:
   - band 1 - four facets: what we are doing (one sentence), why it matters, where (files / components / integration points), what comes next;
   - band 2 - meaning-groups in reading order (Enhancement / Configuration / Tests / Docs), plus a simple ASCII diagram only if a flow spans several components;
   - band 3 - the facet map: TL;DR, entry points & key abstractions, responsibilities & boundaries, data & state, observability surface, config & dependencies, key flows, tests as documentation, glossary & gotchas, where to start. Omit facets that do not apply; never pad.
5. If not understood, go one band lower or one level closer to the core - do not restate the same level in other words, do not add analogies.

## RULES

- Understanding, not evaluation: never flag bugs / security / quality and never make review claims. Finding problems in a diff is `/nxs:review`.
- Plain words; technical terms stay English where customary. One idea at a time. No architectural essays, no motivational endings.
- Read-only, chat only; no durable file.
- The explanation saves time, not spends it. On doubt, prioritize clarity.

## NEXT

Turn into a plan -> `/nxs:plan`. Find problems in a diff -> `/nxs:review`.
