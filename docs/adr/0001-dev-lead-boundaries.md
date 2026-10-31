# Explicit task orchestration within one active harness

The planned `dev-lead` skill lets the user delegate a development task through one explicit invocation. The user and the lead work together on questions and approve the feature plan. The lead checks and approves individual ticket plans against it. Within that plan, the lead autonomously organizes the needed investigation, ticket preparation and execution, review, project-spec, commit and integration stages. This deliberately extends the current manual handoffs: requiring a separate invocation for every stage would retain the coordination work the lead is intended to take over. How existing skill gates consume that authorization still needs an explicit integration design; this record does not change the installed contracts.

Return to the user when new evidence requires changing the task scope, external contract or an approved decision. Show the reason and the proposed change to the affected part of the plan. Routine technical choices, review fixes and integration conflicts that preserve the agreed behavior are handled autonomously and recorded in the journal.

Model selection prioritizes result quality. Use a strong suitable model for difficult decisions and final review; a faster suitable model may handle a clear, bounded task. Select the model and its supported reasoning effort from the available catalog, show the choices in the feature plan and honor explicit user constraints.

An approved plan may authorize dependency installation and migrations when it names both the action and its target environment. The lead may execute those agreed steps autonomously. Keep `ready-for-human` for actions the executor actually cannot perform; an action outside the plan returns to the user for agreement. The autonomous execution contract must carry that authorization explicitly.

The baseline workflow uses nxs alone, with [focused R&D](0004-dev-rnd-decision-only.md) available before ticket slicing. At startup, the lead checks which specific skills are available to the current harness and selects its route accordingly. Companion skills, including mattpocock/skills, may extend the workflow through [verified integrations](0006-companion-skill-integration.md); none is a required dependency. Do not cache whole-bundle installation as a boolean in global instructions: partial installations and harness visibility require checking individual skills. A deterministic discovery script is the proposed implementation; its integration with the live harness must be verified.

The user can still invoke skills independently and attach the lead at any stage. While coordinating, the lead relays executor questions to the user, grouping independent questions into rounds. It may answer from verified facts or already agreed decisions; new decisions requiring human judgment go back to the user with their options, recommendation and consequences.

Executors that change code or documents run in separate visible agterm sessions. Subagents serve bounded investigation and analysis, including internal review roles. Visibility lets the user inspect and intervene in execution while the lead coordinates the results.

Parallel code changes may use [isolated worktrees](0003-parallel-worktree-integration.md), with the results brought together on the feature branch. They follow a [verified sequential cycle and recovery](0005-bounded-runs-and-recovery-first.md); the full target workflow is not the initial implementation scope.

A task uses one active harness at a time. The user may stop it and resume the same feature in another harness. The [shared task journal](0002-shared-task-journal.md) supports that transfer and lets the lead join work started manually.

Codex is the first target for an end-to-end verified implementation; OpenCode follows as a second adapter. The existing nxs skills retain their current target clients. Compatibility claims for the lead must follow actual verification.
