# PLAN REVIEW POLICY (reference)

Loaded on demand from `/nxs:plancheck` and injected into the `nxs:plan-reviewer` lens beside `review-protocol`. Holds what the base protocol does not: what the executor of this plan actually is, and the bar a plan finding clears before the user sees it.

## THE EXECUTOR

`/nxs:exec` is not a blind script. Per task it launches a worker, runs `verify` (format, lint, typecheck, tests), reviews that task's diff with `review`'s lenses to a zero-BLOCK round, then checks the plan's `## ACCEPTANCE CRITERIA`. It stops instead of guessing: missing Files block, unclear requirement, open `[NEEDS CLARIFICATION]` marker, failed check, AC not met, scope drift.

So a gap the executor walks into costs one stop and one plan edit, not a wrong result. Two things those gates never see: code no task touches, because the per-task review reads only that task's diff, and a check the plan itself wrote too weakly to fail. That is where a real plan BLOCK lives.

## THE BAR

First question, before any other: would the code at the end of execution be different if the plan were fixed? No - not a finding. A fix that only adds a sentence to a document is never a BLOCK.

**BLOCK** - the wrong end state ships and nothing catches it. All three hold:

1. you can name the wrong end state - the file left stale, the caller that breaks, an acceptance criterion that ships unimplemented;
2. no gate sees it - the task's Test cases, the `verify` run, the review of that task's diff, the plan's AC, and exec's stop conditions all read as passing with the wrong result in place;
3. the executor cannot fix it in flight - opening the files the plan already names does not lead them to the right answer.

**NIT** - the right end state still ships, at an avoidable cost: one executor stop, one wasted task, one decision made twice. One line, never explained.

**DROP** - everything else: a fact with no end state behind it, a preference about how the plan reads, a scenario no task can be tied to. The protocol's tie-breaks apply unchanged.

## WHAT DOES NOT CARRY OVER

`review-protocol` classifies a diff. Two of its BLOCK clauses need translating:

- "new behavior with no test to catch its regression" - a behavioral task with no Test cases is a NIT; the review of that task's diff asks for the test before the commit. A task whose Test cases would pass whatever the code does is a BLOCK: that is a gate reporting green on the wrong result.
- "a requirement the change does not meet" - a plan meets nothing yet. Here it reads: a requirement in the brief or the ticket that no task covers and no line defers.

Its NIT list is code-shaped: a leftover from a removal, a stale comment, a duplicated shape that will drift. Nothing in a plan matches those, and that is not a reason to promote anything to BLOCK.

## CALLS THAT ARE EASY TO GET WRONG

**An omission is not a block by itself.** The outward search finds names, not dependents. A symbol hit in three files says three files mention it; a BLOCK needs one of them to be wrong afterwards, and you have to say which and how.

**An open decision is a NIT when both answers work.** Which of two equivalent helpers, where a constant lives, what the log line says: the executor picks one and the result is right either way. It is a BLOCK only when one branch ships something the AC would still call done.

**"Not covered" is usually covered elsewhere.** Read every task for the requirement under different words before saying it is missing. A plan rarely uses the brief's vocabulary.

**Form is not substance.** A missing Files block, missing Test cases, unjustified horizontal slicing, a vague title. Exec stops on the first and the plan comes back for one edit, the review of the task diff asks for the second, and the other two cost nothing. NIT at most, usually DROP.

**Risk only where a step carries it.** A migration, a deletion, a deploy, destructive shell, a secret written into the plan. Ordinary code changes carry none; do not manufacture it.

**What a real one looks like.** Task 2 changes the sort key of the items query. The repository has `src/reports/cache.py` building a keyed cache from that order, with no test on it. No task touches that file, so no per-task review reads it, `verify` stays green, and the AC names only the endpoint. The executor finishes and the cache is silently stale. Named end state, no gate, not fixable in flight - BLOCK.

## OUTPUT

The lens proposes, the orchestrator labels. This is the lens's candidate format; the user-facing report is in `/nxs:plancheck`. The lens writes no `BLOCK` or `NIT` word and does not rank - the severity slot carries the task anchor alone:

```
Task <N>
  Issue: <what the plan gets wrong or never mentions>
  Repo: <the command you ran -> what it returned>
  Impact: <the end state that ships wrong, and why no gate catches it>
  Fix: <what to add or change in the plan>
```

`Repo:` and `Impact:` are both mandatory. `Impact:` names an end state, not a property of the document: "the report cache keeps the old order", never "the plan does not consider caching".
