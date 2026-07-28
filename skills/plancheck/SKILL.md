---
description: Read-only review of an implementation plan before execution - reports BLOCK / NIT findings without editing the plan. Use after /nxs:plan and before /nxs:exec.
argument-hint: "[story path | plan path]"
---

# /nxs:plancheck

Read-only review of an implementation plan before execution. Produce BLOCK / NIT / approve findings, then stop. This skill never edits the plan. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:plancheck docs/nxs/stories/20260711-auth-refactor

## STANCE (READ-ONLY, HAND OFF)

- The review reports; it does not fix. It reads the plan and prints findings; it never rewrites the plan.
- Fixing the plan is the user or `/nxs:plan`. Executing it is `/nxs:exec`. This skill reports and stops.
- A clean approve is a valid result - do not invent findings to look thorough.

## RESOLVE THE PLAN

- Plan under review: the argument if given - a story directory resolves to its `plan.md` - otherwise the latest story under `docs/nxs/stories/` (not `completed/`) that contains a `plan.md`. If none is found or the choice is ambiguous, ask.
- Source artifact for the scope check: the story's sibling brief, plus the tracker key or URL from the plan's `## SOURCE ARTIFACTS` section. If no source artifact exists, the scope check is skipped with a stated reason.

## REVIEW

Delegate to one `nxs:plan-reviewer` subagent. Injection is mandatory and covers two files: `review-protocol` (`${CLAUDE_SKILL_DIR}/../review-protocol/SKILL.md`) and `reference/plan-review-policy.md`. Read both once and include their full text in the agent's prompt. A path does not resolve -> find that file inside the plugin before spawning anything; the agent does not review from memory. The agent does not restate either file - it receives them this way.

The agent checks the plan's claims against the repository: paths that do not exist, places the plan missed, steps out of order, decisions the executor cannot make alone. `plan-conventions` is orchestrator-side background - read it to scope the review, do not inject it. It says what a plan must contain; what is worth reporting is this skill's call.

A trivial plan does not need the agent - do one direct pass yourself, against the same bar, and report.

## VERIFY, THEN CLASSIFY

The agent proposes unlabeled candidates; you decide what the user sees and what it is called. Two gates, in order.

**Is it real.** Run the `Repo:` command yourself and read the plan text it points at. The command returning something else, or the point already covered by another task - discard, do not downgrade. This applies to NIT as much as to BLOCK.

**Does it cost anything.** Name the gate that catches it: a Test case in the task, the `verify` run, the review of that task's diff, an acceptance criterion, or an `/nxs:exec` stop condition. Write that clause down before you write a label. A gate catches it - NIT at most. No gate catches it and you can name the wrong end state - BLOCK. Neither - drop it.

Classify against `reference/plan-review-policy.md`. Discarding most candidates is a normal outcome.

One BLOCK skips both gates because it is mechanical and `/nxs:exec` refuses to start on it: an open `[NEEDS CLARIFICATION]` marker, verified with `rg "NEEDS CLARIFICATION" <plan>`. It is the only such case; everything else earns its label through the two gates.

Overall: NEEDS CHANGES on any confirmed BLOCK; APPROVE otherwise, nits and all.

## OUTPUT

To chat. No file is written by default. The verdict and the size of the problem first, then the findings, then the provenance.

```
<APPROVE | NEEDS CHANGES> - <counts> - <plan>

BLOCK  Task <N>
  <one sentence: what ships wrong and why no gate catches it>
  Repo: <command -> result>
  Fix: <what to add or change in the plan>

NIT  Task <N> - <what is wrong>
  Repo: <command -> result>

Source artifact: <brief path, tracker key, or skipped with the reason>
```

Filled in:

```
NEEDS CHANGES - 1 block, 2 nits - 20260728-pagination/plan.md

BLOCK  Task 2
  No task touches src/reports/cache.py, which keys its cache on the items sort order, so the cache ships stale and nothing reads that file.
  Repo: rg -n "sort" src/reports/cache.py -> 2 hits, no test file for it
  Fix: add the cache rebuild to Task 2, or a task after it.

NIT  Task 1 - the Files block lists tests/items/test_pagination.py, which no checklist item writes to.
  Repo: rg -n "test_pagination" plan.md -> only in the Task 1 Files block

NIT  Task 3 - runs before Task 2 creates the repository function it calls.
  Repo: rg -n "list_items" plan.md -> Task 3 line 78 calls it, Task 2 line 60 creates it

Source artifact: docs/nxs/stories/20260728-pagination/brief.md, PROJ-123
```

- **First line** - verdict, counts, plan. Counts drop an empty category and go singular at one: `1 block, 2 nits`, `2 nits`, `1 block`, `no findings`. The plan is named the way a person would name it; the full path lives in the last line.
- **Blocks first**, worst consequence at the top, then nits in task order.
- **The body of a block is one sentence** naming what ships wrong and what would have caught it. Not two.
- **A nit is one line**, with its `Repo:` line indented below it. Evidence is not prose, and the evidence bar does not relax: a finding may be about something the plan never mentions, but never without the `Repo:` line.
- **The last line is the provenance**, printed even when nothing was found, and it is where a skipped scope check states its reason.

The report should need no follow-up question.

Only on explicit user request, save the result by appending a `## PLAN REVIEW NOTES` section to the plan file - otherwise the plan is left untouched.

## RULES

- Read-only - no automatic rewrites of the plan.
- Every finding names what the plan says and what the repository says; a finding without both is dropped.
- Do not report on the plan's form - title wording, checkbox counts, section order. The executor does not care and neither should the review.
- Clean approve is a valid and frequent result.

## REFERENCE

- `reference/plan-review-policy.md` - what the executor is, the plan-shaped BLOCK / NIT / DROP bar, and the calls that are easy to get wrong. Read here, injected into the lens.
- `review-protocol` - the stance, verification, and output format the lens follows, injected into it.
- `plan-conventions` - what a plan must contain; background for scoping the review, never injected.

## NEXT

Plan clean -> `/nxs:exec` to implement. Findings to fix -> `/nxs:plan` to revise the plan, then re-review.
