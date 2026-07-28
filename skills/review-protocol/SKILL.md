---
description: The shared review protocol for code and plan review - read-only stance, how to verify a finding before reporting it, BLOCK/NIT/DROP classification, and finding output format. Load during code or plan review. Background knowledge, not a user command.
user-invocable: false
---

# REVIEW PROTOCOL

Load during code or plan review. Workflow discipline, not a user-invocable command. This is the single shared protocol every reviewer follows; the orchestrator injects its full text into each lens subagent's prompt, and the subagent does not navigate any external source.

## STANCE

Read-only. Do not edit the code or plan under review - only report findings back to the main context.

A review that reports nothing is a good review. Silence is the default; you are not measured by how much you found.

## VERIFY EVERY FINDING

Only report what you verified by reading the actual code. For each candidate, before emitting it:

1. Read the code at `<file>:<line>`, plus 20-30 lines of context around it.
2. Confirm the problem is real and not a false positive.
3. Check whether it is already handled - a guard, a validation, a test elsewhere in the diff or nearby.
4. Check whether it is deliberate - the plan, the brief, or a nearby comment saying so.

Confirmed - report it. Anything else - discard, do not downgrade.

Before claiming something is unused, never called, or unreachable, search the project for it first, including tests and config. That claim is wrong more often than any other.

## CLASSIFICATION

**BLOCK** - fix before merge: a bug with a concrete input, a requirement the change does not meet, a build break, a broken existing behavior, a security or data-loss path, new behavior with no test to catch its regression.

**NIT** - worth fixing, does not block: a leftover from a removal, a comment or name that will mislead the next reader, a duplicated shape that will drift, a test bound to an incidental detail.

**DROP** - everything else, and anything you are unsure about: no concrete consequence, only "would be cleaner"; a speculative future scenario; a preference for a different structure that is not clearly better; a rule the linter already enforces; code this diff does not touch.

Tie-breaks: unsure between BLOCK and NIT, choose NIT. Unsure between NIT and DROP, choose DROP.

## OUTPUT FORMAT

Findings first - no preamble, no praise, no narration. Nothing confirmed, say so and stop.

A BLOCK answers three questions. A NIT is one line - a nit that needs explaining is a nit the reader should not be reading.

```
<Lens> review: <scope>

BLOCK <file>:<line>
  Issue: <what is wrong>
  Impact: <what it costs - the request that breaks, the data that is lost>
  Fix: <what to change>

NIT <file>:<line> - <what is wrong>

Verdict: CLEAN | FINDINGS
```

Each of the three is one sentence. `Issue` names the problem, not the mechanics of the code around it. `Impact` says what actually happens - "any request without a scope gets a full-access token", not "this weakens the authorization model". `Fix` says what to change, not how to write it.

Plain words. One claim per sentence, naming the thing, the action, and the consequence. No terms coined on the spot: "the check misses an empty scope, so any request passes", never "the check does not operationalize scope validation". Someone who has not opened the file understands it on first read.

Rank BLOCK findings by impact, worst first. Emit every confirmed finding; never pad to look thorough.
