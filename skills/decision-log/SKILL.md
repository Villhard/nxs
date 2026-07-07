---
description: The ADR gate and decision routing - decide whether a decision is significant enough to record and where its durable home is (ADR / plan or brief section / note / skip) - load on a significant decision to decide whether and where to record it (ADR gate). Background knowledge, not a user command.
user-invocable: false
---

# DECISION LOG

Load on a significant decision surfaced in a brainstorm, architecture review, prototype, or planning session. Workflow knowledge, not a user-invocable command. The main job is the GATE: decide whether a decision is worth recording at all and where its durable home is - not to spawn an ADR for every trifle.

## PROCEDURE

1. Collect the decision: what was decided, which real alternatives existed, why the selected one won, which tradeoffs were accepted, what was explicitly rejected.
2. Apply the ADR GATE - check all three criteria below. If at least one fails, choose a lighter target.
3. Route to the durable home (ADR / plan or brief section / personal note / nothing).
4. Confirm the target with the user, especially for an ADR or a note.
5. Write only after approval - recording is a durable write, never automatic.

Skip entirely for trivial, obvious, or easily reversible choices: a variable name, a minor library bump, a typical CRUD pattern, a local refactor.

## THE ADR GATE

A project ADR is justified only if all three criteria are true at the same time:

1. Hard to reverse - real cost to change later (data migration, a contract that breaks, a prolonged rollout). Not "we'll have to rewrite a function".
2. Surprising without context - a future reader will look and ask "why like this?". Without a record, reconstructing the motive is expensive.
3. Real trade-off - live alternatives existed and one was chosen deliberately. If the choice was obvious or there were no alternatives, it is not an ADR.

If at least one criterion fails, it is not an ADR. In doubt, default to the lighter level (plan-scoped over ADR; nothing over note). An ADR can always be added later; overdoing it clutters the project.

## ROUTING - where the decision lives

| situation | durable home |
|---|---|
| all three gate criteria met | project ADR |
| important for the current plan or brief, not for the future project | a section in the current plan / brief file |
| personal takeaway about an approach, tool, or typical pitfall | a personal note in your own vault |
| ad-hoc reasoning of a single session, without consequences | write nothing |

### Plan- or brief-scoped section

Add a section directly into the current plan or brief file:

```
## Decision: <short title>

**Decision:** ...
**Reason:** ...
**Explicitly not doing:** ...
```

Include context / options / tradeoffs only when needed for understanding. "Explicitly not doing" is mandatory for non-trivial decisions.

### Personal takeaway

Offer to capture it as a personal note in your own vault (gotcha / cheatsheet / howto). Such takeaways do not belong in the project repo.

### Temporary reasoning

Write nothing. The decision-log is not a journal of musings.

## ADR LOCATION

- If the project already has an ADR convention or directory (`docs/adr/`, `docs/architecture/decisions/`, `adr/`, `architecture/decisions/`, or similar) - follow it; do not invent your own.
- If there is no ADR directory - `docs/adr/` is the default. Create the ADR there; no separate approval is needed for the directory itself, but the decision to write an ADR at all is still gated by the three criteria.
- Filename: `docs/adr/NNNN-<slug>.md` - a zero-padded sequence number plus a short kebab-case slug (e.g. `docs/adr/0007-switch-to-jwt-sessions.md`).

## ADR FORMAT

Minimum ADR - a title plus 1-3 sentences (context, decision, why). That is enough:

```
# <Decision title>

<1-3 sentences: context, decision, why.>
```

Optional sections - add only if they carry new information:

- **Status** - proposed / accepted / superseded by ADR-NNNN;
- **Considered Options** - a short list of real alternatives, one line each;
- **Consequences** - non-trivial consequences (migration steps, constraints, what can no longer be done).

Do not turn the ADR into a template with empty sections. A short ADR beats a long one with ceremony. "Explicitly not doing" stays mandatory for non-trivial ADRs - either in the main text or inside Considered Options.

Example:

```
# Switch session storage from cookies to JWT

Part of the API is called from a mobile client, where a cookie-based session breaks due to CORS and redirects through the native webview. JWT gives stateless auth that survives a domain change; we accept the cost of key rotation and explicitly do not do silent refresh in the first iteration.
```

## RULES

- An ADR is a last resort, not a first one. In doubt -> not an ADR.
- "Explicitly not doing" is mandatory for non-trivial decisions (ADR and plan/brief-scoped). Otherwise in three months someone asks "and why not B?".
- If the project has an ADR convention, follow it; do not propose your own.
- Default ADR directory is `docs/adr/` when the project has none; do not invent a different one.
- Recording is a durable write done on approval, never automatic. Confirm before creating an ADR or a note.

## ANTI-PATTERNS

- an ADR for every small decision;
- an ADR for an obvious choice with no real alternatives;
- an ADR for an easily reversible decision;
- empty sections "for appearance's sake";
- a multi-page essay instead of three sentences;
- an ADR instead of documentation - if the reader needs to know how to use something, that is a README / docs, not an ADR;
- silently creating `docs/adr/` without the user's approval.
