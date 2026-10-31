---
name: to-handoff
description: Save resumable context for entrusted work with or without a task journal, separating accepted, open and unverified state.
argument-hint: "[task or destination path]"
disable-model-invocation: true
---

# /to-handoff

Save a concise handoff for a fresh session. Run only on explicit invocation or in an explicit controlled scope. Read the selected task and explicit sources; a missing explicit path stops. Read [context rules](references/context.md), [project specs](references/project-specs.md) for affected paths and the [template](assets/handoff.md). Read [task journal](references/task-journal.md) before a task write, question or handoff when one exists; an explicit controlled packet additionally requires [controlled run](references/controlled-run.md).

## RECONCILE AND SAVE

1. Resolve the entrusted task from the user's explicit path, supplied artifact or unambiguous current conversation. A branch alone cannot identify a task; ask if multiple tasks fit. Read relevant task records, prior handoffs and the journal when present. Reconcile them with current artifacts, working tree, index and observable effects as applicable. A recorded completion is evidence of a claim, not independent verification.
2. Distinguish accepted decisions and their evidence from open questions and unverified claims or effects. Preserve exact question text and identity, prior authorization, scope, constraints, sources, dependencies, artifact paths and relevant hashes. Unknown launch, commit or migration effects remain uncertain; specify the observation needed before any retry. Never infer completion from absence of an error or replay an uncertain effect.
3. Reuse an explicit or established destination. For a known feature default to `.scratch/<feature-slug>/handoff.md`; without a feature or journal, use a user-specified destination or `.scratch/handoffs/<task-slug>.md` when the task is unambiguous. Do not fabricate a journal. If the destination is ambiguous, ask. Preserve existing handoff history and unrelated content; reconcile existing files before updating.
4. Save the template with enough standalone context to identify the task, current state, intended consumer and next authorized action. Link existing evidence and a journal if one exists; state what was not checked. Exclude secrets and unnecessary private transcripts. A native session identity is client-specific, not transferable across harnesses.
5. Re-read the result and its links, then report the path, open questions, unverified effects and next action. Saving a handoff grants no new implementation, external action or replay authorization.
