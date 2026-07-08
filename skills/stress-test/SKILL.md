---
description: The shared adversarial pressure kernel - steelman then antithesis, the six criteria, assumptions inventory, premortem, kill-criteria, fact-vs-assumption with decisive criteria, the honesty and concrete-justification discipline, and verdict shape. Background knowledge, not a user command.
user-invocable: false
---

# STRESS-TEST KERNEL

Load when pressure-testing an idea, approach, or claim. Workflow discipline, not a user-invocable command. Single shared kernel; injected by `/nxs:rnd` (STRESS) and `/nxs:dialectic`.

## STEELMAN THEN ANTITHESIS

Argue each side at its strongest form, never a straw man. Build the case FOR (steelman) as strong as an advocate would, then build the case AGAINST (antithesis) as strong as a critic would. Argue the strongest form of every side, including the one you expect to lose.

## THE SIX CRITERIA

Analyze each side across the same criteria - do not skew them toward an initial preference:

- what is good;
- what is bad;
- what risks there are (risks are NOT cons: cons always apply, risks apply only in edge cases);
- what happens in edge cases / failure modes;
- hidden assumptions the side depends on;
- maintenance cost.

## ASSUMPTIONS INVENTORY

List what must hold for a side to survive. Make explicit every condition the side silently relies on, separate from what is already established.

## PREMORTEM

Assume the idea has already failed, then name what turned it into a failure. Trace the concrete path from "chosen" to "wrong": which assumption broke, which edge case hit, which cost was underestimated.

## KILL-CRITERIA

State the conditions under which to drop or shrink the idea. Name the observable signal that says "stop" or "scope this down", so the decision to abandon is decided in advance rather than defended after the fact.

## FACT VS ASSUMPTION, DECISIVE CRITERIA

Separate fact from assumption. Mark what is established vs what must hold for a side to win. Name the decisive criteria - the ones that actually tip the choice.

## DISCIPLINE

- Be honest. Do not pretend a clear winner is close. If one side clearly wins, say so - do not pretend they are close. If it is close, say it is close and name the tipping criteria.
- Every pro and con needs a concrete justification, not an abstraction.

## VERDICT SHAPE

```text
Verdict: <holds | fails | holds only when ...>
```

## SCALING

- Trivial input collapses to a one-line verdict. Do not force the full kernel onto a low-stakes question.
- Risky / architectural input expands to the full kernel: all six criteria, assumptions inventory, premortem, kill-criteria, fact-vs-assumption, decisive criteria.
- Mode/consumer subset mapping (keep the output shape of each consumer frozen):
  - A two-option compare (dialectic Mode A: pros / cons / risks -> recommendation) applies the six criteria + risks-not-cons + fact/assumption + decisive criteria, and keeps its own compare structure.
  - Premortem and kill-criteria are scale-optional; they are NOT forced into Mode A's output.
