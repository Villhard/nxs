---
name: rnd-grill
description: Discuss an idea, question or plan through evidence-backed choices; finish in dialogue or explicitly request saving through to-decision.
argument-hint: "[question | plan | saved decision path]"
disable-model-invocation: true
---

# /rnd-grill

Discuss the requested decision and stop at its agreed conclusion or exact open question. Accepted inputs are an idea, question, plan, saved discussion or current session context. A clear request may need no interview.

## ENTRY

Run on explicit invocation or within an explicit controlled scope. Read [discussion](references/discussion.md), [domain modeling](references/domain-modeling.md) and [project specs](references/project-specs.md) before investigating. Use their evidence, rounds and resume rules. Read an explicit input before proceeding; a missing file is a stop, not a new request.

Read [task journal](references/task-journal.md) before a durable task write, question or handoff. Taskless discussion creates no journal. A supplied feature path selects its journal; a branch alone does not. An explicit controlled packet also requires [controlled run](references/controlled-run.md); it changes question relay and outcomes, not the user's decision authority.

## DISCUSS

1. Inspect relevant code, documents and current behavior. Report the facts that affect the choice with source paths or primary-source links; distinguish assumptions and unavailable evidence.
2. Work the discussion frontier in independent rounds. Give real alternatives, consequences and a recommendation for each material choice. Wait for the user's choices in ordinary discussion before deriving dependent questions. Choose routine technical details from evidence instead of inventing an interview.
3. Test significant conclusions against concrete edge cases, assumptions and failure signals. New contradictory evidence reopens only the affected conclusion. Stop when no material choice remains silently assumed, or name the precise pending choice and wait.

For a direct term/ADR request within this invoked scope, use the domain rules to show the concrete proposal. Saving follows the separate authorization below; a domain-only result needs no decision wrapper.

## FINISH OR SAVE

Summarize agreed conclusions, proposals and open questions in dialogue. Discussion alone creates no decision file, glossary/ADR entry, feature spec or ticket. It changes no product code, Git state, settings or installation. Existing supplied artifacts stay intact.

Suggest `to-decision` when the user wants a durable result. If the original instruction expressly includes saving, use that authorized saving step with the same context and journal; first require the saving procedure's content approval. Otherwise wait for a separate invocation or instruction within this expressly invoked scope. The saving procedure owns extracting and presenting the proposed result, exact approval reuse and permitted writes. If unavailable, report that and preserve the discussion rather than substituting another route.

HTML approval alone requests no save. This skill enables no auto coordination; a controlled lead may supply an authorized handoff under the saving procedure's contract. A saved decision is context for a separately requested `to-spec` stage, never an automatic transition.
