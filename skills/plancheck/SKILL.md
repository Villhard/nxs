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
- Source artifact for the scope lens: the plan's `## SOURCE ARTIFACTS` section (brief, root-cause brief, tracker key / URL). If no source artifact exists, the scope lens is skipped with a stated reason.

## REVIEW

Delegate the review to one `nxs:plan-reviewer` subagent. Protocol injection is a mandatory step: read `review-protocol` (`skills/review-protocol/SKILL.md`) once and include its full text in the agent's prompt. The agent does not restate the protocol - it receives it this way.

The agent covers four lenses in one pass - scope, structure, testing, risk - and skips a lens whose precondition is absent, with a one-line reason. `plan-conventions` is orchestrator-side background: read it to scope the review, do not inject it.

A trivial plan does not need the agent at all - do one direct pass yourself and report.

Open `[NEEDS CLARIFICATION]` markers are a BLOCK: a plan with open markers is not ready for execution.

## AGGREGATE

- Classify each finding as BLOCK / NIT per `review-protocol`; apply its pre-emit check (quote a plan excerpt, drop what you cannot quote), high-confidence threshold, anti-speculation filter, and no numeric cap.
- Rank by impact, strongest first.
- overall: NEEDS CHANGES on any BLOCK; APPROVE otherwise. A skipped lens does not affect overall.

## OUTPUT

Findings to chat, in the agent's output format. No file is written by default. Wording of every finding follows the plain-wording rule of review-protocol.

Only on explicit user request, save the result by appending a `## PLAN REVIEW NOTES` section to the plan file - otherwise the plan is left untouched.

## RULES

- Read-only - no automatic rewrites of the plan.
- Every finding quotes a specific task or line and states a concrete required change; no vague "could be better", no "what if later" hypotheticals.
- Reuse the BLOCK / NIT vocabulary from `review-protocol`; do not invent a separate one.
- Clean approve is a valid result.

## NEXT

Plan clean -> `/nxs:exec` to implement. Findings to fix -> `/nxs:plan` to revise the plan, then re-review.
