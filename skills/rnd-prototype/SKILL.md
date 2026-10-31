---
name: rnd-prototype
description: Test one hypothesis with a retained temporary prototype and an evidence-backed verdict, without implementing the result.
argument-hint: "<hypothesis | experiment input path>"
disable-model-invocation: true
---

# /rnd-prototype

Test one explicit hypothesis with the smallest useful temporary experiment. Run only on explicit invocation or in an explicit controlled scope. Read any supplied input before proceeding; a missing file is a stop. Read [project specs](references/project-specs.md) for applicable intent and [prototype](references/prototype.md) for location, evidence and permission rules.

Read [task journal](references/task-journal.md) before a task write, question or handoff. A supplied feature path selects its journal; a branch alone does not. An explicit controlled packet also requires [controlled run](references/controlled-run.md); it relays existing authorization, not new consent.

## EXPERIMENT

1. Identify a single question, a falsifiable hypothesis and an observable check that could support or reject it. Inspect relevant code and existing evidence. If the hypothesis or success criterion is materially ambiguous, ask before building the dependent experiment.
2. Choose a cheap, isolated experiment with a runnable check and a clear boundary around its data and side effects. Objective preparation may proceed within an authorized scope. Ask before a choice dependent on visual or personal preference, or an experiment that is costly or irreversible. A controlled worker relays the question through lead.
3. Build and run the experiment in its retained local prototype directory, using disposable data. Record exact setup, input, check and observed result. If a check cannot run, preserve the prototype and say what prevented it; do not invent an outcome.
4. Save a linked verdict as specified in [prototype](references/prototype.md): supported, rejected or inconclusive, with evidence and limits. Keep prototype files and verdict local and uncommitted by default. Report paths, observations and a useful next action.

## BOUNDARY AND HANDOFF

A successful experiment does not authorize production edits, tickets, deployment or another stage. Transfer to product code, reuse of prototype parts and deletion each require separate user authorization for the intended action. Preserve source and prototype bytes while that authorization is absent. Continue to discussion or design only within the original or a subsequent instruction; the lead selects any controlled handoff. Never change project specs, settings or Git state as part of this experiment.
