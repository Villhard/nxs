# REVIEW POLICY (reference)

Loaded on demand from `/nxs:review`. Carries the full review verdict contract - BLOCK / NIT / DROP classification, the anti-hypothetical filter, the high-confidence threshold, the pre-emit check, ranking, the finding output format, and the Standards / Spec axis classification tables. The operational rules live in SKILL.md; this file is the detail.

APPROVE with no findings is a valid result. Only confirmed findings. Do not invent issues.

## RULE

- BLOCK = must be fixed before MR.
- NIT = a useful improvement.
- Better to skip a weak issue than to create a false positive.
- No endless nitpicking.

## ANTI-HYPOTHETICAL FILTER

Reject:

- "what if someone later..." without specifics;
- useless DRY / style suggestions;
- alternatives that are not clearly better;
- remarks without a concrete file / context / scenario.

## HIGH CONFIDENCE THRESHOLD

Every remark must have:

- a concrete file and line / area;
- a quoted excerpt from the code (5-7 lines with the problem line marked `>`);
- a real scenario in which it manifests;
- a clear explanation of why it matters - but only if the point is not evident from the excerpt.

Without this - drop.

## PRE-EMIT CHECK

Before emitting a finding, every reviewer must:

1. Read 20-30 lines of context around `<file>:<line>`.
2. Quote an excerpt (5-7 lines, the problem line marked `>`).
3. Answer two counter-questions:
   - Is this intentional design? Is there a sign in the code / comments / tests that it was done deliberately?
   - Is it already handled under a different name in this same diff / in the project's existing helpers?

If even one answer is "yes" - drop, do not emit. If you could not quote an excerpt - drop.

## RANKING

- No fixed numeric cap on the number of findings. Emit every finding that passes the high-confidence threshold and the pre-emit check.
- Order findings by real impact, strongest first. Volume is held down by the confidence threshold, the anti-hypothetical filter, and the pre-emit check - not by a count limit.
- No endless nitpicking: a weak or speculative candidate is dropped, never emitted to pad a list. Better to skip a weak issue than create a false positive.

## OUTPUT CONTRACT

- Findings first. No preamble, praise, or investigation diary.
- Each finding in the format:

  ```
  <BLOCK|NIT> <file>:<line> - <one-line issue>

    <2-3 lines of context>
  > <offending line>
    <2-3 lines of context>

    Fix: <concrete action, one phrase>
  ```

- The excerpt is 5-7 lines total, the problem line marked `>`. If the problem spans several lines - mark each one.
- `Fix:` is a concrete action, not "consider X" / "think about Y".
- An optional single `Why:` or `Attack:` line (for security) - only if the point is not obvious from the issue + excerpt. Omit by default.
- For an axis finding (Standards / Spec) - a mandatory single citation line under `Fix:`: `Standard: <path>#<section> - "<rule>"` or `Spec: <path>#<section> - "<requirement>"`. Without a citation - drop.
- No Category / Reason / Scenario as separate fields.
- If there are no findings: `Verdict: APPROVE. Findings: none.`
- A single-line header is printed before the findings: `Source artifact: <path or skipped> | Standards: <sources or skipped>`.

## CLASSIFICATION

### BLOCK

Must fix before MR:

- real bug;
- broken requirement;
- build break;
- regression;
- security / data risk;
- missing important test;
- serious maintainability issue.

### NIT

A useful improvement, optional:

- a small readability improvement;
- simpler debugging / maintenance;
- test clarity;
- user-visible quality.

### NOT A FINDING (DROP)

Do not publish as a remark:

- pure style preference;
- speculative future risk without a concrete scenario;
- abstraction preference;
- DRY suggestion without real benefit;
- an alternative that is not clearly better;
- a request for a test that duplicates an already-covered axis or verifies the same branch under a different name - test value over case-matrix completeness;
- separate near-identical test requests when several same-shaped input variations are genuinely worth covering - suggest parameterizing one test (one NIT) instead.

### TEST DISCIPLINE

Tests encode the contract, not a case matrix or refactoring scaffolding. Counterpart to the test items in NOT A FINDING above: those forbid demanding superfluous tests; these flag superfluous tests already added.

- A test whose meaningful verification rests only on absence / negation (`assert X not in logs`) and does not pin the positive contract -> BLOCK. Such a check is a transient implementation / refactor scaffold; the committed test asserts the positive observable form. Exception: a genuinely negative requirement (a secret / PII must never appear in output) is a valid contract - keep it framed as that requirement, not as a removal leftover.
- A redundant absence assertion next to a real contract assertion -> NIT (remove the scaffold).
- A new test that duplicates the axis of an existing test, or that only re-covers behavior already covered where the existing test should have been updated or parametrized -> NIT (update / parametrize the existing test instead of adding a new one).
- Assertions on incidental / internal details instead of the observable behavioral contract -> NIT; when this makes the test break on a safe refactor, it is the "testing implementation, not behavior" case.

### OVER-ENGINEERING - RELATIVE COMPLEXITY

Over-engineering / premature abstraction is assessed relative to the simplicity of the intended change, not in absolute terms:

- Complex code proportional to the complexity of the task -> NOT A FINDING.
- Code that solves a simple task in a complex way (a factory for a one-off call, an abstraction for a single case, a generic wrapper for a specific task) -> NIT; in clear cases with a real maintenance / readability cost -> BLOCK.
- An abstraction that looks complex in absolute terms but is proportional to the task -> DROP (see "abstraction preference" in NOT A FINDING).

The existing filters "abstraction preference -> drop" and "DRY suggestion without real benefit -> drop" remain and apply to absolute-complexity cases without relative context. The relative-complexity criterion supplements them, it does not replace them.

## STANDARDS AXIS

Checks the diff against the project's documented standards. Active in every run; skipped only when no standards source is found.

### SOURCES

- `docs/.ai/*` - project AI context;
- `docs/.ai/domain-language.md` - ubiquitous language;
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
4. A Jira / task URL - from the plan, the PR description, or specified by the user.
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

After collecting findings from the agents:

1. deduplicate - merge identical findings from different agents.
2. format check - a finding without a quoted excerpt or without a concrete `Fix:` - drop without ceremony. It is unverified or unactionable.
3. verify - check the remaining ones against the real code. Without evidence - drop.
4. apply this policy - classification + filters.
5. rank by impact - strongest first; no numeric cap, weak candidates dropped not capped.
6. output - only confirmed BLOCK and useful NIT in the format above.

## DIFFERENCE FOR EACH REVIEWER

- `nxs:review-quality-reviewer` - bugs / regressions / leaks / stale comments + basic security skim;
- `nxs:review-implementation-reviewer` - missing implementation / stubs / forgotten config / public API surface;
- `nxs:review-testing-reviewer` - coverage / assertions / fragile tests;
- `nxs:review-simplification-reviewer` - over-engineering / premature abstraction / dead code.

All follow this policy.

## CLEAN APPROVE IS VALID

If nothing was found - that is a valid result. Do not invent findings for the sake of a nice report. `Verdict: APPROVE` without findings is normal for a quality diff.
