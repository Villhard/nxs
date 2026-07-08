---
description: The shared documentation-draft contract - the local-draft path scheme, Confluence as the durable home and publish target, and the pre-publish scrub of secrets and identifying details. Background knowledge, not a user command.
user-invocable: false
---

# DOC-DRAFT KERNEL

Load when producing a documentation artifact meant to live in Confluence. Workflow discipline, not a user-invocable command. Single shared kernel; injected by `/nxs:techdoc` and `/nxs:userdoc`.

## ARTIFACT

A documentation artifact is a local draft, never the durable copy:

- Write it to `docs/<kind>/<slug>.md`, where `<kind>` is the consuming skill's document kind (`techdoc`, `userdoc`).
- The path is a local draft in the gitignored `docs/`, not committed into code.
- Durable / shared home is Confluence: you edit the draft and publish it there. Nothing is left in the codebase.

## DRAFT-BEFORE-WRITE

A durable write. Show the full draft and the destination, and write only after the user approves the content and location. Read-only until then.

## PRE-PUBLISH SCRUB

Before a draft is publishable, strip anything that must not leave the repo:

- Never write secrets, tokens, `.env` values, private keys, or passwords into a doc.
- Strip local paths, private remotes, real ticket ids, and colleague names.

Publishing to Confluence or a docs site is an outward-facing side effect. Produce the content for the user to publish; do not publish externally without an explicit, authorized mechanism and user confirmation.
