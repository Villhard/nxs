# dev-exec

## Purpose

Plan and execute an entrusted request, implementation ticket, confirmed bug or selected review correction through inspection, approved scope, implementation and verification. Optional decomposition, local tickets, saved handoffs and authorized checkpoints serve the task; a clear small request needs no directory, artifact or mandatory interview. Review and built-work project specs remain separate operations.

## Ownership

Own execution context, implementation-plan approval, optional decomposition, ticket rules/template and handoff guidance/template. Bundle project-spec reader rules owned by `dev-spec` without depending on another installed skill. Commit safety belongs to `dev-commit`, independent review to `dev-review`, and normal project-spec writes exclusively to `dev-spec`.

## Boundaries

Explicit invocation or an instruction explicitly authorizing the operation permits inspection and planning. Implementation requires approval of the concrete plan and stays within the entrusted task and applicable ticket execution fields. Optional ticket/handoff saves need authorization covering content and destination. Preserve foreign working/index changes and existing task history. Checkpoints require explicit commit-scope approval and native permissions; push, PR and installation changes need separate authorization. Never start review/spec implicitly or use a saved record as new consent.

## Contracts

- Resolve identity from explicit input or established context, never a branch alone. Missing/unreadable input stops. Existing records provide context, not new authority. Remote input needs source, decision and dependency evidence; unknown/unmapped blockers stop affected work and local preparation changes no remote state.
- Optional tickets describe independently checkable end-to-end units with real prerequisites. Read all existing issues first; preserve covered open, resolved and rejected work, branches, numbering, execution text and prohibitions. Append genuinely new scope only after the highest existing number; incompatible revisions need concrete approval. No mandatory feature spec, selection snapshot or ticket is introduced.
- Confirmed diagnosis requires supported cause and intended-behavior agreement where needed. Selected review corrections retain source/scope evidence, verdict distinctions, selection and explicit fix authorization. Verify/reproduce before editing, add regressions when practical and document non-reproduction rather than claiming a fix. Existing ticket exceptions remain local to those tickets.
- Show a concrete plan and wait for human approval, reusing approval only within its actual scope. A ready ticket, saved plan, feature approval or review verdict alone grants no implementation authority. Substantial plan, scope, external-contract and settled-decision changes return for approval. Native mode restrictions remain binding.
- Define separately checkable blocks and propose explicitly scoped checkpoints by default for committable blocks; combine inseparable changes. Plan without checkpoints when commits are not selected or a ticket prohibits them. After necessary checks pass, apply `dev-commit` in the same session and verify commit/parent identities and preservation before continuing. Missing authority, permission, required checks or safe separation stops the affected checkpoint. Preserve `Do not commit` unless a specific revision is separately approved. No commit is required to finish implementation.
- Apply ticket status, blocker-status and clarification gates before implementation. Select the ticket branch before inspecting actual prerequisite results. Status, branch names and ancestry prove no result; a carried or squashed result may pass by current-tree evidence, a reverted result does not. Record missing evidence and stop without implementing, merging or cherry-picking the blocker.
- An install, migration or external action needs direct approval covering the concrete action/target plus native permissions. Missing authority or unverified results block the affected work with expected evidence. Preserve the human-step status round trip and verify actual results on return without repeating the action.
- Verify applicable criteria and required project checks before resolving a ticket. Respect explicit testing limits, including implementation-only assignments; report prohibited/unavailable checks as NOT RUN and leave required verification unresolved. Clear requests report actual outcomes without invented status. Preserve meaningful decisions and exact results in applicable Comments or the result.
- A result or optional saved handoff separates accepted, open and unverified state, preserving scope, requirements, sources, actual Git/checkpoint state, verification and next authorized action. Intended-work coverage includes relevant checkpoints and remaining staged, unstaged and untracked task changes; an agreed earlier baseline may be needed. Foreign ownership or uncertain coverage is a blocker, not permission to alter foreign state. Never replay an uncertain commit, migration or external effect.

## Known limitations

Source contracts establish neither native registration nor permission enforcement. A disposable omp 18.15.0 source-skill smoke returned a plan from an old `Type: task` source without changing it or stopping solely on its metadata. This was prompt-only, not a sandbox; implementation, checkpoints and other clients remain unverified. Existing task data, worktrees and user installations are not migrated by source edits. Saved context promises no cross-client session recovery.
