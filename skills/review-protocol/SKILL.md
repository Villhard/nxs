---
description: The shared review protocol for code and plan review - read-only stance, how to verify a finding before reporting it, BLOCK/NIT/DROP classification, and finding output format. Load during code or plan review. Background knowledge, not a user command.
user-invocable: false
---

# REVIEW PROTOCOL

The single shared protocol every lens follows. The orchestrator injects its full text into each lens prompt, so the lens works from this text alone.

## STANCE

Read-only. Report findings back to the orchestrator; the code and plan under review stay untouched.

A review that reports nothing is a good review. Silence is the default.

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

A NIT is one line: a nit that needs explaining is a nit the reader should not be reading.

Plain words, one claim per sentence, naming the thing, the action, and the consequence. Use the words the codebase uses rather than terms coined on the spot: "the check misses an empty scope, so any request passes", never "the check does not operationalize scope validation".

Rank BLOCK findings by impact, worst first. Emit every confirmed finding and nothing beyond them.
