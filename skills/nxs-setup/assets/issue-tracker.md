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

Execute this ticket directly with `/dev-exec <this file>`.

- Resolve the feature directory from this ticket and use its `decision.log` in standalone and controlled execution. Append concise JSONL events for decisions, questions, answers, completion, blockers and handoff, with unique IDs and artifact/evidence paths; write one complete line at a time with the host's file-write or shell tool. The lead is the only writer in controlled work, so no helper or lock is required; if independent processes can write the same journal, serialize them through the host's own file edit or a lock command available on that system. Never log secrets or full conversations. A branch alone never selects a different journal. Read existing entries and reconcile them with artifacts and actual Git state before continuing; never replay an uncertain side effect.
- Only an explicit controlled-run packet with step/run IDs, approved feature plan and hash, approval reference, cwd, permissions, allowed writes, acceptance checks, result schema and journal path activates lead control. In that context, save the proposed ticket plan and return `needs_input` to lead before implementation; continue that exact native subagent session only after recorded lead approval where the host documents continuation, otherwise start a new bounded run with the approved plan and saved artifacts. Return `done`, `needs_input` or `blocked` with evidence in the supplied envelope. Keep ordinary dialogue and human plan approval outside that context. A packet carries existing authorization, never new consent; scope, external-contract or agreed-decision changes return through lead to the user.

- Stop and ask if **Status** is not `ready-for-agent`, a ticket in **Blocked by** is not `resolved`, or this ticket or its feature's `spec.md` / `root-cause.md` has an open `[NEEDS CLARIFICATION: ...]`.
- If **Branch** is set, work on that branch: switch to it, or create it from the current HEAD when missing. Stop and ask if the switch fails.
- Before the first implementation edit, read each ticket in **Blocked by** and verify, by code inspection and a focused check, that the results this ticket needs exist in the current working tree; **Status**, branch names and Git history alone do not suffice. If every result is present, record the evidence in one line under `## Comments`. If a result is absent or unverifiable, record the missing prerequisite in one line under `## Comments` and stop; never merge, cherry-pick or implement the blocker.
- If a required migration, dependency install or external check is undone or unverifiable, set **Status** to `ready-for-human`, record under `## Comments` the action needed and the evidence you expect, and stop. The human completes it, sets **Status** back to `ready-for-agent` and reruns the selected executor on this ticket. On that rerun, verify the recorded result by checkable evidence in the current environment; a `done` line under `## Comments` alone is not evidence, and never perform the step yourself. In a controlled run only, an approved feature plan naming the action and exact target authorizes the executor to perform and verify it; an unnamed action follows this ready-for-human path. If it is still undone or unverifiable, set `ready-for-human` again and stop.
- Close when the project's full test suite and linter pass and every criterion above is verified against the running code: check each one and set **Status** to `resolved`.
- Add one line under `## Comments` per decision or deviation.
- Apply each planned checkpoint only after the completed block's necessary checks pass, using `dev-commit` in the same session within the explicitly approved plan's commit scope and native permissions; verify the result before the next block. If a planned checkpoint lacks scope or permission, stop that checkpoint and report the limitation without an unauthorized commit. If commits are intentionally not selected, continue without checkpoints and hand off uncommitted changes. Existing tickets with `Do not commit` retain that prohibition unless a specific revision is separately approved; execute them without checkpoints. Journal the verified completion or pending handoff; lead independently checks evidence before accepting a controlled `done`.
````

A decision ticket (a `Type:` line, written by `/rnd-map`) is not an implementation ticket: it gets no `**Branch:**`, no `## Done when` and no triage status, and its answer goes under `## Answer`.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/`, creating the directory when needed.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user normally passes the path or the issue number.

## Wayfinding operations

Used by `/rnd-map`. The map is one file with one child file per ticket.

- Map: `.scratch/<effort>/map.md`, holding the Notes, Decisions-so-far and Fog body.
- Child ticket: `.scratch/<effort>/issues/NN-<slug>.md`, numbered like any new ticket under Conventions, with the question in the body. A `Type:` line records the ticket type (`research`, `prototype`, `grilling` or `task`); a `Status:` line records `claimed` or `resolved`.
- Blocking: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- Frontier: the open, unblocked and unclaimed files in `.scratch/<effort>/issues/`; the lowest number wins.
- Claim: set `Status: claimed` and save before any work.
- Resolve: append the answer under an `## Answer` heading, set `Status: resolved`, then append a pointer (gist and path) to Decisions-so-far in `map.md`.

## Scope

This is the global default for every repository without its own `## Agent skills` block. Project instructions load after these global instructions and win.
