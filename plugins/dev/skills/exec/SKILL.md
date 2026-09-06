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

With no argument, list every `.scratch/<slug>/` that holds an `issues/` directory and no `map.md` - a `map.md` marks a wayfinder effort, not a feature this plugin drives. Exactly one of them with a takeable, claimed or `ready-for-human` ticket - use it and say which. Several - list each with its first takeable ticket and ask. None - say so and stop.

Then walk `issues/*.md` in numeric order:

- skip any file carrying a `Type:` line - that is a wayfinder decision ticket, not an implementation slice;
- resume first: a ticket at `**Status:** claimed` with an open `- [ ]` under `## Implementation` is taken before anything on the frontier. One at `claimed` carrying an `## Implementation` section and no open task checkbox resumes at the closing step instead - run the suite and the linter, verify the criteria, flip them, set `**Status:** resolved`. That close is committed with whatever of the last task is still uncommitted, and on its own as `chore(<scope>): close ticket NN` when the last task's commit already exists; under **no commits** it is written and not committed;
- otherwise a candidate is `**Status:** ready-for-agent` and carries an `## Implementation` section. `needs-triage`, `needs-info`, `wontfix` and `resolved` are skipped; `ready-for-human` is never taken automatically - name it, read out its `## Comments` line, and ask;
- a ticket path given as the argument at `**Status:** resolved` is a reopen, never a skip: say which acceptance criteria the change invalidated and which task checkboxes reopen with them, ask, and only after a yes and after the pre-task checks below flip those to `- [ ]`, set `**Status:** claimed`, and run the cycle over the reopened tasks. At least one task checkbox reopens, or nothing does: reopened criteria alone leave the cycle empty and the ticket closes again on the spot, so stop instead;
- status is written `**Status:** <value>` and a bare `Status:` line reads the same;
- `**Blocked by:**` reads as numbers: take every leading integer, comma separated, and resolve each `NN` against the single `issues/NN-*.md`; text after the number is a title and is ignored. A blocker is satisfied only when that file carries `resolved`. `None (can start immediately)`, or no line at all, is unblocked. An entry carrying no number is matched case-insensitively against the `# <NN>: <title>` headings in `issues/`, and only when nothing matches, ask once which ticket it means;
- first unblocked candidate by number wins.

Four cases that are not a free choice:

- a `Blocked by:` number with no matching file - stop and say which ticket names which missing number. Missing is never read as satisfied;
- nothing takeable while open tickets remain - report each open ticket's status and its first unsatisfied blocker, then stop. That one rule covers a cycle, a blocker parked at `ready-for-human` and a blocker at `wontfix` alike; break none of them yourself;
- `ready-for-agent` with no `## Implementation` - not an error, just unplanned: say `ticket NN has no plan, run /dev:plan <path>` and try the next number;
- `claimed` or `resolved` with no `## Implementation` - stop. The section was removed, and a `to-tickets` re-run over the feature is the likely cause.

Before the first task, and before any write to the ticket, a reopen included: the worktree is clean unless the user approved a dirty start, the ticket holds an `## Implementation` section, and `rg "NEEDS CLARIFICATION" <ticket>` returns nothing.

## THE CYCLE

Claim first: after the clean-worktree check and before the first worker, write `**Status:** claimed` to the ticket, then announce its number, its title, and how many `### Task N:` blocks you found. The claim is not its own commit - it rides task 1's.

Repeat until no `- [ ]` is left under `## Implementation`:

1. **Pick the task** - the first `### Task N:` section with open checkboxes. One section per cycle, all of its checkboxes, then move on. Work is found only inside `### Task N:` sections, and nothing above `## Implementation` is read as work or flipped during the cycle.
2. **Delegate** - record the worktree state first: `git diff HEAD`, plus the content of every file `git ls-files --others --exclude-standard` lists, since a file an earlier task created under **no commits** is untracked and its content before this task shows in no diff. That record is what the task's own changes are told apart from - the claim, an approved dirty start, or an earlier task. Then launch one `dev:worker` with the task text, the acceptance criteria this task serves written as plain lines under `Serves:` and never as checkboxes, the ticket's `## Conventions` section, the project rules bearing on how code is written, and any standing directive from this session. Assemble the conventions and rules once and reuse them verbatim; the task text and its `Serves:` lines change per task. What is not passed does not reach the code. Use a fresh subagent, never `subagent_type: "fork"` - a fork inherits this context and defeats the isolation.
3. **Validate** - read the worker's `Verify:` line. A command counts as run when it is exactly the command the task names, it passed, and the worker ran it after its last edit to code, tests, or config; then do not run it again. `not run`, a failure, a different or narrower command, or any doubt - run it yourself. Fix failures and re-run until green.
4. **Check the task diff** - what changed against the record from step 2, new and untracked files included, compared with the task's checkboxes and its `Serves:` lines. Every checkbox has its evidence - a change in the diff, a command result, or observed behavior, since a test-run checkbox leaves no diff and existing code can already satisfy one - and nothing in the diff serves no checkbox. A criterion that spans several tasks is not expected to hold until the last task it names, so read it for direction here and verify it at the close. A gap goes back to the same worker as a correction, once, and the cycle returns to step 3 after it; still open after that is a stop.
5. **Flip that task's checkboxes** to `- [x]`. On the last task, close the ticket in the same write, before the commit: run the project's full test suite and linter once yourself, verify each acceptance criterion above `## Implementation` against the running code, flip every one to `- [x]`, and set `**Status:** resolved`.
6. **Commit** the code and the ticket together, one commit per task: `<type>(<scope>): <subject>`. When `.scratch/` is gitignored, commit the code alone and say so once - the ticket on disk, not git, is what a resume reads. Under **no commits**, skip this step and change nothing else.
7. Next task.

The close rides the final task's commit because it is written before it, so no extra commit appears. `resolved` is the token every `Blocked by:` in the directory waits on; it does not claim a review happened. The full suite is this command's step, not a task: a plan never carries a task whose only job is to run it.

One worker at a time, sequentially. The worker writes into the working directory, so `isolation: "worktree"` stays off. Read its structured result - files changed, decisions, deviations, follow-ups, blockers - not raw tool output. Collect `Decisions` and `Deviations` from every worker response in this run's context, including `blocked` and `partial` results. In the final message, including when the run stops unfinished, show each entry with its task number and reason; omit empty fields.

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

- dirty worktree at start without explicit approval;
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
