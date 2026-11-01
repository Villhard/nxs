---
name: dev-exec
description: Plan and execute a clear request, implementation ticket, confirmed bug or selected review correction. Optionally decompose work into local tickets or save a handoff; implement only within an approved plan, with checks and authorized commit checkpoints.
argument-hint: "[request | ticket path | source context]"
disable-model-invocation: true
---

# /dev-exec

Plan and execute entrusted work in this session. Ticket production and saved handoffs are optional capabilities, not mandatory stages. A clear small request needs no feature spec, ticket, task directory or journal. Existing tickets retain their execution contract and history.

## INSPECT

Run on explicit invocation or an instruction that explicitly authorizes this operation. Read [execution context](references/execution-context.md) first: it owns input, feature location, ticket gates, branch selection and prerequisite evidence. Read relevant code, callers, tests, project instructions, glossary/ADR entries and [project specs](references/project-specs.md) before proposing changes. State observable success criteria and distinguish verified facts from assumptions.

Trace a reported failure before choosing its fix. For confirmed diagnosis or selected review corrections, apply the evidence gates in [work preparation](references/work-preparation.md#input-evidence). A review verdict alone is not authorization to fix. Reconcile prior task records with actual artifacts, Git and observable effects on continuation; recorded approvals and statuses are context, not new authority. Never automatically repeat an uncertain commit, migration or external action. Legacy coordination records activate no alternate execution mode; clarify conflicting instructions rather than recreating it.

## OPTIONAL DECOMPOSITION

For large work, propose independently checkable units with real prerequisites. Keep a small request in dialogue. When local tickets are useful or requested, read [work preparation](references/work-preparation.md) and the owned [ticket rules](references/ticket.md) and template. Show scope, criteria, dependencies, branches and created versus preserved paths before saving; obtain or reuse approval covering that content and destination. Preserve existing identities, history and execution prohibitions. Creating tickets does not approve their implementation. If the request is preparation-only, return the breakdown and stop; do not execute it.

## PLAN AND WAIT

Show a concrete plan: intended behavior, acceptance criteria, affected paths, implementation approach, relevant checks, write boundaries and material risks or unresolved evidence. Define meaningful, separately checkable logical blocks. By default, make them committable and propose a checkpoint with an explicit commit scope for each block; ask the user to approve those scopes unless already approved. Combine changes that cannot safely be separated. When commits are not selected or an existing ticket prohibits them, explicitly plan without checkpoints. Scale the plan to the task; no mandatory interview or plan file is needed.

Wait for human approval before implementation. Reuse an instruction already approving this concrete plan and scope without asking again. Feature approval, a ready ticket, a saved plan or a review verdict alone does not approve implementation. Resolve material uncertainty first. Reconcile changed inputs on continuation; substantial plan, scope, external-contract or settled-decision changes return for approval before the affected edits. Routine technical choices stay within the approved scope.

Built-in Plan Mode is optional. Respect its actual read/write limits and native permissions. If the active mode prevents a required action, report the restriction and stop that action; do not bypass it. This skill's approval instructions are not a technical write prohibition.

Approval of the plan authorizes its explicitly identified commits and scopes only when the user's approval covers them. Without authorization make no commit; stop an affected planned checkpoint and request its missing scope or authority. If commits are not selected, continue without checkpoints and hand off uncommitted changes. An existing ticket's `Do not commit` remains binding unless a specific revision of that ticket is separately approved; execute it without checkpoints rather than stopping merely because commits are prohibited.

## IMPLEMENT

After approval, recheck the plan, scope, branch, prerequisite evidence and unrelated changes, then implement the agreed work. Match surrounding conventions, reuse existing mechanisms and preserve validation/error handling. Remove code made unused by this change; leave unrelated cleanup alone. Preserve existing ticket execution text and history.

Apply [human-step gates](references/execution-context.md#human-steps) before any required dependency install, migration or external action. Direct approval covering the concrete action and target, plus native permissions, is sufficient; no coordination packet is needed. Authorization never substitutes for a checkable result. Record meaningful decisions or deviations in ticket Comments when applicable, otherwise in the result or an agreed handoff.

Writes stay within the approved task, applicable ticket execution fields and authorized optional tickets or handoff. Project `SPEC.md` and `.SPEC.md` belong only to `dev-spec` in normal task execution; name required spec follow-ups rather than editing them. Do not push, create a PR or alter user installations without separate authorization. Stop for a newly required authorization instead of expanding scope.

## CHECKPOINTS

For each planned checkpoint, run the completed block's necessary checks first. Record HEAD before the first checkpoint. Apply `dev-commit` in this same session within the approved scope and native permissions; follow its complete procedure, including index inspection, atomic grouping, preservation of foreign staged and working-tree changes and stop conditions. A checkpoint may produce multiple atomic commits, never an empty commit. Record each resulting commit and parent OID, approved scope and changed paths; verify identities, scope and preservation before the next block. If the skill or required permission is unavailable, stop the affected checkpoint and report it. Failed or missing required checks and unsafe separation do not establish a checkpoint. Reconcile uncertain commit effects against actual Git state and never replay them automatically.

Separate review follows the selected task rather than every checkpoint. Use `dev-spec` only when durable built-work contracts need recording. Neither operation starts automatically. A commit alone does not complete or accept a ticket.

## VERIFY AND REPORT

Check each acceptance criterion against actual behavior/artifacts. Run the project's required checks and relevant focused regressions; for a bug or selected review fix, add or update a regression check when practical. Follow explicit testing boundaries, including implementation-only work verified by another agent: do not run prohibited checks or claim they passed; report them as NOT RUN and leave required verification pending. Keep instruction/model observations proportionate: avoid matrices and tests that merely repeat prose. Record exact commands, results and limitations, inspect the final diff unless excluded by the approved instructions, and confirm preservation only to the extent actually checked. A source/packaging check does not establish live behavior, client registration or permission enforcement. Label live results as observations of their recorded cases; leave unavailable clients unverified.

For a ticket, identify the project's full test and linter commands from its instructions or other checkable project configuration, unless discovery itself is excluded. Run each required check within the authorized testing scope and record exact commands and results in Comments. If a required command is absent, cannot be identified, is prohibited or cannot run, record what is missing and leave the ticket unresolved; another focused check is not a substitute. Only after every applicable criterion and required check passes, check the criteria and set `**Status:** resolved`. Apply an existing review-origin ticket's explicit non-reproduction/wontfix rule only when that ticket grants it; preserve the remaining history. Otherwise keep a nonreproduced finding documented and unresolved, not silently fixed or rejected. For a clear request, report its result and verification limits without inventing ticket status.

Return changed paths, actual verification, unresolved acceptance criteria and limitations. For checkpointed work, include repository and branch, pre-checkpoint HEAD, each verified commit and parent OID, approved scope, changed paths and remaining staged, unstaged and untracked task changes. Identify foreign changes separately. Carry task requirements and the selected baseline so independent review and optional spec updates can cover the intended net work, not just the index. A checkpoint already on the normal base needs an agreed earlier baseline; ancestry or a path list alone proves no coverage. If evidence is missing or task ownership cannot be safely separated, report incomplete coverage without staging, stashing or rewriting foreign work.

Suggest `dev-review`, optional `dev-spec` and any authorized remaining commit only when relevant and their selected scope can cover the intended work; never start the next operation implicitly. Completion without a commit is valid. On request or an agreed stop, save concise resumable context using [handoff guidance](references/handoff.md) and its template; otherwise report in dialogue without creating an artifact.
