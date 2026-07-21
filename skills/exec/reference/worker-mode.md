# WORKER EXECUTION (reference)

Loaded on demand from `/nxs:exec`. Worker delegation is the standing execution model of /nxs:exec: the orchestrator never writes code itself. For every task it launches one write-capable `nxs:worker` subagent at a time, reads the structured result, and runs the existing verify / review / fix gate before the next task. There is no non-worker path.

## INVARIANTS

- **single-writer** - at most one `nxs:worker` runs at a time; only read roles (explorer / reviewer) may run in parallel.
- **context-isolation** - the `nxs:worker` runs in a clean context and writes into the same working directory (not a worktree); the orchestrator gets back only a compressed structured result, not the worker's raw tool output. This buys clean context, not scope safety - scope drift stays bounded by the execution stop conditions, not by isolation.
- **HITL preserved** - the worker-loop is not autonomous; the orchestrator runs verify / review and the user reviews and commits. The `nxs:worker` never commits, pushes, or runs destructive operations.

## LAUNCH CONTRACT (Claude Code)

- **launch** - the Agent / Task tool with a fresh `nxs:worker` subagent; `prompt` = the task, its acceptance criteria, and the conventions set. NOT `subagent_type: "fork"` - a fork inherits the parent context, which defeats context-isolation.
- **conventions set** - the plan's `## CONVENTIONS` section plus the conventions the orchestrator is working under: project rules that bear on how code is written, and standing directives the user gave in this session. A clean context does not carry them, so what is not passed does not reach the code. Assemble the set once per run and reuse it verbatim for every task - do not re-derive it per task. Nothing to pass -> pass nothing; never invent conventions the project did not state.
- **result** - the agent's final message; the worker's tool output does not enter the orchestrator context. Read back file paths and a structured summary, not raw logs.
- **single-writer** - Agent calls are sequential. `isolation: "worktree"` is not needed under single-writer; the worker writes into the working directory.

## THE PER-TASK LOOP

For each task the orchestrator:

1. Launches one `nxs:worker` subagent with the task + AC + the conventions set (single-writer, sequential).
2. Reads back the structured result (files changed, follow-ups, notes) - not raw tool output.
3. Runs the same `verify` skill on the resulting diff.
4. Runs the same adaptive review scoped to the task diff, with the same BLOCK / NIT handling, 3-round cap, and stalemate detection as the rest of the skill.
5. Runs AC verification.
6. Commits (or, under no-commit, skips git) exactly as the exec gate specifies - the `nxs:worker` itself never commits.
7. Moves to the next task with a fresh `nxs:worker`.

The gate, stop conditions, and never-do lists are in `reference/auto.md`; this file only specifies who writes the code.
