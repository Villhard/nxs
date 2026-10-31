# ARCHITECTURE AUDIT

## INSPECTION AND PRIORITY

Survey meaningful boundaries and callers rather than only names or directory structure. A module's interface includes invariants, errors, ordering and other caller obligations. Look for behavior and knowledge spread across callers, fragile responsibilities, repeated change pressure or difficult verification at an interface. A deeper module can concentrate useful behavior behind a smaller interface, but extra layers and speculative seams have costs; a shallow adapter can still be appropriate. Trace concrete examples before proposing change.

For each opportunity record the relevant code and callers, current behavior, evidence of the problem or change pressure, a possible direction and expected consequences. Estimate relative effort, risk and uncertainty at the precision evidence supports. Rank by the observed impact, frequency or change pressure against cost and risk; explain the order and disclose assumptions. Recommendations are candidates, not approved design. Do not force a fixed count or equate uninspected areas with healthy ones.

## RESULT AND PRESERVATION

Use an explicitly supplied feature directory, or choose `.scratch/<topic-slug>/` with a short lowercase hyphenated slug. If the candidate directory contains `map.md`, choose a different slug unless the user explicitly authorizes work there. Save `research/architecture-audit.md` under that directory. Inspect the destination and existing history first. Preserve other artifacts and user edits; a materially different existing result needs a concrete revision decision rather than silent overwrite. Never edit project `SPEC.md` or `.SPEC.md`.

The result names scope, inspected paths and representative callers, source evidence, uninspected areas and constraints. Record a ranked set of supported opportunities with reasons, consequences, estimated cost and confidence, or a defensible no-change conclusion limited to the evidence inspected. Separate observations, inferences, assumptions and unknowns, and name the next useful check for material uncertainty. Keep secrets, private configuration and raw session transcripts out of artifacts.
