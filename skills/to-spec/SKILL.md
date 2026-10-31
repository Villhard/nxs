---
name: to-spec
description: Turn a saved decision or clear request into a local feature spec, with explicit draft questions and acceptance checks; ticket slicing is a separate step.
argument-hint: "[decision path | request | spec path | tracker key]"
disable-model-invocation: true
---

# /to-spec

Produce a feature spec from agreed decisions or a clear request, then stop. A requested draft can preserve uncertainty; it does not make unresolved work ready for tickets.

## ENTRY

Run on explicit invocation or within an explicit controlled scope. Before reading input, read [feature source](references/feature-source.md) for source validation, location, remote dependencies and preservation. Read [project specs](references/project-specs.md) for affected paths and relevant glossary/ADR entries as evidence. These records remain unchanged.

Before a durable task write, material question or handoff, read [task journal](references/task-journal.md). An existing task keeps its journal; an empty or declined new proposal creates none. An explicit controlled packet additionally requires [controlled run](references/controlled-run.md); a journal path alone activates no lead or automation.

## VALIDATE AND SHAPE

1. Read the source and existing target before proposing content. Check relevant current code, callers, tests and recorded decisions; distinguish verified facts from assumptions. Read [discussion](references/discussion.md) when extracting or resuming decisions, or when material choices remain. Preserve agreed conclusions, proposals, feedback and unanswered questions separately. A clear request needs no forced interview; settled choices reopen only for new contradictory evidence or an explicit request.
2. Carry forward requirements, conditions, defaults, answers, scope limits, rationale/source links and testing requirements. Resolve discoverable facts yourself. Present material contradictions or missing choices with their consequences and wait for the user's answer, relayed by lead in controlled execution. An explicitly requested draft may retain them as specific `[NEEDS CLARIFICATION: <question>]` entries; permission to save uncertainty does not answer it.
3. Read the [feature template](assets/spec.md). Use its seven permitted `##` headings in order: keep Problem Statement and Solution; omit another section only if empty. Integrate answers and acceptance checks into Solution. Implementation Decisions holds current findings, reasons, constraints and project-record links; Testing Decisions holds relevant checks and testing requirements; Out of Scope preserves exclusions. Further Notes holds source identity/path or URL and hash, approval/scope evidence, rejected alternatives with reasons, feedback and any question/answer history. On byte-identical reuse or copy, the journal and handoff carry source pins without rewriting the spec. Keep draft state and open questions within those headings, without adding a status heading.

## PROPOSE, SAVE AND VERIFY

Show the proposed spec, exact destination and whether material questions or dependencies prevent a ready handoff. Reuse authorization already covering that content, destination and scope; otherwise obtain approval before writing. A request to prepare a spec does not approve unseen substantive choices. For an existing different spec, show the concrete revision and obtain approval covering it. Reuse an identical result without rewriting.

Check source and target again before saving. If either changed, reconcile the current content and obtain approval for uncovered revisions. Preserve manual additions and history; broad save permission never authorizes deleting them. Save only the authorized local spec, with an explicit draft label when requested. Re-read it and verify source pins, integrated answers, requirements, exclusions, acceptance checks and remaining questions against the approved proposal. Journal the result and evidence, including no-op reuse and readiness limits.

## BOUNDARY AND HANDOFF

Permitted writes are the authorized local feature spec and applicable task journal records. Keep decision/map histories, tickets, domain/project specs, product code, Git/index, settings and installations unchanged. A saved decision is context, not an implementation ticket or project spec.

Report the spec path/hash, source identity, scope, verified dependencies and precise remaining questions. Material unknowns, contradictory evidence and unknown/unmapped blockers prevent a ready-to-tickets handoff, even after draft approval. Known open mapped dependencies remain explicit; verify needed blocker results in the working tree rather than inferring them from status alone.

Suggest `to-tickets <spec-path>` as a separate step only when readiness evidence supports it; report if the intended consumer is unavailable or unverified. Start no ticket slicing or implementation outside separately covering authorization. In a controlled run, return the outcome and evidence to lead, who selects the next stage.
