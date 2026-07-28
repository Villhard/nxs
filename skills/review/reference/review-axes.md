# REVIEW AXES (reference)

Loaded on demand from `/nxs:review`. The two axes the orchestrator runs itself over the same diff as the lenses: does the change follow the standards this project wrote down, and does it implement its source artifact fully and nothing more. Orchestrator-side only - a lens reviews the diff it was handed and never goes looking for an artifact.

## OUTPUT ADDITIONS

- One header line before the findings: `Source artifact: <path or skipped> | Standards: <sources or skipped>`.
- An axis finding carries its citation on its own line above `Fix:`, and is dropped without one:

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
2. the latest active story under `docs/nxs/stories/` (not `completed/`) - its `plan.md`, the sibling brief beside it, and the plan's `## SOURCE ARTIFACTS` section;
3. a tracker URL from the plan, the PR, or the user;
4. a spec document in the repo that the plan or PR points to.

No `docs/nxs/stories/` at all: step 2 falls back to the latest plan under `docs/nxs/plans/` (not `completed/`) and a brief under `docs/nxs/briefs/` named by the plan, the branch, or the PR description. This is read-only compatibility with the pre-story layout; nothing is ever written there.

None found: report `Spec axis: skipped (no spec/source artifact available)` and move on.

The bar for a spec finding - where a requirement may come from, and when scope creep counts - is in `review-policy.md`, which the lenses also receive.
