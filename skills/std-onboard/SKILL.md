---
description: Onboarding map of a domain / subsystem - load-bearing classes, responsibilities, observability, and how it is operated. Use when you need orientation deep enough to start working in an unfamiliar area, not a one-paragraph answer and not a change description.
argument-hint: "[domain | subsystem | path]"
---

# /nxs:std-onboard

Get someone productive in a domain / subsystem fast: map the load-bearing classes / modules, what they are responsible for, how they connect, how the subsystem is observed and operated (logs, metrics, config, entry points), and the non-obvious gotchas. Self-contained skill. Output language and response style come from global rules, not this file.

## PROCEDURE

1. Resolve scope: a domain / topic name (`billing`, `auth`, `checkout`), one or more paths scoping the subtree, or a branch / diff used only to locate the touched domain (not a change description). No argument -> current working directory / session context. If scope is genuinely unclear, ask one question before reading.
2. If `docs/.ai/index.md` exists and is relevant, read it once as project AI context and use it as a router into the domain; read the actual code before describing behavior.
3. Read breadth-first: build the structural skeleton first (entry points, key types, package layout), then drill into a facet only when it carries signal or the user asks. Do not read the whole subtree.
4. For a wide domain, fan out read-only collection (entry points, observability surface, config, tests) to a read-only explorer subagent (`nxs:explorer` or the built-in Explore) and synthesize the map in the main context, so the main context stays lean.
5. Identify the load-bearing abstractions: the 3-7 classes / modules the domain actually rests on, one-line role each; prefer the types other code depends on.
6. Map responsibilities and boundaries: what the domain owns, what it explicitly does not, who calls in, what it calls out to.
7. Collect the observability surface from the repository: metric names and types, structured log events / keys, trace spans, and in-repo alert / dashboard config. This is the instrumentation visible in code, not live dashboards.
8. Collect config & dependencies, data & state, and the 1-3 main flows through the domain.
9. Point at the tests that pin behavior and how to run them; collect domain glossary terms and the non-obvious gotchas.
10. Emit the facet map below. Omit facets that genuinely do not apply; do not pad. Close with where to start reading, open questions, and suggested follow-ups.

## OUTPUT

Chat map only; read-only, no durable file by default. A curated, facet-based map - facets that do not apply are omitted, not padded:

| facet | what it captures |
|---|---|
| TL;DR | what this domain is and does, 2-3 sentences |
| entry points & key abstractions | the load-bearing classes / modules the domain rests on, one-line role each |
| responsibilities & boundaries | what it owns, what it does not, upstream callers, downstream dependencies |
| data & state | stores, schemas, key entities, migrations |
| observability surface | metric names / types, structured log events, trace spans, in-repo alerts / dashboards |
| config & dependencies | config / env keys, feature flags, external services, key libraries |
| key flows | 1-3 main paths through the domain; ASCII when it helps |
| tests as documentation | where behavior is pinned and how to run it |
| glossary & gotchas | domain terms and non-obvious traps |
| where to start | where to read first, open questions, suggested follow-ups |

## RULES

- Orientation, not evaluation: no bug / security / issue hunting (that is `/nxs:dev-review`).
- Not a change description (`/nxs:std-walkthrough`) and not a one-paragraph explanation (`/nxs:std-explain`); a branch / diff only locates the domain.
- "Metrics / logs" means the in-repo observability surface; do not query live dashboards or run the app.
- Read breadth-first, drill on demand; never dump a file-by-file reference.
- Does not write project memory. If the map is worth persisting, suggest `/nxs:init` (`docs/.ai/`).

## ROUTING

- `/nxs:std-onboard` - a deep domain / subsystem map to get productive (this skill).
- `/nxs:std-walkthrough` - a short overview of one branch / flow / code path.
- `/nxs:std-explain` - a plain-language explanation of one thing.
- `/nxs:dev-review` - find problems in a diff.
