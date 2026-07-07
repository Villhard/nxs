---
description: Compare two concrete approaches head to head, or stress-test a single claim (steelman then attack) to reduce confirmation bias and reach a justified verdict. Use when the options or the claim are already formulated and you need an honest trade-off analysis, not brainstorming.
argument-hint: "[approach A vs B | claim]"
---

# /nxs:dialectic

Argue both sides at their strongest, surface the real trade-offs, and land a reasoned verdict. Self-contained skill: read-only, changes no code, writes no durable file by default. Output language and response style come from global rules, not this file.

Accepted input: two concrete approaches ("A vs B"), or a single claim / thesis to stress-test ("is this really true", "stress test this", "argue both sides"). If the input is vague, clarify before proceeding.

## MODES

- Mode A - compare two approaches: two specific, already-formulated options weighed head to head against the same criteria.
- Mode B - stress-test a claim: one thesis put under adversarial pressure. Build its strongest form (steelman), then build the strongest case against it (antithesis). Counters confirmation bias in a decision already leaning one way.

Pick the mode from the input. If only a fuzzy direction exists and the options are not yet concrete, this is not dialectic - route to `/nxs:rnd` first.

## PROCEDURE

1. Pin down the positions precisely. Mode A: state both options fairly in one line each. Mode B: state the claim, then its sharpest antithesis. If the description is vague, clarify before analyzing.
2. Steelman each side. Argue the strongest form of each position, never a straw man. In Mode B, make the case FOR the claim as strong as an advocate would, then make the case AGAINST as strong as a critic would.
3. Analyze each side across the same criteria - do not skew them toward an initial preference:
   - what is good;
   - what is bad;
   - what risks there are (risks are not cons: cons always apply, risks apply only in edge cases);
   - what happens in edge cases / failure modes;
   - hidden assumptions the side depends on;
   - maintenance cost.
4. Separate fact from assumption. Mark what is established vs what must hold for a side to win. Name the decisive criteria - the ones that actually tip the choice.
5. Synthesize. Produce a recommendation (Mode A) or a verdict on the claim (Mode B), justified with concrete reasoning, not abstractions. If one side clearly wins, say so; if it is close, say it is close and name the tipping criteria. State the conditions under which each side wins, and what is explicitly NOT chosen and why.

## DISCIPLINE

- No straw-manning. Argue the strongest form of every side, including the one you expect to lose.
- Be honest. If one option is clearly better, say so - do not pretend they are close. If they are close, say so and identify the tipping criteria.
- Every pro and con needs a concrete justification, not an abstraction.
- Separate risks from cons - they are different things.
- Separate fact from assumption. Name the decisive criteria explicitly.

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
