---
description: Produce end-user documentation for product users - a how-to-use guide for a feature or product area, at the depth a user-facing doc needs. A local draft published to Confluence per the `doc-draft` kernel.
argument-hint: "[feature | topic]"
---

# /nxs:userdoc

Produce structured end-user documentation for product users: a how-to guide, a Confluence page, an onboarding doc. It explains how to use a feature or product area, at the depth and format a user-facing guide needs. Self-contained skill. Output language and response style come from global rules, not this file.

Audience is product users - the people who use the feature, plus support and onboarding readers. This is user-facing, not technical documentation for programmers (that is `/nxs:techdoc`). The trigger is audience and depth: write a guide when someone needs to learn how to use the thing. Always propose a draft and wait for approval before writing.

Input: an optional feature or topic in the argument; if absent, ask what to document and for whom.

## PROCEDURE

1. Establish subject and audience: which feature / flow, and who reads it (end user, support, onboarding). Ask once if unclear.
2. Gather source material: the feature behavior, supplied context, relevant code / config, and existing docs to extend.
3. Choose the document shape: scale it to the subject (overview + steps + examples + troubleshooting). Omit sections that do not apply.
4. Write for the audience: plain language, concrete examples, no internal jargon unless defined; describe observable behavior, not implementation.
5. Show the full draft and the destination.
6. Write only after the user confirms location and content, then handle the draft per the `doc-draft` kernel: path scheme `docs/userdoc/<slug>.md`, Confluence as the durable home, pre-publish scrub.

## DOCUMENT SHAPE

Scale the structure to the subject; omit any section that does not apply:

- overview - what the feature is and what it is for, in user terms.
- step-by-step usage - the ordered steps, each an observable user action and its result.
- examples - concrete, realistic examples the reader can follow.
- troubleshooting - common problems and how to resolve them.

Keep the format the destination needs. For a Confluence page, use headings, lists, and short paragraphs that map cleanly to the page structure.

## WRITING FOR THE AUDIENCE

- Plain language for product users; define any term you must keep.
- Concrete examples over abstract description.
- Describe observable behavior (what the user sees and does), not implementation.
- No internal jargon unless it is defined in the doc.

## ARTIFACT AND SAFETY

The draft contract - `docs/userdoc/<slug>.md` path scheme, Confluence as the durable home, read-only-until-approval, and the pre-publish scrub - comes from the `doc-draft` kernel. This skill does not restate it.

## NEXT

Technical documentation for programmers -> `/nxs:techdoc`.
