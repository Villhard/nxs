---
description: Code review of a diff - reports confirmed BLOCK / NIT findings without editing code. Use to review staged changes, a branch vs base, a file, or a PR.
argument-hint: "[scope: staged | path | PR url]"
---

# /nxs:review

Read-only code review of a diff. Resolve the scope, run the lenses the diff calls for plus the Standards and Spec axes, then report confirmed BLOCK / NIT findings or a clean approve and stop. This skill reports; fixing is the user or `/nxs:exec`.

Example: /nxs:review staged

## STANCE

- A clean approve is a valid result.
- By default no file is written. Save the report only on explicit user request: propose a location, show the diff / report first, then write after confirmation.

## RESOLVE THE DIFF SCOPE

Resolve to a concrete diff before anything else:

- explicit selector - `staged` (the current staged diff), a file path, or a PR / MR URL -> use it as given;
- no selector -> default: current branch vs base. Detect the base branch explicitly (`origin/HEAD`, else whichever of `main` / `master` exists);
- no selector + mixed state (commits ahead of base plus staged / unstaged changes) -> ask the user once which scope to review, BEFORE running any lens;
- hand the lenses only the diff of the resolved scope.

## AXIS DISCOVERY

- find the source artifact for the Spec axis (see Spec axis below);
- list the standards sources for the Standards axis (see Standards axis below);
- decide which axes are active and which to skip (an axis is skipped only when its source is absent).

## LENSES

Two lenses, each an isolated subagent:

- `nxs:review-quality-reviewer` - the execution paths the diff touches: bugs, races, edge cases, error handling, leaks, regressions, misleading comments, a basic security skim, and whether the tests catch what the code does;
- `nxs:review-fit-reviewer` - the diff against its requirements and the rest of the project: what is missing or unwired, and what is more than the task asked for.

Injection is mandatory and covers two files: `review-protocol` (`${CLAUDE_SKILL_DIR}/../review-protocol/SKILL.md`) and `reference/review-policy.md`. Read both once and include their full text in every lens prompt; a lens reviews from the injected text, never from memory. A path that does not resolve is found inside the plugin before anything is spawned.

Selection scopes effort only - real code with logic is always reviewed:

- trivial or non-code diff (config / dotfiles / docs-only / pure formatting) -> no subagents; the orchestrator does one direct pass against the same bar.
- any diff with logic in it -> both lenses, in parallel where the harness supports it, sequential otherwise. There is no middle setting, and an explicit request for a full review takes this branch whatever the diff looks like.

The security skim lives inside `nxs:review-quality-reviewer`; deep security is out of scope, so auth / payment / crypto / data migration calls for a manual review from outside. Documentation is not a separate lens: stale comments -> quality, public API surface -> fit.

## STANDARDS AND SPEC AXES

Two axes run alongside the lenses, over the same diff: does the diff follow the project's written standards, and does it implement its source artifact fully and nothing more. Both are active unless their source is missing.

Sources, the artifact-finding order, and the citation each axis finding must carry are in `reference/review-axes.md`. An axis finding without its citation is dropped.

## ORCHESTRATOR PASS

The lenses propose; you decide what the user sees.

1. **dedup** - one place, one finding. The collision to expect is not between the two lenses: it is `nxs:review-fit-reviewer` and the Spec axis on the same unmet requirement, and a bug reported apart from the missing test that would have caught it. Merge those, keep the one that names the consequence, and carry the axis citation into whichever survives.
2. **verify against the real code** - read the file at the reported line with its context, confirm the problem exists and is not already handled elsewhere. Confirmed - keep it; anything else - discard, do not downgrade. An unconfirmed nit is pure noise.
3. **classify** - BLOCK / NIT / DROP per `review-protocol`, with the refinements in `reference/review-policy.md`. An axis finding without its `Standard:` / `Spec:` citation - drop.
4. **rank BLOCK findings** by consequence, worst first.

Overall: NEEDS CHANGES on any confirmed BLOCK; APPROVE otherwise, nits and all. Discarding most candidates is a normal outcome.

Run `verify` on the diff for ground the lenses and axes have not covered.

## OUTPUT

The verdict and the size of the problem first, then the findings, then the provenance. No preamble, no praise, no narration.

```
<APPROVE | NEEDS CHANGES> - <counts> - <scope>

BLOCK  <file>:<line>
  <one sentence: what is wrong and what it costs>
  <Standard: | Spec: citation - axis findings only>
  Fix: <what to change>

NIT  <file>:<line> - <what is wrong>

Source artifact: <path or skipped> | Standards: <sources or skipped>
```

Filled in:

```
NEEDS CHANGES - 2 blocks, 3 nits - staged

BLOCK  src/auth/token.py:47
  An empty scope list passes the check, so any request without a scope gets a full-access token.
  Fix: treat an empty list as no scope and reject it.

BLOCK  src/items/repository.py:88
  The page query has no ORDER BY, so two requests for the same offset can return overlapping rows.
  Standard: CONTRIBUTING.md#queries - "every paged query sorts on a unique key"
  Fix: sort by id alongside limit and offset.

NIT  src/auth/token.py:12 - the comment still describes the old two-argument signature.
NIT  src/items/handler.py:34 - parse_page_params runs twice on the same request.
NIT  tests/items/test_handler.py:56 - asserts the literal error string, so rewording the message fails the test.
```

- **First line** - verdict, counts, scope. Counts drop an empty category and go singular at one: `2 blocks, 3 nits`, `3 nits`, `1 block`, `no findings`. Scope is what a person would call it: `staged`, `main..HEAD`, a path, a PR URL.
- **Blocks first**, worst consequence at the top, then nits in file and line order.
- **The body of a block is one sentence** naming the cause and what it costs, not two, and it opens with the cause rather than "this means".
- **A nit is one line.** The only exception is an axis finding, which adds its `Standard:` / `Spec:` citation on an indented line below.
- **The last line is the provenance**, printed even when nothing was found.

The report should need no follow-up question.

## REFERENCE

- `reference/review-policy.md` - where a requirement may come from, and the classification calls that are easy to get wrong. Read here, injected into both lenses beside `review-protocol`.
- `reference/review-axes.md` - standards sources, source-artifact order, axis citations. Orchestrator-side, never injected.
- `review-protocol` - stance, verification, classification, output format. Injected into each lens; the orchestrator follows the same base.
- `verify` - project checks on the diff when useful.

## NEXT

Findings to address -> hand them back to the user or to `/nxs:exec` to fix, then re-review the same scope. Clean approve -> proceed to commit / MR.
