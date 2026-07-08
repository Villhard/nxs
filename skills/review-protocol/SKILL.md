---
description: The shared review protocol for code and plan review - read-only stance, per-finding pre-emit check, BLOCK/NIT/DROP classification, ranking, and finding output format. Load during code or plan review. Background knowledge, not a user command.
user-invocable: false
---

# REVIEW PROTOCOL

Load during code or plan review. Workflow discipline, not a user-invocable command. This is the single shared protocol every reviewer follows; the orchestrator injects its full text into each lens subagent's prompt, and the subagent does not navigate any external source.

## STANCE

Read-only. Do not edit the code or plan under review - only report findings back to the main context. Confidence threshold is high: better to skip a weak issue than emit a false positive. No hypotheticals: a speculative future risk without a concrete scenario is not a finding.

## PRE-EMIT CHECK (per finding, mandatory)

Read the intent before judging: the source artifact (plan / brief / ticket) and nearby comments / tests, to establish what the target is meant to do. A finding that contradicts a stated intention is likely intentional design - drop or downgrade it.

For each finding candidate, before emitting:

1. Read 20-30 lines of context around `<file>:<line>`.
2. Quote a 5-7 line excerpt, marking the offending line with `>`.
3. Answer two counter-questions:
   - Intentional, deliberate decision - any sign it was done on purpose?
   - Already handled elsewhere?

Drop the candidate if either answer is "yes", or if you cannot quote the excerpt.

If a finding rests on an inference rather than a quoted line, mark it explicitly (`Inference: ...`) or drop it. Do not present a guess as an observed fact.

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

Prefer one strong finding over several weak ones. A concern without a concrete failing path is not a finding - do not emit it to look thorough.

## OUTPUT FORMAT

Findings first - no praise, preamble, or process narration. If nothing passes the check, a clean APPROVE is a valid result.

Plain wording (per finding):

- one claim per sentence; a sentence names the subject, the action, and the consequence ("the check misses X"), never a compressed coined term ("the check does not operationalize X");
- no nominalizations or compound terms invented on the spot - describe the concrete failure instead;
- the fix is one phrase with at most one example command per finding; no lists of example commands;
- readability test: a reader who has not seen the target understands the finding on first read.

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
