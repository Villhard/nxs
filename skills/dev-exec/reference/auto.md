# AUTO MODE (reference)

Loaded on demand from `/nxs:dev-exec` when running `auto`. Carries the complete auto cycle, the exhaustive stop-condition and never-do lists, the no-commit override, out-of-scope handling, and cap / stalemate detection. `auto` is a reserved mode word and is never inferred from context.

## PRECONDITIONS

Before starting auto:

- **clean worktree** - required for auto (with or without the no-commit instruction); otherwise stop unless the user explicitly approved a dirty start.
- **plan-review recommended** - if `/nxs:dev-plan-review` was not run, ask once and do not insist twice.
- **plan present and valid** - without a plan it cannot proceed.
- **no open markers** - `rg "NEEDS CLARIFICATION" <plan>` must return zero matches; an open marker is a stop condition.

## AUTO CYCLE

For each remaining unchecked task:

1. Edit code in the main context (worker mode: one `nxs:worker` subagent).
2. Update the plan (check the checkboxes).
3. Run the `verify` skill (tests / lint / format / typecheck / build as relevant).
4. Run adaptive review scoped to the task diff (the review lenses proportional to the change, not unconditionally the full set). On a BLOCK, fix it and re-review the same scope. The loop exits only on a zero-BLOCK round, not "I fixed what was found". NIT findings are logged as follow-up and never gate the commit. Cap: 3 review rounds per task; cap exhausted with a BLOCK remaining -> stop, no commit, report.
5. Run AC verification against the plan's `## ACCEPTANCE CRITERIA`. AC not met is a stop condition.
6. verify pass + zero-BLOCK review round + AC met -> commit via `commit-conventions` with a simple English message; under a no-commit instruction skip git add / commit / push instead.
7. Move to the next task.

Before each round of a repeated cycle (the review-fix loop above, RED -> GREEN retries in TDD), capture a git state fingerprint (`git rev-parse HEAD` plus a hash of `git diff`) for stalemate detection (below).

## COMMIT ALLOWED ONLY AFTER CHECKS

Auto commit:

- only after a successful verify;
- only after a zero-BLOCK review round - "BLOCK fixed" is not "review passed"; a NIT never gates;
- commit message - simple English (see `commit-conventions`);
- do NOT run `git push`;
- do NOT create MR / PR.

## NO-COMMIT OVERRIDE

Under a no-commit instruction ("auto, no commits"):

- do NOT run `git add`;
- do NOT run `git commit`;
- do NOT run `git push`;
- after a successful verify + zero-BLOCK review round, move to the next task.

Everything else in the auto cycle is unchanged: auto still executes the whole remaining low-risk plan, requires a clean worktree, and runs verify and adaptive review after each task.

## STOP CONDITIONS (full list)

- dirty worktree at start without explicit approval;
- unclear requirement;
- missing plan;
- open `[NEEDS CLARIFICATION: ...]` marker in the plan;
- missing Files block in the task;
- destructive operation;
- unexpected large diff;
- unrelated files already changed in the diff (scope drift) - noticed-but-untouched out-of-scope is logged as follow-up instead, not a stop;
- failing checks (verify failed);
- missing required checks;
- AC from the plan not met after verify;
- security / data risk;
- reviewer blocker;
- merge conflict;
- dependency installation risk;
- unexpectedly large generated files;
- review-fix cap (3 rounds) exhausted with findings remaining;
- stalemate: git state fingerprint unchanged for 2 consecutive rounds of a repeated cycle (review-fix, TDD RED -> GREEN retries) - stop with an explicit "stalemate detected after 2 unchanged rounds" report, never a silent continue;
- TDD plan: batched RED tests without an intermediate GREEN;
- TDD plan: missing test seam without a plan-approved fix in this task;
- TDD plan: refactor attempt during RED.

On any of these - stop and report to the user.

## OUT-OF-SCOPE -> FOLLOW-UP

Auto follows the noticed-only follow-up rule from execution discipline (DO NOT EXPAND SCOPE SILENTLY):

- work only noticed in unrelated, still-untouched code -> log `follow-up: <place> - <what> - out of scope` and keep running; emit the list at the end of the run;
- a review NIT that the zero-BLOCK gate does not require fixing -> log `follow-up: <file> - <nit> - review NIT` and keep running; a NIT is never a silent edit inside an auto-task;
- unrelated files already changed in the diff (scope drift) -> stays a STOP condition above;
- follow-up is a recorded note, never an edit - modifying unrelated files stays forbidden below.

## WHAT AUTO NEVER DOES

- `git push`;
- create MR / PR;
- delete files outside the plan;
- modify unrelated files;
- bypass review;
- commit if checks fail;
- continue after a blocker;
- apply a reviewer NIT as a silent edit inside an auto-task;
- `git push --force`;
- destructive shell without explicit approval;
- under a no-commit instruction: `git add` / `git commit`.

## SUBAGENTS READ-ONLY

In auto mode subagents stay read-only. Code edits happen only in the main context - or, under worker mode, in a single `nxs:worker` subagent one at a time (see `reference/worker-mode.md`).

## CAP AND STALEMATE DETECTION

Two guards prevent an auto run from looping forever on the same task:

- **review-fix cap** - at most 3 review rounds per task. If the third round still returns a BLOCK, stop with no commit and report the remaining finding.
- **stalemate detection** - before each round of a repeated cycle, capture the git fingerprint (`git rev-parse HEAD` + hash of `git diff`). If it is unchanged across 2 consecutive rounds, the cycle is making no progress - stop with an explicit stalemate report instead of continuing silently.

## INTERACTION WITH PLAN-REVIEW

If plan-review was not run before auto, ask once:

> "Plan-review was not run. Run /nxs:dev-plan-review before auto mode or continue without it?"

Do not insist twice.
