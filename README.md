# nxs

Development skills for coding agents, from investigation and decisions through execution, review, project specs and commits. Commands are independently invoked; an artifact or approval for one stage does not start the next. Removal from source does not establish a route or installation cutover. [Client scenarios](tests/client-scenarios.md) distinguish observed behavior from unverified routes.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/workflow-dark.svg">
  <img alt="An idea, failure, existing changes or clear request can enter different commands. An approved feature spec, eligible confirmed cause and selected review findings can feed to-tickets. Ready to-tickets work can be handed to dev-exec." src="docs/images/workflow-light.svg">
</picture>

Blue names are commands; orange labels are records and grey labels are conditions or results. Dashed arrows show possible conditional handoffs, not automatic actions. The example is one route, not a required sequence: a clear request can also enter execution directly, and investigation can end with evidence or a decision. A saved artifact does not authorize the next operation by itself. An existing instruction or approval can authorize several operations within its scope; otherwise the applicable request or approval is needed.

Start with the result you need:

- "I have a broad goal and do not know which questions to answer first" - use `rnd-map`.
- "This behavior fails and I need evidence of the cause" - use `rnd-debug`; an eligible confirmed cause can inform tickets.
- "I have an approved feature spec and need executable work" - use `to-tickets`.
- "Implement this clear request" - use `dev-exec` for a plan and execution in the current session.
- "Review these changes" - use `dev-review`; its ordinary route can create selected tickets, while `--to-tickets` saves a selection for a separate `to-tickets` step.

## Target catalog

These 19 commands are in the source tree. Presence and shell checks do not prove registration or live behavior in a client. Invoke explicitly using `/` in supported clients or `@` in OpenCode; `dev-commit` also accepts a direct commit request. Read the linked contract for inputs, approvals and stops.

### Investigation and decisions

| Command | Purpose |
| --- | --- |
| [rnd-map](skills/rnd-map/SKILL.md) | Map an uncertain goal into linked decision questions and dependencies. |
| [rnd-grill](skills/rnd-grill/SKILL.md) | Discuss an idea or plan through evidence-backed choices, ending in dialogue or a request to save. |
| [rnd-research](skills/rnd-research/SKILL.md) | Investigate a question and save attributable findings and limits without making the user's decision. |
| [rnd-prototype](skills/rnd-prototype/SKILL.md) | Test one hypothesis with a retained temporary prototype and an evidence-backed verdict. |
| [rnd-debug](skills/rnd-debug/SKILL.md) | Investigate a failure and save a confirmed root cause or the missing evidence. |
| [rnd-audit](skills/rnd-audit/SKILL.md) | Survey a project and rank evidence-backed architecture opportunities. |
| [rnd-design](skills/rnd-design/SKILL.md) | Design an explicitly selected module or seam and save an agreed interface decision. |

### Artifacts

| Command | Purpose |
| --- | --- |
| [to-decision](skills/to-decision/SKILL.md) | Show and explicitly save approved conclusions or unfinished discussion. |
| [to-spec](skills/to-spec/SKILL.md) | Turn a saved decision or clear request into a feature spec with questions and acceptance checks. |
| [to-tickets](skills/to-tickets/SKILL.md) | Create or revise executable tickets from an approved feature spec, eligible confirmed cause or selected review findings. |
| [to-questionnaire](skills/to-questionnaire/SKILL.md) | Prepare recipient-specific questions for missing facts or decisions without sending them. |
| [to-handoff](skills/to-handoff/SKILL.md) | Save resumable context, separating accepted, open and unverified state. |

### Development

| Command | Purpose |
| --- | --- |
| [dev-exec](skills/dev-exec/SKILL.md) | Execute a ticket or clear request in the current session through an approved plan and checks. |
| [dev-review](skills/dev-review/SKILL.md) | Review changes and verify findings; `--to-tickets` saves a selection for a separate ticket step. |
| [dev-spec](skills/dev-spec/SKILL.md) | Record durable project specs from built work. |
| [dev-commit](skills/dev-commit/SKILL.md) | Commit existing changes in atomic groups. |

### Support and coordination

| Command | Purpose |
| --- | --- |
| [nxs-lead](skills/nxs-lead/SKILL.md) | Coordinate entrusted work using bounded native subagents and independently checked handoffs. |
| [nxs-setup](skills/nxs-setup/SKILL.md) | Audit a setup goal and apply an approved package, or report readiness. |
| [nxs-retro](skills/nxs-retro/SKILL.md) | Review one session and save evidence-based improvement proposals. |

## Using the stages

A possible independent route is `rnd-grill` -> `to-decision` -> `to-spec` -> `to-tickets` -> `dev-exec`; continue only within the authorization already given or after obtaining any missing request or approval. A clear request can go directly to `dev-exec`, which presents a plan before implementation. Review, recording built project intent and committing are separate steps.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/grill-dark.svg">
  <img alt="Discussion can end in dialogue; an approved decision can feed a feature spec and tickets through separately requested steps." src="docs/images/grill-light.svg">
</picture>

For a failure, `rnd-debug` records evidence and an eligible confirmed cause can be passed to `to-tickets`; uncertain causes do not produce ready work.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/bug-dark.svg">
  <img alt="Diagnosis records evidence and classifies a cause; an eligible confirmed cause can be passed to to-tickets, while a feature returns to discussion and uncertainty stops the handoff." src="docs/images/bug-light.svg">
</picture>

`rnd-map` records linked decision questions. Its decision tickets are not implementation tickets; resolving a map does not authorize implementation. Research and prototypes can inform a decision, and a later feature spec and tickets require their own scope.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/wayfinder-dark.svg">
  <img alt="rnd-map links decision questions by dependencies. Research or prototypes can supply evidence; resolving questions recomputes the frontier. Implementation requires separate scope." src="docs/images/wayfinder-light.svg">
</picture>

Ticket status and executor evidence are distinct from coordinator acceptance and commit checkpoints. See [ticket rules](skills/to-tickets/references/ticket.md) and [execution](skills/dev-exec/SKILL.md).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/ticket-status-dark.svg">
  <img alt="Tickets can need information, be ready for an agent, wait for a human, resolve or be closed as wontfix; the executor checks prerequisites and records evidence." src="docs/images/ticket-status-light.svg">
</picture>

## Coordination

`nxs-lead` delegates bounded work through the selected client's native subagent facility, waits for results and independently checks them. Ordinary mode relays substantive decisions; guarded auto requires explicit selection and approvals described in its [contract](skills/nxs-lead/SKILL.md). Native permission enforcement is client-dependent. Recorded Codex and OpenCode observations are limited cases; Claude Code, guarded auto and full coordinated workflows remain unverified.

## Setup and installation

`nxs-setup` supports a specific goal, project or global setup, and report-only readiness. It audits first, shows a coherent proposal and applies the approved package. It does not offer or install companion bundles; its [capability map](skills/nxs-setup/references/capabilities.md) describes source coverage, not registration. Setup and upgrade behavior are not live verified.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/setup-dark.svg">
  <img alt="nxs-setup audits a goal, project or global setup, proposes a package and applies approved changes. Readiness requires project or global and only reports." src="docs/images/setup-light.svg">
</picture>

The Skills CLI can install from the published GitHub source, for example `npx skills@latest add -g Villhard/nxs`, with interactive skill and agent selection. After the desired changes are published, update specific globally installed skills by name, for example `npx skills@latest update -g nxs-lead`; list additional intended names explicitly. An update uses the recorded installation source, not the current checkout, and selecting by name is not a source filter. Even with a name filter, an interactive update may offer to remove other skills from the same source and ref; inspect the proposed removals and do not confirm unplanned deletions. Inspect installed paths and provenance first; do not assume a same-name skill can be replaced safely. The new catalog's clean and existing installation paths, source migration, collision handling, targeted update effects and native registration have not passed the live cutover gate. For an unpublished local candidate, retain the separate disposable preview in [CONTRIBUTING](CONTRIBUTING.md#local-development-and-release).

## Artifacts

Feature records typically live under `.scratch/<feature-slug>/`: decisions, research, feature specs, tickets and handoffs retain their own evidence and history. Existing paths take precedence over defaults. Project `SPEC.md` or private `.SPEC.md` records built intent; `dev-spec` is its only writer. Glossary and ADRs record domain terms and decisions.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/artifacts-dark.svg">
  <img alt="Feature records contain decisions, research, specs, tickets and handoffs; project specs record built intent and glossary and ADRs record domain decisions." src="docs/images/artifacts-light.svg">
</picture>

[CONTRIBUTING.md](CONTRIBUTING.md) documents source conventions and checks. [CHANGELOG.md](CHANGELOG.md) records history.
