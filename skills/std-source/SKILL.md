---
description: Learn from external material (book / course / article / transcript) supplied as pasted text or a local .txt / .md / .srt path - denoise, extract signal, and optionally save one self-contained vault note. Use when you have an external source to ingest and distill.
argument-hint: "[source text | .txt/.md/.srt path] [focus]"
---

# /nxs:std-source

Turn supplied external source material into extracted, denoised knowledge and, on approval, one self-contained root note in the vault. Self-contained skill. Output language and response style come from global rules, not this file.

This is a bounded input adapter for one `/nxs:std-source` action. It does not imply broad `doc` generation. It stays read-only until the user approves the note write.

## SOURCE INTAKE

Run the full intake before drafting anything:

1. Detect the source from the argument shape: pasted text, a chat transcript, or copied documentation used directly; or a local file path where only `.txt`, `.md`, or `.srt` is accepted. Reject unsupported input before processing.
2. Acquire / extract the text and read it.
3. Denoise: drop repeated greetings, filler, timestamps, speaker churn, transport metadata, conversational logistics that do not help a future reader, and duplicated blocks.
4. Segment into useful contexts / topics.
5. Detect signal vs noise, decisions, open questions, contradictions, and uncertainty; mark uncertainty briefly when the source is unclear.
6. If several useful contexts exist and no focus was given in the argument, propose candidate note directions before narrowing to one note. If a focus was given, narrow to it.

## BOUNDARY (bounded adapter)

- Support: pasted text; `.txt`; `.md`; `.srt`; an optional focus after the source argument; an optional vault path and title given in natural language ("vault: <path>", "title: <t>").
- Do NOT support: audio, video, images, screenshots, PDF, cloud transcription, web fetching, API calls, or any file type other than `.txt` / `.md` / `.srt`. This is not broad source triage, transcription, OCR, web fetching, or media ingestion.
- Unsupported source types block before analysis - do not attempt to process them.

## THE NOTE

After intake and approval, `/nxs:std-source` writes exactly ONE self-contained note directly to the vault root - by design, not `_inbox/`. Candidate notes first only when the source holds multiple useful contexts and the user asks for them after seeing the first draft.

- Keep the note self-contained; prefer reusable meaning over meeting minutes.
- Ground everything in the supplied source or in what the user provided: record provenance, extracted context, facts, decisions, and uncertainty. Do not invent facts, decisions, owners, or links. Add links only when grounded in the source or given by the user.
- Ordinary flat notes from source do NOT use a `type` field.
- Choose a title from the invocation ("title: <t>") when suitable, otherwise infer a concise human title from the source.
- Section structure stays light and fits the source (e.g. SHORT VERSION, MAIN POINTS, DETAILS, DECISIONS, OPEN QUESTIONS); do not force empty sections.

For the note conventions - filename, frontmatter schema, vault location, and redaction of secrets - follow the `note-conventions` background skill. Do not restate them here.

## APPROVAL AND SAFETY

- Ask before writing. Show the full draft and the target path, then wait for approval or edits.
- Write only after approval, and only one note by default.
- Do not overwrite an existing note unless the user explicitly approves that exact path.
- Never process secrets, tokens, `.env` values, private keys, or passwords into the note; when content is sensitive (names, tokens), ask before writing and redact.
- Default vault root `~/Documents/notes`; use the vault path from the invocation when provided.

## ROUTING

- `/nxs:std-source` - learn from external material and optionally save a source-backed note (this skill).
- `/nxs:doc-note` - save applied knowledge you already hold, no external source to ingest.
- `/nxs:std-explain` - a plain-language explanation of one thing.
