---
description: Read-only multi-lens review of an implementation plan before execution, especially before auto modes - reports BLOCK / NIT findings without editing the plan. Use after /nxs:plan and before /nxs:exec, and always before /nxs:exec auto.
argument-hint: "[plan path]"
---

# /nxs:plancheck

Read-only review of an implementation plan before execution. Produce BLOCK / NIT / approve findings, then stop. This skill never edits the plan. Self-contained skill. Output language and response style come from global rules, not this file.

Use before `/nxs:exec`, and especially before `/nxs:exec auto`, where the bar is higher.

Example: /nxs:plancheck docs/plans/20260711-auth-refactor.md

## STANCE (READ-ONLY, HAND OFF)

- The review reports; it does not fix. It reads the plan and prints findings; it never rewrites the plan.
- Fixing the plan is the user or `/nxs:plan`. Executing it is `/nxs:exec`. This skill reports and stops.
- A clean approve is a valid result - do not invent findings to look thorough.

## RESOLVE THE PLAN

- Plan under review: the argument path if given, otherwise the latest active plan under `docs/plans/`. If none is found or the choice is ambiguous, ask.
- Source artifact for the scope lens: the plan's `## SOURCE ARTIFACTS` section (brief, root-cause brief, tracker key / URL). If no source artifact exists, the scope lens is skipped with a stated reason.

## LENSES

Up to four independent read-only subagents, run proportional to the plan. Each lens carries its `plan-conventions` criteria embedded in its own FOCUS AREAS - `plan-conventions` is orchestrator-side background (what you read to scope the review), not a text injected into the agents. Protocol injection is a mandatory step: read `review-protocol` (`skills/review-protocol/SKILL.md`) and `reference/plan-protocol-addendum.md` once each, and include the full text of both in the prompt of every plan lens you spawn. The lens agents do not restate the protocol - they receive it via these injected texts.

- `nxs:plan-scope-reviewer` - Spec/Scope: the plan against its source artifact - coverage of acceptance criteria, no scope creep, no invented work.
- `nxs:plan-structure-reviewer` - Decomposition: task sizing, vertical-slice slicing, dependency sequencing, and per-task well-formedness (title, Files block, checklist, success criteria, final verification step).
- `nxs:plan-testing-reviewer` - Verification: presence of test items, behavior-level test cases on the public interface, and TDD-loop discipline where the plan declares TDD.
- `nxs:plan-safety-reviewer` - Risk: dangerous or irreversible operations, reversibility, and auto-execution safety.

Adaptivity: run the lenses proportional to the plan. A trivial plan can be a single orchestrator pass instead of four subagents; a large or risky plan warrants all four. A lens whose precondition is absent (no source artifact, spike approach, no dangerous ops and not auto-targeted) is skipped with a one-line reason, not silently dropped.

## AUTO-MODE BAR

If the plan is headed for `/nxs:exec auto`:

- open `[NEEDS CLARIFICATION]` markers in the plan are a BLOCK - a plan with open markers is not ready for unattended execution;
- the safety lens reviews especially strictly.

## AGGREGATE

- Collect per-lens findings; dedup repeats across lenses, keeping the most specific.
- Classify each as BLOCK / NIT per `review-protocol`; apply its pre-emit check (quote a plan excerpt, drop what you cannot quote), high-confidence threshold, anti-speculation filter, and no numeric cap.
- Rank by impact, strongest first.
- overall: NEEDS CHANGES if any active lens has a BLOCK; APPROVE otherwise. A skipped lens does not affect overall.

## OUTPUT

Findings first, to chat. No file is written by default.
Wording of every finding follows the plain-wording rule of review-protocol.

```
Plan review: <plan-file-path>
Lenses: scope <active|skipped: reason> | structure active | testing <active|skipped: reason> | safety <active|skipped: reason>

Blocking issues:
- <BLOCK> Task <N> (<lens>): <issue> - <required change>

Recommended changes:
- <NIT> Task <N> (<lens>): <issue> - <required change>

Overall: APPROVE | NEEDS CHANGES
```

A clean approve with no findings is valid. Only on explicit user request, save the result by appending a `## PLAN REVIEW NOTES` section to the plan file - otherwise the plan is left untouched.

## RULES

- Read-only - no automatic rewrites of the plan.
- Every finding quotes a specific task or line and states a concrete required change; no vague "could be better", no "what if later" hypotheticals.
- Reuse the BLOCK / NIT vocabulary from `review-protocol`; do not invent a separate one.
- Clean approve is a valid result.

## NEXT

Plan clean -> `/nxs:exec` (or `/nxs:exec auto`) to implement. Findings to fix -> `/nxs:plan` to revise the plan, then re-review.
