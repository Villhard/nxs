---
description: Review a diff with five parallel agents, verify every finding against the code, and report it. Add "fix" to apply the confirmed findings. Use after /dev:exec finishes a plan, or on any branch you want reviewed, including one you pulled from someone else's PR.
argument-hint: "[scope: staged | path] [fix]"
disable-model-invocation: true
---

# /dev:review

Review a diff and report what is really wrong. This is the review gate for a whole plan, not for a single task.

Example: /dev:review
Example: /dev:review fix

## STANCE

- **Reporting is the whole command.** Nothing is edited, staged, or committed. A review of someone else's PR is the normal case, and it must never touch their branch.
- **`fix` in the arguments opts into changing code**, and only then. It applies the confirmed findings, commits them, and re-checks its own work.
- Without `fix`, the run ends at the report even when every finding is trivial and obvious. Offer to fix; do not fix.

## RESOLVE THE SCOPE

The word `fix` anywhere in the arguments turns on fix mode; its absence is report mode. Say which mode you are in before launching anything, so a run that will write is never a surprise.

Resolving the scope produces exactly two commands, a history command and a diff command. Everything downstream runs those two and nothing else - your own read of the context, and every agent you launch.

- no selector - the current branch against its base. Detect the base explicitly: `origin/HEAD`, else whichever of `main` / `master` exists. Then `git log <base>..HEAD --oneline` and `git diff <base>...HEAD`;
- `staged` - what is staged against the last commit: `git log -1 --oneline` and `git diff --staged`;
- a file path - the branch scope narrowed to it: the same two commands with `-- <path>` appended;
- no selector and a mixed state (commits ahead of base plus uncommitted changes) - ask once which scope to review, before launching anything.

Someone else's branch is reviewed by checking it out and running with no selector; there is no PR URL selector, and inventing one from a URL in the arguments is not a substitute.

Read the context yourself with the two resolved commands before launching anything.

## LAUNCH THE AGENTS

**The sweep** launches five agents, all in one message so they run in parallel:

- `dev:review-quality` - bugs, edge cases, error handling, leaks, races, security skim;
- `dev:review-implementation` - goal reached, wiring, completeness, scope creep;
- `dev:review-testing` - coverage over the changed code, fake tests, test quality;
- `dev:review-simplification` - over-engineering this branch introduces;
- `dev:review-documentation` - docs the change needs or made stale, plan checkboxes.

Each prompt carries the two resolved scope commands verbatim, plus the goal in one sentence and the plan path when the work has them. Do not paste the diff into a prompt - each agent runs the commands itself, and an embedded diff makes the launch slow and expensive. An agent given no commands falls back to the whole branch, which is the wrong answer for every selector, so the commands are not optional.

The goal comes from the plan, or from what the user said when they invoked this. With neither - a branch handed to you, whose intent nobody stated - put `no stated goal` in the prompt and pass nothing more. Never manufacture one from commit messages, the branch name, or the diff: an invented goal becomes a requirement the reviewer holds the code to, and findings against a requirement nobody set are worse than no findings.

**The re-check** launches `dev:review-quality` and `dev:review-implementation` only, told to report critical and major findings and skip the rest. It exists to answer one question - did the fixes break something - so it runs in fix mode and nowhere else, after fixes landed in this same run. Re-running the full sweep there would pay five agents to re-read a diff that changed in three places.

A diff nobody has fixed yet never gets a re-check. Report mode is one sweep and no more; a branch pulled from someone else's PR is always that case.

A trivial diff (dotfiles, docs only, pure formatting) does not need agents: do one direct pass yourself against the same bar.

Wait for every agent you launched before doing anything else.

## VERIFY

The agents propose; you decide what is real.

1. **Merge duplicates.** Same place and same problem is one finding, whichever agents raised it.
2. **Check each one against the code.** Read the file at the reported line with 20-30 lines of context. Confirm the problem exists and is not already handled by a guard, a validation, or a test elsewhere. Confirmed - keep it. Anything else - discard, do not downgrade.
3. **Carry the severity of what you kept.** The agent assigned it; change it only when the code says otherwise, and say which way you moved it. In fix mode this field decides whether a re-check runs, so a finding lowered to end the pass early is the one thing you do not do.
4. **Rank what survived** by severity, worst first.

Discarding most candidates is a normal outcome. A pre-existing failure - a broken test, a lint error - is reported like anything else, not waved off because it predates the branch.

## REPORT

Plain text, worst first: location, severity, what is wrong, what it costs, what to change. Say what the agents raised and you discarded, in one line, so a dismissed finding stays visible.

In report mode this ends the run. Offer to fix and stop there - `/dev:review fix` is the user's call, not yours.

## FIX

Fix mode only. Everything below is skipped without it.

1. Launch one `dev:worker` with the confirmed findings as its unit of work: for each one the location, the issue, the impact, and the fix, plus the conventions the branch follows. Pass them verbatim - a finding you compress is a finding the worker has to derive again.
2. Read its structured result, then run the project's tests and linter yourself. All green before the commit.
3. Commit: `fix: address review findings`.
4. A re-check runs only when this pass confirmed a critical or major finding, because those are the fixes big enough to break something else. A pass that confirmed only minors fixes them and ends the run. Three re-checks is the ceiling.

Report the outcome the same way: what was found, what was fixed, what is left and why.

## STOP CONDITIONS

- a finding whose fix goes well past the branch's scope - report it as a follow-up, do not fix it;
- tests or linter that stay red after a reasonable attempt;
- a destructive operation, a migration, or a dependency install needed for a fix;
- an auth, payment, crypto, or migration diff - say plainly that it needs a manual security review beyond this pass;
- fix mode over work the user did not write, a branch pulled from someone else's PR above all - confirm before writing anything.

On any of these - stop and tell the user. The last four apply to fix mode; the first is a report-mode outcome too.

## NEXT

A clean report, or a clean re-check - the branch is ready. `git push` and MR / PR creation happen only on your explicit request.
