---
description: Compare two concrete approaches head to head, or stress-test a single claim (steelman then attack) to reduce confirmation bias and reach a justified verdict. Use when the options or the claim are already formulated and you need an honest trade-off analysis, not brainstorming.
argument-hint: "[approach A vs B | claim]"
---

# /nxs:dialectic

Argue both sides at their strongest, surface the real trade-offs, and land a reasoned verdict. Self-contained skill: read-only, changes no code, writes no durable file by default. Output language and response style come from global rules, not this file.

Accepted input: two concrete approaches ("A vs B"), or a single claim / thesis to stress-test ("is this really true", "stress test this", "argue both sides"). If the input is vague, clarify before proceeding.

Example: /nxs:dialectic REST vs gRPC for the internal API

## MODES

- Mode A - compare two approaches: two specific, already-formulated options weighed head to head against the same criteria. Applies the `stress-test` kernel's compare subset (six criteria + risks-not-cons + fact/assumption + decisive criteria); premortem/kill-criteria stay out of its output.
- Mode B - stress-test a claim: one thesis put under adversarial pressure. Build its strongest form (steelman), then build the strongest case against it (antithesis). Applies the full `stress-test` kernel. Counters confirmation bias in a decision already leaning one way.

Pick the mode from the input. If only a fuzzy direction exists and the options are not yet concrete, this is not dialectic - route to `/nxs:rnd` first.

## PROCEDURE

1. Pin down the positions precisely. Mode A: state both options fairly in one line each. Mode B: state the claim, then its sharpest antithesis. If the description is vague, clarify before analyzing.
2. Apply the `stress-test` background skill to the pinned positions - it owns the adversarial mechanics (steelman then antithesis, the same-criteria pass, fact-vs-assumption, decisive criteria) and the honesty / concrete-justification discipline. Wire the mode to the kernel per its SCALING mode-subset mapping: Mode A applies the compare subset and does NOT surface premortem/kill-criteria in its output; Mode B applies the full kernel.
3. Synthesize into the mode-specific output. Produce a recommendation (Mode A) or a verdict on the claim (Mode B) from the kernel's analysis. Mode A: state the conditions under which each side wins, and what is explicitly NOT chosen and why. Mode B: land the verdict on the claim. The honesty and decisive-criteria discipline comes from the kernel, not from re-inlining it here.

## OUTPUT

A chat report. No code changes, no durable file by default.

Mode A - compare two approaches:

```text
Option A: <name>
- pros: ...
- cons: ...
- risks: ...

Option B: <name>
- pros: ...
- cons: ...
- risks: ...

Recommendation: <A|B>
Reason: <concrete why>
Tradeoffs accepted: <what we give up>
Conditions: <when A wins, when B wins>
Explicitly NOT doing: <other option>, because <reason>
```

Mode B - stress-test a claim:

```text
Claim: <the thesis under test>
Steelman (for): <strongest case the claim is true>
Antithesis (against): <strongest case the claim is false>
Assumptions: <what must hold for the claim to survive>
Verdict: <holds | fails | holds only when ...>
Reason: <concrete why>
```

## NEXT

- dialectic compares two ALREADY-CONCRETE approaches or tests one formulated claim. That is the entry condition.
- Options not yet formulated, still exploring the shape of the solution -> `/nxs:rnd`.
- dialectic and `rnd` STRESS share one adversarial kernel (the `stress-test` skill), not separate copies - editing the kernel updates both.
