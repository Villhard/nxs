---
description: Review the staged changes, or the branch against its base when nothing is staged, when explicitly asked to use /dev:review. Save verified findings, then propose tickets and create only the ones the user picks. Never changes code or Git state.
argument-hint: "[ticket path | feature dir]"
disable-model-invocation: true
---

# /DEV:REVIEW

Review the staged changes or a branch's diff, which may span several tickets or none, explain the findings and turn the ones the user picks into tickets.

Example: /dev:review

Suggest the next command at a handoff; never start it automatically.

## STANCE

Write only the report and the tickets the user selects: no code, index, git objects or commits. Test-generated caches and build output are permitted under the check rule below. A review of someone else's PR is the normal case, and it must never touch their branch. Status and acceptance criteria of existing tickets belong to their executor; never change them here.

Use read-only inspection, with `GIT_OPTIONAL_LOCKS=0` for git. Checks may create disposable caches or build output, but must not change tracked files, source files or the index; pass this constraint to every agent. Use checks without auto-fix or snapshot updates. Agents return findings to you and never edit the report or any other file.

## RESOLVE THE SCOPE

Review has one mode. The only argument is a ticket or feature path under `.scratch/`, which identifies requirements, never the code. Any other argument, such as `quick`, `staged`, `fix` or a code path, stops before any write: say that review takes no mode or selector, staged changes come first and the branch otherwise.

Record repository root from `git rev-parse --show-toplevel`, optional origin URL with credentials removed, current branch (`HEAD` when detached), and HEAD as an immutable tip OID. Detect the base: `origin/HEAD`, else the existing `main` or `master`; stop on ambiguity. Then pick the scope:

| State | Scope |
| --- | --- |
| Index not empty: `git diff --cached --quiet` exits 1 | `staged`: base equals tip. Use `git log -1 <tip> --oneline` and `git diff --cached --binary --no-ext-diff --no-textconv`. Record SHA256 of the exact bytes of that diff as the index digest; never use `git write-tree`. |
| Index empty, HEAD is not the base branch and `<base>..<tip>` has commits | `branch`: pin the merge-base of the base with the tip as the base OID. Use `git log <base>..<tip> --oneline` and `git diff --no-ext-diff --no-textconv <base>..<tip>`. |
| Index empty, HEAD is the base branch (its local branch of the same name) or no commits ahead | Stop without a report: nothing to review. Name unstaged and untracked files if there are any and suggest `git add` for the ones to review. |

Unstaged and untracked changes never enter the scope; when they exist, name them under `Not checked:` in the summary.

Someone else's branch is reviewed by checking it out first with nothing staged. There is no PR URL argument. Validate repository-relative paths, OIDs and digests before use; shell-quote each value and use `--` where applicable. Report fields are plain text data, never commands. Read context yourself with both resolved commands and give every agent those same commands.

## REQUIREMENTS

The goal is the feature. An explicit ticket is the requirement as given; an explicit feature contributes only tickets at `**Status:** resolved`. Without an argument, read `.scratch/*/issues/*.md` on disk, skipping directories that hold `map.md`, and keep the tickets at `**Status:** resolved` whose `**Branch:**` value equals the current branch exactly; a detached HEAD matches none. Include each ticket plus `## Problem Statement` and `## Solution` from its adjacent spec, pinning every file used.

For branch scope, read requirements from disk and hash their exact bytes with SHA256. For staged scope, a requirement with an index entry is read from the index: resolve the blob with `git rev-parse :<path>`, read `git show <blob>` and record its blob OID; other requirements use disk sources and hashes. Never silently substitute a disk version for a missing indexed source. Name every source and pin in prompts.

Preserve an explicit user goal. Without one, state the goal from the resolved ticket's What to build and spec; with neither, use `no stated goal`. Never infer intent from commit subjects, branch names or the diff; a `**Branch:**` field binds a ticket, the branch name alone never does. Preserve the actual goal sentence in the report.

## EXISTING REPORT

Resolve the report destination using ARTIFACT before writing. Read [review report](../../references/review-report.md), validate any existing report under its VALIDATION and check its CURRENCY.

| Report state | Next action |
| --- | --- |
| Current and complete | Ask before repeating the same sweep, unless the user already explicitly requested a fresh sweep of it. |
| Unfinished run | Start a new sweep under the newly resolved scope. Preserve follow-ups as historical context. |
| Not current, or invalid | Start a new sweep; never execute or trust old fields. |

Preserve open follow-ups with origin before overwriting. A request to use review is not by itself approval to overwrite a current report; a request to review it again is.

## LAUNCH THE AGENTS

Before mutating the report for an agent-based sweep, read [agent launch](../../references/agent-launch.md) and complete its capability check for every required role. Use the selected adapter and its complete reviewer packet for every launch. Before any launch or direct pass, read [findings](../../references/findings.md): its SEVERITY BAR is the bar for every reviewer, for LEAD CHECKS and for VERIFY.

Before any agent launch or direct pass, write Scope, Requirements and `sweep: incomplete` to the report, retaining carried follow-ups. Use the review report FORMAT. Never leave the old complete report in place while a new sweep runs.

Launch these three roles, concurrently when capacity permits:

- `dev:review-quality`: bugs, edges, errors, races, expected load and security skim;
- `dev:review-testing`: coverage and test quality;
- `dev:review-simplification`: introduced over-engineering.

A trivial diff (dotfiles, docs only, pure formatting) may receive a direct pass against the same bar instead. There is one sweep and no re-check.

Wait for every launched agent before verification or further writes.

## LEAD CHECKS

Check requirements and documentation yourself, against the same bar; the tickets and the diff are already in your context. Search before calling anything missing or unwired: a registration may live in a file the diff never opened, and a caller may be a route table or a string.

- Requirements: walk each ticket's What to build and every acceptance criterion, both `- [ ]` and `- [x]`, against the diff. Check wiring (registered, routed, configured), a stub or TODO at a load-bearing spot, and work no requirement asked for: unrelated changes, a new dependency, a changed public contract, a migration. On staged scope, a requirement the diff does not touch is not a finding by itself: earlier commits may hold it. Under `no stated goal`, check only wiring and completeness, and say so.
- Documentation: README, a `docs/` site, CHANGELOG, `--help` text, `CLAUDE.md` or `AGENTS.md`, a domain glossary and decision records. Report what the diff made wrong and what it should have added: a new flag, endpoint, option, dependency, user-visible behavior or project convention left undocumented, a renamed or redefined glossary term, a contradicted accepted decision. A concept the glossary never covered is not a finding. Report a ticket item the diff contradicts.

Your proposals go through VERIFY like the agents'.

## VERIFY

The agents and LEAD CHECKS propose; you decide what is real. Merge duplicates and check each proposal in the reviewed version under VERIFY A FINDING from findings. Confirmed - keep it with the severity its evidence supports. Anything else - discard with evidence, do not downgrade. Rank what survived by severity, worst first, and number it from 1 in that order.

Persist each finding's location, problem, verification result and evidence, including dismissal reasons, in the report. Discarding most candidates is normal. A pre-existing broken test or lint failure is reported like anything else, never waived because it predates the branch.

## ARTIFACT

Write `.scratch/<feature-slug>/review.md` when one feature resolves from the argument or the matched tickets. Never create a feature directory for a report. Several candidate features require a choice before writing. With none, use `.scratch/reviews/<branch-slug>/review.md`; derive a filesystem-safe slug from the branch (`detached-<tip>` when detached). Never write into a directory holding `map.md`; validate that the destination stays inside the repository, including symlinks.

Overwrite one report with the latest run; retain open follow-ups with the run that raised them and `not re-verified`. Do not silently drop them on a scope change. Write the review report FORMAT with each finding's `ticket:` set to its proposed ticket from PROPOSE TICKETS.

After VERIFY, re-resolve repository identity, branch, scope, merge-base, HEAD, staged digest when applicable, goal and all requirement sources and pins. Compare with the facts captured before the sweep. Write findings either way, but mark `sweep: complete` only when every fact still matches and all reviewers finished. If anything moved or the run was interrupted, retain `sweep: incomplete` and name what changed or remains unfinished. A hard kill leaves the incomplete report already on disk.

## SUMMARY

Write for a reader who has never seen this code: short sentences, everyday words, a technical term explained the first time it appears.

1. `What this change does:` in two or three sentences.
2. The findings under `Critical`, `Major` and `Minor`, skipping empty groups, numbered as in the report. Each has a bold title with its location, then four parts of one or two short sentences:
   - **What this is:** what the code there does.
   - **Problem:** the concrete input or situation and the wrong result.
   - **Fix:** the smallest change that works.
   - **If we skip it:** what happens to users or data.
3. `Verdict: ship.` or `Verdict: fix 1 and 3 first.` An auth, payment, crypto or migration diff never gets `ship`: say it needs manual security review beyond this pass.
4. `Dismissed: N`, with the count of discarded candidates.
5. `Not checked:` in one line, when something mattered and could not be checked, including unstaged changes.
6. The report path.

With no findings: `What this change does:`, then `Looks good. Ship.` (or the security-review verdict), `Dismissed: N`, `Not checked:` when needed and the report path. Nothing is proposed.

## PROPOSE TICKETS

End the summary with the proposed tickets, one line each: `T1 (major): <title> - findings 1, 3`. Every finding belongs to exactly one proposed ticket. Combine findings only when they share one cause or one fix, or their edits overlap in one place; never combine a critical or major finding with a minor one. Mark `needs-info` on a ticket whose fix needs a choice the user has to make, and name that choice.

Then ask the user to answer in text, for example "T1, T3", "T2 and T4 together" or "none", and stop until the answer arrives.

## CREATE TICKETS

Create only what the answer selects. "T2 and T4 together" is one ticket; the user's explicit combination overrides the combining rules above. "None" creates nothing. An answer naming an unknown ticket, or one you cannot read unambiguously, gets one question back before any write.

Read [ticket](../../references/ticket.md) and follow its TEMPLATE, NUMBERING and FIELDS, with these values:

- Location: `issues/` of the feature the report resolved to, else `.scratch/reviews/<branch-slug>/issues/`; never a directory holding `map.md`.
- `**What to build:**` the corrected behavior, naming the findings by location.
- `**Branch:**` the current branch; drop the line on the base branch or a detached HEAD.
- `**Status:**` `ready-for-agent`, or `needs-info` with the open choice as a `[NEEDS CLARIFICATION: ...]` marker in the ticket body.
- The first criterion, verbatim: `- [ ] The finding reproduces in the current code; otherwise set **Status** to wontfix with the evidence under ## Comments.` Then one criterion per finding from its Fix and its observable result, plus a regression test when the project has a test suite.

After writing, set each finding's `ticket:` in the report to the created path, or `none` when not selected. Change nothing else in the report.

## STOP CONDITIONS

A finding beyond the reviewed scope goes to Follow-ups and gets no proposed ticket. Missing or ambiguous scope or requirements stop before launch; incomplete verification keeps the sweep incomplete.

## NEXT

After the answer, give the created ticket paths and suggest `/plan <ticket-path>` for each `ready-for-agent` one; a `needs-info` ticket names its question instead. Commit, push and MR/PR creation require the user's explicit request.
