---
description: Review the branch diff with five parallel agents, verify every finding against the code, fix what is confirmed, and commit. Use after /dev:exec finishes a plan, or on any branch you want reviewed.
argument-hint: "[scope: staged | path | PR url]"
---

# /dev:review

Review a diff, fix what is really wrong, and commit the fixes. This is the review gate for a whole plan, not for a single task.

Example: /dev:review

## RESOLVE THE SCOPE

- an explicit selector - `staged`, a file path, or a PR / MR URL - is used as given;
- no selector - the current branch against its base. Detect the base explicitly: `origin/HEAD`, else whichever of `main` / `master` exists;
- no selector and a mixed state (commits ahead of base plus uncommitted changes) - ask once which scope to review, before launching anything.

Then read the context yourself:

```
git log <base>..HEAD --oneline
git diff <base>...HEAD
```

## LAUNCH THE AGENTS

Five agents, all in one message so they run in parallel:

- `dev:review-quality` - bugs, edge cases, error handling, leaks, races, security skim;
- `dev:review-implementation` - goal reached, wiring, completeness, scope creep;
- `dev:review-testing` - coverage over the changed code, fake tests, test quality;
- `dev:review-simplification` - over-engineering this branch introduces;
- `dev:review-documentation` - docs the change needs or made stale, plan checkboxes.

Each prompt carries the base branch, the goal in one sentence, and the plan path when there is one. Do not paste the diff into a prompt - each agent fetches it itself, and an embedded diff makes the launch slow and expensive.

A trivial diff (dotfiles, docs only, pure formatting) does not need them: do one direct pass yourself against the same bar.

Wait for all five before doing anything else.

## VERIFY

The agents propose; you decide what is real.

1. **Merge duplicates.** Same place and same problem is one finding, whichever agents raised it.
2. **Check each one against the code.** Read the file at the reported line with 20-30 lines of context. Confirm the problem exists and is not already handled by a guard, a validation, or a test elsewhere. Confirmed - keep it. Anything else - discard, do not downgrade.
3. **Rank what survived** by consequence, worst first.

Discarding most candidates is a normal outcome. A pre-existing failure - a broken test, a lint error - is fixed too, not waved off because it predates the branch.

## FIX AND COMMIT

1. Fix every confirmed finding.
2. Run the project's tests and linter. All green before the commit.
3. Commit: `fix: address review findings`.

Fixed something - run another round, because the fixes can introduce new problems. Zero findings in a round - done. After three rounds, stop and report what is left.

Report the outcome in plain text: what was found, what was fixed, what is left and why.

## STOP CONDITIONS

- a finding whose fix goes well past the branch's scope - report it as a follow-up, do not fix it;
- tests or linter that stay red after a reasonable attempt;
- a destructive operation, a migration, or a dependency install needed for a fix;
- an auth, payment, crypto, or migration diff - say plainly that it needs a manual security review beyond this pass.

On any of these - stop and tell the user.

## NEXT

Clean round - the branch is ready. `git push` and MR / PR creation happen only on your explicit request.
