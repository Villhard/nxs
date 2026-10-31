---
name: to-questionnaire
description: Prepare a recipient-specific document asking for missing facts or decisions without sending it or inventing answers.
argument-hint: "<participant and context | input path>"
disable-model-invocation: true
---

# /to-questionnaire

Prepare a durable document for a known participant. Run only on explicit invocation or in an explicit controlled scope. Read explicit inputs; a missing input stops the work. Read [project specs](references/project-specs.md) for affected paths and [questionnaire rules](references/questionnaire.md) before preparing the document. Read [task journal](references/task-journal.md) before a task write, question or handoff; an explicit controlled packet also requires [controlled run](references/controlled-run.md).

## PREPARE

1. Identify the participant, their role, the decision context and the specific missing facts or choices from supplied evidence. Ask the user to identify the recipient when unknown; never guess who can answer. Reuse known answers and established decisions, attributing them to their sources. Avoid irrelevant private information.
2. For each unknown, write an answerable question, enough context, the affected decision and the consequence of its answer or continued absence. Distinguish known facts, permitted assumptions and unanswered questions. A critical unknown blocks its affected decision, not independent authorized preparation. Never supply an answer on the participant's behalf.
3. Use the [template](assets/questionnaire.md). Reuse an explicit or established artifact path; otherwise save under `.scratch/<feature-slug>/research/questionnaire-<recipient-slug>.md`. If task identity or destination is ambiguous, ask. Preserve existing content and responses, and reconcile any partial response without treating unanswered questions as answered. Link sources and affected decisions without including secrets or unnecessary private transcripts.
4. Verify the document and report its path, remaining questions and affected blockers. Preparing, opening or approving it authorizes no sending, contact, answer submission or dependent implementation. Send only on a separate explicit instruction and through an available authorized channel; if unavailable, report that limitation. Continue independent work only within its existing authorization.
