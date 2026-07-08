# TDD MODE (reference)

Loaded on demand from `/nxs:exec` when the plan sets `Development approach: TDD`. The cycle is per behavior, not per task: one task / vertical slice = one or more short RED -> GREEN -> REFACTOR cycles. Common to default and auto modes. This file covers exec-specific TDD execution detail only; the RED -> GREEN -> REFACTOR cycle and anti-patterns canon live in `skills/plan-conventions/reference/tdd.md`, already loaded by exec by name.

## MISSING TEST SEAM

If the right test seam is absent:

- if the plan explicitly covers creating the seam in this task - create a minimally sufficient seam and continue;
- otherwise stop and explicitly flag it as an architecture / testing limitation; do not bind the test to private internals just to "get it done somehow". Leave the decision to the user.

In auto mode, a missing seam without a plan-approved fix in this task is a stop condition; a refactor attempt during RED is a stop condition.

## UPDATING THE PLAN IN TDD

- checkboxes are checked after each completed RED -> GREEN (and REFACTOR, if there was one) cycle, not batched at the end of the task;
- discovered notes (new behaviors, seam decisions, found limitations) are added to the plan as they appear.

## DEFAULT VS AUTO IN TDD

- **default mode** - one task per invocation; inside the task, as many RED -> GREEN cycles as the slice requires; after the task - stop, self-review the diff, wait for the user.
- **auto mode** - each task goes through the same cycle discipline; verify and adaptive review run after a completed task. Inside the RED phase, verify may run a narrow target test to confirm the failure shape (see the `verify` skill). Commit stays at the task level: one green task that passed verify and review = one commit, unless the plan states otherwise - do not split a commit per micro-cycle. Repeated RED -> GREEN retries fall under stalemate detection (see `reference/auto.md`).
