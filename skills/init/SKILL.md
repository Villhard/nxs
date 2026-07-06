---
description: Initialize or update the project AI context (docs/.ai/) for the current repository - scan the repo and produce a concise navigation map for future agents. Use in a repo that lacks docs/.ai/index.md, or to refresh an existing map.
argument-hint: "[]"
---

# /nxs:init

Initialize or refresh the project AI context in `docs/.ai/` for the current repository. Scan the repo and produce a concise, helicopter-level navigation map that future agents read before acting on the project. Self-contained skill. Output language and response style come from global rules, not this file.

No arguments - run bare in the repo root.

## WHAT IT PRODUCES

`docs/.ai/` is a coarse project map: "where to look", not a source of truth and not a retelling of the code. A run creates this file set, each with one job:

- `index.md` - router: which file to read for which task;
- `overview.md` - what the project does, its domains and boundaries;
- `architecture.md` - layers, main flows, dependency direction;
- `modules.md` - large modules / bounded contexts and where their code lives;
- `operations.md` - how to run, test, lint, typecheck, build; env and local infra;
- `data.md` - DBs, queues, cache, storage, external systems;
- `gotchas.md` - only confirmed, stable, repeatedly useful gotchas;
- `manifest.json` - internal state used to scope a later refresh.

`index.md` is the entry point; the other files are read on relevance, not all at once.

Optional, created lazily and never by a default run:

- `docs/.ai/domain-language.md` - the project's ubiquitous glossary; created only when confirmed project-specific terms exist. Use the `domain-language` background skill for its format and its when-to-create rule - do not restate them here.
- `docs/.ai/code-rules.md` - project-local custom code rules (guardrails, not a map); created and appended only on an explicit user request.

## PROCEDURE

1. Check for `docs/.ai/index.md`.
2. Read the actual code and config before writing anything - entrypoints, build / test / lint config, top-level directories, infra manifests. Do not over-read; stay helicopter-level.
3. Decide the mode:
   - Create (no `docs/.ai/`): build the full file set above from the repo scan.
   - Update (already present): refresh in place - change only what drifted (see REFRESH SCOPE). No staleness check and no staleness warning.
4. Write the file set directly under `docs/.ai/` - no approval gate. Then report a concise summary of created / updated files; review and revert go through git (`docs/.ai/` is repo-tracked and regenerable).

A full rebuild has no separate mode: delete `docs/.ai/` and run `/nxs:init` again.

## REFRESH SCOPE

On update, use drift signals to decide what to touch:

- config / lock / Makefile / compose / CI / settings files changed;
- large directories appeared or disappeared;
- entrypoints changed;
- top-level modules / bounded contexts changed.

With no substantial drift, update `manifest.json` state only. Do not expand the map with detail useful to a single task.

## GRANULARITY

- Prefer "where to look" over "how it works". Record the stable shape - layers, dependency direction, large modules, entrypoints, commands, data / infra dependencies.
- Group modules by area / bounded context; do not catalog every app, model, function, class, or endpoint.
- Store: overview and boundaries, architectural layers, large modules and where their code lives, run / test / lint / typecheck / build commands, entrypoints, infra dependencies, stable conventions, confirmed gotchas.
- Do not store: the current task, a bug's history, transient workarounds, secrets / tokens / .env values, large code chunks, a value-free README retelling, personal preferences (those belong in global config).

## SIZE BUDGET

- `index.md` - up to 80 lines;
- other `docs/.ai/*.md` - up to 50 lines each;
- `gotchas.md` - only confirmed, stable, repeatedly useful gotchas.

An overflowing file is a signal to cut detail, not to split into more files.

## RULES

- One command, no modes or sub-selectors.
- Write directly and report a post-write summary; do not add an approval gate.
- Write only under `docs/.ai/`. Do not create or modify a root `AGENTS.md` or `CLAUDE.md` - read them as input if present, never write them.
- Do not change `.gitignore` or `.git/info/exclude`.
- Do not describe the project down to functions / classes; `docs/.ai/` is not a retelling of the code.
- Do not invent gotchas from file structure, or domain terms from filenames / class names.
- Do not create `domain-language.md` without confirmed terms; do not create `code-rules.md` except on an explicit request.
- On an ambiguous or conflicting domain term, stop and clarify before encoding it into a map, plan, brief, or code.
- Do not store secrets, tokens, .env values, the current task, or large code chunks.

## NEXT

Map written -> future agents read `docs/.ai/index.md` first. Re-run `/nxs:init` when the stack or structure changes. For a plain-language tour of the map -> `/nxs:std-explain`.
