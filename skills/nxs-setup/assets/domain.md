# Domain docs

How the engineering skills consume a repository's domain documentation while exploring the code. Paths are relative to the root of the repository you are working in.

## Before exploring, read these

- `GLOSSARY.md` at the repository root, or
- `GLOSSARY-MAP.md` at the root when it exists: it points at one `GLOSSARY.md` per context. Read each one relevant to the topic.
- `docs/adr/`: read the ADRs that touch the area you are about to work in. In a multi-context repository, also check `src/<context>/docs/adr/` for context-scoped decisions.
- `SPEC.md` and `.SPEC.md` project specs on the path of the files you touch, found by exact name in a directory listing.

When these files are absent, proceed silently: do not flag their absence or suggest creating them upfront. `/to-decision` creates the glossary and ADRs when terms or decisions get resolved.

## File structure

Single-context repository (the default):

```text
/
  GLOSSARY.md
  docs/adr/
    0001-event-sourced-orders.md
    0002-postgres-for-write-model.md
  src/
```

Multi-context repository (a `GLOSSARY-MAP.md` at the root):

```text
/
  GLOSSARY-MAP.md
  docs/adr/                 system-wide decisions
  src/
    ordering/
      GLOSSARY.md
      docs/adr/             context-specific decisions
    billing/
      GLOSSARY.md
      docs/adr/
```

Treat a repository as single-context unless a root `GLOSSARY-MAP.md` says otherwise.

## Use the glossary's vocabulary

When your output names a domain concept (an issue title, a refactor proposal, a hypothesis, a test name), use the term `GLOSSARY.md` defines, not a synonym it avoids.

A concept missing from the glossary is a signal: either the language is invented (reconsider it) or there is a real gap (note it for `/to-decision`).

## Flag ADR conflicts

When your output contradicts an existing ADR, say so explicitly instead of overriding it:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because..._
