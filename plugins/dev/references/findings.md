# FINDINGS

Read this reference before a review sweep. `review` rates and verifies findings with it and pass its SEVERITY BAR to every reviewer verbatim.

## SEVERITY BAR

Rate the demonstrated consequence under reachable conditions:

- **critical** - data loss or corruption, a security breach, or a crash on an ordinary user path.
- **major** - wrong behavior or a broken contract, beyond contained minor impact.
- **minor** - a real defect with contained impact.

For a test finding, name the concrete defect it would miss or the way the test fails incorrectly. A coverage gap over currently correct behavior is minor unless evidence shows a broader present failure in the test process; do not rate a hypothetical production defect as though it already existed. For documentation, name the reader's wrong action or misunderstanding. Rate instructions a machine or agent executes by what their consumer does wrong. Unclear, misleading or misspelled identifiers and test names are minor: explain the ambiguity or mismatch with their actual role and propose a clearer name. A runtime failure or written naming rule is not required. A synonym preference or prose taste alone is not a finding; a prose typo with no changed meaning is not a finding.

Severity measures the defect, not the cost of fixing it. Keep a confirmed in-scope defect in Findings even when its fix is expensive or risky; describe that reach and risk under Fix. Out-of-scope defects belong in Follow-ups.

## VERIFY A FINDING

Read the finding's location with 20-30 lines of context in the version being checked. Trace a reachable input or state through callers and guards to the claimed consequence; cite the locations that establish or disprove it. For naming claims, compare the name with its actual role and uses; cite the ambiguity or mismatch instead of requiring a runtime failure. For coverage or documentation claims, inspect the relevant tests or contract too. A passing test alone does not disprove a runtime defect. Separate what the code proves from inferred consequences.

Same place and same problem is one finding, whichever agent raised it; retain each dismissal reason. Apply SEVERITY BAR; change a proposed severity only when the evidence warrants it, recording the old and new levels and why.
