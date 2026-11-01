---
name: nxs-lead
description: Coordinate an approved task through bounded native subagents and independently checked handoffs.
argument-hint: "[request, feature or ticket]"
disable-model-invocation: true
---

# /nxs-lead

Coordinate explicitly requested work through the active client's native subagents. Ordinary coordination is the default; do not enable auto implicitly. Read [project specs](references/project-specs.md) for affected paths and [task journal](references/task-journal.md) before a task write, question or handoff. Use an explicit [controlled run](references/controlled-run.md) packet only where required by a selected stage.

For explicitly selected auto, read [guarded auto](references/auto.md). For interruption or uncertain effects, read [continuation](references/recovery.md) before continuing.

## COORDINATE

1. Resolve the request, feature or ticket from evidence, not branch alone. Establish user-approved scope, existing decisions, permissions, prerequisites and desired stages. Ask the user for material unresolved decisions; do not invent approval. Keep task records proportionate to the work.
2. Check that the active client can launch a fresh-context native subagent with a complete prompt and collect or wait for its result. If a required capability or permission is unavailable or unverified, report the actual limitation and stop the affected step. Never substitute a different client, nested CLI or runner.
3. Choose an accepted stage within the authorized scope. Give the worker its objective, relevant source and approved context, exact write and permission boundaries, acceptance criteria and expected artifacts and evidence. Preserve native permissions; prompt-only restrictions do not establish enforced read-only access. Workers propose results, not workflow decisions.
4. For execution, obtain a concrete plan before edits. The lead may approve technical plans and corrections inside approved scope. Relay changes to scope, settled decisions, personal priorities or costly or irreversible actions to the user before dependent work. A worker never approves its own plan.
5. Track each required worker by the identity the host provides. Collect or wait for every result needed by the next dependent step using the active client's supported facility; a launch acknowledgment, another worker's result or an interim status is not completion. If the host cannot wait or return a required result, stop the dependent step and report what is pending and how to resume; do not promise automatic background continuation. On interruption, a lost reply or uncertain effects, follow the continuation contract before retrying; never assume a missing reply means no effect.
6. Independently inspect artifacts, required checks, evidence and Git state before accepting a result. Reconcile failures and missing evidence; an assertion or ticket status alone is not acceptance. Choose applicable review, built-work spec and separate atomic commit handoffs within the authorized scope. Verify each before the next dependent step; do not create empty commits or push. Report results, limitations and next action; do not present pending or unverified work as a completed task.
7. When reporting completion of work involving a branch, list remaining worktrees with `git worktree list` and report their paths and branches, or report why the list is unavailable. If the list is unavailable, stop cleanup. Their presence does not establish ownership or that they are stale. Do not remove a worktree without explicit authorization for that specific cleanup. Before any authorized cleanup, inspect its branch and data, including tracked changes, untracked and ignored files; if inspection is incomplete or data preservation is uncertain, stop and report the limitation rather than deleting.
