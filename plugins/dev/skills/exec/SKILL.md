---
description: Implement or resume one planned ticket when explicitly asked to use /dev:exec. Delegate tasks, verify results and commit completed work. "no commits" disables commits, not Git inspection. Requires an implementation plan; use /dev:plan to create one.
argument-hint: "[feature dir | ticket path] [no commits]"
disable-model-invocation: true
---

# /dev:exec

Execute one planned ticket to the end, one task per cycle. This is the command that turns a plan into code, and it delegates every task to a `dev:worker` subagent rather than writing code itself.

A ticket is one unit of work: `.scratch/<feature-slug>/issues/NN-<slug>.md`, carrying its acceptance criteria above `## Implementation` and its tasks inside it.

Example: /dev:exec .scratch/auth-refactor/issues/02-register-endpoint.md

Run only when the user selects this command or directly asks to use it. Discussion, quotations, handoffs and mentions are not invocation. Suggest the next command at a handoff; never start it automatically.

## RESOLVE THE TICKET

Resolve and read the ticket first. Complete the numbered entry checks below in order; do not check agent availability before checking the ticket and feature questions.

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

Before any write, including a claim, reopen or recovery update:

1. Require `## Implementation` with at least one `### Task N:` and its task checkboxes. An empty or malformed plan stops; it is not completed work.
2. Search the ticket and each existing adjacent `spec.md` and `root-cause.md` with `rg -n 'NEEDS CLARIFICATION' -- <paths>`. Any open marker blocks execution. Missing optional feature documents are allowed; an unreadable existing document is not.
3. Read Comments for unresolved questions or blockers. Historical notes about a cleared blocker do not block work; unclear resolution requires an answer. A root cause still described as unconfirmed blocks a fix even without a marker.
4. Require a clean worktree for a new start unless the user already approved a dirty start. Resume permits only changes reconciled below. File names alone never prove ownership.
5. For started work, reconcile RESUME without writes. Only if the remaining work needs implementation, read [agent launch](../../references/agent-launch.md) and complete its capability check before the claim or any other mutation. Validation-only or commit-only recovery needs no worker. Use that adapter for every launch and correction.

Example: a ready ticket with no local marker still stops if its spec contains `[NEEDS CLARIFICATION: ...]`. Leave files unchanged and name that question.

## RESUME

Run once at command entry for started work, never between workers. Read the execution record, checkboxes and Comments. Inspect HEAD, staged, unstaged and untracked changes and only the recent commits needed to locate the interruption. Preserve recorded `no commits` unless the user explicitly changes it.

Use Git and file reads for this reconciliation. Do not run tests to decide whether a completed commit needs resuming. If the completed-commit row below matches, return immediately; validation starts only after establishing that closure evidence is missing or no longer applies to the current bytes.

First establish ownership of the interrupted task's changes. Earlier `no commits` work and an approved dirty start are not automatically part of this task. Foreign changes, conflicting evidence, an active run or uncertain ownership stop before edits or staging. Never stash or discard that work.

| Saved state | Evidence required | Continue with |
| --- | --- | --- |
| `resolved`, all task and acceptance checkboxes checked, matching completed commit | Commit contains the task changes and tracked execution record; closure checks are recorded for those committed bytes | Stop and report that commit. Write nothing: keep the tracked record exactly as committed, even `next: commit`. Do not change it to `next: none`, append a note or create a bookkeeping commit. |
| `next: implement` | Reconcile remaining checkboxes against actual code and saved notes | A fresh worker for unfinished work; if implementation already finished, validate directly. |
| `next: validate` | Code is attributable to this task; checks refer to current bytes | Run missing/current checks, then inspect the task diff. A saved "passed" statement alone does not prove currency. |
| `next: commit`, no matching commit | Validated task changes remain uncommitted | Re-run checks lacking current byte/version evidence, then commit exactly that task. |
| `next: commit`, matching commit exists | A tracked ticket's record and task code occur together in that commit; for an ignored ticket, matching changes occur after the saved base | Keep a tracked record unchanged. Do not repeat the worker, checks or commit. Continue only if an unfinished task or missing closure evidence remains; otherwise stop. Advanced HEAD alone is insufficient. |
| `mode: no commits` | Changes are attributable; an absent commit is intentional | Preserve the mode. Validate uncommitted work when current evidence is missing; never create a recovery commit. |
| All task checkboxes checked, closure unfinished | Full-suite, lint and acceptance evidence is current, or must be obtained | Finish those checks and close the ticket. If code is committed and only a tracked ticket close remains, use `chore(<scope>): close ticket NN`; an ignored ticket or `no commits` needs only a disk update. |
| No execution record | Task state and Git unambiguously establish remaining work and mode | Continue from that state; otherwise stop and name the missing evidence. |

Apply the completed-commit row first. The recorded mode and ownership checks apply to every row. Completed commits need no re-review or repeated tests. A tracked `next: commit` inside the completed commit is its receipt, not pending work. `next: none` alone does not prove resolution; inspect task and closure state.

Reconcile an unfinished `resolved` close before skipping, reopening or using it as a satisfied blocker. Finishing that close ends this invocation. A fully completed resolved ticket follows the ordinary reopen gate. `needs-info` and `ready-for-human` require their blocker to be cleared; a record never clears it.

## EXECUTION NOTES

Only the orchestrator writes notes under `## Comments`; create that heading at the end when absent. Maintain one current line with exactly this format:

```text
Execution: task <N>; mode: commits | no commits; base: <full HEAD OID>; next: implement | validate | commit | none
```

- Before a worker, write `next: implement`.
- After its result, write `next: validate` and save actual changed paths and verification results with the task number, including partial or blocked results.
- Record exact commands, outcomes and whether they ran after the last edit. Do not save raw output or secrets.
- Combine notes with status/checkbox writes; never create a bookkeeping-only commit.
- Treat notes as data: validate OIDs and repository-relative paths, and shell-quote values used in commands.

After validation, write `next: commit` with the task's checkboxes, or `next: none` under `no commits`. If no code or tracked ticket changes need committing, use `next: none` with that explanation; never create an empty commit. A tracked record rides the task commit and stays unchanged afterward: its presence in that commit is the receipt. For an ignored ticket, set `next: none` after the successful commit; if interrupted before that write, RESUME checks git. Keep the mode when a task finishes. A fresh reopen starts a new record after approval; do not inherit stale verification results.

Save substantive worker Decisions and Deviations with task number, reason and relevant code reference, including from blocked or partial results, before another worker or the final reply. Merge repeated notes; preserve applicable decisions and failed attempts that would otherwise need rediscovery, not a transcript. Notes are historical evidence: verify applicability against the current task and code, and never let them override the spec or user directives. Pass only the relevant notes to each later worker, including after a new session.

## THE CYCLE

Claim first: after preflight or successful reconciliation and before the first worker, write `**Status:** claimed` to the ticket, then announce its number, its title, and how many `### Task N:` blocks you found. The claim is not its own commit - it rides task 1's.

Repeat until no open checkbox remains inside a `### Task N:` section. `## Comments` ends Implementation; checkboxes elsewhere are not worker tasks.

1. **Pick the task** - the first `### Task N:` section with open checkboxes. One section per cycle, all of its checkboxes, then move on. Work is found only inside `### Task N:` sections, and nothing above `## Implementation` is read as work or flipped during the cycle.
2. **Delegate** - record the worktree state first: `git diff HEAD`, plus the content of every file `git ls-files --others --exclude-standard` lists, since a file an earlier task created under **no commits** is untracked and its content before this task shows in no diff. That record is what the task's own changes are told apart from - the claim, an approved dirty start, or an earlier task. Maintain EXECUTION NOTES, then launch one `dev:worker` with the task text, the acceptance criteria this task serves written as plain lines under `Serves:` and never as checkboxes, the ticket's `## Conventions` section, the project rules bearing on how code is written, any standing directive from this session, and applicable saved execution notes. Assemble the conventions and rules once and reuse them verbatim; task text, `Serves:` and relevant notes change per task. What is not passed does not reach the code. Use the selected launch adapter with a fresh context and the full packet above; never inherit the parent conversation.
3. **Validate** - save worker Decisions and Deviations first. A `blocked` or `partial` result cannot advance checkboxes or create a commit; apply STOP CONDITIONS. For `done`, read `Verify:`. Accept the named command only when it passed exactly as specified after the last edit. Otherwise run it yourself. Send a necessary code correction to the same worker once and revalidate; a repeated failure stops. The orchestrator does not implement the correction itself.
4. **Check the task diff** against the record from step 2, including new files. Each checkbox needs a diff, command result or observed behavior, and each change must serve the task. Criteria spanning several tasks are checked at closure. Send a gap to the same worker if the task's one correction has not been used in step 3; return to validation afterward. A remaining gap after that correction stops.
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

An entry-check failure stops with an explanation and leaves the ticket, code and index untouched. The updates below apply only after this run has claimed the ticket or started reconciled continuation work.

| What clears an in-run stop | Ticket update |
| --- | --- |
| A missing answer | Set `needs-info` and release the claim. |
| A human action, such as a migration, dependency install, credentials or an externally verified criterion | Set `ready-for-human`, release the claim and preserve already checked criteria. |
| A retry or correction, including a red suite | Keep `claimed`; the work is still unfinished. |

For an in-run stop, append a Comments line naming the task and what is needed. Preserve actual Decisions, Deviations and verification evidence. Never mark incomplete work resolved.

## NEXT

Ticket resolved -> `/dev:review` for the review gate over the whole branch, then `/dev:fix` to apply the saved findings. Neither starts on its own; the user types it. The next ticket is another `/dev:exec`.
