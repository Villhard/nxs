---
description: Save applied-knowledge notes (cheatsheet / howto / reference / gotcha) to the vault inbox - use when knowledge you already hold is worth reopening in a specific future situation.
argument-hint: "[what to capture] [type]"
---

# /nxs:doc-note

Save applied knowledge you already hold to the vault inbox as a short, reusable note. Self-contained skill. Output language and response style come from global rules, not this file.

Use when knowledge worth keeping has emerged: after debugging a nontrivial bug -> gotcha; after learning a new tool -> cheatsheet; after settling on a working recipe -> howto; when a discovered fact will be needed later -> reference. Inputs: what to capture + content + (optional) type, or nothing (then ask).

## APPLIED-KNOWLEDGE FILTER

Save only applied knowledge the user will actually reopen in a specific future situation, in one of four kinds: cheatsheet, howto, reference, gotcha. Favor the non-obvious (not on the first page of the docs), the proven-in-practice, and the compact.

Do NOT save; refuse or redirect instead:
- concept essays and explanations (that is /nxs:std-explain);
- vague ideas with no applied payoff;
- temporary or task-scoped info that is stale in a week;
- personal task lists / TODOs;
- info already in the project README or docs.

If the request is borderline (applied vs vague), say so and ask before writing.

## PROCEDURE

1. Understand what knowledge is being captured.
2. Apply the FILTER. If it is not applied knowledge, refuse or redirect.
3. Pick or confirm the note type: cheatsheet / howto / reference / gotcha. Ask when the type is unclear. Map an unsupported kind to the nearest allowed vault type per `note-conventions`.
4. Ask before writing - always for borderline applied-vs-vague content, an unclear type, or sensitive content.
5. On approval, write to the vault inbox.
6. Tell the user the file path.

## NOTE TYPES

- cheatsheet - a short cheat sheet of the most frequent operations.
- howto - a step-by-step recipe for a specific task.
- reference - a fact / list / table for later lookup.
- gotcha - a pitfall that is easy to step into.

## CONVENTIONS

For the note conventions - note-type definitions and structure, vault location, frontmatter schema, filename convention, and redaction of secrets - follow the `note-conventions` background skill. Do not restate them here.

- Default artifact path `~/Documents/notes/_inbox/<slug>.md`; the target location is vault-schema-driven and comes from `note-conventions` when the vault declares a schema.
- The written `type:` value must be one of the vault's allowed types; when the chosen kind is not allowed, map it to the nearest allowed type per `note-conventions`.

## APPROVAL AND SAFETY

- Read-only until the user approves the write.
- Ask before writing, especially for borderline applied-vs-vague content, an unclear type, or sensitive content.
- Never write secrets, tokens, .env values, private keys, or passwords into a note; redact per `note-conventions`.
- Write to the vault inbox (`_inbox/` by default) only after approval, then report the path.

## ROUTING

- /nxs:doc-note - save applied knowledge you already hold (this skill).
- /nxs:std-source - learn from an external source you supply, then optionally save a source-backed note.
- /nxs:doc-summary - assemble a durable task-doc snapshot from the current task's branch / plan / commits.
