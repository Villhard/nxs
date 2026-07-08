# REVIEW POLICY (reference)

Loaded on demand from `/nxs:review`. Layers the review-specific detail on top of the shared `review-protocol` kernel: the Standards and Spec axes (sources, citation requirements, classification tables), the classification refinements (superfluous tests, test discipline, relative-complexity over-engineering), the orchestrator pass, and per-reviewer differentiation. The operational rules live in SKILL.md; this file is the detail.

## BASE PROTOCOL

The read-only stance, the anti-hypothetical / high-confidence threshold, the per-finding pre-emit check (intent read, context read, excerpt quote, counter-questions, mark-inference), the BLOCK / NIT / DROP definitions and tie-breaks, ranking without a numeric cap, the generic finding output format, and clean-approve validity all live once in `review-protocol` - follow it as the base. This file does not restate them; it adds only the sections below.

## OUTPUT CONTRACT (axis additions)

The generic finding format - findings first with no preamble, the marked `<BLOCK|NIT> <file>:<line>` excerpt block, the concrete `Fix:`, the optional `Why:` / `Attack:` line - lives in `review-protocol` OUTPUT FORMAT; do not restate it. This section adds only the review-specific requirements:

- A single-line header printed before the findings: `Source artifact: <path or skipped> | Standards: <sources or skipped>`.
- For an axis finding (Standards / Spec) - a mandatory single citation line under `Fix:`:

  ```
  Standard: <path>#<section> - "<verbatim quote of the rule>"
  Spec: <artifact-path>#<section> - "<verbatim quote of the requirement>"
  ```

  Without a citation - drop.
- No Category / Reason / Scenario as separate fields.
- If there are no findings: `Verdict: APPROVE. Findings: none.`

## CLASSIFICATION REFINEMENTS

Base BLOCK / NIT / DROP definitions and tie-breaks live in `review-protocol` - do not restate them. This file adds the review-specific refinements below; they layer on the base classification.

### SUPERFLUOUS TEST REQUESTS

Beyond the base DROP list, do not demand:

- a test that duplicates an already-covered axis or verifies the same branch under a different name - test value over case-matrix completeness -> drop;
- separate near-identical test requests when several same-shaped input variations are genuinely worth covering - suggest parameterizing one test (one NIT) instead.

### TEST DISCIPLINE

Tests encode the contract, not a case matrix or refactoring scaffolding. Counterpart to SUPERFLUOUS TEST REQUESTS above: those forbid demanding superfluous tests; these flag superfluous tests already added.

- A test whose meaningful verification rests only on absence / negation (`assert X not in logs`) and does not pin the positive contract -> BLOCK. Such a check is a transient implementation / refactor scaffold; the committed test asserts the positive observable form. Exception: a genuinely negative requirement (a secret / PII must never appear in output) is a valid contract - keep it framed as that requirement, not as a removal leftover.
- A redundant absence assertion next to a real contract assertion -> NIT (remove the scaffold).
- A new test that duplicates the axis of an existing test, or that only re-covers behavior already covered where the existing test should have been updated or parametrized -> NIT (update / parametrize the existing test instead of adding a new one).
- Assertions on incidental / internal details instead of the observable behavioral contract -> NIT; when this makes the test break on a safe refactor, it is the "testing implementation, not behavior" case.

### OVER-ENGINEERING - RELATIVE COMPLEXITY

Over-engineering / premature abstraction is assessed relative to the simplicity of the intended change, not in absolute terms:

- Complex code proportional to the complexity of the task -> NOT A FINDING.
- Code that solves a simple task in a complex way (a factory for a one-off call, an abstraction for a single case, a generic wrapper for a specific task) -> NIT; in clear cases with a real maintenance / readability cost -> BLOCK.
- An abstraction that looks complex in absolute terms but is proportional to the task -> DROP (see "abstraction preference" in the base DROP list).

The base filters "abstraction preference -> drop" and "DRY suggestion without real benefit -> drop" remain and apply to absolute-complexity cases without relative context. The relative-complexity criterion supplements them, it does not replace them.

## STANDARDS AXIS

Checks the diff against the project's documented standards. Active in every run; skipped only when no standards source is found.

### SOURCES

- ADRs (`docs/adr/`, `docs/decisions/`, or wherever they live);
- root `AGENTS.md` / `CLAUDE.md`;
- `CONTRIBUTING.md`, `STANDARDS.md`, `STYLE.md`, `STYLE_GUIDE.md` and their variants in root or `docs/`;
- project config as machine-enforced standards (lint / formatter / typecheck) - but do not duplicate what these tools already check automatically. A config-based Standards finding is valid only when the standard is explicitly described in the project and the tooling does not catch it (or was disabled in the diff).

Read only sources that actually exist. Standards "from memory" - drop.

### CITATION REQUIREMENT

Every Standards finding must contain a single line under `Fix:`:

```
Standard: <path>#<section> - "<verbatim quote of the rule>"
```

Without a citation - drop. "It's accepted in the project" without confirmation in a file - drop.

### STANDARDS CLASSIFICATION

- Binding rule (`must`, `required`, `forbidden`, an ADR in accepted status) -> BLOCK.
- Recommendation (`should`, `prefer`) -> NIT.
- Style preference without a documented rule -> drop.
- A violation of something already caught by lint / formatter / typecheck -> drop (the tooling will already signal it).

## SPEC AXIS

Checks that the diff implements the original source artifact fully and does not go beyond its scope. Active in every run when a source artifact is present.

### FINDING THE SOURCE ARTIFACT

In priority order, stop at the first one found:

1. A command argument (`/nxs:review <path>` points to a plan / brief / spec).
2. An active plan under `docs/plans/` (excluding `docs/plans/completed/`), the latest by date; inside it the `## SOURCE ARTIFACTS` section.
3. A brief under `docs/briefs/` (including root-cause) mentioned in the plan or in the branch / PR description.
4. A tracker / task URL - from the plan, the PR description, or specified by the user.
5. A PRD / spec document in the repo referenced by the plan or PR.

If no source artifact is found - report `Spec axis: skipped (no spec/source artifact available)` and continue without it.

### CITATION REQUIREMENT

Every Spec finding must contain a single line under `Fix:`:

```
Spec: <artifact-path>#<section> - "<verbatim quote of the requirement>"
```

Without a citation - drop.

### ANTI-INVENTION OF SPEC

- Do not reconstruct the spec from git history, branch names, or the dialogue with the user.
- Do not pull the spec from memory of similar projects.
- If something looks like a requirement but is absent from the found artifact - ask the user or drop, do not emit.

### SPEC CLASSIFICATION

- A missing requirement that breaks the source artifact's acceptance criteria -> BLOCK.
- A missing requirement (auxiliary, not breaking acceptance criteria) -> NIT.
- Scope creep with real risk / cost (a new dependency, a change to a public contract, a migration, an added attack surface, noticeable maintenance overhead) -> BLOCK.
- Minimal scope creep, without consequences -> NIT.
- A purely additive improvement without harm -> drop.
- A mismatch of implementation details with the phrasing of the requirement while the behavior matches -> drop.

## ORCHESTRATOR PASS

The operational procedure lives in `skills/review/SKILL.md`'s own `## ORCHESTRATOR PASS` section - this file does not restate it. This section adds only the policy-layer refinements to the classification step: apply the classification refinements above (SUPERFLUOUS TEST REQUESTS, TEST DISCIPLINE, OVER-ENGINEERING - RELATIVE COMPLEXITY) and the Standards / Spec axis classification tables on top of the base `review-protocol` classification.

## DIFFERENCE FOR EACH REVIEWER

- `nxs:review-quality-reviewer` - bugs / regressions / leaks / stale comments + basic security skim;
- `nxs:review-implementation-reviewer` - missing implementation / stubs / forgotten config / public API surface;
- `nxs:review-testing-reviewer` - coverage / assertions / fragile tests;
- `nxs:review-simplification-reviewer` - over-engineering / premature abstraction / dead code.

`nxs:review-quality-reviewer` prioritizes attack surfaces per its `PRIORITIZE (attack surfaces)` block - spend the budget on expensive / dangerous / hard-to-detect failures first.

All follow this policy on top of the `review-protocol` base.
