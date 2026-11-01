---
name: dev-review
description: Independently review intended task changes, including committed checkpoints and uncommitted work, when the user explicitly invokes /dev-review. Save verified findings and hand selected corrections to dev-exec without creating tickets or starting execution. Never changes code or Git state.
argument-hint: "[task context | ticket path | feature dir]"
disable-model-invocation: true
---

# /dev-review

Review the intended net work, explain verified findings and return the corrections the user selects. A task may have committed checkpoints, staged, unstaged and untracked changes, or no tickets at all. No `git add` is required.

Example: /dev-review

Suggest a next operation at a handoff; never start it automatically. Reuse explicit authorization only within its actual scope. A review verdict or finding selection is not implementation approval.

## STANCE

Write only the review report: no code, tickets, project specs, journal, index, Git objects or commits. A review of someone else's PR is the normal case, and it must never touch their branch. Existing task artifacts and ticket statuses are read-only context, not permission to execute. Do not recreate a removed coordinator from a legacy packet; clarify conflicting instructions instead.

Use read-only inspection, with `GIT_OPTIONAL_LOCKS=0` for git. Checks may create disposable caches or build output outside the repository, but must not change its working tree or Git state; pass this constraint to every agent. Use checks without auto-fix or snapshot updates. Agents return findings to you and never edit the report or any other file.

## RESOLVE THE SCOPE

Read [selected snapshot](references/selected-snapshot.md) before resolving scope. It owns baseline selection, checkpoint coverage, source reads and currency. Resolve and pin the scope before any report write or reviewer launch.

Task context or a ticket/feature path identifies requirements, not an automatic code selection. Ordinary scope is the whole intended task, not whichever changes happen to be staged. Preserve an explicit narrower request, such as one commit, staged changes or named files; record its exclusions and never claim it covers the whole task. Clarify an ambiguous request instead of interpreting an unknown flag or word as a mode. Do not add scope-selector flags.

Stop for uncertain task ownership, ambiguous baseline or omitted required checkpoints/working changes. Do not stage, stash, switch branches, manufacture a tree or rewrite foreign work to obtain a scope. An empty index does not mean no work: consider selected unstaged/untracked files first. Only when all intended work is accounted for and the selected net change is empty may you stop without a new report, explaining any intentional cancellation.

## REQUIREMENTS

Use the user's goal, approved task plan and explicitly applicable feature, diagnosis, ticket or prior review context. A small request needs no task directory or ticket. If a feature is supplied, identify its applicable requirements with the user/context; ticket status alone cannot establish task scope or completed behavior. Read each applicable ticket's What to build and acceptance criteria plus the relevant Problem Statement and Solution from its adjacent feature record. Preserve existing identities, history and prohibitions; do not migrate artifacts.

Resolve every file through the selected snapshot's source rules and pin its exact version. A requirement supplied separately as current task context may use disk bytes with SHA256 even in a narrow historical review; label that choice explicitly. Never silently substitute disk for a pinned index or commit source. Read status and branch from the same version as the text.

Preserve an explicit user goal. Without one, state the goal from the applicable requirements; with neither, use `no stated goal`. Never infer intent or ownership from commit subjects, branch names or the diff. Preserve the actual goal sentence and its authorization source in the report. Missing material requirements stop before launch, not with an invented acceptance criterion.

## EXISTING REPORT

Resolve the report destination using ARTIFACT before writing. Read [review report](references/review-report.md), validate any existing report under its VALIDATION and check its CURRENCY.

| Report state | Next action |
| --- | --- |
| Current and complete | Ask before repeating the same sweep, unless the user already explicitly requested a fresh sweep of it. |
| Unfinished run | Start a new sweep under the newly resolved scope. Preserve follow-ups as historical context. |
| Not current, or invalid | Start a new sweep; never execute or trust old fields. |

Preserve open follow-ups with origin before overwriting. A request to use review is not by itself approval to overwrite a current report; a request to review it again is.

## LAUNCH THE AGENTS

Before mutating the report for an agent-based sweep, read [agent launch](references/agent-launch.md) and complete its capability check for every required role. Use the selected native subagent facility and its complete reviewer packet for every launch. Before any launch or direct pass, read [findings](references/findings.md): its SEVERITY BAR is the bar for every reviewer, for ORCHESTRATOR CHECKS and for VERIFY, and its VERIFY A FINDING decides every verdict.

Before any agent launch or direct pass, write Scope, Requirements and `sweep: incomplete` to the report, retaining carried follow-ups. Use the review report FORMAT. Never leave the old complete report in place while a new sweep runs.

Launch these three finder roles, concurrently when capacity permits:

- `review-quality`: bugs, edges, errors, races, expected load and security skim;
- `review-testing`: coverage and test quality;
- `review-simplification`: introduced over-engineering, reuse and fixes at the wrong depth.

The fourth role, `review-verify`, runs under VERIFY after every finder has returned. A trivial diff (dotfiles, docs only, pure formatting) may receive a direct pass against the same bar instead, with no agent: you find the candidates and give them the verdicts of VERIFY A FINDING yourself. There is one sweep and no re-check.

Wait for every launched agent and complete the before/after checks in agent launch before verification, another launch or further writes. A failed or incomplete check stops the sweep; preserve changes and report the limitation without resetting them.

## ORCHESTRATOR CHECKS

Check requirements, documentation and conventions yourself, against the same bar. These are orchestrator checks, not a separate coordination stage. Search before calling anything missing or unwired: a registration may live in a file the diff never opened, and a caller may be a route table or a string.

- Requirements: walk the approved behavior and every acceptance criterion, both `- [ ]` and `- [x]` when present, against the selected net work and its surrounding code. Check wiring (registered, routed, configured), a stub or TODO at a load-bearing spot, and work no requirement asked for: unrelated changes, a new dependency, a changed public contract, a migration. In a narrow review, an untouched requirement is not a finding by itself: other work may hold it. Under `no stated goal`, check only wiring and completeness, and say so.
- Documentation: README, a `docs/` site, diagrams and their captions and accessibility text, CHANGELOG, `--help` text, `CLAUDE.md` or `AGENTS.md`, a domain glossary and decision records. For a changed command or route, search the old and new names in affected documentation, including outside the diff; distinguish an obsolete description from a still-valid legacy or historical use. Search and read changed and unchanged documentation through the selected snapshot, including selected unstaged and untracked files; never fall back to tip/index versions that omit them or include excluded working changes. Report what the diff made wrong and what it should have added: a new flag, endpoint, option, dependency, user-visible behavior or project convention left undocumented, a renamed or redefined glossary term, a contradicted accepted decision. A concept the glossary never covered is not a finding. Report a requirement the diff contradicts.
- Project specs: read them per [project specs](references/project-specs.md) for the changed paths, applying its exact-name listings and reads to the selected snapshot rather than unrelated disk versions. Explicitly applicable private `.SPEC.md` context uses pinned disk bytes. A changed line that contradicts a spec statement is a finding; quote the statement with its spec path. A missing spec, an uncovered module, behavior the diff adds that no spec mentions yet (that is `/dev-spec` work) and a contradiction with an `(unconfirmed)` statement are not findings. Nor is an agreed spec change: a contradiction with a requirement that replaces the statement by naming the new behavior, when the diff matches that behavior, such as an approved correction or decision that reopened the statement. List it under Follow-ups as `pending dev-spec` with the requirement path or exact user instruction as origin and the quoted statement with its spec path, also when the verifier refuted a candidate on this ground. The exception covers only that statement: naming the spec path without the replacing behavior, another contradicted statement of the same spec, a diff that does not match the replacement and a code defect in the same lines stay findings.
- Conventions: read the `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` and `AGENTS.override.md` files that govern the changed files: the repository root's and those in a directory that is an ancestor of a changed file, which apply only at or below it. Report a changed line that clearly breaks a rule they state. Quote the rule with its file path and the line that breaks it; no style preference and no "spirit of the document" inference. A rule the diff makes wrong is a documentation finding instead.

Your proposals go through VERIFY like the agents'.

## VERIFY

The finders and ORCHESTRATOR CHECKS propose; the verifier decides what is real. Merge duplicates under VERIFY A FINDING and move a candidate beyond the reviewed scope to Follow-ups. Give every remaining candidate an id and send all of them, your own checks included, to one `review-verify` launch with the packet from agent launch; never tell it which role raised a candidate. Wait for its result.

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

Write `.scratch/<feature-slug>/review.md` when one existing feature resolves unambiguously from the explicit task context; a ticket under `.scratch/reviews/` resolves none. Never create a feature directory for a report. Several candidate features require a choice before writing. With none, use `.scratch/reviews/<branch-slug>/review.md`; derive a filesystem-safe slug from the branch (`detached-<tip>` when detached). Never write into a directory holding `map.md`; validate that the destination stays inside the repository, including symlinks. If the default destination is itself reviewed work or owned by another writer, agree on a safe repository-local report path or stop.

Overwrite one report with the latest run; retain open follow-ups with the run that raised them and `not re-verified`. Do not silently drop them on a scope change. Preserve prior ticket references only as historical context, never as a request to create, update or execute a ticket.

After VERIFY, re-resolve the selected snapshot, baseline, checkpoint coverage, repository identity, branch, HEAD, index digest, goal and all requirement/context pins under review report CURRENCY. Write findings either way, but mark `sweep: complete` only when every fact still matches, the mandatory state comparisons passed and all required reviewers finished. If anything moved or the run was interrupted, retain `sweep: incomplete` and name what changed or remains unfinished. A hard kill leaves the incomplete report already on disk. After an unexpected state change, do not overwrite unfamiliar report edits; report the limitation without discarding any changes.

## SUMMARY

Write for a reader who has never seen this code: short sentences, everyday words, a technical term explained the first time it appears.

1. `What this change does:` in two or three sentences.
2. The findings under `Critical`, `Major` and `Minor`, skipping empty groups, numbered as in the report. Each has a bold title with its location, then four parts of one or two short sentences:
   - **What this is:** what the code there does.
   - **Problem:** the concrete input or situation and the wrong result.
   - **Fix:** the smallest change that works.
   - **If we skip it:** what happens to users or data.

   A plausible finding has `(plausible)` after its title and a fifth part, **What would confirm it:**.
3. `Verdict: ship.` or `Verdict: fix 1 and 3 first.` A plausible finding counts toward the verdict like a confirmed one. A narrow review qualifies the verdict with its boundary; it never approves the whole task. An incomplete sweep never gets `ship`. An auth, payment, crypto or migration diff never gets `ship`: say it needs manual security review beyond this pass.
4. `Dismissed: N`, with the count of refuted candidates.
5. `Not checked:` in one line, when something mattered and could not be checked, plus explicit scope exclusions. Selected unstaged and untracked changes are reviewed, not automatically excluded here.
6. The report path.

With no findings, use `Looks good. Ship.` only for a complete full-task sweep with no security-review limitation. Otherwise state the narrow boundary, security requirement or incomplete status. Include the dismissal count, relevant limitations and report path. Nothing is proposed when there are no kept findings.

## SELECTED CORRECTIONS

When corrections are wanted, use the finding numbers from this report. Reuse an explicit existing selection; otherwise ask for numbers, `all` or `none`. Clarify unknown or ambiguous numbers and material fix choices. A refuted candidate or unverified follow-up is not a verified finding. Do not create tickets, selection files or report copies, or modify existing tickets.

Before handoff, recheck report CURRENCY and require a complete sweep. If it is stale, incomplete or has been replaced since the selection, stop and resolve the evidence/selection rather than reusing numbers from another sweep.

Return the report path, its SHA256 at handoff, selected finding numbers, goal, scope/head/base/tip and snapshot pins, verdicts, evidence, remaining confirmation steps and settled/open choices in the response. Keep unselected findings in the report. `none` ends the review without a fix handoff. These are inputs to `dev-exec`, not a new artifact protocol or permission to start it.

## STOP CONDITIONS

A finding beyond the reviewed scope goes to Follow-ups. Missing or ambiguous scope, ownership, baseline or material requirements stop before launch; incomplete verification or a failed state check keeps the sweep incomplete. Preserve unfamiliar changes and never reset, clean or overwrite them.

## NEXT

Suggest `dev-exec` with the report and selected finding numbers directly; no ticket is required. Execution must obtain applicable fix/plan approval, inspect current prerequisites and reproduce or otherwise confirm each selected finding before changing code. A plausible finding still needs its named confirmation. If a finding does not reproduce, retain that result and evidence as unconfirmed, not silently fixed; do not implement its proposed fix. Confirmed corrections need focused verification and a regression test where practical. Open material choices or missing prerequisites remain blockers.

Never start execution automatically. A selection, `ship` verdict or saved report authorizes neither implementation nor commit, push or MR/PR creation. An existing explicit instruction covering several operations may be reused only within its actual approved scope.
