# nxs

Seven independently invoked skills for coding agents. Discuss an uncertain idea with `rnd-grill`, diagnose a failure with `rnd-debug`, or bring a clear request directly to `dev-exec`. Review the intended changes, record material project contracts when needed, and commit only within explicit authorization. Setup is a separate support operation.

## Skill catalog

| Skill | Result |
| --- | --- |
| [rnd-grill](skills/rnd-grill/SKILL.md) | Investigate uncertainty, compare alternatives and agree on a solution; directly save useful approved results when requested. |
| [rnd-debug](skills/rnd-debug/SKILL.md) | Reproduce a failure and save a confirmed cause or the exact missing evidence, without implementing a fix. |
| [dev-exec](skills/dev-exec/SKILL.md) | Establish acceptance criteria, obtain approval for a concrete plan, implement and verify; decompose or save a handoff when useful. |
| [dev-review](skills/dev-review/SKILL.md) | Independently review intended changes, verify findings and return selected corrections to execution without creating tickets. |
| [dev-spec](skills/dev-spec/SKILL.md) | Optionally record material built-work contracts in project `SPEC.md` or private `.SPEC.md`. |
| [dev-commit](skills/dev-commit/SKILL.md) | Make authorized atomic commits while preserving unrelated working and staged changes. |
| [nxs-setup](skills/nxs-setup/SKILL.md) | Audit a scoped goal, project or global setup and apply its exact approved package, or report readiness without writes. |

The six skills other than `dev-commit` require explicit selection or an instruction explicitly covering their work. `dev-commit` also accepts a direct commit request, not a discussion about commits. Use the selected client's skill invocation, such as `/dev-exec` or `@dev-exec` where supported. Source presence does not establish native registration or live compatibility; see [client scenarios](tests/client-scenarios.md).

## Development flow

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/workflow-dark.svg">
  <img alt="rnd-grill, rnd-debug or a clear request feed dev-exec, followed by dev-review, optional dev-spec and authorized dev-commit. Selected review corrections return to dev-exec. nxs-setup stands outside the chain." src="docs/images/workflow-light.svg">
</picture>

Arrows are possible handoffs, not automatic launches or new authorization. Dashed routes are conditional or return paths. Reuse an instruction already explicitly covering several operations only within its actual scope. Implementation can finish without a commit; authorized checkpoints may also occur during execution.

- **Uncertain idea:** use `rnd-grill` for evidence and meaningful choices. Research, dependent-question mapping, opportunity surveys, selected-boundary design and explicitly scoped isolated experiments are techniques, not mandatory stages.
- **Failure:** use `rnd-debug`. A confirmed eligible cause goes directly to `dev-exec`; uncertain causes stop with missing evidence, not a ready fix.
- **Clear request:** use `dev-exec` directly. A small task needs no feature spec, ticket, task directory or journal. Execution still presents a concrete plan and waits for applicable approval before implementation.
- **Existing changes:** use `dev-review`. Ordinary review covers the whole intended net task, including relevant committed checkpoints and remaining staged, unstaged and untracked changes. It requires no `git add`. Explicit narrower scope stays narrow; ambiguous ownership or missing coverage stops the affected review.
- **Selected corrections:** pass the review report and finding numbers directly to `dev-exec`. Selection or a verdict alone does not authorize a fix. Execution obtains applicable plan/fix approval and reproduces or confirms each selected finding first; a nonreproduced finding stays documented, not silently fixed.
- **Material built intent:** use `dev-spec` when a durable project contract needs recording. No durable change means no spec edit, only after intended-work coverage is established.
- **Commit:** use `dev-commit` for authorized remaining changes or approved execution checkpoints. Existing `Do not commit` instructions remain binding.

## Discussion and diagnosis

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/grill-dark.svg">
  <img alt="rnd-grill can finish in dialogue, directly save an approved useful record, or suggest dev-exec for sufficient agreed scope; saving and implementation have separate approval boundaries." src="docs/images/grill-light.svg">
</picture>

Agreement can stay in dialogue. A requested save shows content and destination and reuses only matching approval. Choose the useful record, not one of every kind: a decision, feature description, evidence report or participant questionnaire. Glossary and ADR proposals require their own concrete approval; a questionnaire authorizes no sending. An experiment remains isolated and retained; success authorizes no production transfer, reuse or deletion.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/bug-dark.svg">
  <img alt="rnd-debug saves root-cause evidence. A confirmed right cause can feed dev-exec; silent and wrong require intent agreement, feature returns to rnd-grill, and unconfirmed causes need another probe." src="docs/images/bug-light.svg">
</picture>

Diagnosis records observed evidence separately from intended behavior. `right` means records establish intent and the code differs; `silent` needs agreement on intent, and `wrong` needs agreement on correcting the record. `feature` means changing a decided behavior and returns to discussion. Project-spec corrections belong to `dev-spec` after the fix, not diagnosis.

## Optional tickets and continuation

`dev-exec` owns [ticket rules](skills/dev-exec/references/ticket.md), the [template](skills/dev-exec/assets/ticket.md), optional decomposition and [handoff saving](skills/dev-exec/references/handoff.md). Large work can use independently checkable units and real prerequisites. Saving tickets is not approval to implement them. Existing ticket identities, numbering, branches, execution text, prohibitions and history stay intact.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/ticket-status-dark.svg">
  <img alt="Optional tickets move from needs-info to ready-for-agent, may wait in ready-for-human, and resolve only after criteria and required checks pass. Returning from a human step requires actual result verification; wontfix needs a user decision or an existing ticket exception." src="docs/images/ticket-status-light.svg">
</picture>

Status alone proves no prerequisite result. The executor checks the selected working tree and environment, including after a human step. An install, migration or external action needs approval covering the concrete action and target plus native permissions; otherwise the affected work stops with expected evidence. Interrupted or uncertain effects are reconciled before retrying.

A saved handoff is optional and carries the goal, approved scope, decisions, open questions, relevant paths, verification, actual Git/checkpoint state and next authorized action. It promises no cross-client session recovery. Old task records remain context, not a live coordination protocol or fresh authorization.

## Artifacts and ownership

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/artifacts-dark.svg">
  <img alt="rnd-grill owns approved preparation and domain records, rnd-debug diagnosis, dev-exec optional tickets and handoffs, dev-review its report, and dev-spec built-work project specs. No universal artifact chain is required." src="docs/images/artifacts-light.svg">
</picture>

Reuse established paths. When durable local task records are needed, `.scratch/<feature-slug>/` is the default, not an entry requirement. A lowercase feature `spec.md` describes proposed behavior; project `SPEC.md` or private `.SPEC.md` records built intent and belongs exclusively to `dev-spec` in normal execution. [GLOSSARY.md](GLOSSARY.md) and ADRs record terms and decisions. Preserve existing artifacts and history rather than migrating them as a side effect of a source update.

## Setup and installation

`nxs-setup` is useful independently, not a required development stage. It audits a concrete goal, `project` or `global`, shows one coherent package and writes only the approved diff. Decline changes nothing; an already-current setup is a no-op. `project --readiness` and `global --readiness` only report relevant prerequisites. Native review workers are not a prerequisite for ordinary discussion or execution. The [capability map](skills/nxs-setup/references/capabilities.md) describes source coverage, not registration or a live compatibility result.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/setup-dark.svg">
  <img alt="nxs-setup audits a goal, project or global target, shows an exact package and applies only approved changes. Readiness takes project or global and stops with a report; decline and current repeats write nothing." src="docs/images/setup-light.svg">
</picture>

Source edits do not update installed copies or personal settings. Setup neither installs the catalog nor offers companion bundles. After publication, the Skills CLI can install from the published source, for example `npx skills@latest add -g Villhard/nxs`, with interactive skill and agent selection. A scoped update can name a retained skill, for example `npx skills@latest update -g dev-exec`; list other intended names explicitly. Inspect installed paths, provenance and proposed changes first: a name filter is not a source filter, and an interactive update may offer to remove other entries from the same source/ref. Do not confirm unplanned deletions or same-name replacements. Clean installation, upgrade effects and native registration for the simplified contracts remain unverified. Use the separate disposable preview in [CONTRIBUTING](CONTRIBUTING.md#local-development-and-release) for an unpublished candidate.

## History and verification

[ADR 0009](docs/adr/0009-seven-skill-direct-flow.md) records the seven-skill decision and supersedes the former coordination and mandatory journaling design. There is no lead/auto or retrospective stage. Independent review's finder/verifier workers remain. Historical ADRs, releases and [earlier client observations](docs/history/client-scenarios-before-0.77.md) are preserved; none proves the changed contracts. The simplified flow and both diagram themes require separate verification.

[CONTRIBUTING.md](CONTRIBUTING.md) documents source conventions and checks. [CHANGELOG.md](CHANGELOG.md) records history.
