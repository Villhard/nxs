# Plan-lens protocol addendum

This addendum supplements `review-protocol` for plan-lens agents. Both `review-protocol` and this addendum must be injected into every plan-lens prompt.

## PRE-EMIT SPECIALIZATION FOR PLANS

Your target is plan text, not code. Pre-emit: quote the relevant plan excerpt (the task block or line the finding is about) - there is no code excerpt to read; drop if you cannot quote it.

## COUNTER-QUESTION READINGS FOR A PLAN

Counter-question readings for a plan: intentional = a decision justified by a filled `## COMPLEXITY TRACKING` row (non-empty "why simpler alternative rejected" cell); already-handled = covered by another task (a stated rollback / guard / confirmation) or explicitly deferred.

## COMPLEXITY-TRACKING JUSTIFICATION

A policy deviation already justified by a filled `## COMPLEXITY TRACKING` row (with a non-empty "why simpler alternative rejected" cell) is justified - downgrade or drop per the justification. An unjustified deviation, or one whose "why simpler alternative rejected" cell is empty, stays a finding.

## OUTPUT FORMAT (PLAN LENSES)

```
<Lens> plan review: <plan-file-path>

Findings:
- <BLOCK|NIT> Task <N> (<lens>): <issue>
  > <quoted plan excerpt: the task block / line the finding is about>
  Required change: <concrete fix>
  (optional single `Why: ...` line only if not obvious from the excerpt)
- ...

Verdict: APPROVE | NEEDS CHANGES
```
