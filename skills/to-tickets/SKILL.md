---
name: to-tickets
description: Turn an approved feature spec, confirmed eligible root cause or selected review findings into executable local tickets, preserving existing decisions, dependencies and execution history; stop before implementation.
argument-hint: "[feature spec | root-cause | review report and selection]"
disable-model-invocation: true
---

# /to-tickets

Turn an approved feature spec, confirmed eligible root cause or selected review findings into bounded implementation tickets, then stop. For a root cause, read [cause input](references/cause-input.md). For review findings, read [review input](references/review-input.md). Apply the chosen input's eligibility and repeat gates, SAVE AND VERIFY and BOUNDARY AND HANDOFF below; the spec slicing steps apply only to spec input.

## ENTRY

Run on explicit invocation or within an explicit controlled scope. For a feature spec, read [spec input](references/spec-input.md) before consuming input or choosing the feature directory. Read relevant code, callers, tests, glossary/ADR entries and [project specs](references/project-specs.md) before proposing work. Validate current facts and distinguish them from assumptions. The source's existence, hash or ready label is not approval.

Before a durable task write, material question or handoff, read [task journal](references/task-journal.md). Keep an established feature's journal. An explicit controlled packet also requires [controlled run](references/controlled-run.md); a journal path alone activates no lead or automation.

## RECONCILE BEFORE SLICING

Read every existing `issues/*.md`, regardless of type or status, before proposing a breakdown. Inventory file names, numbers, scope, dependencies, branch fields, statuses, checked criteria, saved plans, comments and execution notes. Preserve existing files byte-for-byte on repeated covered input; their paths are the output, not templates to regenerate. New work appends after the highest existing number, including decision records in that count.

| Existing state | Action |
| --- | --- |
| Bare or Markdown-bold `Type:` field, including ready decision work | Preserve the entire file; exclude it from implementation execution and coverage claims. |
| Covered open implementation ticket, including `needs-info` or `ready-for-human` | Reuse unchanged; preserve its gates and execution history. |
| Covered `resolved` implementation ticket | Reuse unchanged; verify any result needed by new work in the working tree. A missing result stops the affected handoff, not permission to reopen it. |
| Covered `wontfix` implementation ticket | Preserve the rejection; renewed work needs an explicit concrete scope/revision decision. |
| Genuinely new authorized implementation scope | Append distinct tickets without changing existing files or dependencies. |
| Changed scope or graph incompatible with existing records | Show affected files and the proposed concrete revision, then stop for a decision before writing. |

General permission to save tickets does not approve replacing history. An explicitly approved revision applies only to its named changes; retain identities and execution records. Recheck source and existing issue bytes before saving; reconcile changed inputs instead of overwriting concurrent work.

## SLICE AND PROPOSE

Read [ticket rules](references/ticket.md) and their template before writing. Carry the spec's requirements, conditions, defaults, exclusions, integrated answers, reasons and testing requirements into the breakdown. Settled choices reopen only for contradictory evidence or an explicit revision request. Material uncertainty follows the stop rules in spec input; approval to save a draft never answers it.

Each ticket is one end-to-end behavior a user or API can exercise and demonstrate independently, sized for one fresh context window. Small work normally yields one ticket. Use observable positive and blocking acceptance criteria rather than an implementation task list. For a broad refactor, use expand, passing migration batches and contract; if intermediate tickets cannot pass, stop for a compatible breakdown.

Number new tickets in ascending dependency order. Map each prerequisite explicitly; unknown evidence is never `None`. Known open local prerequisites may gate later tickets; verify their identity and keep them in `Blocked by`. For an existing resolved prerequisite needed now, inspect its required result and a focused check in the actual working tree. Missing or unverifiable results stop the affected ready handoff; never implement, merge or cherry-pick the blocker while slicing.

Show proposed ticket titles, scope, criteria, dependencies, every `**Branch:**` line and created versus preserved paths before saving. Controlled tickets use the exact approved feature branch; standalone branch proposals follow the bundled rules. Reuse authorization covering that content and destination; otherwise obtain approval. A new substantive decision or incompatible graph revision returns to the user through lead in controlled execution.

## SAVE AND VERIFY

Save only authorized new tickets or specifically approved revisions in the resolved `issues/` directory. Copy the template's complete English `## Done when` verbatim, retaining `/plan`, branch, blocker-result, ready-for-human and no-commit semantics. Preserve existing execution text on repeats; do not migrate old tickets to a new executor.

Re-read saved files against the approved breakdown and current source; for review input apply its report-link exception. Verify numbering, dependency order, branches, criteria and exact execution block; compare all preserved issue bytes with their pre-write state. Journal the source identity/path/hash, local spec hash when applicable, approval/scope, created and reused paths, dependency evidence, limitations and no-op reuse. Pins belong in the journal and handoff without adding a Parent section or rewriting an unchanged spec/ticket.

## BOUNDARY AND HANDOFF

Writes are limited to authorized local implementation tickets, applicable task journal records and the narrowly permitted review ticket-link updates. Source/local specs, decision/map histories, product code, project/domain specs, Git/index, settings, installations and remote records remain unchanged. Ticket creation does not execute tickets or authorize review/commit.

Return source/spec pins, created or preserved paths, scope and precise remaining blockers. Suggest `/plan <ticket-path>` only for the first `ready-for-agent` non-decision implementation ticket with resolved, inspected prerequisite results and no material open questions. Open dependencies or missing evidence have no ready handoff; resolved/wontfix repeats are not new work. dev-exec is not this candidate's executor handoff. In a controlled run return the bounded outcome and evidence to lead, who chooses the next stage.
