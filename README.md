# nxs

Development skills for coding agents: shape features and bugs into tickets for the client's plan mode, review changes, record project specs and commit in atomic groups. The standalone skills target Claude Code, Codex and OpenCode; [tests/client-scenarios.md](tests/client-scenarios.md) records the flows verified in each client. Standalone stages are commands you start yourself. Explicit `dev-lead` delegates a sequential cycle through the selected client's native subagents, within a feature plan you approve.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/workflow-dark.svg">
  <img alt="Delegated route: dev-lead requires a native subagent capability, user feature approval and lead ticket-plan approval; each accepted independent ticket has checks, review, fixes, specs and atomic commits, followed by complete-feature review. Separate manual route: rnd, bug or dim dashed companions write tickets for /plan, with optional review/spec and separate commit; a clear request can go straight to /plan." src="docs/images/workflow-light.svg">
</picture>

## Skills

| Skill | Use it to |
| --- | --- |
| [dev-lead](skills/dev-lead/SKILL.md) | Delegate one task through an approved feature plan, native subagents and a checks/review/spec/commit checkpoint before each next independent ticket. |
| [dev-setup](skills/dev-setup/SKILL.md) | `global`: wire every client to one instruction file with the rules the skills rely on, and install chosen mattpocock/skills bundles (Core, Wayfinding, Architecture, Sessions) configured for local `.scratch/` tickets; `project`: add the branch rule and check commands to a repository and keep `.scratch/` out of Git. Each through one approved diff; optional `global --readiness` or `project --readiness` only reports lead prerequisites. |
| [dev-rnd](skills/dev-rnd/SKILL.md) | Shape a feature or open question into an agreed spec and tickets; `--decision-only` saves a research conclusion without tickets. |
| [dev-bug](skills/dev-bug/SKILL.md) | Investigate a reported failure; write a fix ticket once the cause is confirmed. |
| [dev-review](skills/dev-review/SKILL.md) | Review staged changes, or the branch; create only the tickets you pick. |
| [dev-spec](skills/dev-spec/SKILL.md) | Record durable project specs from landed work. |
| [dev-commit](skills/dev-commit/SKILL.md) | Commit existing changes in atomic groups. |
| [rnd-grill](skills/rnd-grill/SKILL.md) | Discuss an idea, question or plan; conclude in dialogue without saving or starting development. Candidate route alongside dev-rnd. |
| [to-decision](skills/to-decision/SKILL.md) | Show and save an approved decision or unfinished discussion; write only approved glossary/ADR proposals. Candidate route alongside existing manual saving. |
| [to-spec](skills/to-spec/SKILL.md) | Prepare a local feature spec from a saved decision or clear request; retain draft questions and stop before tickets. Candidate route alongside dev-rnd. |
| [rnd-debug](skills/rnd-debug/SKILL.md) | Investigate a failure and save evidence without creating a ticket. Candidate route. |
| [rnd-research](skills/rnd-research/SKILL.md) | Save evidence and limitations for a question without deciding a material choice. Candidate route; live behavior is unverified. |
| [rnd-prototype](skills/rnd-prototype/SKILL.md) | Test a hypothesis with a retained prototype and verdict. Candidate route; live behavior is unverified. |
| [rnd-design](skills/rnd-design/SKILL.md) | Agree and save a selected module's interface and responsibilities. Candidate route; live behavior is unverified. |
| [rnd-audit](skills/rnd-audit/SKILL.md) | Survey a project and save ranked architecture opportunities. Candidate route; live behavior is unverified. |
| [to-handoff](skills/to-handoff/SKILL.md) | Save resumable task context with or without a journal. Candidate route; live behavior is unverified. |
| [to-questionnaire](skills/to-questionnaire/SKILL.md) | Prepare a participant questionnaire without sending it. Candidate route; live behavior is unverified. |
| [rnd-map](skills/rnd-map/SKILL.md) | Map a broad goal into linked decisions and dependencies. Candidate route; live behavior is unverified. |
| [to-tickets](skills/to-tickets/SKILL.md) | Turn an approved feature spec or confirmed eligible root cause or selected review findings into local implementation tickets while preserving existing ticket history. Candidate route alongside dev-rnd. |
| [dev-exec](skills/dev-exec/SKILL.md) | Execute a ticket or clear request in the current session after plan approval, then check and report. Candidate route alongside `/plan`. |

`dev-lead`, `dev-setup`, `dev-rnd`, `dev-bug`, `dev-review` and `dev-spec` run only on explicit invocation; `dev-commit` also accepts a direct request such as "commit this". For OpenCode, select a skill with `@dev-<name>` instead of `/dev-<name>`.

`rnd-grill`, `rnd-debug`, `rnd-research`, `rnd-prototype`, `rnd-design`, `rnd-audit`, `rnd-map`, `to-questionnaire`, `to-handoff`, `to-decision`, `to-spec` and `to-tickets` also require explicit invocation (OpenCode uses `@` and the skill name). They are additive candidates; existing manual and coordinator routes remain available. See client scenarios for actual verification limits before relying on a client route.

Use `to-spec <decision-path>` or `to-spec <clear request>` to propose a feature spec without slicing tickets. Existing approval is reused within its scope; a changed existing spec needs approval of its concrete revision. An expressly requested draft keeps its open questions and cannot hand off ready work while material evidence is missing. See [to-spec](skills/to-spec/SKILL.md) for its source, preservation and handoff rules. This addition leaves the complete `dev-rnd` route and existing installations available.

Use `dev-review --to-tickets` to produce a verified report and selection for a separate `to-tickets` invocation. This additive route is unverified; ordinary `dev-review` retains its existing review-to-fix route.

Use `rnd-debug` for diagnosis without ticket creation; an eligible confirmed cause can be passed explicitly to `to-tickets <root-cause-path>`. The existing `dev-bug` route remains available. These candidates have not passed a live route switch gate.

Use `rnd-research <question>` to save source-linked findings and limitations. The candidate does not choose a material decision or start a further stage without authorization; manual research remains available. Its client behavior has not been verified live.

Use `rnd-prototype <hypothesis>` to retain a local experiment and its verdict. Transferring, reusing or deleting it requires separate authorization; the existing prototype route remains available. Its client behavior has not been verified live.

Use `rnd-design <module>` to compare and save an agreed design for a selected module. It does not select a project-wide target or implement the result. Existing design routes remain available; client behavior is unverified.

Use `rnd-audit [project path]` to save prioritized architecture opportunities or a reasoned no-change result. The audit does not select or implement an opportunity. Existing inspection routes remain available; client behavior is unverified.

Use `rnd-map <goal or map path>` to chart or continue local decision work. Each question needs explicit permission; mapping alone does not authorize implementation. Existing maps and the optional wayfinder route remain available; client behavior is unverified.

Use `to-tickets <spec-path>` to propose implementation tickets from an approved local feature spec. Covered tickets and decision histories stay unchanged; genuinely new scope appends. It retains the `/plan` executor handoff. See [to-tickets](skills/to-tickets/SKILL.md) for source, dependency and revision gates. This candidate does not replace an installed same-name skill or switch the existing manual/coordinator routes.

Explicit `/dev-exec <ticket-path>` or `/dev-exec <clear request>` proposes a plan and waits for approval before implementation in the current session; OpenCode uses `@dev-exec`. Built-in Plan Mode is optional and native permissions still apply. Clear requests need no ticket. Review, project specs and commit remain separate. See [dev-exec](skills/dev-exec/SKILL.md) for approval and execution rules and client scenarios for unverified behavior. Existing `/plan` handoffs remain the default while this candidate is evaluated.

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
  <img alt="Normal dev-setup global shares client instructions and installs approved companion bundles; project adds repository rules and ignores .scratch. Both use an approved diff. Optional global --readiness and project --readiness report selected lead prerequisites and stop without a setup proposal, setup writes or installs." src="docs/images/setup-light.svg">
</picture>

Both modes audit first, show what they found and one diff, and write only what you approve. Declining writes nothing; running again updates only the sections the command owns.

- `global` makes `~/.agents/AGENTS.md` the one instruction file every client reads: an `@~/.agents/AGENTS.md` import in Claude Code, symlinks for Codex and OpenCode. An existing client file is merged into it, never overwritten. It adds a `## nxs` section, so an agent executing a ticket reads project specs on its path and names branches by the rule, then offers groups of working rules (communication, investigation, code changes, verification, git) for you to accept, edit or decline. It skips any rule your instructions already state. It also offers the [companion skill bundles](#companion-skills-not-part-of-nxs).
- `project` adds a `## nxs` section to the repository's `AGENTS.md` or `CLAUDE.md` with the branch rule and the test, lint and typecheck commands it finds in `Makefile`, `justfile`, `package.json`, CI config or `pyproject.toml`, so a ticket's "full test suite and linter" means real commands. It keeps `.scratch/` out of Git through `.git/info/exclude`, or `.gitignore` if you prefer.

To audit the selected lead environment without running setup, use an explicit mode:

```text
/dev-setup global --readiness
/dev-setup project --readiness
```

These optional commands report Git, native subagent capability, the selected CLI and native skill/model discovery, with exact missing items or errors and remedies. They stop without a setup proposal, setup writes, installs or automatic remediation. A successful report establishes only the audited prerequisites, not worker execution, permission enforcement or workflow compatibility. Details: [readiness report](skills/dev-setup/references/readiness.md).

## Usage

### Delegate a task

```text
/dev-lead <request or .scratch/feature path>
```

Before invoking `dev-lead`, check that the client exposes a native subagent facility: a tool that starts a fresh-context agent with a complete prompt and reports or waits for its result. If it does not, `dev-lead` stops before task effects with the missing capability; standalone skills remain available. Discovery errors and unverified client routes are reported by their actual cause.

The lead resolves questions with you and waits for approval of a feature plan covering scope, permissions, checks and model choices. It approves technical ticket plans within that scope, then delegates one writing subagent at a time with the complete packet, write boundaries and expected result. A subagent starts from a fresh context; the lead never passes the parent conversation. New scope, external-contract or agreed-decision changes return to you.

Before the next independent ticket, each independently accepted implementation and its verified dependent corrections pass relevant/full required checks, scoped read-only `dev-review`, in-scope fixes, built-work `dev-spec` and atomic `dev-commit`. The lead verifies the resulting checkpoint and HEAD. Executors never commit; research, planning and no-change groups create no empty commits. A final complete-feature review includes committed tickets and remaining task changes before final checks/spec/commit reconciliation. It never pushes. See [the checkpoint contract](skills/dev-lead/SKILL.md#review-and-finish).

The lead publishes its stage, ticket/action and wait or blocker reason in [local status records](#where-things-live). Questions use the host's native dialog when one is exposed, otherwise the conversation. A revision reopens only affected scope; dismissal and timeout grant no approval. See [local progress and questions](skills/dev-lead/references/questions.md).

A subagent session is closed or released only through the host's documented mechanism after its result is collected. A lost reply is reconciled from artifacts and host records, never replayed automatically. After interruption, reconcile journal, questions, subagent runs, outcomes and Git state before retrying an uncertain effect. See [native subagents](skills/dev-lead/references/subagents.md#failure-and-recovery) and [recovery](skills/dev-lead/SKILL.md#recovery).

The skills require Git, the selected Claude Code, Codex or OpenCode client and its native subagent facility. One feature branch and nxs alone form the baseline; parallel worktrees, merges and autonomous companion integrations remain outside its scope. [dev-lead](skills/dev-lead/SKILL.md) owns the delegation policy. [Client scenarios](tests/client-scenarios.md) distinguish recorded native-subagent observations, consumer permission failures and unverified routes; availability does not establish full multi-client workflow compatibility.

### Shape a feature

To discuss and optionally save a decision through the candidate route:

```text
/rnd-grill <question or plan>
/to-decision <discussion or saved decision path>
```

Discussion waits for material choices and can finish without files. Saving first shows the proposed conclusions and destination, then uses approval covering that exact content. You can approve saving unfinished state with open questions. Domain proposals are approved individually; a direct domain-document request within an expressly invoked scope needs no decision wrapper. New decisions default to `.scratch/<feature-slug>/research/decision.md`; existing paths and user content are preserved. HTML approval alone saves nothing. A feature spec, tickets and implementation remain separate requests. Details: [discussion](skills/rnd-grill/SKILL.md) and [saving](skills/to-decision/SKILL.md).

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
  <img alt="Standalone dev-bug reproduces the symptom and classifies the cause: right, silent and wrong lead to a fix ticket run by /plan; feature hands off to /dev-rnd with root-cause.md." src="docs/images/bug-light.svg">
</picture>

Result: `.scratch/<feature-slug>/root-cause.md` and, once the cause is confirmed, one fix ticket. It changes no product code. Next: `/plan <ticket-path>`. Details: [dev-bug](skills/dev-bug/SKILL.md).

### Run a ticket

A ticket runs in the client's own plan mode:

```text
/plan .scratch/rate-limiting/issues/01-limit-per-key.md
```

For standalone use, the ticket's `## Done when` block is the whole execution contract: work on the ticket's branch, confirm each blocker's result in the working tree, verify every criterion, run the full test suite and linter, record decisions under `## Comments`, set the status, and never commit.

If a blocker's result is missing from the working tree, the executor names it under `## Comments` and stops; bring that result onto the ticket's branch and rerun `/plan`.

When the ticket needs a migration, a dependency install or an external check, the executor sets `ready-for-human`, names the step and the evidence it expects under `## Comments` and stops. Do the step, set the status back to `ready-for-agent` and rerun `/plan`: the executor checks the result in the current environment and continues, or sets `ready-for-human` again.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/ticket-status-dark.svg">
  <img alt="A written ticket starts as ready-for-agent, or needs-info while a clarification is open; once answered it becomes ready-for-agent. The executor sets resolved or ready-for-human; after your step you set ready-for-human back to ready-for-agent and rerun /plan; wontfix is set by you, or by a review ticket's executor when no finding reproduced. These standalone statuses are separate from controlled outcomes, lead acceptance and commit checkpoints; executors never commit." src="docs/images/ticket-status-light.svg">
</picture>

In a lead-controlled run, an explicit [controlled-run packet](skills/dev-lead/references/controlled-run.md) adds the approved feature context, lead technical-plan approval, permissions and bounded outcome. It preserves ticket status meanings: `resolved` is distinct from independent lead acceptance and a verified commit checkpoint. Controlled executors preserve the index as their packet requires and leave commits to the lead's dedicated `dev-commit` stage. Approved environment actions must name their exact target; otherwise the standalone human handoff still applies.

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
  <img alt="Feature-local records include spec, root cause, tickets, review, decision.log and research/dev-lead feature-plan/status/runs/questions. Manual task skills also journal decisions. dev-spec records built intent as SPEC.md or private local .SPEC.md; manual domain-modeling maintains glossary and ADRs." src="docs/images/artifacts-light.svg">
</picture>

Feature records stay local under `.scratch/<feature-slug>/`: spec, root cause, tickets, research, review reports and append-only JSONL `decision.log`. Task skills journal standalone work too. The lead keeps its feature plan, readable `status.md`, `runs/<run-id>/` and `questions/<question-id>/` under `research/dev-lead/`; status names the stage, ticket/action, wait reason, accepted tickets, current run, last verified commit and observation time. The journal and independently checked evidence establish accepted progress. When review resolves no feature, its report and tickets go under `.scratch/reviews/<branch-slug>/`. Keep `.scratch/` ignored; `dev-setup project` does that for you. Tracker issues are read, never written.

Durable knowledge lives in the repository: project specs (committed `SPEC.md` or private local `.SPEC.md`), and a glossary with decision records when the project keeps them. Feature records contain plans and execution evidence; project specs capture durable intent established by built work.

## Companion skills (not part of nxs)

These skills come from [mattpocock/skills](https://github.com/mattpocock/skills), not from this repository. nxs works without them. They are manual routes outside lead automation, marked MP with dim dashed outlines and readable labels in the diagrams. `dev-setup global` offers them in bundles, installs the ones you choose together with the skills they call, and configures them to write local `.scratch/` tickets in the nxs format:

| Bundle | Skills | Where it fits |
| --- | --- | --- |
| Core (recommended) | `grilling`, `grill-me`, `domain-modeling`, `grill-with-docs`, `to-spec`, `to-tickets` | Interview a plan, keep `GLOSSARY.md` and decision records that every dev skill reads, and turn the outcome into a spec and tickets |
| Wayfinding (needs Core) | `wayfinder`, `research`, `prototype` | Plan work bigger than one session as a map of decision tickets, answered by research, prototypes and grilling |
| Architecture (needs Core) | `improve-codebase-architecture`, `codebase-design` | Find modules worth deepening and design their interfaces |
| Sessions | `handoff`, `retro`, `writing-for-agents`, `to-questionnaire` | Carry context between sessions, look back on them, write instructions for agents |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/bundles-dark.svg">
  <img alt="Manual companion bundles: Core is recommended; Wayfinding and Architecture need Core; Sessions stands alone. Each skill lists the skills it calls, and dev-setup adds missing ones. setup-matt-pocock-skills is never offered." src="docs/images/bundles-light.svg">
</picture>

A skill that calls another pulls it in: choosing Wayfinding without Core also installs `grilling` and `domain-modeling`. `setup-matt-pocock-skills` is never offered, because `dev-setup global` writes the configuration it would create.

Two routes lead to the same `spec.md` and `issues/` files:

- `dev-rnd` alone: it asks its own questions, compares approaches and writes the spec and tickets in one command. Use it when you start from a request.
- `grill-me` or `wayfinder`, then `to-spec` and `to-tickets`: the interview or the map settles the decisions, and the `to-*` skills only write them down. `dev-rnd` would ask again, so use this route when the decisions are already made in the session. `/dev-rnd <spec-path>` can also slice a spec written by `to-spec`.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/grill-dark.svg">
  <img alt="Manual companion route: grill-with-docs writes the glossary, to-spec writes spec.md in the same session, to-tickets writes tickets in the tracker format, and /plan runs them; /dev-rnd with the spec path is the alternative slicer." src="docs/images/grill-light.svg">
</picture>

For work bigger than one session, `wayfinder` keeps a map of decision tickets across sessions and hands the settled destination to the same `to-spec` and `to-tickets`:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/wayfinder-dark.svg">
  <img alt="Manual companion route: session 1 of wayfinder writes map.md and decision tickets; later sessions resolve one ticket each and update the map; once the way is clear, to-spec and to-tickets write a new feature for /plan." src="docs/images/wayfinder-light.svg">
</picture>

Tickets from either route run with `/plan <ticket-path>`. In a feature that already has tickets, new ones are numbered after the highest existing number.

For local previews and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md).

Use `to-questionnaire <participant and context>` to prepare a document linking unanswered questions to affected decisions. Sending requires a separate explicit instruction; client behavior is unverified.

Use `to-handoff [task or destination path]` to save accepted, open and unverified context for a fresh session. A branch alone does not identify a task; client behavior is unverified.
