---
description: Execute an implementation plan task by task and write the code. Use after a plan is ready and plan-reviewed; add "no commits" to skip git.
argument-hint: "[story path | plan path] [no commits]"
---

# /nxs:exec

Execute an existing implementation plan task by task, to the end. This is the one skill that changes project code, and it delegates every task to one write-capable `nxs:worker` subagent rather than writing code itself.

Example: /nxs:exec docs/nxs/stories/20260711-auth-refactor

## STANCE

- The plan is the source of truth: execute what it specifies, flip checkboxes as tasks complete, and keep the plan matching the work actually done.
- Minimal diff for the task, no speculative abstractions. Out-of-scope findings become follow-ups.
- One `nxs:worker` per task, sequential. Review subagents stay read-only.
- Commits are the orchestrator's. `git push` and MR / PR creation stay outside the run, on a later explicit request.
- A natural-language **no commits** instruction skips git and changes nothing else about the cycle.
- Archiving a finished story happens only on explicit user confirmation; `plan-conventions` says where it goes.

## RESOLVE THE PLAN

Plan to execute: the argument if given - a story directory resolves to its `plan.md` - otherwise the latest story under `docs/nxs/stories/` (not `completed/`) that contains a `plan.md`. None found, or the choice ambiguous -> ask.

Then read the plan's `## DEVELOPMENT APPROACH` section (see `plan-conventions`) and branch:

- `default` - the cycle below applies unchanged.
- `TDD` - the cycle runs per behavior, not per task: one task = one or more RED -> GREEN -> REFACTOR cycles (see TDD MODE).
- `tracer-bullet` / `spike` - semantics unchanged, follow the plan as is. For a spike, commit and clean up only on explicit user confirmation.
- Not recorded -> treat as `default` and suggest the user record it (a note, not a stop).

## PRECONDITIONS

Check before the first task; each failure is a stop condition below.

- clean worktree (with or without no-commit), unless the user approved a dirty start;
- plan present and valid;
- `/nxs:plancheck` run - if not, ask once and take the answer;
- `rg "NEEDS CLARIFICATION" <plan>` returns zero matches.

## THE CYCLE

For each remaining unchecked task:

1. Launch one `nxs:worker` with the task, its acceptance criteria, and the conventions set (see WORKER LAUNCH). Read back its structured result - files changed, follow-ups, notes - not raw tool output.
2. Update the plan checkboxes.
3. Run `verify` scoped to the task change (format first in apply mode, then lint / typecheck / tests) so review sees a formatted, lint-clean diff.
4. Review the task diff with `review`'s lenses - both on a task that changed logic, the orchestrator's direct pass on a trivial one - classified per `review-protocol`. On a BLOCK, fix and re-review the same scope until a zero-BLOCK round: a zero-BLOCK round, not "I fixed what was found". NIT findings are logged as follow-up and never gate the commit.
5. Compare the result against the plan's `## ACCEPTANCE CRITERIA`. AC not met is a stop condition. The task's Test cases are a mini-AC at the step level; the plan's AC is the global contract.
6. verify pass + zero-BLOCK round + AC met -> commit via `commit-conventions`; under no-commit, skip git. One green task is one commit - never one per layer the slice spans, never one per TDD micro-cycle; a capability is one logical change.
7. Next task.

Two guards prevent looping forever on one task:

- **review-fix cap** - at most 5 review rounds per task, since one task now carries a whole capability. Fifth round still returning a BLOCK -> stop, no commit, report the remaining finding. Rounds that make no progress are cut earlier by stalemate detection.
- **stalemate detection** - before each round of a repeated cycle (review-fix, TDD RED -> GREEN retries) capture a git fingerprint (`git rev-parse HEAD` plus a hash of `git diff`). Unchanged across 2 consecutive rounds -> stop and report "stalemate detected after 2 unchanged rounds".

## WORKER LAUNCH

- **launch** - the Agent / Task tool with a fresh `nxs:worker`; `prompt` = the task, its acceptance criteria, and the conventions set. A fresh subagent, not `subagent_type: "fork"` - a fork inherits the parent context and defeats the isolation.
- **conventions set** - the plan's `## CONVENTIONS` section plus what the orchestrator itself works under: project rules bearing on how code is written, and standing directives from this session. What is not passed does not reach the code. Assemble once per run, reuse verbatim for every task, and include only conventions the project actually stated.
- **single writer** - one worker at a time, calls sequential; only read roles run in parallel. The worker writes into the working directory, so `isolation: "worktree"` stays off.
- **HITL preserved** - the worker never commits, pushes, or runs destructive operations. The orchestrator runs verify / review and commits; the user reviews.

## EXECUTION DISCIPLINE

- **Stop on blockers.** On any stop condition, stop and inform the user rather than guessing.
- **Scope changes are explicit.** Needing changes beyond the task means updating the plan first. A refactor outside the task's scope becomes a separate task and commit.
  - **expanded-within-task** - the task is locked by its goal, not a fixed file list. Reaching past the initial file set is allowed where the locked task requires it, and is labeled in the diff report: `expanded-within-task: <file/symbol> - <why it was necessary>`.
  - **out-of-scope -> follow-up** - work noticed in unrelated, still-untouched code is recorded as `follow-up: <place> - <what> - out of scope` and left alone; emit the collected list at the end of the run. A review NIT is logged the same way. Unrelated files already changed in the diff are the separate case, and they stay a stop condition.
- **Simplicity first.** Complexity proportionate to the task, no abstraction or configurability ahead of need.
- **Phase handoff is a full stop.** Run the plan to the end and stop; the user decides what runs next.

## STOP CONDITIONS

- dirty worktree at start without explicit approval;
- missing plan, or an open `[NEEDS CLARIFICATION: ...]` marker in it;
- missing Files block in the task;
- unclear requirement;
- destructive operation, or dependency installation risk;
- a diff reaching well past the task's Files block and goal, or generated files - a large diff that matches the slice the task describes is expected, not a stop;
- unrelated files already changed in the diff (scope drift);
- verify failed, or required checks missing;
- AC not met after verify;
- security / data risk, or a reviewer blocker;
- merge conflict;
- review-fix cap exhausted with a BLOCK remaining, or stalemate detected;
- under TDD: batched RED tests without an intermediate GREEN, a missing test seam without a plan-approved fix in this task, or a refactor attempt during RED.

On any of these - stop and report to the user.

## TDD MODE

Active when `## DEVELOPMENT APPROACH` names TDD. Cycle discipline and anti-patterns: `plan-conventions` -> `reference/tdd.md`. Exec-specific detail:

- **checkbox granularity** - checked per completed cycle, not batched at the end.
- **missing test seam** - if the plan covers creating the seam in this task, create a minimally sufficient one and continue; otherwise stop and flag it as an architecture / testing limitation. Tests bind to the public interface even when private internals would be faster.
- **verify inside the loop** - within RED, verify may run a narrow target test to confirm the failure shape (see `verify`). Format and lint join at the task level, not inside every cycle.

## NEXT

Plan executed -> `/nxs:review` for a standalone review of the whole branch if you want one. Archive a finished story on your confirmation.
