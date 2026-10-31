# to-decision

## Purpose

Make an approved discussion result durable while retaining why it was chosen and what remains unsettled. An approved unfinished result is valid context, not approval to resolve its questions or begin implementation.

## Boundaries

Explicit invocation or an explicit controlled scope permits preparation of a save. Writes are limited to approved decision artifacts, approved glossary/ADR entries and applicable task journal records. Feature specs, tickets, project specs, product code, Git/index, settings and installations remain outside this operation.

## Contracts

- Show proposed content and its exact destination before writing; reuse approval only when it covers that content, destination and scope. A save request alone approves no unseen conclusions. Domain proposals have separate approval boundaries; a direct approved domain-document request needs no wrapper decision or new feature directory.
- Preserve scope, reasons, rejected alternatives, source links, feedback and the distinction between agreed conclusions, proposals and open questions. Existing artifact paths take precedence over the new-decision default `.scratch/<feature-slug>/research/decision.md`.
- A repeat preserves manual additions and earlier rationale. An identical result is a no-op; a revision requires approval covering its concrete changes, including changes to the target since the proposal. A broad save request never authorizes deleting existing content.
- Use the bundled discussion/domain rules owned by `rnd-grill` without requiring its installation. A saved state label or journal record is not independent approval evidence; verify the saved content and preservation against the approved proposal.

## Known limitations

An explicitly authorized lead handoff can supply an existing final local HTML defense to link from the approved decision. Missing defense evidence blocks that claimed handoff. This skill neither creates the defense nor enables auto coordination; HTML approval alone requests no save. The suggested `to-spec` handoff is a separate request and does not establish that the next-stage candidate is installed or verified.
