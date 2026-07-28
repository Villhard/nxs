---
description: The check-runner discipline - run the minimal relevant checks (tests / lint / format / typecheck / build) for a change, with TDD-loop verify behavior and its role in the exec commit gate - load before or after checking a code change (tests / lint / format / typecheck / build). Background knowledge, not a user command.
user-invocable: false
---

# VERIFY

Used by `/nxs:exec` (after every task) and `/nxs:review` (to check the diff).

## PROCEDURE

1. Inspect the project for a build / task manifest: `package.json` / `pyproject.toml` / `go.mod` / `Makefile` / `Cargo.toml`.
2. Find existing scripts: test, lint, format, typecheck, build.
3. Run only commands that exist in the project - its own scripts first, ad-hoc commands only where the project has none.
4. Format runs first, in apply mode, scoped to the files touched by the current task diff when the tool accepts file arguments (existing `format` script, prettier, ruff format, gofmt, black). Files outside the task diff stay untouched. Report whether it changed anything.
5. Lint runs in check mode only, without auto `--fix`, since lint fixes can change behavior. Failures go to the report; the orchestrator fixes them consciously.
6. Run only what permissions allow; mark anything without permission as skipped.
7. Keep heavy / long commands for when they are needed - a build on a unit-test change is overkill. Destructive operations (db migrate, deploy, prod-touching) stay out entirely.
8. Select the minimal command set by change type (table below).
9. Run the whole set even after a failure, then collect output, classify it, and return the report.

## MINIMAL COMMAND SET BY CHANGE TYPE

| change type | minimal set |
|---|---|
| typed languages (TS / Go / Rust) | format + lint + typecheck + tests |
| dynamic languages (Python / JS) | format + lint + tests |
| docs only | markdown lint if available |
| config only | validate config if a tool exists |
| migrations | tests + dry migration |

## OUTPUT FORMAT

"skipped", "not found", and "failed" mean different things and stay in separate lines.

```
commands run: <list>
commands skipped: <list + reason>
commands not found: <list + reason>
failures: <list with output>
follow-up needed: <list>
```

## TDD-LOOP VERIFY BEHAVIOR

When the plan fixes the TDD development approach, verify operates per-behavior within a slice rather than project-wide each time:

- RED - run exactly the new test (or a narrow group) expected to fail. Confirm the failure comes from the missing behavior, not from a compile / setup / import / fixture error. The full suite waits.
- GREEN - run the same test and confirm it passes, plus the relevant neighboring tests of the module to catch regressions from the minimal implementation.
- REFACTOR - run at minimum the tests of the affected module; behavior must not change. Runs only once the cycle is green.
- After a slice / task is finished - run the standard scope from the change-type table (format / lint / typecheck / module tests). Format and lint join at the slice / task level, not inside every RED -> GREEN cycle.

If RED cannot technically be confirmed (no infrastructure to run a single test, no runner for the required framework), note it in the report as `confirm RED skipped: <reason>`, leave the cycle unmarked as a full TDD, and hand the decision to the user.

## GATE ROLE

Verify is mandatory after every task in `/nxs:exec` and before any commit: a verify pass is a precondition of the commit gate, and a failure or a missing required check blocks the commit until the orchestrator fixes it and re-runs verify. The gate contract itself, and the rest of the cycle (task loop, review-fix loop, stop conditions), lives in `/nxs:exec`.
