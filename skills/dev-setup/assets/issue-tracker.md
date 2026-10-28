# Issue tracker: Local Markdown

Issues and specs (a spec is also called a PRD) live as Markdown files under `.scratch/`, inside whichever repository you are working in.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- The spec is `.scratch/<feature-slug>/spec.md`.
- Implementation issues are one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`; never one combined tickets file. A new ticket takes `NN` one past the highest existing number in `issues/`, whichever skill wrote those tickets; it is `01` only when `issues/` is empty or missing. Never renumber existing tickets.
- Triage state is the `**Status:**` line near the top of each issue file; `~/.agents/docs/triage-labels.md` maps the role names to its values.
- Comments and conversation history append to the bottom of the file under a `## Comments` heading.

## Local ticket format

Applies to every implementation ticket written as a local file: any `.scratch/<feature-slug>/issues/NN-<slug>.md` without a `Type:` line, whichever skill writes it. It extends the writing skill's own ticket template: keep everything that template asks for and add what is missing here.

- Fields in bold, in this order: the title `# NN: <title>`, `**What to build:**`, `**Blocked by:**`, `**Branch:**`, `**Status:**`, then the acceptance criteria as `- [ ]` lines.
- `**Blocked by:**` names ticket numbers, or `None (can start immediately)` when no dependency remains.
- `**Branch:**` proposes `<type>/<feature-slug>`, shaped by the project's branch rule when one exists, with `<type>` from the work: `feat`, `fix`, `refactor`, `chore` or `docs`. A project without a branch rule still gets the line.
- `**Status:**` is `ready-for-agent`, or `needs-info` while an open `[NEEDS CLARIFICATION: ...]` sits in the ticket.
- After the criteria, end the ticket with this block, copied verbatim and in English:

````markdown
## Done when

Execute this ticket directly, for example with `/plan <this file>`.

- Stop and ask if **Status** is not `ready-for-agent`, a ticket in **Blocked by** is not `resolved`, or this ticket or its feature's `spec.md` / `root-cause.md` has an open `[NEEDS CLARIFICATION: ...]`.
- If **Branch** is set, work on that branch: switch to it, or create it from the current HEAD when missing. Stop and ask if the switch fails.
- Before the first implementation edit, read each ticket in **Blocked by** and verify, by code inspection and a focused check, that the results this ticket needs exist in the current working tree; **Status**, branch names and Git history alone do not suffice. Record the evidence or the missing prerequisite in one line under `## Comments`. If a result is absent or unverifiable, stop and ask; never merge, cherry-pick or implement the blocker.
- If a required migration, dependency install or external check is undone or unverifiable, set **Status** to `ready-for-human`, record under `## Comments` the action needed and the evidence you expect, and stop. The human completes it, sets **Status** back to `ready-for-agent` and reruns `/plan`. On that rerun, verify the recorded result by checkable evidence in the current environment; a `done` line under `## Comments` alone is not evidence, and never perform the step yourself. If it is still undone or unverifiable, set `ready-for-human` again and stop.
- Close when the project's full test suite and linter pass and every criterion above is verified against the running code: check each one and set **Status** to `resolved`.
- Add one line under `## Comments` per decision or deviation.
- Do not commit.
````

A decision ticket (a `Type:` line, written by `/wayfinder`) is not an implementation ticket: it gets no `**Branch:**`, no `## Done when` and no triage status, and its answer goes under `## Answer`.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/`, creating the directory when needed.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user normally passes the path or the issue number.

## Wayfinding operations

Used by `/wayfinder`. The map is one file with one child file per ticket.

- Map: `.scratch/<effort>/map.md`, holding the Notes, Decisions-so-far and Fog body.
- Child ticket: `.scratch/<effort>/issues/NN-<slug>.md`, numbered like any new ticket under Conventions, with the question in the body. A `Type:` line records the ticket type (`research`, `prototype`, `grilling` or `task`); a `Status:` line records `claimed` or `resolved`.
- Blocking: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- Frontier: the open, unblocked and unclaimed files in `.scratch/<effort>/issues/`; the lowest number wins.
- Claim: set `Status: claimed` and save before any work.
- Resolve: append the answer under an `## Answer` heading, set `Status: resolved`, then append a pointer (gist and path) to Decisions-so-far in `map.md`.

## Scope

This is the global default for every repository without its own `## Agent skills` block. Project instructions load after these global instructions and win.
