# nxs

Development skills for coding agents: shape features and bugs into tickets for the client's plan mode, review changes, record project specs and commit in atomic groups. The standalone skills target Claude Code, Codex and OpenCode; [tests/client-scenarios.md](tests/client-scenarios.md) records the flows verified in each client. Standalone stages are commands you start yourself. Explicit `dev-lead` delegates a sequential cycle in the selected client within a feature plan you approve.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/workflow-dark.svg">
  <img alt="Workflow: dev-rnd, dev-bug or the dimmed mattpocock route to-spec and to-tickets write a ticket; a clear request goes straight to /plan; /plan runs the ticket; optional dev-review sends picked findings back as tickets; optional dev-spec records specs; dev-commit commits. Run dev-setup first." src="docs/images/workflow-light.svg">
</picture>

## Skills

| Skill | Use it to |
| --- | --- |
| [dev-lead](skills/dev-lead/SKILL.md) | Coordinate one task through an approved feature plan, sequential Claude Code, Codex or OpenCode workers in agterm, review, specs and atomic commits. |
| [dev-setup](skills/dev-setup/SKILL.md) | `global`: wire every client to one instruction file with the rules the skills rely on, and install chosen mattpocock/skills bundles (Core, Wayfinding, Architecture, Sessions) configured for local `.scratch/` tickets; `project`: add the branch rule and check commands to a repository and keep `.scratch/` out of Git. Each through one approved diff. |
| [dev-rnd](skills/dev-rnd/SKILL.md) | Shape a feature or open question into an agreed spec and tickets; `--decision-only` saves a research conclusion without tickets. |
| [dev-bug](skills/dev-bug/SKILL.md) | Investigate a reported failure; write a fix ticket once the cause is confirmed. |
| [dev-review](skills/dev-review/SKILL.md) | Review staged changes, or the branch; create only the tickets you pick. |
| [dev-spec](skills/dev-spec/SKILL.md) | Record durable project specs from landed work. |
| [dev-commit](skills/dev-commit/SKILL.md) | Commit existing changes in atomic groups. |

`dev-lead`, `dev-setup`, `dev-rnd`, `dev-bug`, `dev-review` and `dev-spec` run only on explicit invocation; `dev-commit` also accepts a direct request such as "commit this". For OpenCode, select a skill with `@dev-<name>` instead of `/dev-<name>`.

## Install

Install with the [skills CLI](https://skills.sh) and pick your agents at the prompt:

```bash
npx skills@latest add -g Villhard/nxs
```

The CLI installs one copy per skill into the shared agents skills directory (`~/.agents/skills`) and links it into each selected agent; agents that read that directory natively need no link. For a project-level install, drop `-g`. To install from a local checkout, pass its path instead of the repository.

## Update

```bash
npx skills@latest update -g
```

Start a new session after updating.

## Set up

Run `/dev-setup global` once per machine and `/dev-setup project` once in each repository. Without an argument, the command asks which mode you mean inside a Git repository and runs `global` outside one.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/setup-dark.svg">
  <img alt="dev-setup global links ~/.claude/CLAUDE.md, ~/.codex/AGENTS.md and ~/.config/opencode/AGENTS.md to ~/.agents/AGENTS.md, which holds the nxs, rule group and engineering sections; mattpocock/skills bundles install into ~/.agents/skills. dev-setup project writes an nxs section into AGENTS.md, imported by CLAUDE.md, and adds .scratch/ to .git/info/exclude." src="docs/images/setup-light.svg">
</picture>

Both modes audit first, show what they found and one diff, and write only what you approve. Declining writes nothing; running again updates only the sections the command owns.

- `global` makes `~/.agents/AGENTS.md` the one instruction file every client reads: an `@~/.agents/AGENTS.md` import in Claude Code, symlinks for Codex and OpenCode. An existing client file is merged into it, never overwritten. It adds a `## nxs` section, so an agent executing a ticket reads project specs on its path and names branches by the rule, then offers groups of working rules (communication, investigation, code changes, verification, git) for you to accept, edit or decline. It skips any rule your instructions already state. It also offers the [companion skill bundles](#companion-skills-not-part-of-nxs).
- `project` adds a `## nxs` section to the repository's `AGENTS.md` or `CLAUDE.md` with the branch rule and the test, lint and typecheck commands it finds in `Makefile`, `justfile`, `package.json`, CI config or `pyproject.toml`, so a ticket's "full test suite and linter" means real commands. It keeps `.scratch/` out of Git through `.git/info/exclude`, or `.gitignore` if you prefer.

## Usage

### Delegate a task

```text
/dev-lead <request or .scratch/feature path>
```

The lead resolves questions with you, shows a feature plan with scope, permissions, checks and actual model choices, and waits for your approval. It then approves technical ticket plans, runs one worker at a time in visible agterm sessions, checks results, organizes review and fixes, updates specs through `dev-spec` and commits through `dev-commit`. New scope, external-contract or agreed-decision changes return to you. It never pushes.

The adapters require Python 3, Git, agterm and the selected Claude Code, Codex or OpenCode v2 CLI. Read-only Claude/OpenCode workers also require macOS sandbox-exec. One feature branch and nxs alone form the baseline. Parallel worktrees, merges and autonomous companion integrations remain outside its scope. Manual stages remain available. Details and recovery rules: [dev-lead](skills/dev-lead/SKILL.md). Verification claims are limited to [client scenarios](tests/client-scenarios.md).

### Shape a feature

Use `dev-rnd` when a change needs decisions before code. Give it a request, a tracker key or URL, a spec path or an open question:

```text
/dev-rnd add rate limiting to the public API
```

It reads the relevant code first and shows what it found, then asks only what the code does not answer, in rounds of independent questions with options and a recommendation. It lays out two to four approaches, waits for your choice, pressure-tests the chosen one and shows the proposed spec and ticket breakdown before writing anything. A request that needs no decisions gets an offer to go straight to `/plan` instead of a spec.

Result: `.scratch/<feature-slug>/spec.md` and one ticket per vertical slice in `issues/NN-<slug>.md`. Next: `/plan <ticket-path>` for the first ready ticket. An approved spec, yours or external, goes in as `/dev-rnd <spec-path>` and is sliced without repeating settled questions. Details: [dev-rnd](skills/dev-rnd/SKILL.md).

For a focused decision without implementation tickets, use `/dev-rnd --decision-only <question>`. It saves the conclusion, evidence and remaining questions in `research/<topic>.md` in the feature directory.

### Fix a bug

Use `dev-bug` for a reported failure: pass a tracker key, pasted report, stack trace, log or path.

```text
/dev-bug checkout fails when the cart is empty
```

It reproduces the symptom, finds the root cause with evidence and classifies it against the project's glossary, decision records and specs:

| Class | Meaning | Outcome |
| --- | --- | --- |
| `right` | Records describe the expected behavior; only code is wrong | Fix ticket |
| `silent` | Records say nothing | You confirm the intended behavior, then a fix ticket |
| `wrong` | Records describe the buggy behavior | You confirm the correction, then a fix ticket |
| `feature` | The behavior was decided; the report asks for another decision | No ticket; continue with `/dev-rnd <root-cause path>` |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/bug-dark.svg">
  <img alt="dev-bug reproduces the symptom and classifies the cause: right, silent and wrong lead to a fix ticket run by /plan; feature hands off to /dev-rnd with root-cause.md." src="docs/images/bug-light.svg">
</picture>

Result: `.scratch/<feature-slug>/root-cause.md` and, once the cause is confirmed, one fix ticket. It changes no product code. Next: `/plan <ticket-path>`. Details: [dev-bug](skills/dev-bug/SKILL.md).

### Run a ticket

A ticket runs in the client's own plan mode:

```text
/plan .scratch/rate-limiting/issues/01-limit-per-key.md
```

The ticket's `## Done when` block is the whole execution contract: work on the ticket's branch, confirm each blocker's result in the working tree, verify every criterion, run the full test suite and linter, record decisions under `## Comments`, set the status, and never commit.

If a blocker's result is missing from the working tree, the executor names it under `## Comments` and stops; bring that result onto the ticket's branch and rerun `/plan`.

When the ticket needs a migration, a dependency install or an external check, the executor sets `ready-for-human`, names the step and the evidence it expects under `## Comments` and stops. Do the step, set the status back to `ready-for-agent` and rerun `/plan`: the executor checks the result in the current environment and continues, or sets `ready-for-human` again.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/ticket-status-dark.svg">
  <img alt="A written ticket starts as ready-for-agent, or needs-info while a clarification is open; once answered it becomes ready-for-agent. The executor sets resolved or ready-for-human; after your step you set ready-for-human back to ready-for-agent and rerun /plan; wontfix is set by you, or by a review ticket's executor when no finding reproduced." src="docs/images/ticket-status-light.svg">
</picture>

### Review a branch

Run `dev-review` on finished work. It reviews the staged changes, or the branch against its base when nothing is staged; an optional ticket or feature path supplies the requirements.

```text
/dev-review
```

Three finder roles run concurrently when the client allows, then a verifier marks each candidate finding confirmed, plausible or refuted; a trivial diff may get a direct pass. The report is saved under `.scratch/`, and the findings are explained with proposed tickets as groups of finding numbers. Answer with numbers such as "1, 3", "all" or "none"; only those tickets are created. A change that contradicts a project spec statement a ticket explicitly replaces is not a finding: the report lists it as a `pending dev-spec` follow-up. Review never changes code or Git state. Next: `/plan` for each new ticket. Details: [dev-review](skills/dev-review/SKILL.md).

### Record project specs

Run `dev-spec` after review and before the commit, on a branch:

```text
/dev-spec .scratch/rate-limiting
```

It writes what the work established and the code does not show: a module's purpose, boundaries, contracts, known limitations and rationale. It works from the diff, using the feature directory only as context, and reports "nothing durable changed" when that is the case. The first run in a repository asks for the mode once: committed `SPEC.md` files, or private `.SPEC.md` files kept out of Git through the clone's exclude file. `dev-rnd`, `dev-bug` and `dev-review` read these specs; only `dev-spec` writes them. Details: [dev-spec](skills/dev-spec/SKILL.md).

### Commit

```text
/dev-commit
```

It commits what is already there in atomic groups, one logical change per commit, with a one-line `<type>(<scope>): <subject>` message. It stops on secrets, generated artifacts or hunks that will not split, and never pushes. Details: [dev-commit](skills/dev-commit/SKILL.md).

## Where things live

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/artifacts-dark.svg">
  <img alt="dev-rnd writes spec.md and issues, dev-bug writes root-cause.md and issues, dev-review writes review.md and issues, all under .scratch/feature-slug/; dev-spec writes SPEC.md or .SPEC.md in the repository; domain-modeling maintains GLOSSARY.md and docs/adr/." src="docs/images/artifacts-light.svg">
</picture>

Feature records stay local under `.scratch/<feature-slug>/`: spec, root cause, tickets, research, review reports and append-only JSONL `decision.log`. Task skills journal standalone work too; controlled launch state and evidence live under `research/dev-lead/`. When review resolves no feature, its report and tickets go under `.scratch/reviews/<branch-slug>/`. Keep `.scratch/` ignored; `dev-setup project` does that for you. Tracker issues are read, never written.

Durable knowledge lives in the repository: project specs (`SPEC.md` or `.SPEC.md`), and a glossary with decision records when the project keeps them. Feature records hold what was planned; specs hold what was built.

## Companion skills (not part of nxs)

These skills come from [mattpocock/skills](https://github.com/mattpocock/skills), not from this repository. nxs works without them; they appear dimmed and dashed in the diagrams. `dev-setup global` offers them in bundles, installs the ones you choose together with the skills they call, and configures them to write local `.scratch/` tickets in the nxs format:

| Bundle | Skills | Where it fits |
| --- | --- | --- |
| Core (recommended) | `grilling`, `grill-me`, `domain-modeling`, `grill-with-docs`, `to-spec`, `to-tickets` | Interview a plan, keep `GLOSSARY.md` and decision records that every dev skill reads, and turn the outcome into a spec and tickets |
| Wayfinding (needs Core) | `wayfinder`, `research`, `prototype` | Plan work bigger than one session as a map of decision tickets, answered by research, prototypes and grilling |
| Architecture (needs Core) | `improve-codebase-architecture`, `codebase-design` | Find modules worth deepening and design their interfaces |
| Sessions | `handoff`, `retro`, `writing-for-agents`, `to-questionnaire` | Carry context between sessions, look back on them, write instructions for agents |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/bundles-dark.svg">
  <img alt="Core is recommended; Wayfinding and Architecture need Core; Sessions stands alone. Each skill lists the skills it calls, and dev-setup adds missing ones. setup-matt-pocock-skills is never offered." src="docs/images/bundles-light.svg">
</picture>

A skill that calls another pulls it in: choosing Wayfinding without Core also installs `grilling` and `domain-modeling`. `setup-matt-pocock-skills` is never offered, because `dev-setup global` writes the configuration it would create.

Two routes lead to the same `spec.md` and `issues/` files:

- `dev-rnd` alone: it asks its own questions, compares approaches and writes the spec and tickets in one command. Use it when you start from a request.
- `grill-me` or `wayfinder`, then `to-spec` and `to-tickets`: the interview or the map settles the decisions, and the `to-*` skills only write them down. `dev-rnd` would ask again, so use this route when the decisions are already made in the session. `/dev-rnd <spec-path>` can also slice a spec written by `to-spec`.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/grill-dark.svg">
  <img alt="grill-with-docs writes the glossary, to-spec writes spec.md in the same session, to-tickets writes tickets in the tracker format, and /plan runs them; /dev-rnd with the spec path is the alternative slicer." src="docs/images/grill-light.svg">
</picture>

For work bigger than one session, `wayfinder` keeps a map of decision tickets across sessions and hands the settled destination to the same `to-spec` and `to-tickets`:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/wayfinder-dark.svg">
  <img alt="Session 1 of wayfinder writes map.md and decision tickets; later sessions resolve one ticket each and update the map; once the way is clear, to-spec and to-tickets write a new feature for /plan." src="docs/images/wayfinder-light.svg">
</picture>

Tickets from either route run with `/plan <ticket-path>`. In a feature that already has tickets, new ones are numbered after the highest existing number.

For local previews and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md).
