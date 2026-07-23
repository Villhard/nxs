---
description: The check-runner discipline - run the minimal relevant checks (tests / lint / format / typecheck / build) for a change, with TDD-loop verify behavior and its role in the exec commit gate - load before or after checking a code change (tests / lint / format / typecheck / build). Background knowledge, not a user command.
user-invocable: false
---

# VERIFY

Load before or after checking a code change. Workflow knowledge, not a user-invocable command. Used by `/nxs:exec` (after every task) and `/nxs:review` (to check the diff).

## PROCEDURE

1. Inspect the project for a build / task manifest: `package.json` / `pyproject.toml` / `go.mod` / `Makefile` / `Cargo.toml`.
2. Find existing scripts: test, lint, format, typecheck, build.
3. Prefer the project's scripts over ad-hoc commands.
4. Format runs first, in apply mode, scoped to the files touched by the current task diff when the tool accepts file arguments (existing `format` script, prettier, ruff format, gofmt, black). Never format files outside the task diff - no drive-by formatting. Report whether it changed anything.
5. Lint runs in check mode only - no auto `--fix` (lint fixes can change behavior). Failures go to the report; the main context fixes them consciously.
6. Run only what permissions allow; mark anything without permission as skipped.
7. Do not run heavy / long commands without need (a build on a unit-test change is overkill).
8. Select the minimal command set by change type (table below).
9. Collect output, classify it, return the report.

## MINIMAL COMMAND SET BY CHANGE TYPE

| change type | minimal set |
|---|---|
| typed languages (TS / Go / Rust) | format + lint + typecheck + tests |
| dynamic languages (Python / JS) | format + lint + tests |
| docs only | markdown lint if available |
| config only | validate config if a tool exists |
| migrations | tests + dry migration |

## OUTPUT FORMAT

```
commands run: <list>
commands skipped: <list + reason>
commands not found: <list + reason>
failures: <list with output>
follow-up needed: <list>
```

## RULES

- Do not invent commands - use only what exists in the project.
- Do not run destructive operations (db migrate, deploy, prod-touching).
- Distinguish "skipped", "not found", and "failed" - they mean different things.
- Do not abort on the first failure - continue with the rest and collect a summary.

## TDD-LOOP VERIFY BEHAVIOR

When the plan fixes the TDD development approach, verify operates per-behavior within a slice, not project-wide each time:

- RED - run exactly the new test (or a narrow group) expected to fail. Confirm the failure comes from the missing behavior, not from a compile / setup / import / fixture error. Do not run the full suite in this phase.
- GREEN - run the same test and confirm it passes. Additionally run the relevant neighboring tests of the module to catch regressions from the minimal implementation.
- REFACTOR - run at minimum the tests of the affected module; behavior must not change. Never runs while the cycle is in RED.
- After a slice / task is finished - run the standard scope from the change-type table (format / lint / typecheck / module tests), not a project-wide build every cycle. Format and lint join at the slice / task level, not inside every RED -> GREEN cycle.

If RED cannot technically be confirmed (no infrastructure to run a single test, no runner for the required framework), note it in the report as `confirm RED skipped: <reason>` and do not mark the cycle as a full TDD; hand the decision to the user.

## GATE ROLE

Verify is mandatory after every task in `/nxs:exec` and before any commit. A verify pass is a precondition of the commit gate; the gate contract itself is owned by `/nxs:exec`. Verify failing, or required checks missing, blocks the commit - the main context fixes the failure and re-runs verify before proceeding. The rest of the cycle (task loop, review-fix loop, stop conditions) lives in `/nxs:exec`.
