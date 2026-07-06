---
description: Produce expanded end-user / Confluence documentation for product users - use to write a structured how-to-use guide for a feature or product area, at the depth a user-facing doc needs.
argument-hint: "[feature | topic]"
---

# /nxs:doc-guide

Produce expanded, structured end-user documentation for product users: an end-user guide, a Confluence page, an onboarding doc. It explains how to use a feature or product area, at the depth and in the format a user-facing guide needs. Self-contained skill. Output language and response style come from global rules, not this file.

Audience is product users - the people who use the feature, plus support and onboarding readers. It is NOT a change record for reviewers or team (that is /nxs:doc-summary) and NOT applied-knowledge personal notes (that is /nxs:doc-note). The trigger is audience and depth: write a guide when someone needs to learn how to use the thing. Always propose a draft and wait for approval before writing anywhere.

Input: an optional feature or topic in the argument; if absent, ask what to document and for whom.

## PROCEDURE

1. Establish subject and audience: which feature / change / flow, and who reads it (end user, support, onboarding). Ask once if unclear.
2. Gather source material: the change, the feature behavior, supplied context, relevant code / config, and existing docs to extend.
3. Choose the document shape: scale it to the subject (overview + steps + examples + troubleshooting). Omit sections that do not apply.
4. Write for the audience: plain language, concrete examples, no internal jargon unless defined; describe observable behavior, not implementation.
5. Show the full draft and the proposed destination to the user.
6. Write only after the user confirms location and content.

## DOCUMENT SHAPE

Scale the structure to the subject; omit any section that does not apply:

- overview - what the feature is and what it is for, in user terms.
- step-by-step usage - the ordered steps to complete the task, each one an observable user action and its result.
- examples - concrete, realistic examples the reader can follow.
- troubleshooting - common problems and how to resolve them.

Keep the format the destination needs. For a Confluence page, use headings, ordered / unordered lists, and short paragraphs that map cleanly to the page structure.

## WRITING FOR THE AUDIENCE

- Plain language for product users; define any term you must keep.
- Concrete examples over abstract description.
- Describe observable behavior (what the user sees and does), not implementation.
- No internal jargon unless it is defined in the doc.

## OUTPUT

- Default: a chat draft. Show the full draft and the proposed destination before writing anything.
- Saved doc only after the user confirms both location and content, at the location the user confirms (`<path>/<slug>.md`). By default nothing is written to disk.

## SAFETY

- Read-only until the user approves the write.
- Publishing to an external system (Confluence, a docs site) is an outward-facing side effect. Produce the content for the user to publish; do not publish to an external service without an explicit, authorized mechanism and user confirmation.
- Never write secrets, tokens, .env values, private keys, or passwords into a guide; redact per `note-conventions`.

## CONVENTIONS

For shared writing and filing conventions - vault location, frontmatter schema, filename convention, and redaction of secrets - follow the `note-conventions` background skill when the saved doc lands in the vault. Do not restate them here.

## ROUTING

- /nxs:doc-guide - expanded end-user / Confluence documentation for product users, how to use a feature or product area (this skill).
- /nxs:doc-summary - a concise change record of one task (what / why / how) for reviewers and team, drawn from its branch / plan / commits.
- /nxs:doc-note - free-standing applied-knowledge personal notes (cheatsheet / howto / reference / gotcha) you already hold.
