# Seven skills with direct, explicitly authorized handoffs

Status: accepted. Date: 2026-11-01.

This decision supersedes the earlier lead/auto coordination, mandatory shared-journal and artifact-command design. It records a source-contract transition, not publication, installation migration or a live compatibility result.

## Context

Separate commands for every evidence method and saved record made simple work look like a mandatory workflow. The useful engineering actions remain needed, but their entry points and coordination protocol are not prerequisites for every task. Investigation, implementation, independent review, project-spec recording and commit safety have different approval/write boundaries worth retaining.

## Decision

Retain exactly seven independently installable skills:

| Owner | Intent and result |
| --- | --- |
| `rnd-grill` | Investigate uncertainty, discuss alternatives and agree on a solution; directly save useful approved preparation/domain records on request. |
| `rnd-debug` | Reproduce a failure, establish intent and confirm its cause or save missing evidence before choosing a fix. |
| `dev-exec` | Establish acceptance criteria, obtain approval for a concrete plan, optionally decompose, implement and verify. Own optional tickets and handoff saving. |
| `dev-review` | Independently review intended changes, verify findings and return selected corrections without creating tickets. |
| `dev-spec` | Optionally record material built-work contracts; remain the exclusive normal writer of project `SPEC.md` and `.SPEC.md`. |
| `dev-commit` | Make explicitly authorized atomic commits while preserving unrelated staged and working changes. |
| `nxs-setup` | Independently audit and apply an exact approved setup package, or report relevant prerequisites without writes. |

```text
rnd-grill ----+
              |
rnd-debug ----+--> dev-exec --> dev-review --> [dev-spec] --> dev-commit
              |       ^             |
clear request +       +-- selected corrections

nxs-setup: separate support, not a development stage.
```

The spec stage is conditional. A direct authorized review of existing changes is also valid. Arrows never implicitly invoke a skill or create authorization. Reuse explicit approval covering multiple operations only within its actual scope. Execution presents a concrete plan and waits for applicable approval. Checkpoint commits may occur during execution only with explicit commit-scope approval through the complete commit safety procedure; no commit is required to finish implementation. Existing `Do not commit` remains binding.

Small clear work requires no decision, feature description, ticket, task directory or journal. Save only useful authorized artifacts, reusing established paths before `.scratch/<feature>/` defaults. Agreement alone saves nothing. Content/destination approval, source preservation and concurrent-change reconciliation still apply. Domain-record approval is separate from other saves. Isolated prototypes require concrete authorization and remain retained; success authorizes no production transfer, reuse or deletion. Questionnaire preparation authorizes no contact or sending.

Ordinary review covers intended net work: relevant committed checkpoints and remaining staged, unstaged and untracked task changes. A nonempty index cannot narrow it. Pin baseline, requirements and actual source view first; preserve explicit narrower scope and its exclusions. Review and spec recording stop for omitted work or uncertain ownership/coverage without staging, stashing or rewriting foreign changes. Work already on a normal base needs an agreed earlier boundary. Finders and the independent verifier remain, with native restrictions described honestly and mandatory state comparisons preserved. Their presence is not a separate lead workflow.

Selected findings carry report identity and source/scope evidence directly to execution. A verdict or selection is not implementation approval. Confirm/reproduce before fixing and use regressions where practical; a nonreproduced finding stays documented and unconfirmed. No selection snapshot or mandatory fix ticket is introduced.

An install, migration or external action requires concrete action/target approval plus native permissions directly, not a lead packet. Verify prerequisites and returned human-step results in the actual working tree/environment; status is not evidence. Reconcile interrupted or uncertain effects before retrying. An optional handoff records approved scope, accepted/open/unverified state, verification, actual Git/checkpoints and next authorized action, without promising cross-client session recovery.

## Consolidation and removal

The following names are historical migration context, not supported command routes or aliases:

| Former commands | Retained capability |
| --- | --- |
| `rnd-map`, `rnd-research`, `rnd-prototype`, `rnd-audit`, `rnd-design` | Optional `rnd-grill` dependent-question discussion, attributable research, isolated experiment, requested survey and selected-boundary design. No mandatory typed decision state machine. |
| `to-decision`, `to-spec`, `to-questionnaire` | Direct approved `rnd-grill` decision/unfinished-state, feature-description and participant-question saving. |
| `to-tickets`, `to-handoff` | Optional `dev-exec` decomposition/tickets and resumable handoff. |
| `nxs-lead`, `nxs-retro` | Removed without replacement commands; no lead/auto or retrospective stage. |

No hidden routing skill, compatibility alias, nested client runner, background hook or universal workflow engine replaces these commands. Installed copies, global instructions, settings, locks, existing tickets, journals, prototypes and worktrees are not automatically changed or cleaned up.

## Superseded decisions and retained principles

Earlier ADR files remain unchanged as historical records. For current contracts, this record takes precedence as follows:

| Earlier record | Superseded scope | Retained principle |
| --- | --- | --- |
| [0001](0001-dev-lead-boundaries.md) | Lead-owned routing, technical approval, worker launch and workflow progression. | Scope/decision approval, concrete environment authority and evidence-limited compatibility. |
| [0002](0002-shared-task-journal.md) | Mandatory shared journal and its setup injection/transfer protocol. | Preserve useful context and reconcile it against actual artifacts/state. |
| [0003](0003-parallel-worktree-integration.md) | Lead-managed parallel branches, integration and commit ownership. No replacement integration mode is introduced. | Prerequisite results must exist where work runs; isolated success does not prove combined behavior. |
| [0004](0004-dev-rnd-decision-only.md) | Separate decision-only mode and later ticket-slicing chain. | Focused investigation can end with conclusions and open questions, without implementation. |
| [0005](0005-bounded-runs-and-recovery-first.md) | Autonomous lead cycle, structured worker envelope, manual-skill journaling and recovery machinery. | Completion needs actual evidence; uncertain effects are not blindly replayed. |
| [0006](0006-companion-skill-integration.md) | Lead runner/integration and shared-journal prerequisites. | No required companion dependency or unverified compatibility assumption; no implied installation change. |
| [0007](0007-skill-names.md) | Fixed `dev-` prefix and former catalog scope. Retain the approved seven names without new aliases. | Short recognizable collision-aware names; rename only for a real intent problem. |
| [0008](0008-native-subagent-coordination.md) | Lead delegation and append-only coordination-state requirements. | No custom orchestration runtime or nested client fallback; native review remains capability-dependent and evidence-scoped. |

## Consequences

Runtime guidance stays in self-contained skills, not root documents. `rnd-grill` owns preparation templates; `dev-exec` owns ticket rules/template and handoff; `dev-review` owns review resources/roles; `dev-spec` owns project-spec reader/template; `dev-commit` owns commit safety; setup owns setup/writing resources. Copy only genuinely shared resources to actual consumers and keep them identical.

Historical ADRs, releases and client observations remain history, not current-route proof. Updated source/packaging checks, focused behavioral observations and light/dark diagram verification are separate evidence. This implementation-only documentation change claims none of them passed. The contract change warrants minor version `0.77.0` under the project's `0.x` rule; publication and installation cutover require separate authorization.

Rejected alternatives: keeping aliases or hidden mandatory modes preserves the old command surface; requiring all saved artifacts recreates the pipeline; replacing the lead with another coordinator recreates its complexity; dropping independent reviewer protections or commit safety loses useful boundaries rather than simplifying entry.
