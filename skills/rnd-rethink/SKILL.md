---
description: Stop the current approach, diagnose why it is bad, abandon it, and search for a genuinely different alternative. Use when the current path is stuck, thrashing, fighting the grain, or accumulating complexity - a signal to stop rather than push harder.
argument-hint: "[what is stuck | current approach]"
---

# /nxs:rnd-rethink

Stop the current approach, diagnose why it is bad, abandon it, and find a genuinely different alternative. Self-contained skill: read-only, changes no code, writes no durable file by default. Output language and response style come from global rules, not this file.

Accepted input: a description of what is stuck or the current approach, or nothing (pick up the current session context). If the input is vague, clarify which approach is in question before proceeding.

## WHEN TO USE

Trigger this when the current approach is stuck, thrashing, fighting the grain, or accumulating complexity when it should shrink - a signal to stop rather than push harder. Concrete signals: the user says "wrong", "this isn't working", "stop", "start over"; several iterations failed; complexity grows when it should shrink; you are about to commit a questionable solution.

## PROCEDURE

1. Name the current approach. Briefly describe what we are doing now, what is not working or raises doubt, and the assumptions it was built on. State it plainly and stop defending it.
2. Diagnose why it is bad. Find the root cause of the friction, not a symptom - what constraint it violates, what it is fighting, which assumption turned out false. Separate sunk cost from real value: effort already spent is not a reason to keep going. Common roots: wrong assumption about data shape / API contract; solution too abstract for the task; wrong technical choice (framework / library); scope bloat; working on the wrong cause; premature optimization; premature abstraction.
3. Identify the untested assumptions. What was assumed but never checked - these are often the root.
4. Decide: abandon or keep. If the approach is genuinely broken, abandon it explicitly. If it is actually fine and the problem lies elsewhere, say so - do not manufacture a rethink.
5. Search for a genuinely different alternative. Propose 2-4 approaches that attack the root cause, not the symptom - not tweaks of the same approach. At least one must be "do it as simply as possible".
6. Validate and recommend. Check each alternative against the same failure that killed the old one - it must not reproduce it. Recommend the safest simple approach and justify it. If all alternatives are worse, say so directly - maybe the current approach really is best and the problem lies elsewhere.

## DISCIPLINE

- Separate sunk cost from real value. Effort already spent is not a reason to keep an approach.
- Do not rescue the old approach out of attachment. State it plainly, stop defending it.
- The alternative must attack the root cause, not the symptom, and must not reproduce the failure that killed the old one.
- At least one alternative must be simpler than the current approach.
- Be honest about whether a rethink is warranted. Sometimes the approach is fine and the user should push through - say that instead of inventing alternatives.
- No emotions, no "you were right, I was wrong". Just facts. A previous choice is not a mistake - it is a normal iterative step.

## OUTPUT

A chat report. No code changes, no durable file by default.

```text
Current approach: <what we are doing now>
Why it fails: <root cause, not symptom - what it violates / fights>
Untested assumptions: <what was assumed but not checked>
Decision: <abandon | keep and look elsewhere>
Alternatives:
- <A> (simplest): <how it attacks the root cause>
- <B>: <how it attacks the root cause>
Recommendation: <which>
Why it avoids the same failure: <concrete reason it does not reproduce the old failure>
```

## ROUTING

- rethink stops and replaces a CURRENT stuck approach. That is the entry condition.
- Two already-formed approaches to weigh head to head -> `/nxs:rnd-dialectic`.
- A not-yet-started task still being shaped -> `/nxs:rnd-brainstorm`.
- A design question that depends on runtime behavior you can observe -> `/nxs:rnd-prototype`.
