---
description: Execute an implementation plan task by task and write the code, committing each finished task. Use after a plan is ready; add "no commits" to skip git.
argument-hint: "[story path | plan path] [no commits]"
---

# /nxs:exec

Execute a plan to the end, one task per cycle. This is the one command that changes project code, and it delegates every task to a `nxs:worker` subagent rather than writing code itself.

Example: /nxs:exec docs/nxs/stories/20260711-auth-refactor

## RESOLVE THE PLAN

The argument if given - a story directory resolves to its `plan.md` - otherwise the latest story under `docs/nxs/stories/` (not `completed/`) that holds a `plan.md`. None found, or the choice ambiguous - ask.

Before the first task: the worktree is clean unless the user approved a dirty start, the plan exists, and `rg "NEEDS CLARIFICATION" <plan>` returns nothing.

## THE CYCLE

Repeat until no `- [ ]` is left:

1. **Pick the task** - the first `### Task N:` section with open checkboxes. One section per cycle, all of its checkboxes, then move on.
2. **Delegate** - launch one `nxs:worker` with the task text, the plan's `## Conventions` section, the project rules bearing on how code is written, and any standing directive from this session. Assemble that set once and reuse it verbatim. What is not passed does not reach the code. Use a fresh subagent, never `subagent_type: "fork"` - a fork inherits this context and defeats the isolation.
3. **Validate** - run the test and lint commands the task names. Fix failures and re-run until green.
4. **Flip the checkboxes** to `- [x]`.
5. **Commit** the code and the plan together, one commit per task: `<type>(<scope>): <subject>`. Under **no commits**, skip this step and change nothing else.
6. Next task.

One worker at a time, sequentially. The worker writes into the working directory, so `isolation: "worktree"` stays off. Read its structured result - files changed, follow-ups, blockers - not raw tool output.

## DISCIPLINE

- **Minimal diff.** Complexity proportionate to the task, no abstraction or configurability ahead of need.
- **The task is locked by its goal, not by its Files list.** Reaching past that list to finish the same capability is fine - label it in the report as `expanded-within-task: <file> - <why>`.
- **Out of scope stays out.** Work noticed in unrelated code is recorded as `follow-up: <place> - <what>` and left alone. Emit the collected list at the end of the run.
- **A real scope change updates the plan first.** A refactor outside the task becomes its own task and its own commit.
- **The run ends with the plan.** `git push` and MR / PR creation stay outside it, on a later explicit request.

## COMMIT FORMAT

```
<type>(<scope>): <subject>
```

Single line, no body. Subject fully lowercase, including abbreviations. Types: `feat`, `fix`, `refactor`, `chore`, `docs`. Plain simple verbs - add, fix, remove, update, show, hide, validate - never tighten, streamline, leverage, harden.

Stage the task's files by name, never `git add -A`. Check the staged diff before committing. Never `--force`, never `--no-verify` without explicit approval, never amend a published commit.

## STOP CONDITIONS

- dirty worktree at start without explicit approval;
- missing plan, or an open `[NEEDS CLARIFICATION: ...]` marker in it;
- tests or linter still failing after a reasonable attempt;
- a destructive operation, a migration, or a dependency install;
- a diff reaching well past the task's goal, or unrelated files already changed;
- a secret, a credential, or a large generated artifact in the diff;
- an unclear requirement, or a merge conflict.

On any of these - stop and tell the user rather than guessing.

## NEXT

Plan executed -> `/nxs:review` for the review gate over the whole branch.
