# NOTE TYPES

Four note types for applied-knowledge capture in note mode (`/nxs:doc-note`). Applied knowledge only - each note must actually be useful in a specific future situation. A supplied kind maps to one of these as the frontmatter `type` (or to the vault's own allowed set when it defines one).

Task-doc (`/nxs:doc-summary`) is a separate artifact (`type: task-doc`), not one of the note types below.

## CHEATSHEET

Short cheatsheet with the most common operations on a topic. Use when you have learned a tool / language / system and want to capture commands and idioms.

Structure: sections by task (not by concept); commands / snippets with brief comments; no long explanations.

Examples: `cheatsheet-grep.md`, `cheatsheet-docker-compose.md`, `cheatsheet-git-rebase.md`.

## HOWTO

Step-by-step recipe for a specific task. Use when you successfully solved a non-trivial task and want to repeat it.

Structure: goal in the first paragraph; preconditions; steps in order; result verification; typical failures and how to avoid them.

Examples: `howto-rotate-postgres-creds.md`, `howto-fix-merge-conflict-binary.md`.

## REFERENCE

A fact / list / table for later lookup. Use when you need quick access to data you would otherwise have to google.

Structure: tables; lists; key-value; minimal explanations.

Examples: `reference-http-status-codes.md`, `reference-sql-isolation-levels.md`, `reference-example-projects.md`.

## GOTCHA

A pitfall that is easy to step on. Use when you wasted time on a pitfall and do not want to repeat it.

Structure: what happened (symptom); why (root cause); how to avoid; how to fix if it already happened.

Examples: `gotcha-go-time-zone.md`, `gotcha-postgres-jsonb-index.md`.

## HOW TO CHOOSE

| situation | type |
|---|---|
| "I use this often, I want a handy reference" | cheatsheet |
| "I did a complex procedure, I want to repeat it" | howto |
| "I need to look up data quickly" | reference |
| "I wasted an hour on a dumb problem" | gotcha |

## ANTI-PATTERNS

- an essay about a concept ("what is Docker") - not applicable, drop;
- vague "interesting thoughts" with no application - drop;
- "might come in handy someday" - drop;
- personal correspondence / temporary task lists - drop.
