---
description: Execute an implementation plan task by task and write the code - default runs one task per invocation then stops for the user to commit; auto runs all remaining low-risk tasks with verify + adaptive review + commit on each. Use after a plan is ready and ideally plan-reviewed to implement it; add "no commits" to skip git.
argument-hint: "[plan path] [auto] [no commits]"
---

# /nxs:dev-exec

Execute an existing implementation plan task by task. This is the one skill that changes project code - the orchestrator does not write it itself but delegates each task to one write-capable `nxs:worker` subagent. Explorer / reviewer subagents stay read-only. Self-contained skill. Output language and response style come from global rules, not this file.

## STANCE

- The plan is the source of truth: execute exactly what the plan specifies, update checkboxes as tasks complete, and add discovered notes back to the plan. When code and plan diverge, update the plan to reflect the work actually done.
- Minimal diff for the task, no speculative abstractions - choose the simplest solution that works. Out-of-scope findings become follow-ups, not edits.
- The orchestrator does not write code itself - it delegates each task to one `nxs:worker` subagent (single writer); review / explorer subagents stay read-only.
- Moving a plan to `docs/plans/completed/` happens only on explicit user confirmation, never automatically.

## RESOLVE THE PLAN

- Plan to execute: the argument path if given, otherwise the latest active plan under `docs/plans/`. If none is found or the choice is ambiguous, ask.
- Before starting, read the plan's **Development approach** (see `plan-conventions`) and branch on it:
  - `default` - ordinary implementation; the modes below apply unchanged.
  - `TDD` - switch to a per-behavior RED -> GREEN -> REFACTOR cycle (see `reference/tdd.md`).
  - `tracer-bullet` / `spike` - execution semantics do not change; follow the plan as is. For a spike, do not commit or cleanup without explicit user confirmation.
  - Not recorded -> treat as `default` and suggest the user clarify it in the plan (a note, not a stop).

## MODES

- **default** (no mode word) - one task per invocation; delegate the task to one `nxs:worker` subagent (single writer); review / explorer subagents read-only; verify; self-review the diff; AC check; then stop and propose a commit message. Does NOT run git add / commit / push.
- **auto** - a reserved mode word, explicit only, never inferred from context. Executes all remaining low-risk tasks with verify + adaptive review + commit on each.
- A natural-language **no commits** instruction in the invocation ("auto, no commits") skips only git add / commit / push and changes nothing else about the cycle.

### DEFAULT MODE

One invocation = one task:

1. Read the plan file.
2. Find the first unchecked task.
3. Delegate this task to one `nxs:worker` subagent (single writer); it implements the task and returns a structured result.
4. Subagents (explorer / reviewer) stay read-only.
5. Run the `verify` skill scoped to the task change (format first in apply mode, then lint / typecheck / tests) so review sees a formatted, lint-clean diff.
6. Self-review your own diff via adaptive review scoped to the task diff (the review lenses proportional to the change, not unconditionally the full set); report BLOCK / NIT.
7. Run AC verification (below), then stop. Review is already done - no separate `/nxs:dev-review` run is needed.
8. Report verify results and propose a commit message (see `commit-conventions` for the format).
9. Do NOT run git add. Do NOT run git commit. Do NOT run git push. Do NOT move the plan to completed. The user reviews and commits.

### AUTO MODE

Preconditions before starting auto:

- **clean worktree** - required (with or without no-commit); otherwise stop unless the user explicitly approved a dirty start.
- **plan-review recommended** - if `/nxs:dev-plan-review` was not run, ask once, do not insist twice.
- **plan present and valid**.
- **no open markers** - mechanical check `rg "NEEDS CLARIFICATION" <plan>` must return zero matches; an open marker is a stop condition.

Cycle for each remaining unchecked task:

1. Delegate the task to one `nxs:worker` subagent.
2. Update the plan (check the checkboxes).
3. Run the `verify` skill (tests / lint / format / typecheck / build as relevant).
4. Run adaptive review scoped to the task diff. On a BLOCK, fix it and re-review the same scope until a zero-BLOCK round (a zero-BLOCK round, not "I fixed what was found"). NIT findings are logged as follow-up and never gate the commit. Cap: 3 review rounds per task; cap exhausted with a BLOCK remaining -> stop, no commit, report.
5. Run AC verification (below). AC not met is a stop condition.
6. verify pass + zero-BLOCK review round + AC met -> commit via `commit-conventions` (a simple English message); under a no-commit instruction skip git add / commit / push instead.
7. Move to the next task.

Under no-commit, auto still executes the whole remaining low-risk plan, requires a clean worktree, and runs verify and adaptive review after each task - only git add / commit / push are skipped.

The full stop-condition list, the exhaustive "what auto never does" list, no-commit override, out-of-scope handling, and stalemate / cap detection are in `reference/auto.md`. Summary of stop conditions: dirty worktree without approval, unclear requirement, missing plan or Files block, open NEEDS CLARIFICATION marker, destructive operation, unexpected large diff, unrelated files already changed (scope drift), failing or missing checks, AC not met, security / data risk, reviewer blocker, merge conflict, dependency install risk, unexpectedly large generated files, 3-round review cap exhausted with a BLOCK, stalemate (unchanged git fingerprint for 2 rounds), and the TDD-specific violations. Summary of what auto NEVER does: push, create MR / PR, delete files outside the plan, modify unrelated files, bypass review, commit on failing checks, continue after a blocker, apply a NIT as a silent edit, force-push, run destructive shell without approval; under no-commit also no git add / commit.

## EXECUTION DISCIPLINE

- **The orchestrator delegates writing to a single `nxs:worker`; subagents read-only.** The orchestrator does not Edit or Write itself - it delegates writing to one `nxs:worker` subagent, one at a time; reviewer / explorer subagents never Edit or Write.
- **One task at a time in default mode.** One invocation = one task, then stop.
- **Stop on blockers.** On any stop condition, stop and inform the user rather than guessing or pushing through.
- **Do not expand scope silently.** If completing the task needs changes beyond it, update the plan explicitly - no silent "while I'm here" edits. A refactor outside the current task's scope becomes a separate task / commit, not mixed in. Trivial fixes on a line you already touch (a typo) are fine without ceremony.
  - **expanded-within-task label** - the task is locked by its goal, not a fixed file list. Touching a file or symbol beyond the task's initial set is allowed when necessary to complete the locked task, but must be labeled in the diff report: `expanded-within-task: <file/symbol> - <why it was necessary for the locked task>`. Mandatory for non-trivial expansion; work that does not serve the locked task is not "expanded-within-task", it is out of scope.
  - **out-of-scope -> follow-up (noticed only)** - when you only notice work in unrelated, still-untouched code (a bug, smell, refactor), do not edit it and do not stop; record `follow-up: <place> - <what> - out of scope` and continue. Emit the collected follow-up list at the end of the task. This applies in default and auto. It does NOT cover the case where the diff already contains changes to unrelated files - that stays a STOP condition.
- **Simplicity first.** The simplest solution that works; complexity proportionate to the task, no abstraction / flexibility / configurability ahead of need.
- **Phase handoff is a full stop.** dev-exec does not auto-call the next skill (no Skill tool, sub-prompt, or otherwise). Default mode does one task and stops; auto runs the plan to the end and stops. The user decides what runs next.
- **Plan is the source of truth.** Keep checkboxes and discovered notes current; if the plan is outdated, update it rather than ignore it.

## EXECUTION VIA WORKER (standing model)

The orchestrator never writes code itself. For every task - default and auto - it launches exactly one `nxs:worker` subagent (single-writer: one write-worker at a time; only read roles - reviewers, explorer - may run in parallel), passes the task plus its acceptance criteria, reads back the compressed structured result (not raw tool output), then runs the same verify / review / fix gate and AC check before the next task.

Launch is via the Agent / Task tool with a fresh `nxs:worker` subagent, prompt = task + AC; NOT a fork (a fork inherits the parent context). Calls are sequential (single-writer). The `nxs:worker` never commits, pushes, or runs destructive operations - the orchestrator runs verify / review and (in auto) commits; the user reviews. Full launch contract, single-writer, and context-isolation: `reference/worker-mode.md`.

## AC VERIFICATION

After verify (default or auto), compare what was achieved against the plan's `## ACCEPTANCE CRITERIA`:

- default mode - mention the result in the report; if AC are not met, suggest additional steps or adjust the plan.
- auto mode - AC not met is a stop condition: do not commit, stop, inform the user.

Each task's test cases are a mini-AC at the step level; the plan's AC is the global contract.

## TDD MODE

Active when the plan sets `Development approach: TDD`. The cycle is per behavior, not per task: one task / vertical slice = one or more short RED -> GREEN -> REFACTOR cycles. Choose one behavior, write one failing test through the public interface, confirm RED, write the minimal code to pass, confirm GREEN, refactor only while green. Checkboxes are checked per completed cycle, not batched at the end. Full cycle discipline, the forbidden list (batched RED, speculative implementation, refactor while RED, private-internals tests), missing-seam handling, and default-vs-auto TDD behavior: `reference/tdd.md`.

## REFERENCES

- `reference/auto.md` - full auto cycle, the exhaustive stop-condition and never-do lists, no-commit override, out-of-scope handling, plan-review interaction, cap and stalemate detection.
- `reference/tdd.md` - per-behavior RED -> GREEN -> REFACTOR discipline in execution, forbidden patterns, missing-seam handling, plan updates, default vs auto.
- `reference/worker-mode.md` - the standing worker execution model: the Claude Code launch contract, single-writer, and context-isolation.

Reference skills used by name: `verify` (after every task and before any commit), `commit-conventions` (before any git add / commit / push), `plan-conventions` (the Development approach and plan structure).

## NEXT

Default task done -> review the findings, commit, then run `/nxs:dev-exec` again for the next task, or `/nxs:dev-exec auto` for the rest. For a standalone code review -> `/nxs:dev-review`. To archive a finished plan (only on your confirmation) -> `/nxs:dev-cleanup`.
