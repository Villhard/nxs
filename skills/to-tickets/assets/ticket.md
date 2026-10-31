# <NN>: <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list>

**Blocked by:** <the numbers and titles of the tickets that gate this one, or "None (can start immediately)">

**Branch:** <optional: the branch this work goes on; drop the line when there is none>

**Status:** ready-for-agent

- [ ] <acceptance criterion>
- [ ] <acceptance criterion>

## Done when

Execute this ticket directly, for example with `/plan <this file>`.

- Resolve the feature directory from this ticket and use its `decision.log` in standalone and controlled execution. Append concise JSONL events for decisions, questions, answers, completion, blockers and handoff, with unique IDs and artifact/evidence paths; use the task skill's bundled `scripts/journal.py` when available, otherwise append under a system file lock. Never log secrets or full conversations. A branch alone never selects a different journal. Read existing entries and reconcile them with artifacts and actual Git state before continuing; never replay an uncertain side effect.
- Only an explicit controlled-run packet with step/run IDs, approved feature plan and hash, approval reference, cwd, permissions, allowed writes, acceptance checks, result schema and journal path activates lead control. In that context, save the proposed ticket plan and return `needs_input` to lead before implementation; resume the saved session only after recorded lead approval. Return `done`, `needs_input` or `blocked` with evidence in the supplied envelope. Keep ordinary dialogue and human plan approval outside that context. A packet carries existing authorization, never new consent; scope, external-contract or agreed-decision changes return through lead to the user.

- Stop and ask if **Status** is not `ready-for-agent`, a ticket in **Blocked by** is not `resolved`, or this ticket or its feature's `spec.md` / `root-cause.md` has an open `[NEEDS CLARIFICATION: ...]`.
- If **Branch** is set, work on that branch: switch to it, or create it from the current HEAD when missing. Stop and ask if the switch fails.
- Before the first implementation edit, read each ticket in **Blocked by** and verify, by code inspection and a focused check, that the results this ticket needs exist in the current working tree; **Status**, branch names and Git history alone do not suffice. If every result is present, record the evidence in one line under `## Comments`. If a result is absent or unverifiable, record the missing prerequisite in one line under `## Comments` and stop; never merge, cherry-pick or implement the blocker.
- If a required migration, dependency install or external check is undone or unverifiable, set **Status** to `ready-for-human`, record under `## Comments` the action needed and the evidence you expect, and stop. The human completes it, sets **Status** back to `ready-for-agent` and reruns `/plan`. On that rerun, verify the recorded result by checkable evidence in the current environment; a `done` line under `## Comments` alone is not evidence, and never perform the step yourself. In a controlled run only, an approved feature plan naming the action and exact target authorizes the executor to perform and verify it; an unnamed action follows this ready-for-human path. If it is still undone or unverifiable, set `ready-for-human` again and stop.
- Close when the project's full test suite and linter pass and every criterion above is verified against the running code: check each one and set **Status** to `resolved`.
- Add one line under `## Comments` per decision or deviation.
- Do not commit. Journal the verified completion or pending handoff; lead independently checks evidence before accepting a controlled `done`.
