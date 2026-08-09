---
description: Review the branch diff with five parallel agents, verify every finding against the code, fix what is confirmed, and commit. Use after /dev:exec finishes a plan, or on any branch you want reviewed.
argument-hint: "[scope: staged | path | PR url]"
disable-model-invocation: true
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

Round 1 launches five agents, all in one message so they run in parallel:

- `dev:review-quality` - bugs, edge cases, error handling, leaks, races, security skim;
- `dev:review-implementation` - goal reached, wiring, completeness, scope creep;
- `dev:review-testing` - coverage over the changed code, fake tests, test quality;
- `dev:review-simplification` - over-engineering this branch introduces;
- `dev:review-documentation` - docs the change needs or made stale, plan checkboxes.

Each prompt carries the base branch, the goal in one sentence, and the plan path when there is one. Do not paste the diff into a prompt - each agent fetches it itself, and an embedded diff makes the launch slow and expensive.

Round 2 and later launch `dev:review-quality` and `dev:review-implementation` only, told to report critical and major findings and skip the rest. A later round exists to catch what the fixes broke; re-running the full sweep pays five agents to re-read a diff that changed in three places.

Rounds are counted inside one invocation and nowhere else. Every `/dev:review` opens at round 1 with all five, whatever ran earlier in the session - a diff arriving for the first time gets the full sweep, and reviewing someone else's PR is always that case.

A trivial diff (dotfiles, docs only, pure formatting) does not need them: do one direct pass yourself against the same bar.

Wait for every agent of the round before doing anything else.

## VERIFY

The agents propose; you decide what is real.

1. **Merge duplicates.** Same place and same problem is one finding, whichever agents raised it.
2. **Check each one against the code.** Read the file at the reported line with 20-30 lines of context. Confirm the problem exists and is not already handled by a guard, a validation, or a test elsewhere. Confirmed - keep it. Anything else - discard, do not downgrade.
3. **Carry the severity of what you kept.** The agent assigned it; change it only when the code says otherwise, and say which way you moved it. This field decides whether another round runs, so a finding lowered to critical-free to end the pass early is the one thing you do not do.
4. **Rank what survived** by severity, worst first.

Discarding most candidates is a normal outcome. A pre-existing failure - a broken test, a lint error - is fixed too, not waved off because it predates the branch.

## FIX AND COMMIT

1. Launch one `dev:worker` with the confirmed findings as its unit of work: for each one the location, the issue, the impact, and the fix, plus the conventions the branch follows. Pass them verbatim - a finding you compress is a finding the worker has to derive again.
2. Read its structured result, then run the project's tests and linter yourself. All green before the commit.
3. Commit: `fix: address review findings`.

Another round runs only when this one confirmed a critical or major finding, because those are the fixes big enough to break something else. A round that confirmed only minors fixes them and ends the pass. Zero findings ends it too. Three rounds is the ceiling.

Report the outcome in plain text: what was found, what was fixed, what is left and why.

## STOP CONDITIONS

- a finding whose fix goes well past the branch's scope - report it as a follow-up, do not fix it;
- tests or linter that stay red after a reasonable attempt;
- a destructive operation, a migration, or a dependency install needed for a fix;
- an auth, payment, crypto, or migration diff - say plainly that it needs a manual security review beyond this pass.

On any of these - stop and tell the user.

## NEXT

Clean round - the branch is ready. `git push` and MR / PR creation happen only on your explicit request.
