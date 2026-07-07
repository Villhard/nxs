# TDD MODE (reference)

Loaded on demand from `/nxs:exec` when the plan sets `Development approach: TDD`. The cycle is per behavior, not per task: one task / vertical slice = one or more short RED -> GREEN -> REFACTOR cycles. Common to default and auto modes.

## PER-BEHAVIOR STEPS

1. Choose exactly one behavior from the current vertical slice.
2. Write one failing test (or set up one failing verification) through the public interface / observable behavior.
3. Run the test and confirm **RED** - failure specifically due to the missing behavior, not a compile / setup / import / fixture error.
4. Write the minimal code to make exactly this test pass.
5. Run the test and confirm **GREEN**.
6. **REFACTOR** - only when all tests are green; do not change behavior, do not start a new RED in this phase.
7. Move on to the next behavior - a new RED.
8. After completing the slice (all its behaviors) - run the relevant verification via the `verify` skill.

## FORBIDDEN IN TDD MODE

- writing all tests at the start of the task and then implementing everything (a test-first dump, not TDD);
- holding several failing tests at once without an intermediate GREEN (no batched RED - between each RED there must be a GREEN);
- speculative implementation "will come in handy for future tests";
- refactor while RED;
- tests through private internals / private methods instead of the public interface;
- skipping the RED confirmation when RED is technically feasible.

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
