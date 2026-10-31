# Changelog

All notable changes to the `dev` skills are documented in this file. Releases before 0.17.0 shipped under the name `nxs`; releases up to 0.43.0 shipped as the `dev` plugin.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Lead design records (2026-10-30) define coordinator, plan and decision-log terms, autonomy and reapproval boundaries, model policy, approved environment steps, optional companions, focused R&D, parallel worktree integration, shared task journaling and Codex-first verification.
- Lead reliability design (2026-10-30) prioritizes a sequential full cycle and recovery, bounded structured worker outcomes and deterministic helpers, and states the limits of journaling manually invoked companion skills.
- Companion integration decision (2026-10-30) distinguishes manual dialogue from verified lead execution contracts and records selective adoption into nxs as a future investigation.
- `CONTRIBUTING.md` states the skill name rule - `dev-` plus one short word the user recognizes, in a namespace that stays clear of companion skills and client commands - and [ADR 0007](docs/adr/0007-skill-names.md) records why the existing names stay.

### Changed

- README and diagrams (2026-11-01) map skill entry points, conditional handoffs, task records and setup routes with current authorization boundaries.
- README catalog and workflow diagrams (2026-11-01) group skills by purpose and show conditional paths between them.
- README, CONTRIBUTING, GLOSSARY, project spec, client scenarios and diagrams describe the additive catalog, retained legacy routes and unverified cutover.
- README "Run a ticket" says what to do when the executor stops on a missing blocker result.

### Fixed

- Shell skill checker validates frontmatter scalars and release dates and rejects empty release entries.
- README distinguishes same-name nxs and companion skills before choosing a route.
- Ticket template and `dev-setup` tracker template `## Done when` record a missing blocker result in one `## Comments` line and stop instead of asking, so Claude Code plan mode writes the line after the plan is approved.

## [0.74.1] - 2026-11-01

### Fixed

- Ticket status diagrams show the selected executor after a human step; the workflow diagram and README emphasize the current `dev-exec` handoff and remove the legacy section.

## [0.74.0] - 2026-11-01

### Changed

- `to-tickets` hands eligible ready work to `dev-exec`; the shared ticket, setup tracker and triage label templates support both that executor and retained `/plan` routes, including the human-step return.
- README, CONTRIBUTING and client scenarios describe the selected handoff and observed verification limits.

## [0.73.1] - 2026-11-01

### Changed

- Project and `to-tickets` specs reconcile the additive workflow and its verification limits.

### Fixed

- Shell skill checks reject malformed or duplicate frontmatter, invalid invocation policy blocks and broken reference-style resource links.
- Pre-commit hook checks the staged snapshot so partial staging cannot bypass the structural checks.
- README places installation collision and verification guidance before install and update commands.

## [0.73.0] - 2026-11-01

### Changed

- `nxs-setup` source catalog and upgrade guidance distinguish the 19 agreed commands from retained routes and unverified registration.

## [0.72.0] - 2026-11-01

### Added

- `nxs-setup` adds independent global configuration and a 15-capability source map.

## [0.71.0] - 2026-11-01

### Added

- `nxs-setup` adds scoped goal and project setup with approved changes and report-only readiness; `nxs-retro` shares its writing guidance.

## [0.70.0] - 2026-11-01

### Changed

- Shared controlled-run references recognize explicit `nxs-lead` authorization alongside the retained lead.
- `dev-review` and contributor guidance name native subagents for retained routes.

## [0.69.0] - 2026-11-01

### Added

- `nxs-lead` defines explicit guarded auto and a local HTML defense.

## [0.68.0] - 2026-11-01

### Added

- `nxs-lead` defines evidence-based continuation without a recovery engine.

## [0.67.0] - 2026-11-01

### Added

- `nxs-lead` adds an explicit ordinary native-subagent coordinator candidate.

## [0.66.0] - 2026-11-01

### Added

- `nxs-retro` reviews one session and proposes evidence-based improvements within authorization boundaries.

## [0.65.0] - 2026-11-01

### Added

- `to-handoff` saves resumable context with or without a task journal.

## [0.64.0] - 2026-11-01

### Added

- `to-questionnaire` prepares recipient-specific questions without unsolicited sending or invented answers.

## [0.63.0] - 2026-11-01

### Added

- `rnd-map` charts and resumes local decision maps with explicit per-question permission and preserved dependencies.

## [0.62.0] - 2026-11-01

### Added

- `rnd-audit` saves a prioritized architecture survey or evidence-limited no-change result without implementing an opportunity.

## [0.61.0] - 2026-11-01

### Added

- `rnd-design` compares and saves an agreed design for a selected module without implementing it.

## [0.60.0] - 2026-11-01

### Added

- `rnd-prototype` tests a hypothesis with a retained local experiment and verdict without authorizing production changes.

## [0.59.0] - 2026-11-01

### Added

- `rnd-research` saves source-linked findings and limitations for a question as an additive candidate without deciding or starting a further stage.

## [0.58.0] - 2026-11-01

### Added

- `dev-review` offers an additive selection handoff to `to-tickets`, which creates tickets from current selected findings; the legacy review-to-fix route remains available.

## [0.57.0] - 2026-11-01

### Added

- `rnd-debug` records evidenced diagnosis without creating fix tickets; `to-tickets` accepts eligible confirmed causes as an additive candidate.

## [0.56.0] - 2026-11-01

### Fixed

- `dev-exec` records and runs the full checks a ticket requires and leaves it unresolved when a required test or linter command is missing or fails; `tests/client-scenarios.md` covers the completion gate.

## [0.55.0] - 2026-11-01

### Added

- `dev-lead` delegates bounded steps to the selected client's native subagents through `references/subagents.md`, and keeps progress and questions in ordinary local files through `references/questions.md`; missing capability stops the affected step.
- `dev-review` launches finder and verifier roles only through native subagents, with host-enforced permissions and prompt prohibitions reported separately.
- Shell structural checks in `.github/scripts/check-skills.sh` and a runtime guard in `.github/scripts/check-no-runtime.sh` replace the Python checker; both run in CI and the pre-commit hook.
- [ADR 0008](docs/adr/0008-native-subagent-coordination.md) records native-subagent coordination and the removal of the custom runtime.
- `tests/client-scenarios.md` covers native-subagent delegation, local questions, capability stops and the structural checks.

### Changed

- `dev-lead`, `dev-review`, `dev-setup` readiness, `README.md`, `SPEC.md` and `CONTRIBUTING.md` no longer require Python 3, a terminal session, a controller, a HUD, a nested CLI runner or the removed terminal app.
- Task journals and controlled-run packets use plain append-only files; the shared ticket `## Done when` block and the `dev-setup` tracker copy record the journal and native-continuation rules.
- Setup and workflow diagrams and their alternative text describe native subagents and the current readiness checks.

### Removed

- All repository Python: the `dev-lead` runner, approval, status, inventory, harness, outcome, mechanics and commit helpers, the `dev-review` adapter copies, every bundled `journal.py`, the Python checker and its regression suite, and `tests/test_dev_lead.py` and `tests/test_harnesses.py`.
- Bundled `scripts/` and `__pycache__` directories, the bounded CLI review route and the terminal identity, HUD, questionnaire-waiter and owned-terminal cleanup contracts.

## [0.54.0] - 2026-10-31

### Added

- `dev-exec` adds an explicit standalone ticket/clear-request executor candidate with plan approval, prerequisite-result checks, human-step gates and separate review/spec/commit handoffs.

### Changed

- Checker catalog and fixtures include `dev-exec` policies and self-contained shared resources while preserving existing ticket templates and `/plan` routes.
- README, CONTRIBUTING and client scenarios document the additive executor, resource propagation and proportionate verification limits.

## [0.53.0] - 2026-10-31

### Added

- `to-tickets` adds explicit independent feature-spec slicing, history-preserving reuse, dependency evidence and authorized revision gates with the retained `/plan` handoff.

### Changed

- `to-tickets` owns the byte-identical ticket rules/template consumed by `dev-rnd`, `dev-bug` and `dev-review`; existing routes and execution text remain available.
- Checker catalog, shared-copy expectations, tracker Done when source and regression fixtures include the self-contained `to-tickets` candidate.
- README, CONTRIBUTING and client scenarios document the additive ticket candidate, canonical propagation and proportionate observation limits.

## [0.52.0] - 2026-10-31

### Added

- `to-spec` adds explicit independent feature spec preparation from decisions or clear requests, authorized drafts, source/dependency evidence and preservation gates, without ticket slicing.

### Changed

- Checker catalog and fixtures include `to-spec` policies and self-contained shared resources; `to-spec` owns the byte-identical feature spec template while legacy routes stay available.
- README, CONTRIBUTING and client scenarios document the additive spec candidate, resource ownership and proportionate observation boundaries.

## [0.51.0] - 2026-10-31

### Added

- `rnd-grill` adds an explicit discussion-only candidate with evidence-backed choice rounds, shared discussion/domain rules and resume boundaries.
- `to-decision` adds explicit approved or unfinished decision saving, approved glossary/ADR proposals, direct domain-only requests within invoked scope and preservation on repeat saves.
- Checker fixtures and client scenarios cover the additive candidates, explicit policies and self-contained shared resources; existing manual and coordinator routes remain available.

### Changed

- README documents candidate usage and separate saving approval; CONTRIBUTING records canonical resource ownership and the independent-workflow naming extension.

## [0.50.0] - 2026-10-31

### Changed

- `dev-lead` explicitly finishes HUD presentation before releasing its controller, preserving final local status, foreign UI and non-replayed close evidence across recovery.

## [0.49.0] - 2026-10-31

### Added

- `dev-lead` adds lead-only timestamped status/HUD presentation and durable bounded questionnaire transport, with recoverable ownership of updated HUDs, genuine approval/form regressions and release-controlled pending fixtures; the lead retains approval and workflow decisions.
- `dev-setup` adds explicit global/project `--readiness` reports with bundled native discovery, actual requirement diagnoses and remedies, without setup writes or installation.

### Changed

- `dev-lead` checkpoints each accepted implementation and its verified review corrections through checks, scoped review, built-work specs and atomic commits before the next independent ticket, retaining conservative commit recovery and final whole-feature review. README and all eight light/dark diagram pairs show agterm-only delegation alongside manual routes, report-only readiness, local status/journal/run records and distinct ticket/checkpoint acceptance, with matching Mono surfaces and readable labels.
- Runtime tests and client scenarios cover checkpoint composition, lost commit responses, foreign index preservation and readiness/setup boundaries, separating mechanics fixtures from consumer and live verification.

### Fixed

- `dev-lead` outcome packets, schema descriptions and shared controlled-run instructions clarify existing status fields and file artifacts for native emitters.
- `dev-lead` and the bundled `dev-review` runner recheck accepted artifacts and command evidence after terminal observation, preserving journal-prefix growth; disposable regressions cover changed or missing evidence before cleanup.
- `dev-lead` generated-form regression executes the extracted submit script with existing Node and checks decoded choice/text payloads; absent Node skips only JavaScript coverage, while controls and probe checks still run.

## [0.48.0] - 2026-10-30

### Fixed

- `dev-lead` and the bundled `dev-review` runner (2026-10-30) require stopped recorded processes and groups before continuation or another launch, including successful CLI exits; runtime regressions cover surviving children and worker destination rejection.

### Changed

- `dev-lead` requires verified agterm entry before coordination side effects and pins worker destinations and normalized unique labels in run records.
- `dev-lead` and the bundled `dev-review` runner retain terminal and primary-pane ownership separately from native sessions and close verified stopped shell/command-wait terminals, including answered and resolved blocked turns tied explicitly to accepted exact continuations, through recorded, non-replayed cleanup.
- Runtime tests and client scenarios cover agterm identity failures, focus changes, naming collisions, owned cleanup and lost close responses, distinguishing fixtures from live verification.

## [0.47.0] - 2026-10-30

### Changed

- `dev-lead` supports native Claude Code, Codex and OpenCode v2 discovery, model effort validation, bounded outcomes and exact-session continuation without silent runtime substitution.
- `dev-review` bundles the native CLI adapter for all finder and verifier roles, with enforced repository write denial on Claude Code and OpenCode read-only runs.
- Lead packets, guides and client scenarios distinguish native registration from pinned candidate context, native permissions, protocol tests and live verification; shared helper and CI checks cover every adapter.

## [0.46.0] - 2026-10-30

### Added

- `dev-lead` adds an explicit Codex-only sequential coordinator with feature and ticket plan approval, visible agterm workers, bounded outcomes and independent acceptance checks.
- `dev-lead` helpers discover actual skills and models, persist launch and commit intent, validate outcomes and reconcile interrupted work without replaying unknown effects.
- Task journal and controlled-run resources are bundled identically in `dev-lead`, `dev-rnd`, `dev-bug`, `dev-review`, `dev-spec` and `dev-commit`.
- Sequential lead regressions cover question continuation, invalid results, discovery failure, locking, interrupted runs, lost responses, duplicate prevention and stale evidence.

### Changed

- `dev-rnd --decision-only` saves a research conclusion, evidence and remaining questions without implementation tickets; normal invocation retains spec and ticket slicing.
- Ticket executor and tracker templates record task outcomes and accept lead ticket-plan approval only in an explicit authorized controlled context.
- `dev-review` bundles a Codex read-only finder and verifier launch route while retaining all existing roles and orchestrator report ownership.
- `dev-spec` and `dev-commit` retain source and Git boundaries while recording task journal events; project-spec readers include `dev-lead`.
- `SPEC.md` records the built controller, journal and independent acceptance boundaries.
- `dev-setup` global and project templates propose journal rules without changing the user's installation during source development.
- README, CONTRIBUTING and client scenarios document the lead, invocation boundaries, local artifacts and verification limits.
- Skill-tree checks validate the seventh skill, shared journal and runner copies and runtime resource isolation; CI retains `House style + frontmatter` and runs lead regressions.

### Fixed

- CI declares `pull_request` beside `push`, so pull requests can trigger the required checks.

## [0.45.0] - 2026-10-28

### Added

- `dev-spec` records durable project specs from landed work: committed `SPEC.md`, or private `.SPEC.md` kept out of Git through the clone's exclude file.
- `dev-setup project` audits a repository and, through one approved diff, writes a `## nxs` instruction section with the branch rule and the test, lint and typecheck commands, and ignores `.scratch/`.
- `dev-setup` accepts `global` or `project`; without an argument it asks inside a Git repository and uses `global` outside one.
- `dev-setup global` wires Claude Code, Codex and OpenCode to `~/.agents/AGENTS.md`, merging existing client files into it instead of replacing them, and through one approved diff adds a `## nxs` section (read project specs on the path, branch rule) and the rule groups the user accepts from a bundled template.
- `dev-setup global` offers mattpocock/skills as a recommended Core bundle (grilling, domain modeling, `to-spec` and `to-tickets`) plus Wayfinding, Architecture and Sessions bundles, adds the skills a chosen skill depends on and names each as required by it, checks the names against the upstream listing, installs the chosen ones after approval, and writes an `## Engineering skill defaults` section and `~/.agents/docs/{issue-tracker,triage-labels,domain}.md` for local `.scratch/` tickets numbered after the existing ones.
- `dev-setup global` skips a `## nxs` line whose rule the source already states elsewhere and reports it as covered; a section left empty is not created.
- `dev-setup global` counts a client path that resolves to the source as wired and never links over it, links a copy identical to the source without merging it, strips `## nxs` and `## Engineering skill defaults` from merged content, and merges a file reached through several client paths once.
- `dev-setup` treats its owned sections as template-owned: `global` and `project` say that an edit inside `## nxs` is replaced on the next run and custom rules go outside it, where the audit reports them as covered with the stating line; `global` puts merged content under its own `## Merged from <path>` heading, so it never joins a `## nxs` section that ends the source.
- `dev-setup project` resolves `AGENTS.md` and `CLAUDE.md` with `realpath` and counts `## nxs` headings per real file, so a repeat on `CLAUDE.md -> AGENTS.md` updates the one section instead of stopping on a duplicate heading.
- Shared `project-specs` reference: how `dev-rnd`, `dev-bug`, `dev-review` and `dev-spec` find and read project specs.

### Changed

- Ticket template, `dev-setup` tracker template and triage labels make `ready-for-human` a round trip: the human does the step, sets `ready-for-agent` back and reruns `/plan`, and the executor verifies the result in the current environment instead of repeating the step; the `ticket` reference says so.
- Ticket template and `dev-setup` tracker template `## Done when` have the executor confirm each direct blocker's result in the working tree before the first implementation edit; `resolved` alone no longer suffices, and the `ticket` reference says so.
- CONTRIBUTING allows a setup skill to write rules and config into client instructions only through an approved diff.
- `dev-spec` creates no module spec in a directory that holds a foreign `SPEC.md` and reports the module as skipped.
- `dev-bug` classifies a confirmed cause as `right`, `silent`, `wrong` or `feature` against domain documents and specs; `feature` writes no fix ticket and hands off to `dev-rnd`.
- `dev-bug` fix ticket for a `wrong` cause names a spec record only as context; `dev-spec` corrects the spec after the fix lands.
- `dev-rnd` accepts a `root-cause.md` path as a request source.
- `dev-review` reports a diff that contradicts a project spec.
- `dev-review` lists a spec contradiction that a requirement replaces, with a matching diff, as a `pending dev-spec` follow-up instead of a finding; the verifier packet carries the same rule.
- `feature-directory` reference counts project specs as domain documents.
- `dev-rnd` clarifies in rounds of independent questions instead of one question at a time, frames options as observable behavior and decides internal-only choices itself, recording the reason in the spec.
- Checker test covers every shared copy.
- Checker fails when the fenced `## Done when` block in `dev-setup`'s `issue-tracker` template differs from `dev-rnd`'s ticket template; its test covers the drift.
- `dev-setup` states the approval, owned-section, repeat, "already set up" and check rules once in a CONTRACT section that both modes follow; `global` rule groups reuse the `## nxs` coverage table, and the `project` section template points to AUDIT step 3 for the branch rule.
- `dev-setup global` counts a mattpocock skill as installed only from a lock entry with source `mattpocock/skills`; a same-name skill directory without it is reported as unverified, kept out of the install command and never overwritten, and the skills that need it are reported as blocked.
- `dev-setup` `issue-tracker` template numbers wayfinder child tickets after the existing tickets in `issues/`.
- README names Claude Code, Codex and OpenCode as target clients and links `tests/client-scenarios.md` for verified flows instead of claiming identical behavior.

### Fixed

- CI runs the skills CLI discovery check on Node 22, which the skills CLI requires.

## [0.44.0] - 2026-10-27

### Changed

- Distribution moves from the `dev` plugin (marketplaces and the OpenCode installer) to standalone agent skills installed with the skills CLI; each skill installs into the shared agents skills directory and is linked per client.
- Commands are renamed: `rnd`, `bug`, `review` and `commit` become `dev-rnd`, `dev-bug`, `dev-review` and `dev-commit`.
- Skills declare frontmatter `name` and bundle their references, templates and reviewer roles inside their own directories.
- Agent launch keeps a single generic route: any host tool that starts a fresh-context agent with a complete prompt; plugin-registered agent identities and the installer route are removed.

### Removed

- The `plugins/dev` packaging, the `nxs` marketplace manifest and the OpenCode installer.

## [0.43.0] - 2026-10-26

### Changed

- `rnd` stops after laying out approaches and runs stress and shows the proposed spec only after the user chooses; a reply asks one thing.
- `rnd` shows all four stress parts in the reply before the proposed spec.

### Fixed

- `rnd` stops after offering `/plan` for a request that makes the spec ceremony, without drafting a spec or tickets.
- Ticket `**Branch:**` is proposed even when the project has no branch rule.
- `review` tickets always carry `**Blocked by:**`.

## [0.42.0] - 2026-10-23

### Changed

- OpenCode invokes `rnd`, `bug`, `review` and `commit` as `@<name>` skill mentions.

### Removed

- OpenCode installer no longer generates the `/dev/rnd`, `/dev/bug`, `/dev/review` and `/dev/commit` commands; updating removes them.

## [0.41.1] - 2026-10-23

### Changed

- `commit` states each rule once and ends with the step 5 report.
- `commit` message format lists plain verbs without a banned-verb list.
- `rnd` and `bug` keep the handoff rule only in the introduction; `rnd` clarifies code first, then a fuzzy domain term.
- `review-quality` and `review-testing` defer naming findings to the severity bar; `review-simplification` reports large in-scope fixes in reviewer terms.
- Agent launch reference drops client-testing guidance, now in the dev contributing guide.
- `review` heading uses the lowercase command name.

## [0.41.0] - 2026-10-23

### Changed

- `commit` description covers requests with limits such as "commit only X" and routes every commit through the skill.

### Fixed

- `bug` repeat rule leaves `root-cause.md` and the open ticket unchanged on the same confirmed cause.
- `commit` message format forbids body and trailer lines unless requested.

## [0.40.1] - 2026-10-22

### Changed

- README no longer describes the optional `revdiff-planning` companion.

## [0.40.0] - 2026-10-21

### Added

- OpenCode 2 installer `opencode/install.py`: copies this version into the OpenCode config directory, registers its skills and writes the `dev/review-*` subagents, the `/dev/<name>` commands and a `/plan` command when none exists.
- `agent launch` OpenCode route: the `subagent` tool with the installed `dev/<role>` agents and their host-enforced permissions.
- Client scenarios for OpenCode installation, invocation, the `/plan` handoff and the review launch.

### Changed

- `rnd`, `bug`, `review` and `commit` descriptions name the OpenCode `/dev/<name>` invocation.
- `rnd` and `bug` suggest `/plan <ticket-path>` in OpenCode too.
- README covers OpenCode installation and the steps verified in OpenCode.

## [0.39.0] - 2026-10-21

### Added

- `review-verify` role: one verifier checks every merged `review` candidate and returns confirmed, plausible or refuted with quoted evidence.
- `review` keeps plausible findings, at most major, with what would confirm them; the summary and tickets mark them.
- `review` lead conventions check: a changed line that breaks a quoted rule of a governing `CLAUDE.md` or `AGENTS.md`.
- `review-simplification` checks reuse of existing helpers and fixes at the wrong depth.
- `review-quality` checks moved code that lost a guard and wrappers that bypass the wrapped instance.

### Changed

- `review` VERIFY applies the verifier's verdicts instead of the orchestrator's own checks.
- Finder roles report a `Scenario:` line; `review-quality` passes an uncertain trigger to verification instead of dropping it.
- Review report requires `verdict:` on findings and dismissals; reports without it are invalid and start a new sweep.

## [0.38.3] - 2026-10-18

### Changed

- README names the steps verified in Codex and adds the one-command Claude Code install.
- `rnd`, `bug`, `review` and `commit` descriptions name the Codex `$dev:<name>` invocation.

### Removed

- Author email from the Claude Code manifest.

## [0.38.2] - 2026-10-17

### Added

- README names revdiff-planning as an optional `/plan` companion, verified in Claude Code.

## [0.38.1] - 2026-10-16

### Fixed

- Client scenarios for `review` restore the fixture's `.scratch/` before each ticket answer and ignore `.scratch/` entirely.
- Client scenarios ask for a fresh sweep on repeated `review` runs, and "Checked requirements" stages a diff on a feature branch.
- Client scenarios expect the feature's `spec.md` with the resolved ticket in `review` Requirements.

## [0.38.0] - 2026-10-16

### Changed

- `review` tickets list each finding's location and Problem under What to build.
- `review` writes `Branch:` on the base branch too; only a detached HEAD drops it.
- `review` checks findings against open tickets under `.scratch/reviews/<branch-slug>/issues/` and in the resolved feature's `issues/`.
- `bug` stops and asks on a repeat with a new confirmed cause while the fix ticket is open: update its criteria or close it.
- The `ticket` reference no longer lists command branch values; `bug` takes the project's branch rule with `<type>` `fix`.

### Fixed

- Staged `review` and its report currency no longer depend on `origin/HEAD`, `main` or `master`.
- Staged `review` reads a ticket's status and `Branch:` from the same version as its text.
- `review` keeps the ticket path of a covered finding after the answer instead of setting `none`.

## [0.37.1] - 2026-10-16

### Fixed

- Ticket reference no longer requires one branch for every ticket of a feature, matching the `Branch:` values `bug` and `review` write.

## [0.37.0] - 2026-10-16

### Changed

- `bug` writes the next fix ticket on a repeat when the existing one is `resolved` or `wontfix`.
- Client scenarios cover the `bug` repeat after a resolved ticket, `ready-for-human` and clarification markers in plan mode, the clear-request handoff to `/plan`, `review` of a feature or ticket path, the lead documentation check and tickets on the base branch.

## [0.36.0] - 2026-10-16

### Changed

- `review` tickets start with a criterion checkable at close: each finding reproduced before the change, a finding that did not is named and its criteria removed, `wontfix` only when none reproduced.
- The `ticket` reference lets the executor remove the criteria of a review finding that did not reproduce and set `wontfix` only when none did.
- `review` without an argument also reads resolved tickets of the current branch under `.scratch/reviews/<branch-slug>/issues/`.
- `review` links a finding an open ticket already covers to that ticket under `Already ticketed:` instead of proposing it again; `review.md` records that path in `ticket:`.
- `agent launch` no longer mentions saved notes in the reviewer packet.

## [0.35.0] - 2026-10-16

### Changed

- `review` ends with recommended tickets as groups of finding numbers: one per critical or major finding unless a named reason joins them, a minor finding with the major one that touches the same place, and the remaining minor findings together.
- `review` takes the answer as finding numbers ("1, 3", "all", "7 separately", "1 and 3 together", "none"); selected findings follow their recommended groups.
- `review` names an open user choice with a recommendation and splits the finding into its own `needs-info` ticket only when the answer leaves the choice open.
- `review.md` records `ticket: proposed <finding numbers>` until the answer.

### Removed

- `T<n>` labels of proposed tickets in `review`.

## [0.34.0] - 2026-10-16

### Changed

- `rnd` sends an already clear task to the client's `/plan` instead of `/dev:plan`.
- `commit` and the `commit format` reference serve standalone commits only.
- `agent launch` covers only the three review roles.
- The `ticket` reference no longer mentions `## Implementation`; the executor under `Done when` alone sets `ready-for-human` and `resolved`.

### Removed

- `plan` and `exec` commands, with the implementation template and the `exec no commits` option.
- `worker` role.
- `checks/` directory of the feature.

## [0.33.0] - 2026-10-16

### Added

- `review` ends with proposed tickets, combining findings with one cause, one fix or overlapping edits, and creates only the ones the user picks in text.
- `ticket:` field on each finding in `review.md`.
- Expected-load check in `review-quality`.

### Changed

- `review` has one mode: staged changes, otherwise the branch against its base; it stops on the base branch with nothing staged.
- `review` checks requirements and documentation itself and summarizes findings with what, problem, fix and the cost of skipping it.
- `review` finds requirements through the resolved tickets whose `Branch:` field names the current branch.
- `review.md` replaces `## Mode` with `## Sweep`.
- The `ticket` reference lets the executor set `wontfix` under the first criterion of a review ticket.

### Removed

- `fix` command.
- `review quick`, the `staged` and code path selectors and the `fix` argument.
- `review-implementation` and `review-documentation` roles.
- `fix:`, `fixed at:`, `re-check:`, `result:` and `mode:` fields of `review.md`, and the `review_phase: recheck` marker.

## [0.32.0] - 2026-10-16

### Added

- `ticket` reference owning the ticket template, numbering, fields and statuses for `rnd`, `bug` and `plan`.
- Optional `Branch:` field and a verbatim `Done when` section in the ticket template, so harness plan mode can execute a ticket with `/plan <ticket-path>`.

### Changed

- `bug` writes one fix ticket for a confirmed cause and none for an unconfirmed one.
- `rnd` and `bug` suggest `/plan <ticket-path>` at the handoff.
- `rnd` proposes a `Branch:` line for each ticket; `bug` sets `fix/<feature-slug>`.
- `plan` drafts new tickets by the `ticket` reference.
- `exec` does not apply a ticket's `Done when` section.

## [0.31.0] - 2026-10-16

### Changed

- `review quick` runs `review-quality` and `review-implementation` with their normal bounds and no longer covers tests, simplification or documentation.
- `fix` commits with a scoped `fix(<scope>): address review findings` message.

### Removed

- The `review_mode: quick` prompt marker and the quick-mode sections of `review-quality` and `review-implementation`.

## [0.30.1] - 2026-10-16

### Changed

- `review` and `fix` read the severity bar and finding verification from the `findings` reference.
- `review` and `fix` read the report format, validation and currency rules from the `review-report` reference.
- `commit` and `exec` read the message format and Git rules from the `commit-format` reference.
- `rnd`, `plan` and `bug` read feature location, local storage, tracker input, external specs and domain documents from the `feature-directory` reference.
- The `agent-launch` reviewer packet is the single packet definition for `review` and `fix` and carries the read-only check rule.

## [0.30.0] - 2026-10-16

### Added

- `rnd` saves research results and their raw data under the feature's `research/` directory.
- `bug` saves investigation probes under the feature's `research/` directory.
- `plan` places a ticket's local checks in the feature's `checks/<NN>-<slug>/` directory.

### Changed

- `exec` records a `Branch:` line in the ticket for every new start with commits.
- `review` finds resolved tickets of an ignored `.scratch/` by their `Branch:` line.

## [0.29.3] - 2026-10-14

### Changed

- `commit` derives the message scope from the changed area and stops only on an unclear type.

### Removed

- `commit` no longer restates the branch naming rule.

## [0.29.2] - 2026-10-14

### Added

- `review-quality` checks the contracts that comments on the changed code state.
- `review-quality` checks retries, restarts, concurrent instances, unenforced assumptions and unvalidated data from files, the network, subprocesses and the environment.

## [0.29.1] - 2026-10-13

### Fixed

- Codex plugin metadata enables discovery of the seven dev commands in BB.

## [0.29.0] - 2026-10-08

### Changed

- `exec` names the next ticket from a fresh read, with `plan` for an unplanned ticket and `exec` for a planned one.
- `exec` asks once before committing a new start on the review base branch.
- `plan` writes without a separate approval turn when invoked on an existing ticket path with no open question.
- `plan` pairs each acceptance criterion with its task checkbox before writing and asks when their literal values differ.
- `plan` proposes a concrete spec revision when an answer changes a recorded decision.
- Client scenarios cover unplanned tickets at `exec`, the next-ticket handoff, default-branch starts, named-ticket plans and spec revisions.

## [0.28.0] - 2026-10-05

### Changed

- `rnd`, `plan` and `bug` read an existing domain glossary and decision records for the affected area, read-only.
- `rnd` marks an approach that contradicts a recorded decision; `plan` carries applicable terms and decisions into Conventions.
- `review-documentation`, and `review-implementation` in quick mode, report a glossary or decision record the diff made stale.

## [0.27.2] - 2026-09-18

### Changed

- Condense every changelog entry to one-line bullets and state the entry format in CONTRIBUTING.

## [0.27.1] - 2026-09-18

### Fixed

- `rnd` skips tickets with bare or bold Type fields when selecting an implementation ticket for the plan handoff.

## [0.27.0] - 2026-09-18

### Changed

- `rnd` and `plan` use local Markdown storage only, with no tracker configuration, backend selection or assumed external commands.
- `rnd` accepts approved specs and compatible local artifacts and preserves decisions, blockers and existing history during slicing.
- `rnd` classifies decision inputs, requires remote source, parent and blocker evidence, and rejects breakdowns that pass checks only at final integration.
- `plan` reports missing execution plans from observed state.

## [0.26.0] - 2026-09-18

### Changed

- Simplify the user and contributor guides around command selection.
- `plan` separates new-ticket planning from frontier selection, blocks fix plans on unconfirmed causes and keeps unresolved hypotheses until evidence rejects them.
- `exec` checks clarification markers before starting and reconciles completed commits before re-running checks.
- `exec` requires complete worker packets and stops on partial results.
- `review` and `fix` read checked acceptance criteria as requirements and share report gates.
- `commit` activates only for standalone requests and preserves unrelated staged and unstaged changes.
- Guides document instruction contracts and repeatable scenarios instead of line-count targets.

## [0.25.0] - 2026-09-17

### Changed

- `exec`, `review` and `fix` share explicit context packets and capability checks, with fresh-context launches beside native named agents.
- `review` schedules every required reviewer within available agent capacity.
- Guides document prompt-only tool restrictions, client compatibility limits and reproducible client scenarios.

## [0.24.0] - 2026-09-17

### Changed

- `rnd`, `bug`, `plan`, `exec`, `review` and `fix` require explicit invocation in Codex as in Claude Code; `commit` still accepts natural-language commit requests.
- Discussion, quotations and handoffs never invoke a command.

## [0.23.4] - 2026-09-10

### Changed

- `rnd` and `plan` templates move into skill-local assets.

## [0.23.3] - 2026-09-10

### Changed

- Guides are rewritten concisely with centralized client setup and links to the owning instructions.

## [0.23.2] - 2026-09-10

### Changed

- Guides add Codex setup, skill invocation and isolated local preview instructions.

## [0.23.1] - 2026-09-10

### Changed

- Guides document installation in both clients, command routing, no-commit execution, review scope and commit activation.

## [0.23.0] - 2026-09-07

### Added

- `exec` saves worker decisions and deviations in the ticket's Comments and passes them to later workers.
- `exec` records the current task, git mode, starting commit and remaining step, and reconciles interrupted work on the next invocation.

### Changed

- `exec` resumes preserve `no commits` and stop on changes not attributable to the interrupted work.
- Tracked tickets use the task commit as their receipt without a separate bookkeeping commit.

## [0.22.2] - 2026-09-07

### Changed

- `rnd` shows current behavior, change points and reusable code before discussing approaches and records findings in the spec.
- `plan` carries applicable decisions and exclusions into task text or Conventions.

## [0.22.1] - 2026-09-07

### Changed

- `review` and `fix` share one severity bar passed to every reviewer.
- Verification traces reachable triggers, cites evidence and separates demonstrated defects from inferred consequences.
- Unclear or misspelled identifiers are minor findings; style alone is not a finding.

## [0.22.0] - 2026-09-06

### Added

- `fix` applies a saved review report, verifies open findings and commits code before recording the outcome.
- `review` persists confirmed findings, dismissal reasons and follow-ups in `review.md` across sessions.
- `review quick` runs two reviewers with wider duties and records that mode.

### Changed

- `review` writes only the report; `fix` owns the bounded re-check.
- `review-quality` and `review-implementation` accept `review_phase: recheck`.
- Test runs may create disposable caches and build output while tracked files stay untouched.

### Removed

- `fix` as a `review` argument.

## [0.21.0] - 2026-09-06

### Added

- `exec` reopens a `resolved` ticket passed as the argument after naming the invalidated criteria and asking.
- `exec` passes each worker the acceptance criteria its task serves as `Serves:` lines and checks the task's changes against them before the commit.
- `review` accepts a ticket path or feature directory as the goal.
- `worker` reports each verification command exactly as run and whether it ran after the last edit.

### Changed

- `exec` closes the ticket before the last task's commit and runs the full suite and linter once at the close.
- `exec` does not re-run a passing task test the worker already ran after its last edit.
- `plan` drops the `3-7 tasks` bound and the final verify task, offers a direct edit for single-step requests, and owns the `needs-info` and `ready-for-agent` status values.
- `review` records the base commit for the `staged` scope, reads resolved tickets from the diff, and ends after the third re-check with remaining findings reported as unresolved.
- `bug` drops the `3-5 hypotheses` floor.

## [0.20.1] - 2026-09-05

### Changed

- Worker results may include `Decisions` and `Deviations`; `exec` and `review fix` carry them into final reports.
- `review` passes finding verification and fix history to both re-check agents.

## [0.20.0] - 2026-08-29

### Added

- `rnd` slices the spec into tickets written as `issues/NN-<slug>.md` in dependency order.
- `exec` walks the ticket frontier, takes one ticket per run and writes `**Status:**` values (`claimed`, `resolved`, `ready-for-human`, `needs-info`).
- `rnd` and `plan` check the tracker configuration before the first write into a new feature directory.
- `rnd`, `bug` and `plan` never write into a directory that holds a `map.md`.
- `plan` self-checks task headings, checkbox placement and blocker order.

### Changed

- Artifacts move to `.scratch/<feature-slug>/`: `spec.md`, `root-cause.md` and tickets under `issues/`.
- `rnd` writes `spec.md` with seven fixed headings.
- `plan` appends `## Conventions` and `## Implementation` to one ticket instead of writing a plan file.
- `exec` commits code and ticket together when git tracks the ticket, and code alone otherwise.
- `review` takes the goal from the ticket and writes no status line.
- README and CONTRIBUTING describe features, tickets, status values and the frontier rule.

### Deprecated

- The story directory, with no migration.

## [0.19.2] - 2026-08-11

### Added

- `review-quality` checks what each deleted or replaced line took away.

### Changed

- `review-quality` reads the enclosing function in full and names concrete correctness traps.
- `review-testing` covers mismatched setup and teardown.

## [0.19.1] - 2026-08-11

### Changed

- `rnd`, `bug` and `plan` accept a local ticket path on the `- Tracker:` line.

## [0.19.0] - 2026-08-09

### Added

- `review` is read-only by default; `review fix` applies confirmed findings through a `worker`, commits and re-checks.
- `review` ends with a report that names dismissed findings.

### Changed

- `review` runs a five-agent sweep and a two-agent re-check gated on confirmed critical or major findings.
- `worker` accepts a list of confirmed review findings as a unit of work.
- `exec` and `plan` point to `review fix` beside `review`.

### Fixed

- `review` scope selectors (`staged`, a path) reach the agents; the `PR / MR URL` selector is removed.
- `review-implementation` and `review-documentation` handle a branch with no plan or stated goal.
- `plan` fills `## Conventions` and passes it through the `plan -> exec` contract.

## [0.18.0] - 2026-08-09

### Changed

- `rnd`, `bug`, `plan`, `exec` and `review` become type-only (`disable-model-invocation: true`); `commit` keeps model invocation.
- `rnd`, `bug` and `plan` carry the tracker-ticket rule again.

### Removed

- The SessionStart hook and `hooks/`.

## [0.17.0] - 2026-08-08

### Changed

- The plugin is renamed from `nxs` to `dev` and moves to `plugins/dev/`; commands read `/dev:<name>` and agents `dev:<name>`.
- CONTRIBUTING and README are scoped to the plugin; repository-wide rules move to the root.
- `docs/nxs/` stays as the artifact path.

### Fixed

- `review-simplification` frontmatter parses again.

## [0.16.1] - 2026-08-08

### Changed

- `commit` description names its trigger: any request to commit work outside `exec`.

## [0.16.0] - 2026-08-08

### Changed

- CONTRIBUTING gains a ubiquitous-language table and covers all three handoff contracts.
- `rnd` and `bug` name the story, slug and date rules; `task` becomes `request` in `rnd`.
- `plan` reads the source artifact by its headings and never overwrites an existing `plan.md` silently.
- `review-implementation` accepts requirements from the root cause.

### Removed

- The archiving rule from `plan` and `exec`; archiving is a user action.

## [0.15.0] - 2026-08-08

### Changed

- `review` launches five agents in parallel, verifies candidates, fixes confirmed findings and commits, up to three rounds.
- `plan` absorbs `plancheck` and `plan-conventions`, including the template and decomposition rules.
- `exec` runs the plan straight through, committing each green task.
- `commit` absorbs `commit-conventions`.
- `rnd` and `bug` are shortened.

### Added

- `review-quality`, `review-implementation`, `review-testing`, `review-simplification` and `review-documentation` as self-contained read-only reviewers.

### Removed

- The background skill tier, `plancheck`, `plan-reviewer`, the two old review lenses, the development approaches, the review step inside `exec` and `examples/`.

## [0.14.0] - 2026-07-31

### Changed

- A plan task is one complete capability across every layer; `plan-conventions` targets 2-5 tasks with 7 as the ceiling and names the split criteria.
- `exec` measures the large-diff stop against the task's Files block and raises the review-fix cap to five rounds.
- `plancheck` treats slicing as a NIT, never a BLOCK.

### Removed

- The `~5 checkboxes per task` target and its split and merge thresholds.

## [0.13.1] - 2026-07-28

### Removed

- `## RULES` recap sections, duplicated `exec` sections, essence summaries in `plan-conventions` and redundant self-description lines in skills.

### Changed

- Reviewer agents use plain imperative wording; one term per concept.

## [0.13.0] - 2026-07-28

### Added

- `plancheck` gains a plan review policy with a plan-shaped BLOCK / NIT / DROP bar and fixture plans.
- `review-fit-reviewer` replaces the implementation and simplification reviewers.
- `review` splits the axes reference out of the review policy.

### Changed

- `plancheck` classifies candidates and requires an `Impact:` naming an end state.
- `review-quality-reviewer` also owns test coverage and quality.
- `review` and `plancheck` reports open with the verdict, counts and scope.

### Removed

- `review-implementation-reviewer`, `review-testing-reviewer` and `review-simplification-reviewer`.

## [0.12.0] - 2026-07-28

### Added

- A read-only fallback to the old `docs/nxs/briefs/` and `docs/nxs/plans/` layout in the Spec axis.

### Changed

- Artifacts live in one story directory `docs/nxs/stories/YYYYMMDD-<slug>/` holding `brief.md`, `root-cause.md` and `plan.md`.
- `plancheck` and `exec` resolve the latest story containing a `plan.md`.

## [0.11.0] - 2026-07-23

### Added

- `commit` commits working changes as atomic conventional commits.
- A SessionStart hook injects the `using-nxs` discipline.

### Changed

- `commit-conventions` is a pure convention; the exec commit gate lives in `exec`.
- `rnd`, `bug` and `plan` drop their `INTAKE` sections.

### Removed

- The `intake` background skill.

## [0.10.1] - 2026-07-22

### Fixed

- The plan source-artifact section has one name, `## SOURCE ARTIFACTS`.
- `review` and `plancheck` resolve the protocol path inside the plugin.
- `exec` keys TDD mode off the `## DEVELOPMENT APPROACH` section.
- Section names, template fields and skill self-descriptions match each other.

### Removed

- `examples/epic-sample.md`, `examples/adr-sample.md` and the duplicated output block in `plan-reviewer`.

### Changed

- `rnd` and `bug` accept input without a tracker key.
- CONTRIBUTING documents agent frontmatter and the full repository layout.

## [0.10.0] - 2026-07-22

### Changed

- Brief files carry the writing command as a suffix: `-rnd.md` and `-bug.md`.

## [0.9.2] - 2026-07-22

### Removed

- The Fowler smell baseline reference.

### Changed

- The review flow is shortened to what the model cannot infer about the project.

## [0.9.1] - 2026-07-22

### Changed

- `review` and `plancheck` findings use `Issue:` / `Impact:` / `Fix:`.
- `review-protocol` verification is four steps; unconfirmed findings are discarded.
- `plan-reviewer` checks the plan against the repository and records the command it ran.
- CONTRIBUTING is in English.

## [0.9.0] - 2026-07-22

### Removed

- Commands `dialectic`, `wrong`, `epic`, `explain`, `clean`, `recommit`, `techdoc` and `userdoc`.
- Background skills `stress-test`, `doc-draft` and `decision-log`.
- Agents `explorer` and `diagnose-investigator`.
- The `exec` default / auto mode split.

### Changed

- `plancheck` uses one `plan-reviewer` agent.
- `exec` and `commit-conventions` fold their references into `SKILL.md`.
- Artifacts move to `docs/nxs/plans/` and `docs/nxs/briefs/`.

## [0.8.0] - 2026-07-22

### Added

- An optional `## CONVENTIONS` plan section.

### Changed

- `exec` passes the task, its acceptance criteria and the conventions set to each worker.
- `worker` follows the passed conventions and matches surrounding code where they are silent.

## [0.7.0] - 2026-07-14

### Added

- `epic` gains a `Tasks` section with statuses, a map header, invocation modes, a notes folder and a closure step.
- `clean` archives completed epic maps.
- `examples/epic-sample.md`.

### Changed

- `epic` map names carry the epic's tracker key; Frontier `task` items become `prep`.
- `plan` confirms all blockers are done before planning an epic task.

## [0.6.0] - 2026-07-13

### Changed

- `bug` root-cause brief names include the tracker identifier.

## [0.5.0] - 2026-07-13

### Added

- `rnd` writes an inline brief skeleton with an `Acceptance criteria` section and offers a full-collapse escape hatch.

### Changed

- Brief and plan file names include the tracker identifier.

### Fixed

- Acceptance criteria from `rnd` have a fixed home in the brief.

## [0.4.0] - 2026-07-11

### Added

- MIT `LICENSE`, manifest metadata, `CHANGELOG.md`, a versioning convention, CI validation and a pull-request template.
- `examples/` with a `CLAUDE.md.sample` and sample artifacts.
- `doc-draft` warns when `docs/` is not gitignored.

### Changed

- Review lenses are tool-enforced read-only.
- Skill descriptions state when-to-use triggers and each command gains an `Example` line.

### Fixed

- Duplicated commit and review rules, legacy skill self-names and contradictions in `exec` and `doc-draft`.

## [0.3.0] - 2026-07-09

### Added

- `epic` entry point for multi-session efforts.
- Fowler code-smell baseline in the review quality and simplification lenses.

## [0.2.0] - 2026-07-08

### Changed

- The orchestrator injects one protocol kernel into every lens agent.
- Shared kernels are extracted for stress-testing, doc drafting, TDD and bug diagnosis.
- Skills name a tool-agnostic "tracker".

## [0.1.0] - 2026-07-06

### Added

- Initial release with `/nxs:*` command skills, background rule skills and read-only review and plan agents.
