---
name: dev-exec
description: Execute a ticket or clear request in the current session through an approved plan, implementation, checks and authorized commit checkpoints; leave review and project specs to separate stages.
argument-hint: "[ticket path | clear request]"
disable-model-invocation: true
---

# /dev-exec

Execute the entrusted task in this session. `to-tickets` can hand eligible work to this executor; existing `/plan` tickets retain their execution contract. Live observations are limited to the cases recorded for the selected client, and source presence does not establish registration.

## INSPECT

Run on explicit invocation or within an explicit controlled scope. Read [execution context](references/execution-context.md) first: it owns input, feature location, ticket gates, branch selection and prerequisite evidence. Read relevant code, callers, tests, project instructions, glossary/ADR entries and [project specs](references/project-specs.md) before proposing changes. Trace a reported failure before choosing its fix. State observable success criteria and distinguish verified facts from assumptions.

Before a durable task write, material question or handoff, read [task journal](references/task-journal.md) and reconcile existing events with artifacts and actual Git state. An explicit controlled packet also requires [controlled run](references/controlled-run.md). A journal path alone retains standalone dialogue and human approval.

## PLAN AND WAIT

Show a concrete plan: intended behavior, affected paths, implementation approach, relevant checks, write boundaries and material risks or unresolved evidence. Define meaningful, separately checkable logical blocks. By default, make them committable and propose a checkpoint with an explicit commit scope for each block; ask the user to approve those scopes unless already approved. Blocks may depend on earlier blocks; combine related changes that cannot safely be separated. If the user intentionally selects no commits or an existing ticket prohibits them, explicitly plan without checkpoints instead. Scale the plan to the task; a clear request needs no invented ticket or mandatory interview. Resolve material uncertainty before implementation.

| Context | Approval gate |
| --- | --- |
| Standalone | Keep the plan in dialogue and wait for human approval before implementation. Reuse existing approval only when it covers this concrete plan and scope. Journal meaningful decisions and approval; a separate plan file is optional. |
| Complete controlled packet | Save the proposed plan under the resolved feature's `research/`, pin its content hash and scope, journal the exact approval question, and return `needs_input` before implementation. Lead records technical approval. Where the host documents continuation, resume the same saved native session; otherwise, after reconciling prior effects, start a new bounded run with the approved answer, saved plan and artifacts, plan hash, recorded approval and original boundaries. In either case verify approval against the current plan before implementation; unresolved effects stop the affected action without automatic replay. |

Review changed inputs on continuation. A substantial plan change returns for approval before the affected edits. In controlled work, scope, external-contract or agreed-decision changes return through lead to the user; routine technical choices stay within the approved scope. Feature approval, a ready ticket or a saved plan alone does not approve implementation.

Built-in Plan Mode is optional. Respect its actual read/write limits and native permissions, including restrictions on journal writes. If the active mode prevents a required action, report the restriction and stop that action; do not bypass it. This skill's approval instructions are not a technical write prohibition.

Approval of the plan authorizes its explicitly identified commits and scopes only when the user's approval covers them. A controlled packet and lead technical approval cannot expand that authorization. Without authorization make no commit; stop the affected checkpoint and request approval for its scope. If an explicitly planned checkpoint lacks scope or permission, stop that checkpoint and report the missing authority. If commits are intentionally not selected, continue without checkpoints and hand off uncommitted changes. An existing ticket's `Do not commit` remains binding unless a specific revision of that ticket is separately approved; continue its execution without checkpoints rather than stopping merely because commits are prohibited.

## IMPLEMENT

After approval, recheck the plan, scope, branch, prerequisite evidence and unrelated changes, then implement the agreed work. Match surrounding conventions, reuse existing mechanisms and preserve validation/error handling. Remove code made unused by this change; leave unrelated cleanup alone. Preserve existing ticket execution text and history.

Apply [human-step gates](references/execution-context.md#human-steps) before any required dependency install, migration or external action. Authorization never substitutes for a checkable result or bypasses native permissions. Record meaningful decisions or deviations in ticket Comments when applicable and in the journal.

Writes stay within the approved task, its ticket execution fields and journal records. Project `SPEC.md` and `.SPEC.md` belong only to `dev-spec`. Do not push, create a PR or alter user installations without separate authorization. Stop for a newly required authorization instead of expanding scope.

## CHECKPOINTS

In standalone and controlled execution, for each planned checkpoint, run the completed block's necessary checks first. Record HEAD before the first checkpoint. Apply `dev-commit` in this same session within the approved scope and native permissions; follow its complete procedure, including index inspection, atomic grouping, preservation of foreign staged and working-tree changes and stop conditions. A checkpoint may produce multiple atomic commits, never an empty commit. Record each resulting commit and parent OID, approved scope and changed paths; verify identities, scope and preservation before the next block. If the skill or required permission is unavailable, stop the affected checkpoint and report it. Failed checks or unsafe separation do not establish a checkpoint. Reconcile uncertain commit effects against actual Git state and never replay them automatically.

Separate review follows the ticket rather than every checkpoint. Use `dev-spec` when needed as a separate stage. A commit alone does not complete or accept a ticket.

## VERIFY AND REPORT

Check each acceptance criterion against actual behavior/artifacts. Run the project's required checks and relevant focused regressions; for a bug, add or update a regression check when practical. Keep instruction/model observations proportionate: avoid matrices and tests that merely repeat prose. Record exact commands, results and limitations, inspect the final diff and confirm unrelated changes remain preserved. A source/packaging check does not establish live behavior, client registration or permission enforcement. Label live results as observations of their recorded cases; leave unavailable clients unverified.

For a ticket, identify the project's full test and linter commands from its instructions or other checkable project configuration. Run each check required by the ticket and record the exact command and result in Comments. If a required command is absent, cannot be identified or cannot run, record what is missing and leave the ticket unresolved; another syntax check or focused test is not a substitute unless it is the required project command. Only after every applicable criterion and required check passes, check the criteria and set `**Status:** resolved`. Record one Comments line per meaningful decision/deviation. Apply a review-origin ticket's explicit non-reproduction/wontfix rule only when that ticket grants it; preserve the remaining history. For a clear request, report its checked result without creating ticket status or a new ticket.

Journal completion, blockers or pending handoff. For checkpointed work, pass a checkpoint handoff in the journal and result: repository and branch, pre-checkpoint HEAD, each verified commit and parent OID, approved task scope and changed paths, and any remaining task changes in the index or working tree. Identify foreign staged or working changes separately. Include missing or uncertain evidence as a blocker, not a completed handoff. Tell the next stage to verify coverage against its own selected diff; commit ancestry alone does not prove the net changes remain there. Warn that staged review excludes committed checkpoints and that base-branch commits are outside both default branch review and built-work spec input. Do not suggest a next command as if it covers the task when its default scope omits any task work; report the limitation and leave the user to choose how to proceed without changing foreign state.

Return changed paths, commit identities and evidence, actual verification and remaining limitations, plus separate review, built-work spec and any remaining commit next steps when relevant. A standalone handoff reports to the user, suggests the next command when its scope covers the task and stops. A controlled handoff returns the seven-field outcome and evidence to lead for independent acceptance; lead selects subsequent steps and carries the checkpoint handoff forward.
