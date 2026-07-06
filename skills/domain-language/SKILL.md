---
description: The project's ubiquitous domain glossary (docs/.ai/domain-language.md) and how to record and disambiguate terms - load when resolving fuzzy or ambiguous domain terms. Background knowledge, not a user command.
user-invocable: false
---

# DOMAIN LANGUAGE

Load when resolving fuzzy or ambiguous domain terms. Workflow knowledge, not a user-invocable command. A single ubiquitous language shared between user and agent reduces mismatch between what the user asks and how the agent encodes it into plans, briefs, diagnoses, and code.

## WHERE THE LANGUAGE LIVES

- The project glossary lives in `docs/.ai/domain-language.md`. It is optional and created lazily - only when the project has confirmed terms.
- When it exists, read it before encoding domain terms into a plan, brief, diagnosis, or code.
- It holds only canonical terms, aliases, relationships, ambiguities, and optionally example dialogue. It is not an implementation spec, not project documentation, not a scratchpad for current discussions, and not auto-generated from filenames or classes.

## REAL TERM VS CASUAL WORD

A word is a domain term only if confirmed by one of:

- discussion with the user / domain expert (this or a prior session);
- existing project docs (README, design docs, ADR, tickets);
- code semantics with an explicit signal (stable usage in module names, sql table names, API contracts);
- repeated usage across several independent places in the project.

Do not derive a term from a single filename or a single class name - that is a weak signal, not confirmation. Generic programming concepts (Service, Repository, Controller, DTO) stay out unless they carry a project-specific meaning.

## RESOLVING FUZZY OR AMBIGUOUS TERMS

When a task uses a term that `domain-language.md` marks as ambiguous, or that conflicts with a canonical term, stop before encoding it into plan / brief / code:

1. Notice the ambiguity / conflict.
2. Reference the specific place in `domain-language.md`.
3. Ask one clarifying question.
4. After the answer, continue - and update the glossary only if the term should be recorded.

If there is no glossary yet and a term's meaning is unclear, ask rather than guess.

## RECORDING (durable write - approval only)

Writing or updating `docs/.ai/domain-language.md` is a durable change; do it only when the user asks or approves, through the init flow (`/nxs:init`). Create the file when:

- the user explicitly asks to record the domain language;
- the project has at least one confirmed term with project-specific meaning (not filler);
- an existing root `CONTEXT.md` / `CONTEXT-MAP.md` is being adapted into this format and the user wants it.

Update it when a new confirmed term appears, the canonical term changes (the old one becomes an alias), an ambiguity worth recording is found, or a term is retired. In all other cases do not create the file or mention it.

Keep it compact and helicopter-level: up to 80 lines, each term defined in 1-2 sentences without retelling the code. Growth is a signal to trim generic terms, not to inflate the glossary.

## GLOSSARY FORMAT

When creating or updating `docs/.ai/domain-language.md`, use this structure:

```text
# Domain Language

## Language

**<Term>**:
<1-2 sentence definition>
_Avoid_: <aliases, comma-separated>

## Relationships

- <Term A> has many <Term B>
- <Term C> is a kind of <Term D>

## Flagged ambiguities

- <Term>: <what the ambiguity is, which variant is canonical>

## Example dialogue

> Dev: ...
> Domain expert: ...
```

The Relationships, Flagged ambiguities, and Example dialogue sections are optional - include them only when they actually help the agent.
