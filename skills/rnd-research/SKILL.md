---
name: rnd-research
description: Investigate a question and save attributable findings and limits without deciding the user's material choice.
argument-hint: "<question | research input path>"
disable-model-invocation: true
---

# /rnd-research

Research the requested question and save reusable evidence. Run only on explicit invocation or in an explicit controlled scope. Read explicit input before investigating; a missing input is a stop. Read [project specs](references/project-specs.md) for relevant repository intent, and [research output](references/research.md) for source, location and repeat rules.

Read [task journal](references/task-journal.md) before a task write, question or handoff. A supplied feature path selects its journal; a branch alone does not. An explicit controlled packet also requires [controlled run](references/controlled-run.md); it relays existing authorization, not new consent.

## INVESTIGATE AND SAVE

1. Identify the question, scope and evidence needed. Inspect relevant local code, callers, tests, existing decisions and documentation. For external facts, seek primary sources that own each claim, using available access. State source dates or versions when they affect currency.
2. Compare material evidence and distinguish observed behavior from source contracts, inferences and assumptions. A failed fetch or unavailable source is unknown, never evidence of absence. Record conflicting, stale or missing evidence and its consequence for conclusions. If material user priorities determine the answer, leave the choice open rather than choose for them.
3. Save the result under the location and preservation rules in [research output](references/research.md). Attribute each material finding to its source and include the question, findings, assumptions, unknowns, limitations and useful next steps. A partial result is still useful when evidence is insufficient; identify the next discriminating source or check.

## FINISH

Return the saved path, supported findings and important limitations. Offer concrete next actions, such as discussion of unresolved choices. Continue to `rnd-grill` or another stage only when the original instruction or a subsequent instruction authorizes that stage; a controlled lead chooses its own next step. Research does not itself create a decision, feature spec, ticket or implementation, change product code, Git state, settings or installations, or publish material.
