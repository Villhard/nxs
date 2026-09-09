# CONTRIBUTING (STD)

Follow the [shared rules and checks](../../CONTRIBUTING.md).

## CONTRACT

The contract is the `std` plugin, `teach` skill, conversational teaching by default, and [learning artifacts](skills/teach/references/workspace.md). Keep both manifests pointed at one shared skill; do not add platform-specific lessons or require other skills for the core dialogue.

## BEHAVIOR CHECKS

When teaching behavior changes, run real conversations in temporary learning directories. Judge responses and saved state:

1. Book excerpt: a small chat explanation and grounded mission/resources.
2. Confusion and full-example request: explain instead of continuing the quiz.
3. Valid objection: recheck assumptions/sources and correct the example.
4. Partly correct answer, then "understood": record the supported insight and remaining gap without claiming mastery.
5. Pause mid-exercise, then a fresh session: resume from saved files without revealing the answer.
6. Nontechnical topic and inaccessible source: disclose limits; do not require code.

Also check that a factual question without skill invocation creates no learning files. Verify discovery in both clients. Record actual limits; format validation does not evaluate teaching.
