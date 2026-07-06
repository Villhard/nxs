---
description: Shared conventions for writing notes, task-docs, and source-backed notes - note types, vault location, frontmatter schema, filename and safety rules - load when writing a note, doc, or summary. Background knowledge, not a user command.
user-invocable: false
---

# NOTE CONVENTIONS

Load when writing a note, doc, or summary. Shared conventions for `/nxs:doc-note`, `/nxs:doc-summary`, `/nxs:doc-guide`, `/nxs:doc-handoff`, and `/nxs:std-source`. Workflow knowledge, not a user-invocable command.

## THREE VAULT ARTIFACTS

- **note** (`/nxs:doc-note`) - applied knowledge: cheatsheet / howto / reference / gotcha. Full type detail: `reference/note-types.md`.
- **task-doc** (`/nxs:doc-summary`) - a snapshot of work on a specific task (what / why / how / impact).
- **source-backed note** (`/nxs:std-source`) - one self-contained note learned from external material.

## WHERE NOTES LIVE

- The Obsidian vault. Default root `~/Documents/notes` (placeholder `{{obsidian_vault_path}}` in harness config).
- `/nxs:doc-note` and `/nxs:doc-summary` write only to `_inbox/` (the default location). From `_inbox/` the user moves the file to the right context or deletes it. Do not write directly to `work/`, `study/`, `_system/`, or other top-level vault folders.
- `/nxs:std-source` writes an approved flat note directly to the vault root by design (not `_inbox/`).
- **Vault schema wins.** If the vault's root `AGENTS.md` / `CLAUDE.md` defines its own schema (allowed `type` values, field set, where finished notes live), that is the source of truth - follow it. Absent that, the fallback is `_inbox/<slug>.md`.

## ASK BEFORE WRITING

- Default: ask the user before writing. Ask especially when the knowledge is borderline (applied vs vague), the type is unclear, or the content is sensitive (names, tokens).
- In doc mode always show the draft and wait for approval.

## WHAT BELONGS

Applied knowledge only - what the user will actually open in a specific future situation. Do not save:

- conceptual essays and write-ups;
- vague ideas without application;
- temporary information (outdated within a week);
- secrets, tokens, .env values;
- large chunks of code without context;
- personal task lists;
- information already in the project README / docs.

Boundary: concept and term definitions belong in the domain glossary (`docs/.ai/domain-language.md`), not in a note. A note captures durable applied knowledge, not a running scratchpad.

## FILE NAMING

**Note mode:**

- lowercase kebab-case;
- Latin script (transliterate Cyrillic);
- `.md` extension;
- a descriptive name: `cheatsheet-grep.md`, `howto-fix-merge-conflict.md`, `gotcha-timezone.md`.

**Doc mode:**

- `YYYY-MM-DD.task.[<id>].<slug>.md` (with identifier);
- `YYYY-MM-DD.task.<slug>.md` (without identifier);
- `<id>` preserves the case the user entered (`PROJ-1234` or `proj-1234`);
- `<slug>` - kebab-case, Latin script, Cyrillic transliterated.

## FRONTMATTER

**Note mode** - fallback template. The vault schema wins when it defines one (array style, allowed `type` values, field set). Use inline arrays:

```yaml
---
type: cheatsheet | howto | reference | gotcha
aliases: []
tags: []
updated: YYYY-MM-DD
---
```

A supplied note kind maps to one allowed `type`. When the vault defines its own set of `type` values, choose from that set.

**Doc mode** (task-doc):

```yaml
---
type: task-doc
task: <jira-key or slug or null>
plan: <path to plan in repo or null>
commits: [<short-hash>, ...]
aliases: []
tags:
  - type/task-doc
updated: YYYY-MM-DD
---
```

A task-doc also has an `IMPACT ON CONTEXT` section - a placeholder for later ingest by the user. The applied-knowledge filter is not applied to a task-doc. It is raw material: the user moves it from `_inbox/` to `<context>/raw/` and ingests it into their wiki.

**Flat note from source:**

```yaml
---
aliases: []
tags: []
updated: YYYY-MM-DD
---
```

No `type` field is used for ordinary flat notes from source.

## SOURCE MODE

`/nxs:std-source <source> [focus]`:

- the source is detected from the argument shape: pasted text or a local `.txt` / `.md` / `.srt` path;
- runs source intake before drafting: acquire / extract, denoise, segment into useful contexts, detect conflicts and uncertainty, then choose or ask for focus when needed;
- proposes candidate note directions when the source has multiple useful contexts and no focus is given;
- writes one approved self-contained flat note to the vault root; does not use note types;
- a bounded input adapter, not broad source triage, transcription, OCR, web fetching, or media ingestion.

## SAFETY AND FILING

- Never save secrets, tokens, or `.env` values. When content is sensitive (names, tokens), ask before writing and redact.
- Do not duplicate information already in the project README / docs.
- Notes land flat in `_inbox/` (or the vault root for source notes). There is no automatic cross-linking - the user files and links them later.

## REFERENCE

- `reference/note-types.md` - the four note types (cheatsheet / howto / reference / gotcha): when to use each, internal structure, examples, choose-table, and anti-patterns.
