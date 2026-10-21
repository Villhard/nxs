# FINDINGS

Read this reference before a review sweep. `review` rates and verifies findings with it, passes its SEVERITY BAR to every reviewer verbatim and passes VERIFY A FINDING to the verifier verbatim.

## SEVERITY BAR

Rate the demonstrated consequence under reachable conditions:

- **critical** - data loss or corruption, a security breach, or a crash on an ordinary user path.
- **major** - wrong behavior or a broken contract, beyond contained minor impact.
- **minor** - a real defect with contained impact.

For a test finding, name the concrete defect it would miss or the way the test fails incorrectly. A coverage gap over currently correct behavior is minor unless evidence shows a broader present failure in the test process; do not rate a hypothetical production defect as though it already existed. For documentation, name the reader's wrong action or misunderstanding. Rate instructions a machine or agent executes by what their consumer does wrong. Unclear, misleading or misspelled identifiers and test names are minor: explain the ambiguity or mismatch with their actual role and propose a clearer name. A runtime failure or written naming rule is not required. A synonym preference or prose taste alone is not a finding; a prose typo with no changed meaning is not a finding.

A plausible finding is at most **major**: critical requires a confirmed trigger.

Severity measures the defect, not the cost of fixing it. Keep a confirmed or plausible in-scope defect in Findings even when its fix is expensive or risky; describe that reach and risk under Fix. Out-of-scope defects belong in Follow-ups.

## VERIFY A FINDING

Read the finding's location with 20-30 lines of context in the version being checked. Trace a reachable input or state through callers and guards to the claimed consequence; cite the locations that establish or disprove it. For naming claims, compare the name with its actual role and uses; cite the ambiguity or mismatch instead of requiring a runtime failure. For coverage or documentation claims, inspect the relevant tests or contract too. A passing test alone does not disprove a runtime defect. Separate what the code proves from inferred consequences.

Give each candidate exactly one verdict:

- **confirmed** - you can name the input or state that triggers it and the wrong result. Quote the line.
- **plausible** - the mechanism is real, the trigger is uncertain (timing, environment, configuration). State what would confirm it.
- **refuted** - the code does not say that, the case is impossible by type, constant or invariant, this diff already handles it, or it is style with no observable effect. Quote the line that proves it.

Plausible is the default for realistic states: a race, nil or undefined on a rare but reachable path (an error handler, a cold cache, a missing optional field), falsy zero treated as missing, off-by-one on a boundary the code does not exclude, a retry or partial failure, a regex or allowlist that lost its anchor. Never refute a candidate only for being speculative or depending on runtime state when that state is realistic.

Same place and same problem is one finding, whichever agent raised it; retain each dismissal reason. Apply SEVERITY BAR; change a proposed severity only when the evidence warrants it, recording the old and new levels and why.
