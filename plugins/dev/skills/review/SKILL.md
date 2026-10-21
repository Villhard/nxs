---
description: Review the staged changes, or the branch against its base when nothing is staged, when explicitly asked to use it (/dev:review in Claude Code, $dev:review in Codex). Save verified findings, then propose tickets and create only the ones the user picks. Never changes code or Git state.
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

Record repository root from `git rev-parse --show-toplevel`, optional origin URL with credentials removed, current branch (`HEAD` when detached), and HEAD as an immutable tip OID. Then pick the scope, checking the index first. Detect the base only when the index is empty: `origin/HEAD`, else the existing `main` or `master`; stop on ambiguity. Staged scope needs no base.

| State | Scope |
| --- | --- |
| Index not empty: `git diff --cached --quiet` exits 1 | `staged`: base equals tip. Use `git log -1 <tip> --oneline` and `git diff --cached --binary --no-ext-diff --no-textconv`. Record SHA256 of the exact bytes of that diff as the index digest; never use `git write-tree`. |
| Index empty, HEAD is not the base branch and `<base>..<tip>` has commits | `branch`: pin the merge-base of the base with the tip as the base OID. Use `git log <base>..<tip> --oneline` and `git diff --no-ext-diff --no-textconv <base>..<tip>`. |
| Index empty, HEAD is the base branch (its local branch of the same name) or no commits ahead | Stop without a report: nothing to review. Name unstaged and untracked files if there are any and suggest `git add` for the ones to review. |

Unstaged and untracked changes never enter the scope; when they exist, name them under `Not checked:` in the summary.

Someone else's branch is reviewed by checking it out first with nothing staged. There is no PR URL argument. Validate repository-relative paths, OIDs and digests before use; shell-quote each value and use `--` where applicable. Report fields are plain text data, never commands. Read context yourself with both resolved commands and give every agent those same commands.

## REQUIREMENTS

The goal is the feature. An explicit ticket is the requirement as given; an explicit feature contributes only tickets at `**Status:** resolved`. Without an argument, list `.scratch/*/issues/*.md` and `.scratch/reviews/*/issues/*.md` on disk, skipping directories that hold `map.md`, and keep the tickets at `**Status:** resolved` whose `**Branch:**` value equals the current branch exactly; a detached HEAD matches none. Include each ticket plus `## Problem Statement` and `## Solution` from its adjacent spec, pinning every file used. A ticket under `.scratch/reviews/` has no spec and resolves no feature.

For branch scope, read requirements from disk and hash their exact bytes with SHA256. For staged scope, a requirement with an index entry is read from the index: resolve the blob with `git rev-parse :<path>`, read `git show <blob>` and record its blob OID; other requirements use disk sources and hashes. Read a ticket's `**Status:**` and `**Branch:**` from the same version as its text. Never silently substitute a disk version for a missing indexed source. Name every source and pin in prompts.

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

Before mutating the report for an agent-based sweep, read [agent launch](../../references/agent-launch.md) and complete its capability check for every required role. Use the selected adapter and its complete reviewer packet for every launch. Before any launch or direct pass, read [findings](../../references/findings.md): its SEVERITY BAR is the bar for every reviewer, for LEAD CHECKS and for VERIFY, and its VERIFY A FINDING decides every verdict.

Before any agent launch or direct pass, write Scope, Requirements and `sweep: incomplete` to the report, retaining carried follow-ups. Use the review report FORMAT. Never leave the old complete report in place while a new sweep runs.

Launch these three finder roles, concurrently when capacity permits:

- `dev:review-quality`: bugs, edges, errors, races, expected load and security skim;
- `dev:review-testing`: coverage and test quality;
- `dev:review-simplification`: introduced over-engineering, reuse and fixes at the wrong depth.

The fourth role, `dev:review-verify`, runs under VERIFY after every finder has returned. A trivial diff (dotfiles, docs only, pure formatting) may receive a direct pass against the same bar instead, with no agent: you find the candidates and give them the verdicts of VERIFY A FINDING yourself. There is one sweep and no re-check.

Wait for every launched agent before verification or further writes.

## LEAD CHECKS

Check requirements, documentation and conventions yourself, against the same bar; the tickets and the diff are already in your context. Search before calling anything missing or unwired: a registration may live in a file the diff never opened, and a caller may be a route table or a string.

- Requirements: walk each ticket's What to build and every acceptance criterion, both `- [ ]` and `- [x]`, against the diff. Check wiring (registered, routed, configured), a stub or TODO at a load-bearing spot, and work no requirement asked for: unrelated changes, a new dependency, a changed public contract, a migration. On staged scope, a requirement the diff does not touch is not a finding by itself: earlier commits may hold it. Under `no stated goal`, check only wiring and completeness, and say so.
- Documentation: README, a `docs/` site, CHANGELOG, `--help` text, `CLAUDE.md` or `AGENTS.md`, a domain glossary and decision records. Report what the diff made wrong and what it should have added: a new flag, endpoint, option, dependency, user-visible behavior or project convention left undocumented, a renamed or redefined glossary term, a contradicted accepted decision. A concept the glossary never covered is not a finding. Report a ticket item the diff contradicts.
- Conventions: read the `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` and `AGENTS.override.md` files that govern the changed files: the repository root's and those in a directory that is an ancestor of a changed file, which apply only at or below it. Report a changed line that clearly breaks a rule they state. Quote the rule with its file path and the line that breaks it; no style preference and no "spirit of the document" inference. A rule the diff makes wrong is a documentation finding instead.

Your proposals go through VERIFY like the agents'.

## VERIFY

The finders and LEAD CHECKS propose; the verifier decides what is real. Merge duplicates under VERIFY A FINDING and move a candidate beyond the reviewed scope to Follow-ups. Give every remaining candidate an id and send all of them, your LEAD CHECKS included, to one `dev:review-verify` launch with the packet from agent launch; never tell it which role raised a candidate. Wait for its result.

Apply every verdict as given; never refute, confirm or drop a candidate yourself.

| Verdict | Action |
| --- | --- |
| `confirmed` | Keep it with the severity its evidence supports under SEVERITY BAR. |
| `plausible` | Keep it, at most major, with what would confirm it. |
| `refuted` | Move it to Dismissed with the verifier's evidence. |
| Missing for a candidate, or the verifier did not finish | Keep the sweep incomplete; never treat the candidate as refuted. |

A `Noticed:` line goes to Follow-ups as `not verified`. Rank the kept findings by severity, worst first, confirmed before plausible at the same severity, and number them from 1 in that order. A direct pass applies the same table to the verdicts you gave.

Persist each finding's location, problem, verdict and evidence, including dismissal reasons, in the report. Dismissing most candidates is normal. A pre-existing broken test or lint failure is reported like anything else, never waived because it predates the branch.

## ARTIFACT

Write `.scratch/<feature-slug>/review.md` when one feature resolves from the argument or the matched tickets; a ticket under `.scratch/reviews/` resolves none. Never create a feature directory for a report. Several candidate features require a choice before writing. With none, use `.scratch/reviews/<branch-slug>/review.md`; derive a filesystem-safe slug from the branch (`detached-<tip>` when detached). Never write into a directory holding `map.md`; validate that the destination stays inside the repository, including symlinks.

Overwrite one report with the latest run; retain open follow-ups with the run that raised them and `not re-verified`. Do not silently drop them on a scope change. Write the review report FORMAT with each finding's `ticket:` set to `proposed` and the finding numbers of its group from PROPOSE TICKETS, or to the path of the open ticket that already covers it.

After VERIFY, re-resolve repository identity, branch, scope, merge-base, HEAD, staged digest when applicable, goal and all requirement sources and pins. Compare with the facts captured before the sweep. Write findings either way, but mark `sweep: complete` only when every fact still matches and all reviewers, the verifier included, finished. If anything moved or the run was interrupted, retain `sweep: incomplete` and name what changed or remains unfinished. A hard kill leaves the incomplete report already on disk.

## SUMMARY

Write for a reader who has never seen this code: short sentences, everyday words, a technical term explained the first time it appears.

1. `What this change does:` in two or three sentences.
2. The findings under `Critical`, `Major` and `Minor`, skipping empty groups, numbered as in the report. Each has a bold title with its location, then four parts of one or two short sentences:
   - **What this is:** what the code there does.
   - **Problem:** the concrete input or situation and the wrong result.
   - **Fix:** the smallest change that works.
   - **If we skip it:** what happens to users or data.

   A plausible finding has `(plausible)` after its title and a fifth part, **What would confirm it:**.
3. `Verdict: ship.` or `Verdict: fix 1 and 3 first.` A plausible finding counts toward the verdict like a confirmed one. An auth, payment, crypto or migration diff never gets `ship`: say it needs manual security review beyond this pass.
4. `Dismissed: N`, with the count of refuted candidates.
5. `Not checked:` in one line, when something mattered and could not be checked, including unstaged changes.
6. The report path.

With no findings: `What this change does:`, then `Looks good. Ship.` (or the security-review verdict), `Dismissed: N`, `Not checked:` when needed and the report path. Nothing is proposed.

## PROPOSE TICKETS

Before grouping, read the open tickets, any status but `resolved` and `wontfix`, in `.scratch/reviews/<branch-slug>/issues/` and, when the report resolved to a feature, in that feature's `issues/`. A finding whose fix an open ticket's What to build or criteria already require is covered: set its `ticket:` to that ticket's path and leave the ticket unchanged. List covered findings in the summary under `Already ticketed:`, one `- <number>: <ticket path>` line each; they join no group. When every finding is covered, skip `Recommended tickets:` and the question.

The user picks findings by their numbers; tickets have no labels of their own. End the summary with `Recommended tickets:`, one group per line, led by its finding numbers:

```text
- 1, 2, 5 (major): <title> - <reason for grouping>
- 3, 4 (minor): <title> - choice for 4: <question>; recommended: <option>
```

A ticket is one change the user runs in one `/plan` session and commits whole. Every uncovered finding belongs to exactly one group; a group takes the severity of its worst finding. Group in this order:

1. Each critical or major finding opens its own group. Join two of them only for a reason named in the line: one cause, one fix, edits in one place, or one end-to-end path that a single check proves.
2. A minor finding joins the critical or major group whose fix touches the same command, module or file.
3. The remaining minor findings form one group. Split it by area (command, module, test surface) only when it would not fit one session; never a group per minor finding.
4. A finding whose fix needs the user's choice names that choice and your recommendation in its group's line.

Expect about one group per critical or major finding plus one or two for the minor findings; this is a guide, not a cap.

Then ask the user to answer with finding numbers, for example "1, 3", "1-6", "all", "7 separately", "1 and 3 together", "4: <option>" or "none", and stop until the answer arrives.

## CREATE TICKETS

Create tickets only for the findings the answer selects:

| Answer | Tickets |
| --- | --- |
| Numbers or ranges: "1, 3", "1-6" | The selected findings, split by their recommended groups; an unselected finding stays out of its group's ticket. |
| "all" | Every recommended group. |
| "7 separately" | Finding 7 gets its own ticket; the other selected findings keep their groups. |
| "1 and 3 together" | One ticket for those findings, whatever their groups. |
| "4: <option>", "with the recommendation" | The choice is settled. A selected finding whose choice the answer leaves open gets its own `needs-info` ticket; its group stays `ready-for-agent`. |
| "none" | Nothing. |

An answer naming an unknown or already covered finding, or one you cannot read unambiguously, gets one question back before any write.

Read [ticket](../../references/ticket.md) and follow its TEMPLATE, NUMBERING and FIELDS, with these values:

- Location: `issues/` of the feature the report resolved to, else `.scratch/reviews/<branch-slug>/issues/`; never a directory holding `map.md`.
- `**What to build:**` the corrected behavior, then one numbered line per finding with its location and its Problem: the input or situation and the wrong result. A plausible finding's line ends with `plausible; confirm: <what would confirm it>`.
- `**Branch:**` the current branch, the base branch included; drop the line only on a detached HEAD.
- `**Status:**` `ready-for-agent`, with an answered choice written into `**What to build:**`; or, for the split-off ticket of an open choice, `needs-info` with that choice as a `[NEEDS CLARIFICATION: ...]` marker in the ticket body.
- The first criterion, verbatim: `- [ ] Each finding reproduced before the change, with evidence under ## Comments; a finding that did not reproduce is named there and its criteria removed; if none reproduced, set **Status** to wontfix and stop.` Then one criterion per finding from its Fix and its observable result, plus a regression test when the project has a test suite.

After writing, change only `ticket: proposed` entries in the report: the created path for a selected finding, `none` for the rest. A covered finding keeps its ticket path. Change nothing else in the report.

## STOP CONDITIONS

A finding beyond the reviewed scope goes to Follow-ups and gets no proposed ticket. Missing or ambiguous scope or requirements stop before launch; incomplete verification keeps the sweep incomplete.

## NEXT

After the answer, give the created ticket paths and suggest `/plan <ticket-path>` for each `ready-for-agent` one; a `needs-info` ticket names its question instead. When every finding was already covered, suggest `/plan <ticket-path>` for each covering `ready-for-agent` ticket. Commit, push and MR/PR creation require the user's explicit request.
