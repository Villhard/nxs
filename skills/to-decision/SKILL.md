---
name: to-decision
description: Show and explicitly save approved conclusions or unfinished discussion; apply only approved glossary or ADR proposals within the invoked scope.
argument-hint: "[discussion | draft | decision path | domain-document request]"
disable-model-invocation: true
---

# /to-decision

Extract a proposed decision from discussion, drafts or supplied context, show it, and save only approved content. A direct domain-document request within this expressly invoked or controlled scope can produce only the requested glossary/ADR edits, without a wrapper artifact.

## ENTRY

Run on explicit invocation or within an explicit controlled scope. Read [discussion](references/discussion.md) and [domain modeling](references/domain-modeling.md) before extracting conclusions or domain proposals. Read [project specs](references/project-specs.md) for affected paths; project specs are evidence, never this skill's output. A missing explicit input stops the step.

Read [task journal](references/task-journal.md) before the first durable task write, question or handoff. Taskless domain work and declined write proposals create no journal. An existing task keeps its journal for required semantic records. An explicit controlled packet additionally requires [controlled run](references/controlled-run.md); a journal path alone activates no lead or automation.

## EXTRACT AND SHOW

1. Read source context and any existing target. Carry forward scope, agreed decisions, proposals, reasons, rejected alternatives, sources, feedback and open questions. Distinguish facts from assumptions. Apply the shared resume rules rather than interviewing again about settled decisions.
2. Resolve the destination from an explicit path or existing feature/artifact first. For a new local decision, default to `.scratch/<feature-slug>/research/decision.md`, with a short lowercase hyphenated slug. Ask if multiple features or different existing targets make the destination ambiguous. Existing artifacts and their paths win over defaults. Never convert a map's typed decision tickets into implementation work.
3. Read the [decision template](assets/decision.md). Show the proposed content and exact destination, including its agreed or unfinished state. For a repeat, show the concrete revision instead of regenerating the file. Show optional glossary/ADR proposals as separate concrete entries/diffs under the domain rules. A domain-only request skips the decision template and destination.
4. Identify the approval that covers each proposed write. Reuse prior approval only for that exact content, destination and scope. Otherwise ask for approval and stop before writing. A save request authorizes this preparation; it does not approve unseen conclusions. The user may approve preserving unfinished state without answering its open questions. Declining saves no decision/domain record.

## SAVE AND VERIFY

Write only approved decision content and domain entries. Check the target again before writing: if it changed since the proposal, reconcile the new bytes and obtain approval for any uncovered revision. Preserve existing decisions, feedback, links, manual additions and history; a broad request to save never authorizes deleting them. Reuse an identical result without a write. Record revisions explicitly when approved changed content supersedes earlier conclusions.

An explicitly authorized auto handoff may supply the final local standalone HTML defense. Verify that supplied file exists and link it from the approved decision; preserve its path and content. Missing final defense evidence blocks that claimed handoff. This skill does not enable auto coordination or generate a defense. HTML approval alone requests no decision save and approves no unseen Markdown/domain content.

Re-read the saved files and verify the approved content, state, source links and preservation of preexisting content. Report written paths, preserved/no-op results, declined entries and exact remaining questions. Journal applicable decisions, approvals, checks and handoff with source identity and artifact hashes. Never treat the journal or a saved state label as independent approval evidence.

## BOUNDARY AND NEXT

Permitted writes are approved decision artifacts, approved glossary/ADR records and applicable task journal records. Keep product code, feature specs, tickets, project specs, Git/index, settings and installations unchanged. A domain request grants no implementation authority.

Suggest `to-spec <decision-path>` only as a separately requested next stage, carrying the source identity, approved conclusions, scope and remaining questions. Report if that candidate is not installed or verified. Open questions remain open after saving; neither a saved artifact nor approval implicitly starts a spec, tickets or implementation.
