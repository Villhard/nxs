---
name: rnd-audit
description: Survey a project and save ranked, evidence-backed architecture opportunities without selecting or implementing one.
argument-hint: "[project path | audit scope]"
disable-model-invocation: true
---

# /rnd-audit

Survey the requested project for architecture improvement opportunities and save the result. Run only on explicit invocation or within an explicit controlled scope. Read any supplied input before proceeding; a missing path is a stop. Read [project specs](references/project-specs.md) for applicable intent and [audit](references/audit.md) for inspection, ranking and output rules.

Read [task journal](references/task-journal.md) before a task write, question or handoff. A supplied feature path selects its journal; a branch alone does not. An explicit controlled packet also requires [controlled run](references/controlled-run.md); it relays existing authorization, not new consent.

## SURVEY

1. Establish the requested scope and inspect project instructions, relevant specs, glossary and decisions. Map meaningful modules, responsibilities and callers across that scope; trace representative behavior and tests across the interfaces. Record what was inspected and what was inaccessible or sampled.
2. Investigate candidate opportunities against actual code and caller evidence. Compare the current behavior, change pressure and consequences of improvement with the cost and risk of change. Use the depth and prioritization guidance in [audit](references/audit.md); distinguish verified facts, assumptions and confidence. Do not infer design quality from size or a dependency graph alone.
3. Rank supported opportunities with explicit reasons, not a fixed number. If none is justified by the evidence, save a reasoned no-change result. When coverage is incomplete, say what was not checked and whether it limits that conclusion.
4. Save the survey under the output rules, then report its path, leading opportunities or no-change conclusion, and meaningful limits. Suggest a concrete next action without choosing an opportunity for the user.

## HANDOFF

Selection, design approval and implementation are distinct actions. An audit alone does not authorize selecting an opportunity, changing product code, tests or project specs, creating implementation tickets, deploying, or changing Git, settings or installations. Offer a selected-module `rnd-design`, discussion or spec as a possible next step; start one only when the original instruction or a subsequent instruction authorizes it. In controlled work the lead chooses the authorized next step.
