# Changelog

All notable changes to the `dev` plugin are documented in this file. Releases before 0.17.0 shipped under the name `nxs`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
