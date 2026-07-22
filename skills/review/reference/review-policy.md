# REVIEW POLICY (reference)

Loaded on demand from `/nxs:review`. Holds what the base `review-protocol` does not: where this project keeps its standards, how to find the artifact a diff is supposed to implement, and the few classification calls that are easy to get wrong.

## OUTPUT ADDITIONS

- One header line before the findings: `Source artifact: <path or skipped> | Standards: <sources or skipped>`.
- An axis finding carries its citation under `Fix:`, and is dropped without one:

  ```
  Standard: <path>#<section> - "<verbatim quote of the rule>"
  Spec: <artifact-path>#<section> - "<verbatim quote of the requirement>"
  ```

## STANDARDS AXIS

Does the diff follow the standards this project actually wrote down. Look in:

- ADRs (`docs/adr/`, `docs/decisions/`, wherever they live);
- root `AGENTS.md` / `CLAUDE.md`;
- `CONTRIBUTING.md`, `STANDARDS.md`, `STYLE.md` and variants, in root or `docs/`;
- lint / formatter / typecheck config - but only for a rule the project states explicitly and the tooling does not enforce on its own, or that the diff disabled.

Read only what exists. A standard from memory, or "it is accepted here" without a file behind it, is not a finding. Neither is anything the tooling already catches - it will report itself.

## SPEC AXIS

Does the diff implement its source artifact fully, and nothing else. Find that artifact in this order, stopping at the first hit:

1. a path given as the command argument;
2. the latest active plan under `docs/nxs/plans/` (not `completed/`), and its `## SOURCE ARTIFACTS` section;
3. a brief under `docs/nxs/briefs/` named by the plan, the branch, or the PR description;
4. a tracker URL from the plan, the PR, or the user;
5. a spec document in the repo that the plan or PR points to.

None found: report `Spec axis: skipped (no spec/source artifact available)` and move on.

Never reconstruct a requirement from git history, branch names, the dialogue, or memory of similar projects. If something reads like a requirement but is not in the artifact, ask or drop it.

Scope creep counts as a finding when it costs something real - a new dependency, a changed public contract, a migration, added attack surface. A purely additive improvement that harms nothing does not.

## CALLS THAT ARE EASY TO GET WRONG

**Negative-only assertions.** A test whose meaningful check rests only on absence (`assert X not in logs`) and never pins the positive contract is scaffolding left in the commit - BLOCK. The exception is a genuinely negative requirement, such as a secret that must never appear in output; that is a real contract, keep it framed that way.

**Complexity is relative.** Judge it against the task, never in the abstract. Code as complex as its problem is not a finding, however elaborate it looks. A factory for one call site is.

**Do not ask for a case matrix.** Tests encode the contract, not every permutation. Several same-shaped variations worth covering are one suggestion to parameterize, not several findings - and a case already covered under a different name is not a gap.
