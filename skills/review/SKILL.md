---
description: Code review of a diff - resolve the diff scope, select the reviewer lenses proportional to the change, run the Standards and Spec axes, and report confirmed BLOCK / NIT findings without editing code. Use to review staged changes, a branch vs base, a file, or a PR.
argument-hint: "[scope: staged | path | PR url]"
---

# /nxs:review

Read-only code review of a diff. Resolve the scope, run an adaptive set of reviewer lenses plus the Standards and Spec axes, then report confirmed BLOCK / NIT findings or a clean approve and stop. This skill never edits code. Self-contained skill. Output language and response style come from global rules, not this file.

## STANCE (READ-ONLY, HAND OFF)

- The review reports; it does not fix. It reads the diff and prints findings; it never edits code.
- Fixing is the user or `/nxs:exec`. This skill reports and stops.
- A clean approve is a valid result - do not invent findings to look thorough.
- By default no file is written. Save the report only on explicit user request: propose a location, show the diff / report first, then write after confirmation.

## RESOLVE THE DIFF SCOPE

Resolve to a concrete diff before anything else:

- explicit selector - `staged` (the current staged diff), a file path, or a PR / MR URL -> use it as given;
- no selector -> default: current branch vs base. Detect the base branch explicitly (`origin/HEAD`, else whichever of `main` / `master` exists) - never guess;
- no selector + mixed state (commits ahead of base plus staged / unstaged changes) -> ask the user once which scope to review, BEFORE running any agents;
- hand the reviewers only the diff of the resolved scope - nothing outside it.

## AXIS DISCOVERY

- find the source artifact for the Spec axis (see Spec axis below);
- list the standards sources for the Standards axis (see Standards axis below);
- decide which axes are active and which to skip (an axis is skipped only when its source is absent).

## REVIEWERS (adaptive selection)

Select the reviewer set proportional to the resolved diff and run only the lenses the diff needs. Each selected reviewer is an isolated subagent. Protocol injection is a mandatory step: read `review-protocol` (`skills/review-protocol/SKILL.md`) once and include its full text in the prompt of every lens you spawn. The lens agents do not restate the protocol - they receive it via this injected prompt. Parallel if the harness supports it, sequential fallback.

- `nxs:review-quality-reviewer` - any diff touching behavioral code: bugs / regressions / leaks / stale comments + a basic security skim;
- `nxs:review-implementation-reviewer` - feature / multi-file / public-surface changes: missing implementation / stubs / forgotten config / public API;
- `nxs:review-testing-reviewer` - a diff that adds or changes code that should be covered: coverage / assertions / fragile tests;
- `nxs:review-simplification-reviewer` - non-trivial new code / abstractions: over-engineering / premature abstraction / dead code.

Selection rules:

- trivial or non-code diff (config / dotfiles / docs-only / pure formatting) -> skip the reviewer agents; the orchestrator does one direct pass and reports. No subagents spawned.
- substantial or security-sensitive diff (auth / payment / crypto / data migration / broad logic) -> run the full set.
- explicit user request for a full review -> run the full set regardless of size.

Adaptivity scopes effort - it never skips review of real code with logic. The security skim lives inside `nxs:review-quality-reviewer`; there is no deep security review - for auth / payment / crypto / data migration call a manual review from outside. Documentation is not a separate lens: stale comments -> quality, public API surface -> implementation.

## STANDARDS AND SPEC AXES

Run in parallel with or after the agents, over the diff against the found sources. Both axes are always active, skipped only when their source is unavailable.

### Standards axis

Does the diff conform to the project's documented standards. Read only sources that actually exist, do not invent them:

- ADRs (`docs/adr/`, `docs/decisions/`, or wherever they live in the project);
- root `AGENTS.md` / `CLAUDE.md`;
- `CONTRIBUTING.md`, `STANDARDS.md`, `STYLE.md`, `STYLE_GUIDE.md` and their variants in root or `docs/`;
- project config as machine-enforced standards (lint / formatter / typecheck) - but do not duplicate what these tools already catch. Record a config-based violation only when the standard is explicitly documented and the tooling does not catch it (or was disabled in the diff).

Every Standards finding carries a single citation line under `Fix:`: `Standard: <path>#<section> - "<verbatim rule>"`. Without a citation - drop. A standard "from memory" - drop.

### Spec axis

Does the diff implement the source artifact fully and without scope creep. Find the source artifact in priority order, stop at the first one found:

1. Command argument (`/nxs:review <path>` points to a plan / brief / spec).
2. Active plan under `docs/plans/` (excluding `docs/plans/completed/`), the latest by date; inside it the `## SOURCE ARTIFACTS` section.
3. Brief under `docs/briefs/` (including root-cause) named in the plan or in the branch / PR description.
4. Jira / task URL from the plan, the PR description, or the user.
5. PRD / spec document in the repo referenced by the plan or PR.

If no source artifact is found, report the single line `Spec axis: skipped (no spec/source artifact available)` and continue. Every Spec finding carries a single citation line under `Fix:`: `Spec: <path>#<section> - "<verbatim requirement>"`. Without a citation - drop. Do not invent a spec from memory, git history, branch names, or the dialogue - if a requirement is absent from the found artifact, ask the user or drop.

## ORCHESTRATOR PASS

After collecting agent + axis findings:

1. dedup - merge identical findings from different lenses, keep the most specific.
2. format check - drop any finding without a quoted excerpt or without a concrete `Fix:`; an axis finding without its `Standard:` / `Spec:` citation - drop.
3. verify - check each remaining finding against the real code (axis findings against the source artifact too); without evidence - drop.
4. classify - apply the review-policy classification (BLOCK / NIT / DROP; see CLASSIFICATION and `reference/review-policy.md`).
5. rank by impact, strongest first - no numeric cap; a weak or speculative candidate is dropped, never emitted to pad the list.

The orchestrator may run the `verify` skill on the diff when useful (project checks: tests / lint / format / typecheck / build), but do not duplicate what the reviewers or axes already cover.

## CLASSIFICATION

The orchestrator classifies findings on the same base as the lenses; do not restate the definitions here.

- Base BLOCK / NIT / DROP and tie-breaks - `review-protocol` (the kernel injected into every lens; the orchestrator follows the same base).
- Review-specific refinements - over-engineering relative to the task, test discipline, and the Standards / Spec axis classification tables - `reference/review-policy.md`, where they live once.

## OUTPUT

Header first (single line), then findings, no preamble / praise / process narration:

```
Source artifact: <path or skipped> | Standards: <sources or skipped>
```

Findings body - only confirmed BLOCK / NIT, each with a quoted excerpt (5-7 lines, the problem line marked `>`), a concrete `Fix:`, and the `Standard:` / `Spec:` citation for an axis finding. A clean approve is valid: `Verdict: APPROVE. Findings: none.`

## RULES

- Read-only - report, never edit code.
- Every remark has a concrete file / line / excerpt; the confidence threshold is high - skip a weak issue over a false positive.
- Anti-hypothetical filter - no "what if someone later".
- DRY / style suggestions without real benefit - drop.
- A clean approve is valid.

## REFERENCE

- `reference/review-policy.md` - the Standards / Spec axis classification tables and citation formats, the classification refinements (superfluous tests, test discipline, relative-complexity over-engineering), the orchestrator pass, and per-reviewer differentiation - layered on the `review-protocol` base.

Reference skills used by name: `review-protocol` (the shared base protocol each selected lens follows - stance, pre-emit check, BLOCK / NIT / DROP, ranking, output format - injected into each lens and followed by the orchestrator too), `verify` (project checks on the diff when useful).

## NEXT

Findings to address -> hand them back to the user or to `/nxs:exec` to fix, then re-review the same scope. Clean approve -> proceed to commit / MR.
