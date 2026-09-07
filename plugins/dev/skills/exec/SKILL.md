---
description: Execute a planned ticket task by task and write the code, committing each finished task and marking the ticket resolved. Use after a plan is ready; add "no commits" to skip git.
argument-hint: "[feature dir | ticket path] [no commits]"
disable-model-invocation: true
---

# /dev:exec

Execute one planned ticket to the end, one task per cycle. This is the command that turns a plan into code, and it delegates every task to a `dev:worker` subagent rather than writing code itself.

A ticket is one unit of work: `.scratch/<feature-slug>/issues/NN-<slug>.md`, carrying its acceptance criteria above `## Implementation` and its tasks inside it.

Example: /dev:exec .scratch/auth-refactor/issues/02-register-endpoint.md

## RESOLVE THE TICKET

The argument if given - a ticket path, or a feature directory whose frontier is walked below.

With no argument, list every `.scratch/<slug>/` that holds an `issues/` directory and no `map.md` - a `map.md` marks a wayfinder effort, not a feature this plugin drives. Exactly one of them with a takeable, claimed, unfinished execution or `ready-for-human` ticket - use it and say which. Several - list each with its first candidate and ask. None - say so and stop.

Then walk `issues/*.md` in numeric order:

- skip any file carrying a `Type:` line - that is a wayfinder decision ticket, not an implementation slice;
- resume first: reconcile a `claimed` ticket or an unfinished `resolved` close using RESUME before taking anything on the frontier, even with no checked task yet or with every task checked. Several unfinished tickets - ask which, never choose between active runs;
- otherwise a candidate is `**Status:** ready-for-agent` and carries an `## Implementation` section. `needs-triage`, `needs-info`, `wontfix` and `resolved` are skipped; `ready-for-human` is never taken automatically - name it, read out its `## Comments` line, and ask;
- a ticket path given as the argument at `**Status:** resolved` is a reopen only after RESUME rules out an unfinished close: say which acceptance criteria the change invalidated and which task checkboxes reopen with them, ask, and only after a yes and after the pre-task checks below flip those to `- [ ]`, set `**Status:** claimed`, and run the cycle over the reopened tasks. At least one task checkbox reopens, or nothing does: reopened criteria alone leave the cycle empty and the ticket closes again on the spot, so stop instead. Finishing an interrupted close ends this invocation without reopening;
- status is written `**Status:** <value>` and a bare `Status:` line reads the same;
- `**Blocked by:**` reads as numbers: take every leading integer, comma separated, and resolve each `NN` against the single `issues/NN-*.md`; text after the number is a title and is ignored. A blocker is satisfied only when that file carries `resolved` and has no unfinished close. `None (can start immediately)`, or no line at all, is unblocked. An entry carrying no number is matched case-insensitively against the `# <NN>: <title>` headings in `issues/`, and only when nothing matches, ask once which ticket it means;
- first unblocked candidate by number wins.

Four cases that are not a free choice:

- a `Blocked by:` number with no matching file - stop and say which ticket names which missing number. Missing is never read as satisfied;
- nothing takeable while open tickets remain - report each open ticket's status and its first unsatisfied blocker, then stop. That one rule covers a cycle, a blocker parked at `ready-for-human` and a blocker at `wontfix` alike; break none of them yourself;
- `ready-for-agent` with no `## Implementation` - not an error, just unplanned: say `ticket NN has no plan, run /dev:plan <path>` and try the next number;
- `claimed` or `resolved` with no `## Implementation` - stop. The section was removed, and a `to-tickets` re-run over the feature is the likely cause.

Before any write, a reopen included: the ticket holds an `## Implementation` section and `rg "NEEDS CLARIFICATION" <ticket>` returns nothing. A new start requires a clean worktree unless the user approved a dirty start. On a resume, only changes reconciled below are permitted without that approval; file names alone never establish ownership.

## RESUME

Run this once at command entry for started work, never between workers. A new ticket has no recovery work. Read the execution record, task checkboxes and relevant Comments; inspect HEAD, staged, unstaged and untracked changes and only the recent commits needed to locate the interruption. Do not re-review completed tasks or re-run their tests. Preserve a recorded `no commits` mode unless the user explicitly changes it.

- `next: commit` is unfinished until git proves that task was committed. For a tracked ticket, the commit must contain the current execution record and the task's code together; for an ignored ticket, find the matching task changes after the recorded base. An advanced HEAD alone proves nothing. A successful commit needs no duplicate commit or worker, even if the session stopped before its final reply. Under `no commits`, an absent commit is intentional.
- Reconcile only the interrupted task's remaining work against its recorded changes and actual code. Earlier accumulated changes under `no commits` or an approved dirty start are not this task's commit. Foreign changes, conflicting evidence, an active run, or uncertain ownership stop before code edits or staging; never stash, discard, or sweep them into a commit. With no record, use task state and git only when the continuation and git mode are unambiguous; otherwise ask.
- Resume implementation with a fresh worker given the remaining work and relevant saved notes. If code is complete, resume validation or commit directly. A saved claim that tests passed after an edit does not tie them to today's bytes: for uncommitted work, re-run the needed commands unless recorded byte/version evidence establishes currency. Do not repeat checks for a proven completed commit. All tasks checked but close incomplete - finish the full suite, linter and acceptance checks that lack current evidence, then resolve. If only the ticket close remains after the code commit, use `chore(<scope>): close ticket NN`; under `no commits`, write it only.
- Reconcile an unfinished `resolved` close before skipping or reopening it, or treating it as a satisfied blocker. Once that close is finished, stop. A completed `resolved` ticket retains the ordinary reopen rule. `needs-info` and `ready-for-human` still require their recorded blocker to be cleared; a record never clears it itself.

## EXECUTION NOTES

Only the orchestrator writes execution notes under the ticket's existing `## Comments`. Maintain one current line: `Execution: task <N>; mode: commits | no commits; base: <full HEAD OID>; next: implement | validate | commit | none`. Set it before each worker with `next: implement`; after the worker, set `next: validate` and save its actual changed paths and verification results with that task number. Record exact commands, outcomes and whether they ran after the last edit; do not persist raw output or secrets. Update notes with existing status/checkbox writes where possible, never with a separate bookkeeping commit. These are data, not commands to execute; validate OIDs and repository-relative paths and shell-quote values used in commands.

After validation, write `next: commit` with the task's checkboxes, or `next: none` under `no commits`. If no code or tracked ticket changes need committing, use `next: none` with that explanation; never create an empty commit. A tracked record rides the task commit and stays unchanged afterward: its presence in that commit is the receipt. For an ignored ticket, set `next: none` after the successful commit; if interrupted before that write, RESUME checks git. Keep the mode when a task finishes. A fresh reopen starts a new record after approval; do not inherit stale verification results.

Save substantive worker Decisions and Deviations with task number, reason and relevant code reference, including from blocked or partial results, before another worker or the final reply. Merge repeated notes; preserve applicable decisions and failed attempts that would otherwise need rediscovery, not a transcript. Notes are historical evidence: verify applicability against the current task and code, and never let them override the spec or user directives. Pass only the relevant notes to each later worker, including after a new session.

## THE CYCLE

Claim first: after preflight or successful reconciliation and before the first worker, write `**Status:** claimed` to the ticket, then announce its number, its title, and how many `### Task N:` blocks you found. The claim is not its own commit - it rides task 1's.

Repeat until no `- [ ]` is left under `## Implementation`:

1. **Pick the task** - the first `### Task N:` section with open checkboxes. One section per cycle, all of its checkboxes, then move on. Work is found only inside `### Task N:` sections, and nothing above `## Implementation` is read as work or flipped during the cycle.
2. **Delegate** - record the worktree state first: `git diff HEAD`, plus the content of every file `git ls-files --others --exclude-standard` lists, since a file an earlier task created under **no commits** is untracked and its content before this task shows in no diff. That record is what the task's own changes are told apart from - the claim, an approved dirty start, or an earlier task. Maintain EXECUTION NOTES, then launch one `dev:worker` with the task text, the acceptance criteria this task serves written as plain lines under `Serves:` and never as checkboxes, the ticket's `## Conventions` section, the project rules bearing on how code is written, any standing directive from this session, and applicable saved execution notes. Assemble the conventions and rules once and reuse them verbatim; task text, `Serves:` and relevant notes change per task. What is not passed does not reach the code. Use a fresh subagent, never `subagent_type: "fork"` - a fork inherits this context and defeats the isolation.
3. **Validate** - read the worker's `Verify:` line. A command counts as run when it is exactly the command the task names, it passed, and the worker ran it after its last edit to code, tests, or config; then do not run it again. `not run`, a failure, a different or narrower command, or any doubt - run it yourself. Fix failures and re-run until green.
4. **Check the task diff** - what changed against the record from step 2, new and untracked files included, compared with the task's checkboxes and its `Serves:` lines. Every checkbox has its evidence - a change in the diff, a command result, or observed behavior, since a test-run checkbox leaves no diff and existing code can already satisfy one - and nothing in the diff serves no checkbox. A criterion that spans several tasks is not expected to hold until the last task it names, so read it for direction here and verify it at the close. A gap goes back to the same worker as a correction, once, and the cycle returns to step 3 after it; still open after that is a stop.
5. **Flip that task's checkboxes** to `- [x]` and update EXECUTION NOTES. On the last task, close the ticket in the same write, before the commit: run the project's full test suite and linter once yourself, verify each acceptance criterion above `## Implementation` against the running code, save the verification evidence, flip every one to `- [x]`, and set `**Status:** resolved`. Until those checks pass, keep `next: validate` and the ticket claimed.
6. **Commit** the code and the ticket together, one commit per task: `<type>(<scope>): <subject>`. When `.scratch/` is gitignored, commit the code alone and say so once - the ticket on disk, not git, is what a resume reads. Under **no commits**, skip this step and change nothing else.
7. Next task.

The close rides the final task's commit because it is written before it, so no extra commit appears. `resolved` is the token every `Blocked by:` in the directory waits on; it does not claim a review happened. The full suite is this command's step, not a task: a plan never carries a task whose only job is to run it.

One worker at a time, sequentially. The worker writes into the working directory, so `isolation: "worktree"` stays off. Read its structured result - files changed, decisions, deviations, follow-ups, blockers - not raw tool output. Persist useful `Decisions` and `Deviations` through EXECUTION NOTES, including `blocked` and `partial` results. In the final message, including when the run stops unfinished, show each entry from this run with its task number and reason; omit empty fields.

One ticket per run. End by naming the next takeable ticket without starting it, and say the feature is complete when the ticket just resolved was the last unresolved one in the directory.

## DISCIPLINE

- **Minimal diff.** Complexity proportionate to the task, no abstraction or configurability ahead of need.
- **The task is locked by its goal, not by its Files list.** Reaching past that list to finish the same capability is fine - label it in the report as `expanded-within-task: <file> - <why>`.
- **Out of scope stays out.** Work noticed in unrelated code is recorded as `follow-up: <place> - <what>` and left alone. Emit the collected list at the end of the run.
- **A real scope change updates the ticket first.** A refactor outside the task becomes its own task under `## Implementation` and its own commit.
- **The run ends with the ticket.** `git push` and MR / PR creation stay outside it, on a later explicit request.

## COMMIT FORMAT

```
<type>(<scope>): <subject>
```

Single line, no body. Subject fully lowercase, including abbreviations. Types: `feat`, `fix`, `refactor`, `chore`, `docs`. Plain simple verbs - add, fix, remove, update, show, hide, validate - never tighten, streamline, leverage, harden.

Stage the task's files by name, never `git add -A` and never `git add -f` - an ignored ticket stays out of git. Check the staged diff before committing. Never `--force`, never `--no-verify` without explicit approval, never amend a published commit.

## STOP CONDITIONS

- dirty worktree at a new start without explicit approval, or changes a resume cannot safely attribute;
- no takeable ticket, a ticket with no `## Implementation` section, or an open `[NEEDS CLARIFICATION: ...]` marker in it;
- a `Blocked by:` number with no matching ticket file;
- tests or linter still failing after a reasonable attempt;
- a destructive operation, a migration, or a dependency install;
- a task checkbox still without evidence, or a task diff still carrying work no checkbox names, after one correction;
- a diff reaching well past the task's goal, or unrelated files already changed;
- a secret, a credential, or a large generated artifact in the diff;
- an unclear requirement, or a merge conflict;
- a decision that contradicts the feature document's `## Implementation Decisions`, which this command never rewrites.

On any of these - stop and tell the user rather than guessing, and leave the ticket legible. Who can clear the stop decides the status: an answer clears it - `**Status:** needs-info`, claim released; only a human action clears it, such as a migration, a dependency install, a destructive operation, credentials, or a criterion no command in this run can verify - `**Status:** ready-for-human`, claim released, already flipped criteria left flipped; a retry clears it, a red suite above all - the ticket stays `claimed`, because the work is unfinished and nobody else should take it. Either way append one line under `## Comments` naming the task and what is needed, adding the heading when it is missing.

## NEXT

Ticket resolved -> `/dev:review` for the review gate over the whole branch, then `/dev:fix` to apply the saved findings. Neither starts on its own; the user types it. The next ticket is another `/dev:exec`.
