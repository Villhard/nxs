---
name: rnd-design
description: Design an explicitly selected module or seam and save an agreed interface decision without implementing it.
argument-hint: "<module | responsibility | seam>"
disable-model-invocation: true
---

# /rnd-design

Design the selected module, responsibility or seam and save the agreed result. Run only on explicit invocation or within an explicit controlled scope. If the selection is missing or ambiguous, ask which module or boundary to design; do not select an architecture-wide target. Read explicit input before proceeding; a missing file is a stop.

Read [discussion](references/discussion.md), [domain modeling](references/domain-modeling.md), [project specs](references/project-specs.md) and [design](references/design.md) before investigating. Read [task journal](references/task-journal.md) before a task write, question or handoff. A supplied feature path selects its journal; a branch alone does not. An explicit controlled packet also requires [controlled run](references/controlled-run.md); it relays existing authorization, not new consent.

## DESIGN

1. Inspect the selected module, its callers, tests and applicable decisions and specs. Trace current responsibilities, interface, invariants, error modes and change points. Identify missing evidence rather than assuming caller needs or ownership.
2. Compare real options for responsibilities, interface and seam using [design](references/design.md). Explain effects on callers, testability, locality and tradeoffs with evidence. Work material choices through the shared discussion rules; ordinary substantive choices require user agreement, not an inferred choice. Reuse prior approval within its exact scope.
3. Pressure-test the chosen design against concrete use, failure and change scenarios. If ownership or evidence remains unresolved, state the exact question and preserve it as open. Do not turn an open design into ready implementation work.

## SAVE AND HANDOFF

Show the proposed result and obtain content approval before saving; an explicit design invocation requests the design artifact, but does not approve unshown content. Use the location and preservation rules in [design](references/design.md). Save an agreed result with its scope, evidence, chosen responsibilities and interface, alternatives, consequences and verification implications. Save unfinished state only when explicitly requested and approved, labeled open. Domain changes follow the shared domain rules and require approval of the concrete entries.

Return the saved path, agreement and open questions. Offer `to-decision` or `to-spec` as an optional next step; start another stage only within original or subsequent authorization. Design alone creates no spec or ticket and authorizes no product refactoring or test deletion. Any later test replacement or deletion requires applicable explicit confirmation and passing checks through the new interface. Do not change project specs, Git, settings or installations.
