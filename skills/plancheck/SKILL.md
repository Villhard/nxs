---
description: Read-only review of an implementation plan before execution - reports BLOCK / NIT findings without editing the plan. Use after /nxs:plan and before /nxs:exec.
argument-hint: "[plan path]"
---

# /nxs:plancheck

Read-only review of an implementation plan before execution. Produce BLOCK / NIT / approve findings, then stop. This skill never edits the plan. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:plancheck docs/nxs/plans/20260711-auth-refactor.md

## STANCE (READ-ONLY, HAND OFF)

- The review reports; it does not fix. It reads the plan and prints findings; it never rewrites the plan.
- Fixing the plan is the user or `/nxs:plan`. Executing it is `/nxs:exec`. This skill reports and stops.
- A clean approve is a valid result - do not invent findings to look thorough.

## RESOLVE THE PLAN

- Plan under review: the argument path if given, otherwise the latest active plan under `docs/nxs/plans/`. If none is found or the choice is ambiguous, ask.
- Source artifact for the scope check: the plan's `## SOURCE ARTIFACTS` section (brief, root-cause brief, tracker key / URL). If no source artifact exists, the scope check is skipped with a stated reason.

## REVIEW

Delegate to one `nxs:plan-reviewer` subagent. Protocol injection is mandatory: read `review-protocol` (`${CLAUDE_SKILL_DIR}/../review-protocol/SKILL.md`) once and include its full text in the agent's prompt. The agent does not restate the protocol - it receives it this way.

The agent checks the plan's claims against the repository: paths that do not exist, places the plan missed, steps out of order, decisions the executor cannot make alone. `plan-conventions` is orchestrator-side background - read it to scope the review, do not inject it.

A trivial plan does not need the agent - do one direct pass yourself and report.

## VERIFY BEFORE REPORTING

The agent proposes; you decide what the user sees. For each finding: run the `Repo:` command yourself and read the plan text it points at. The command returning something else, or the point already covered by another task - discard, do not downgrade. This applies to NIT as much as to BLOCK.

Discarding most candidates is a normal outcome.

Open `[NEEDS CLARIFICATION]` markers are a BLOCK, verified mechanically: `rg "NEEDS CLARIFICATION" <plan>`.

Overall: NEEDS CHANGES on any confirmed BLOCK; APPROVE otherwise.

## OUTPUT

To chat. No file is written by default. BLOCK findings in full, nits folded into one line.

```
Plan review: <plan-file-path>

BLOCK Task <N>
  Issue: <what the plan gets wrong or never mentions>
  Repo: <command -> result>
  Impact: <what the executor does, and what breaks when they do it>
  Fix: <what to add or change in the plan>

Nits (<n>): Task <N> <what is wrong>, Task <N> <what is wrong>, ...

Verdict: APPROVE | NEEDS CHANGES
```

No nits confirmed, no nits line. Nothing confirmed: `Verdict: APPROVE. Findings: none.`

A finding may be about something the plan never mentions, but never without the `Repo:` line. The report should need no follow-up question.

Only on explicit user request, save the result by appending a `## PLAN REVIEW NOTES` section to the plan file - otherwise the plan is left untouched.

## RULES

- Read-only - no automatic rewrites of the plan.
- Every finding names what the plan says and what the repository says; a finding without both is dropped.
- Do not report on the plan's form - title wording, checkbox counts, section order. The executor does not care and neither should the review.
- Clean approve is a valid and frequent result.

## NEXT

Plan clean -> `/nxs:exec` to implement. Findings to fix -> `/nxs:plan` to revise the plan, then re-review.
