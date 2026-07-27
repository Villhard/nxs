---
description: The shared review protocol for code and plan review - read-only stance, the checks a finding survives before it is reported, the finding output format with confidence and severity, and the BLOCK/NIT/DROP labels the orchestrator applies to what the lenses propose. Load during code or plan review. Background knowledge, not a user command.
user-invocable: false
---

# REVIEW PROTOCOL

Load during code or plan review. Workflow discipline, not a user-invocable command. This is the single shared protocol every reviewer follows; the orchestrator injects its full text into each lens subagent's prompt, and the subagent does not navigate any external source.

## STANCE

Read-only. Do not edit the code or plan under review - only report findings back to the main context.

## BEFORE YOU REPORT

Check whether it is deliberate - the plan, the brief, or a nearby comment saying so.

Before claiming something is unused, never called, or unreachable, search the project for it first, including tests and config. That claim is wrong more often than any other.

## CLASSIFICATION (ORCHESTRATOR)

The lenses propose findings; the orchestrator applies these labels to them.

**BLOCK** - fix before merge, and exactly two things qualify: you can name the concrete input or state where the shipped behavior is wrong (a bug, a build break, a broken existing behavior, a security or data-loss path), or the diff does not meet a requirement written in the plan or the brief. The test is "would I refuse to merge over this" - if no, it is not a BLOCK. Wording, naming, a check that could be more precise, a preference for another structure, a document's own phrasing: never a BLOCK, whatever severity the lens gave it.

**NIT** - worth fixing, never gates: a leftover from a removal, a comment or name that will mislead the next reader, a duplicated shape that will drift, a test bound to an incidental detail.

**DROP** - everything else: no concrete consequence, only "would be cleaner"; a speculative future scenario; a preference for a different structure that is not clearly better; a rule the linter already enforces; code this diff does not touch.

## OUTPUT FORMAT

Findings first - no preamble, no praise, no narration. Nothing found, say so and stop.

```
<Lens> review: <scope>

<file>:<line>
  Issue: <what is wrong>
  Impact: <what it costs - the request that breaks, the data that is lost>
  Fix: <what to change>
  Confidence: high | medium | low
  Severity: high | medium | low

Verdict: CLEAN | FINDINGS
```

`Issue`, `Impact`, and `Fix` are one sentence each. `Issue` names the problem, not the mechanics of the code around it. `Impact` says what actually happens - "any request without a scope gets a full-access token", not "this weakens the authorization model". `Fix` says what to change, not how to write it. `Confidence` is how sure you are the finding is real; `Severity` is what it costs if it is.

Plain words. One claim per sentence, naming the thing, the action, and the consequence. No terms coined on the spot: "the check misses an empty scope, so any request passes", never "the check does not operationalize scope validation". Someone who has not opened the file understands it on first read.

Report every finding you have - the orchestrator decides which ones reach the user; never pad to look thorough.
