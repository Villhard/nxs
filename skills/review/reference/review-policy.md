# REVIEW POLICY (reference)

Loaded on demand from `/nxs:review` and injected into both review lenses beside `review-protocol`. Holds what the base protocol does not: where a requirement may come from, and the few classification calls that are easy to get wrong. Each call binds whichever lens owns that ground; it never widens a lens's ground. The orchestrator's own work - finding the source artifact, listing the standards, the report header - is in `review-axes.md`, and no lens sees it.

## WHERE A REQUIREMENT COMES FROM

The source artifact, and nothing else. Never reconstruct a requirement from git history, branch names, the dialogue, or memory of similar projects. If something reads like a requirement but is not in the artifact, ask or drop it.

Scope creep counts as a finding when it costs something real - a new dependency, a changed public contract, a migration, added attack surface. A purely additive improvement that harms nothing does not.

## CALLS THAT ARE EASY TO GET WRONG

**Negative-only assertions.** A test whose meaningful check rests only on absence (`assert X not in logs`) and never pins the positive contract is scaffolding left in the commit - BLOCK. The exception is a genuinely negative requirement, such as a secret that must never appear in output; that is a real contract, keep it framed that way.

**Complexity is relative.** Judge it against the task, never in the abstract. Code as complex as its problem is not a finding, however elaborate it looks. A factory for one call site is.

**Do not ask for a case matrix.** Tests encode the contract, not every permutation. Several same-shaped variations worth covering are one suggestion to parameterize, not several findings - and a case already covered under a different name is not a gap.
