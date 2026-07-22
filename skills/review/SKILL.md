---
description: Code review of a diff - reports confirmed BLOCK / NIT findings without editing code. Use to review staged changes, a branch vs base, a file, or a PR.
argument-hint: "[scope: staged | path | PR url]"
---

# /nxs:review

Read-only code review of a diff. Resolve the scope, run an adaptive set of reviewer lenses plus the Standards and Spec axes, then report confirmed BLOCK / NIT findings or a clean approve and stop. This skill never edits code. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:review staged

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

Select the reviewer set proportional to the resolved diff and run only the lenses the diff needs. Each selected reviewer is an isolated subagent. Protocol injection is mandatory: read `review-protocol` (`skills/review-protocol/SKILL.md`) once and include its full text in the prompt of every lens you spawn. Parallel if the harness supports it, sequential fallback.

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

Two axes run alongside the agents, over the same diff: does it follow the project's written standards, and does it implement its source artifact fully and nothing more. Both are active unless their source is missing.

Sources, the artifact-finding order, and the citation each axis finding must carry are in `reference/review-policy.md`. An axis finding without its citation is dropped.

## ORCHESTRATOR PASS

The lenses propose; you decide what the user sees.

1. **dedup** - merge identical findings from different lenses, keep the most specific.
2. **verify each one against the real code** - read the file at the reported line with its context, confirm the problem exists and is not already handled elsewhere. Not confirmed - discard, do not downgrade. This applies to NIT as much as to BLOCK: an unconfirmed nit is pure noise.
3. **classify** - BLOCK / NIT / DROP per `review-protocol`, with the review-specific refinements in `reference/review-policy.md`. An axis finding without its `Standard:` / `Spec:` citation - drop.
4. **rank BLOCK findings** by consequence, worst first.

Discarding most candidates is a normal outcome.

The orchestrator may run the `verify` skill on the diff when useful (project checks: tests / lint / format / typecheck / build), but do not duplicate what the reviewers or axes already cover.

## OUTPUT

One header line, then confirmed BLOCK findings, then every NIT folded into a single line. No preamble, no praise, no narration.

```
Source artifact: <path or skipped> | Standards: <sources or skipped>

BLOCK <file>:<line>
  Issue: <what is wrong>
  Impact: <what it costs>
  Fix: <what to change>

Nits (<n>): <file>:<line> <what is wrong>, <file>:<line> <what is wrong>, ...

Verdict: APPROVE | NEEDS CHANGES
```

The nits line stays one line however many there are; expand a NIT only when asked. No nits, no line. Nothing confirmed at all: `Verdict: APPROVE. Findings: none.`

The report should need no follow-up question. A user asking "why is that a problem?" means the finding was written badly.

## REFERENCE

- `reference/review-policy.md` - where the project keeps its standards, how to find the source artifact, the citation formats, and the classification calls that are easy to get wrong.
- `review-protocol` - the stance, verification, classification, and output format every lens follows, injected into each one; the orchestrator follows the same base.
- `verify` - project checks on the diff when useful.

## NEXT

Findings to address -> hand them back to the user or to `/nxs:exec` to fix, then re-review the same scope. Clean approve -> proceed to commit / MR.
