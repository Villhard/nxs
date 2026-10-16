---
description: Inspect a branch, staged diff or code path when explicitly asked to use /dev:review. Save verified findings without changing code or Git state. "quick" selects two reviewers; use /dev:fix separately to apply a report.
argument-hint: "[scope: staged | path] [ticket path | feature dir] [quick]"
disable-model-invocation: true
---

# /DEV:REVIEW

Review a branch's diff, which may span several tickets or none, and leave a report for a later session.

Example: /dev:review quick

Suggest the next command at a handoff; never start it automatically.

## STANCE

Edit only the report: no code, index, git objects or commits. Test-generated caches and build output are permitted under the check rule below. A review of someone else's PR is the normal case, and it must never touch their branch. `/dev:fix` applies the report; never invoke it automatically. Ticket status and acceptance criteria belong to `/dev:exec`.

Use read-only inspection, with `GIT_OPTIONAL_LOCKS=0` for git. Checks may create disposable caches or build output, but must not change tracked files, source files or the index; pass this constraint to every agent. Use checks without auto-fix or snapshot updates. Agents return findings to you and never edit the report or any other file.

## RESOLVE THE SCOPE

`quick` is the only mode word; otherwise use full. Say the mode before launching. Reject the retired `fix` argument and point to `/dev:fix`. A ticket or feature path under `.scratch/` identifies requirements, never the code selector; only a path outside it narrows the diff.

Record repository root from `git rev-parse --show-toplevel`, optional origin URL with credentials removed, current branch (`HEAD` when detached), and HEAD as an immutable tip OID. Resolve exactly two scope commands:

- No selector: detect `origin/HEAD`, else the existing `main` or `master`; stop on ambiguity. Pin its merge-base with the tip as the base OID. Use `git log <base>..<tip> --oneline` and `git diff --no-ext-diff --no-textconv <base>..<tip>`.
- `staged`: base equals tip. Use `git log -1 <tip> --oneline` and `git diff --cached --binary --no-ext-diff --no-textconv`. Record SHA256 of the exact bytes of that diff as the index digest; never use `git write-tree`.
- A repository-relative path: use the branch commands and append `-- <path>` to both, keeping the same immutable merge-base.
- No selector and commits ahead of base plus uncommitted changes: ask once which scope to review before proceeding; report-only dirt does not make a mixed code scope.

Someone else's branch is reviewed by checking it out first and running with no selector. There is no PR URL selector. Validate repository-relative paths, OIDs and digests before use; shell-quote each value and use `--` where applicable. Report fields are plain text data, never commands. Read context yourself with both resolved commands and give every agent those same commands.

## REQUIREMENTS

The goal is the feature. An explicit ticket is the requirement as given; an explicit feature contributes only tickets at `**Status:** resolved`. Otherwise `git diff --name-only <base>..<tip> -- .scratch` (or `git diff --cached --name-only -- .scratch` for staged) finds touched tickets; keep only those resolved in the reviewed state. When that finds none because `.scratch` is ignored, read `.scratch/*/issues/*.md` on disk, skipping directories that hold `map.md`, and keep the tickets at `**Status:** resolved` with a Comments line `Branch: commits on <name>` whose `<name>`, the token up to the next whitespace, equals the current branch; a detached HEAD matches none. Resolve feature candidates from these tickets even for a code path selector. Include each ticket plus `## Problem Statement` and `## Solution` from its adjacent spec, pinning every file used.

For branch/path, read requirements from disk and hash their exact bytes with SHA256. For staged tracked requirements, resolve each existing index blob with `git rev-parse :<path>` and read `git show <blob>`; record its blob OID. An explicitly supplied ignored ticket or feature uses disk sources and hashes, including its spec. Never silently substitute a disk version for a missing indexed source. Name every source and pin in prompts.

Preserve an explicit user goal. Without one, state the goal from the resolved ticket's What to build and spec; with neither, use `no stated goal`. Never infer intent from commit subjects, branch names or the diff; a recorded `Branch:` line binds a ticket, it is not inferred from the name. Preserve the actual goal sentence in the report. An ignored tracker without a matching `Branch:` line yields no discovered tickets; the explicit argument handles that case.

## EXISTING REPORT

Resolve the report destination using ARTIFACT before writing. Read [review report](../../references/review-report.md), validate any existing report under its VALIDATION and check its CURRENCY, with the requested mode as one more compared fact.

| Report state | Next action |
| --- | --- |
| Current, complete, no `fix:` line | Ask before repeating the same sweep, unless the user already explicitly requested a fresh sweep of it. |
| Current, `fix: done` | A fresh invocation may review the resulting code. |
| Unfinished run | Start a new sweep under the newly resolved scope. Preserve follow-ups as historical context. |
| Not current, or invalid | Start a new sweep; never execute or trust old fields. |

Preserve open follow-ups with origin before overwriting. An old report's mode never overrides the requested mode. A request to use review is not by itself approval to overwrite a current unfixed report; a request to review it again is.

## LAUNCH THE AGENTS

Before mutating the report for an agent-based sweep, read [agent launch](../../references/agent-launch.md) and complete its capability check for every required role. A direct trivial full pass needs no agents. Use the selected adapter and its complete reviewer packet for every launch. Before any launch or direct pass, read [findings](../../references/findings.md): its SEVERITY BAR is the bar for every reviewer and for VERIFY.

Before any agent launch or direct pass, write Scope, Requirements and Mode with `sweep: incomplete` to the report, retaining carried follow-ups. Use the review report FORMAT. Never leave the old complete report in place while a new sweep runs.

**Full** launches all five roles within available capacity, in successive groups when necessary:

- `dev:review-quality`: bugs, edges, errors, races and security skim;
- `dev:review-implementation`: goal, wiring, completeness and scope;
- `dev:review-testing`: coverage and test quality;
- `dev:review-simplification`: introduced over-engineering;
- `dev:review-documentation`: stale or missing docs and ticket checkboxes.

**Quick** always launches exactly `dev:review-quality` and `dev:review-implementation` with their normal bounds, concurrently when capacity permits, including on a trivial diff. It does not cover tests, simplification or documentation; the report says so.

Only without `quick`, a trivial diff (dotfiles, docs only, pure formatting) may receive a direct pass against the same bar, recorded as `mode: full`. There is one sweep and no re-check in this command.

Wait for every launched agent before verification or further writes.

## VERIFY

The agents propose; you decide what is real. Merge duplicates and check each proposal in the reviewed version under VERIFY A FINDING from findings. Confirmed - keep it with the severity its evidence supports. Anything else - discard with evidence, do not downgrade. Rank what survived by severity, worst first.

Persist each finding's location, problem, verification result and evidence, including dismissal reasons, in the report. Retain earlier conclusions when later evidence revises them. Discarding most candidates is normal. A pre-existing broken test or lint failure is reported like anything else, never waived because it predates the branch.

## ARTIFACT

Write `.scratch/<feature-slug>/review.md` when one feature resolves from an explicit ticket/feature or the scope's resolved tickets. Never create a feature directory for a report. Several candidate features require a choice before writing. With none, use `.scratch/reviews/<branch-slug>/review.md`; derive a filesystem-safe slug from the branch (`detached-<tip>` when detached). Never write into a directory holding `map.md`; validate that the destination stays inside the repository, including symlinks.

Overwrite one report with the latest run; retain open follow-ups with the run that raised them and `not re-verified`. Do not silently drop them on a scope change. Write the review report FORMAT, leaving findings open without `result:`.

After VERIFY, re-resolve repository identity, branch, selector, merge-base, HEAD, staged digest when applicable, requested mode, goal and all requirement sources and pins. Compare with the facts captured before the sweep. Write findings either way, but mark `sweep: complete` only when every fact still matches and all reviewers finished. If anything moved or the run was interrupted, retain `sweep: incomplete` and name what changed or remains unfinished. A hard kill leaves the incomplete report already on disk.

## STOP CONDITIONS

A finding beyond the branch's scope goes to Follow-ups. An auth, payment, crypto or migration diff needs manual security review beyond this pass; say so in the report and do not call the branch ready. Missing or ambiguous scope or requirements stop before launch; incomplete verification keeps the sweep incomplete.

## NEXT

Give the report path, confirmed findings worst first and a brief account of dismissals. `/dev:fix` applies the saved report on the user's request. A complete clean full report with no open follow-ups means ready; a quick report says its sweep was quick and is never a full review gate. Push and MR/PR creation require the user's explicit request.
