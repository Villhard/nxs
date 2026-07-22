---
description: Execute an implementation plan task by task and write the code - runs the plan to the end, with verify, review, and a commit after each task. Use after a plan is ready and plan-reviewed; add "no commits" to skip git.
argument-hint: "[plan path] [no commits]"
---

# /nxs:exec

Execute an existing implementation plan task by task, running the plan to the end. This is the one skill that changes project code - the orchestrator does not write it itself but delegates each task to one write-capable `nxs:worker` subagent. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:exec docs/nxs/plans/20260711-auth-refactor.md

## STANCE

- The plan is the source of truth: execute exactly what it specifies, update checkboxes as tasks complete, and add discovered notes back to the plan. When code and plan diverge, update the plan to reflect the work actually done.
- Minimal diff for the task, no speculative abstractions - the simplest solution that works. Out-of-scope findings become follow-ups, not edits.
- The orchestrator does not write code itself. For every task it launches exactly one `nxs:worker` subagent (single writer, sequential); reviewer subagents stay read-only.
- A natural-language **no commits** instruction skips git and changes nothing else about the cycle.
- Moving a plan to `docs/nxs/plans/completed/` happens only on explicit user confirmation, never automatically.

## RESOLVE THE PLAN

- Plan to execute: the argument path if given, otherwise the latest active plan under `docs/nxs/plans/`. If none is found or the choice is ambiguous, ask.
- Read the plan's `## DEVELOPMENT APPROACH` section (see `plan-conventions`) and branch on it:
  - `default` - ordinary implementation; the cycle below applies unchanged.
  - `TDD` - the cycle is per behavior, not per task: one task = one or more short RED -> GREEN -> REFACTOR cycles (see TDD MODE below).
  - `tracer-bullet` / `spike` - execution semantics do not change; follow the plan as is. For a spike, do not commit or clean up without explicit user confirmation.
  - Not recorded -> treat as `default` and suggest the user clarify it in the plan (a note, not a stop).

## PRECONDITIONS

- **clean worktree** - required (with or without no-commit); otherwise stop unless the user explicitly approved a dirty start.
- **plan present and valid**.
- **plan-review recommended** - if `/nxs:plancheck` was not run, ask once, do not insist twice.
- **no open markers** - `rg "NEEDS CLARIFICATION" <plan>` must return zero matches; an open marker is a stop condition.

## THE CYCLE

For each remaining unchecked task:

1. Launch one `nxs:worker` subagent with the task, its acceptance criteria, and the conventions set (see WORKER LAUNCH). Read back its structured result - files changed, follow-ups, notes - not raw tool output.
2. Update the plan (check the checkboxes).
3. Run the `verify` skill scoped to the task change (format first in apply mode, then lint / typecheck / tests) so review sees a formatted, lint-clean diff.
4. Review the task diff with `review`'s adaptive lens set (the lenses proportional to the change, not the full set) and `review-protocol`'s BLOCK / NIT classification. On a BLOCK, fix it and re-review the same scope until a zero-BLOCK round - a zero-BLOCK round, not "I fixed what was found". NIT findings are logged as follow-up and never gate the commit.
5. Run AC verification against the plan's `## ACCEPTANCE CRITERIA`. AC not met is a stop condition.
6. verify pass + zero-BLOCK review round + AC met -> commit via `commit-conventions`; under no-commit, skip git instead.
7. Move to the next task.

Two guards prevent looping forever on one task:

- **review-fix cap** - at most 3 review rounds per task. Third round still returning a BLOCK -> stop, no commit, report the remaining finding.
- **stalemate detection** - before each round of a repeated cycle (review-fix, TDD RED -> GREEN retries) capture a git fingerprint (`git rev-parse HEAD` plus a hash of `git diff`). Unchanged across 2 consecutive rounds -> stop with an explicit "stalemate detected after 2 unchanged rounds" report, never a silent continue.

## WORKER LAUNCH

- **launch** - the Agent / Task tool with a fresh `nxs:worker` subagent; `prompt` = the task, its acceptance criteria, and the conventions set. NOT `subagent_type: "fork"` - a fork inherits the parent context, which defeats context isolation.
- **conventions set** - the plan's `## CONVENTIONS` section plus the conventions the orchestrator is working under: project rules that bear on how code is written, and standing directives the user gave in this session. A clean context does not carry them, so what is not passed does not reach the code. Assemble the set once per run and reuse it verbatim for every task. Nothing to pass -> pass nothing; never invent conventions the project did not state.
- **single writer** - at most one worker runs at a time; calls are sequential. Only read roles may run in parallel. `isolation: "worktree"` is not needed - the worker writes into the working directory.
- **HITL preserved** - the worker never commits, pushes, or runs destructive operations. The orchestrator runs verify / review and commits; the user reviews.

## EXECUTION DISCIPLINE

- **Stop on blockers.** On any stop condition, stop and inform the user rather than guessing or pushing through.
- **Do not expand scope silently.** If completing the task needs changes beyond it, update the plan explicitly - no silent "while I'm here" edits. A refactor outside the current task's scope becomes a separate task / commit.
  - **expanded-within-task** - the task is locked by its goal, not a fixed file list. Touching a file or symbol beyond the task's initial set is allowed when necessary to complete the locked task, but must be labeled in the diff report: `expanded-within-task: <file/symbol> - <why it was necessary>`. Work that does not serve the locked task is not expansion, it is out of scope.
  - **out-of-scope -> follow-up** - when you only notice work in unrelated, still-untouched code, do not edit it and do not stop; record `follow-up: <place> - <what> - out of scope` and continue. Emit the collected list at the end of the run. A review NIT the zero-BLOCK gate does not require is logged the same way, never applied as a silent edit. This does NOT cover unrelated files already changed in the diff - that stays a stop condition.
- **Simplicity first.** Complexity proportionate to the task, no abstraction or configurability ahead of need.
- **Phase handoff is a full stop.** The orchestrator does not auto-call the next skill. It runs the plan to the end and stops; the user decides what runs next.

## STOP CONDITIONS

- dirty worktree at start without explicit approval;
- missing plan, or an open `[NEEDS CLARIFICATION: ...]` marker in it;
- missing Files block in the task;
- unclear requirement;
- destructive operation, or dependency installation risk;
- unexpectedly large diff or generated files;
- unrelated files already changed in the diff (scope drift);
- verify failed, or required checks missing;
- AC not met after verify;
- security / data risk, or a reviewer blocker;
- merge conflict;
- review-fix cap exhausted with a BLOCK remaining, or stalemate detected;
- under TDD: batched RED tests without an intermediate GREEN, a missing test seam without a plan-approved fix in this task, or a refactor attempt during RED.

On any of these - stop and report to the user.

## WHAT EXEC NEVER DOES

- `git push` (with or without force), or create an MR / PR;
- delete files outside the plan, or modify unrelated files;
- bypass review, or commit when checks fail;
- continue after a blocker;
- run destructive shell without explicit approval;
- under no-commit: `git add` / `git commit`.

## AC VERIFICATION

After verify, compare what was achieved against the plan's `## ACCEPTANCE CRITERIA`. AC not met is a stop condition: do not commit, stop, inform the user. Each task's test cases are a mini-AC at the step level; the plan's AC is the global contract.

## TDD MODE

Active when the plan's `## DEVELOPMENT APPROACH` section names TDD. Choose one behavior, write one failing test through the public interface, confirm RED, write the minimal code to pass, confirm GREEN, refactor only while green. Checkboxes are checked per completed cycle, not batched at the end. Full cycle discipline and anti-patterns: `plan-conventions` -> `reference/tdd.md`.

Exec-specific detail:

- **missing test seam** - if the plan explicitly covers creating the seam in this task, create a minimally sufficient one and continue; otherwise stop and flag it as an architecture / testing limitation. Never bind a test to private internals just to get it done.
- **verify inside the loop** - within RED, verify may run a narrow target test to confirm the failure shape (see the `verify` skill). Format and lint join at the task level, not inside every cycle.
- **commit granularity** - one green task that passed verify and review = one commit; do not split a commit per micro-cycle.

## REFERENCE SKILLS

`verify` (after every task and before any commit), `review` (the adaptive lens set the review step applies to the task diff), `review-protocol` (the BLOCK / NIT classification), `commit-conventions` (before any git write), `plan-conventions` (the plan structure and development approach).

## NEXT

Plan executed -> `/nxs:review` for a standalone review of the whole branch if you want one. Archive a finished plan by moving it to `docs/nxs/plans/completed/` on your confirmation.
