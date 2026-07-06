---
description: The shared review protocol for code and plan review - read-only stance, per-finding pre-emit check, BLOCK/NIT/DROP classification, ranking, and finding output format. Load during code or plan review. Background knowledge, not a user command.
user-invocable: false
---

# REVIEW PROTOCOL

Load during code or plan review. Workflow discipline, not a user-invocable command. This is the single shared protocol every reviewer follows; a reviewer subagent has it inlined and does not navigate any external source.

## STANCE

Read-only. Do not edit the code or plan under review - only report findings back to the main context. Confidence threshold is high: better to skip a weak issue than emit a false positive. No hypotheticals: a speculative future risk without a concrete scenario is not a finding.

## PRE-EMIT CHECK (per finding, mandatory)

For each finding candidate, before emitting:

1. Read 20-30 lines of context around `<file>:<line>`.
2. Quote a 5-7 line excerpt, marking the offending line with `>`.
3. Answer two counter-questions:
   - Intentional design? Any sign in the code / comments / tests that this was done deliberately?
   - Already handled elsewhere - under a different name in this same diff, or in existing project helpers?

Drop the candidate if either answer is "yes", or if you cannot quote the excerpt.

## CLASSIFICATION

BLOCK - must be fixed before merge:

- real bug;
- broken requirement (does not do what it should);
- build break;
- regression (old behavior is broken);
- security / data risk;
- missing important test (new functionality without coverage);
- serious maintainability issue (code is genuinely unreadable).

NIT - useful to fix, does not block merge:

- small readability improvement (no semantic change);
- simpler debugging / maintenance;
- clearer tests;
- minor user-visible quality;
- naming that reflects the meaning more precisely;
- removal of small dead code.

DROP - not a finding, do not emit:

- pure style preference without justification;
- speculative future risk without a concrete scenario;
- abstraction preference without real benefit;
- DRY suggestion that does not reduce coupling;
- an alternative that is not clearly better;
- any candidate without a concrete file / line / scenario.

Tie-breaks: in doubt between BLOCK and NIT, choose NIT; in doubt between NIT and DROP, choose drop.

## RANKING

No fixed numeric cap. Emit every finding that passes the pre-emit check, ordered by real consequences, strongest first. Drop weak / speculative candidates rather than padding the list.

## OUTPUT FORMAT

Findings first - no praise, preamble, or process narration. If nothing passes the check, a clean APPROVE is a valid result.

```
<Reviewer> review: <scope>

Findings:

<BLOCK|NIT> <file>:<line> - <one-line issue>

  <2-3 lines of context>
> <offending line>
  <2-3 lines of context>

  Fix: <concrete action, one phrase>

(optional `Why: ...` line if the point is not obvious from the excerpt;
for a security finding, `Attack: <scenario>`)

...

Verdict: APPROVE | NEEDS CHANGES
```
