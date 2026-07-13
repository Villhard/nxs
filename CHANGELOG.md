# Changelog

All notable changes to the `nxs` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2026-07-14

### Added

- `epic`: an implementation layer on the map - a `Tasks` section of goal-level chunks with `blocked -> ready -> planned -> done` statuses; a ready task hands off to `/nxs:plan`, which finds the concrete implementation against the current code. Hard rule: no plan while a blocker is open.
- `epic`: map header (`Date` / `Status` / `Tracker`), a `Mode: HITL | AFK` line per Frontier item, invocation mode detection (map path / name / no argument), and a closure step - `Status: complete` when nothing is open and every task is done.
- `epic`: a notes folder next to the map (`docs/epics/YYYYMMDD-<slug>/`) as the home for research / spike findings notes.
- `clean`: archives completed epic maps (`docs/epics/` -> `docs/epics/archive/`, the notes folder moves along); the argument accepts `epics`.
- `examples/epic-sample.md` - a filled sample map.

### Changed

- `epic`: the map name carries the epic's own tracker key (`YYYYMMDD-<EPIC-KEY>-<slug>.md`); the key names the map only and does not flow down to task briefs / plans - each task is named by its own key.
- `epic`: the Frontier item type `task` is renamed to `prep` (manual unblock work), freeing the word for implementation tasks; `decide` items gain a direct-answer resolution path recorded as a gist-only map line.
- `intake`: `/nxs:epic` listed as a consumer; the extracted identifier names the epic map and stops at the epic boundary.
- `plan`: a guard for epic-map tasks - confirm all blockers are done before planning, else route back to `/nxs:epic`.
- CONTRIBUTING artifact paths table covers `/nxs:epic` and the epics archive.

## [0.6.0] - 2026-07-13

### Changed

- `bug`: the root-cause brief file name includes the tracker identifier (`YYYYMMDD-<KEY>-<slug>-root-cause.md`) when intake extracted one, matching `rnd` and `plan`.

## [0.5.0] - 2026-07-13

### Added

- `rnd`: an inline brief skeleton with stable headings that `/nxs:plan` consumes, including a new `Acceptance criteria` section.
- `rnd`: a full-collapse escape hatch - when all three phases collapse (CLARIFY 0 questions, EXPLORE one obvious approach, STRESS ~0), the user chooses between routing straight to `/nxs:plan` and a short brief for traceability.

### Changed

- Brief and plan file names include the tracker identifier (`YYYYMMDD-<KEY>-<slug>.md`) when intake extracted one, fulfilling the `intake` navigability contract in both consumers.
- `examples/brief-sample.md` gains an `Acceptance criteria` section matching the new skeleton.

### Fixed

- Acceptance criteria surfaced in `rnd` CLARIFY now have a fixed home in the brief; the artifact spec omitted them while `/nxs:plan` expected to pull them from the brief.

## [0.4.0] - 2026-07-11

### Added

- MIT `LICENSE` and plugin manifest metadata (`license`, `repository`, `homepage`).
- `CHANGELOG.md` and a versioning convention in `CONTRIBUTING.md`.
- CI workflow (`claude plugin validate --strict`, a frontmatter check, and a house-style lint for forbidden dashes / quotes) plus a pull-request template with a PUBLIC SAFETY reminder.
- `examples/`: a `CLAUDE.md.sample` safety starter and sample plan / brief / ADR artifacts.
- README value proposition, quickstart, and a command table for all 14 commands.
- `doc-draft`: a pre-write check that warns and offers to gitignore `docs/` when the consumer project does not ignore it.

### Changed

- The four `review-*-reviewer` lenses are tool-enforced read-only (Bash removed); `explorer` and `diagnose-investigator` document that they run read-only shell only and write nothing.
- README and CONTRIBUTING inventory corrected to 14 commands (adds `epic`) and 8 background skills (adds `doc-draft`, `stress-test`).
- Skill descriptions tightened to when-to-use triggers, each command gains an `Example` line, and the agent guard strings are unified to one form.
- Completed the `worker` destructive-op list (`git clean -f`, `git checkout -- <path>`).

### Fixed

- Removed duplicated commit and review rules that restated their reference files.
- The `exec` auto reference no longer contradicts the single-writer worker model.
- Legacy skill self-names (`dev-plan`, `dev-exec`, `Brainstorm`, `Diagnose`, `rethink`) replaced with the actual commands.
- `doc-draft` no longer claims `docs/` is guaranteed gitignored.
- The review quality and simplification lenses guard the injected smell baseline.
- `plancheck` wording matches what it injects; `epic` marks `deep-research` as an optional external skill.
- The CONTRIBUTING dev-loop uses the real marketplace name so the install command works.

## [0.3.0] - 2026-07-09

### Added

- `/nxs:epic` entry point for foggy, multi-session efforts.
- Fowler code-smell baseline in the review quality and simplification lenses.

## [0.2.0] - 2026-07-08

### Changed

- Single-source protocol model: the orchestrator injects one protocol kernel into every lens agent instead of each agent restating it.
- Deduped the review and plancheck lens agents against the injected protocol; each agent keeps only a guard line plus its domain content.
- Extracted shared kernels: adversarial stress-test, doc-draft contract, TDD cycle, and the bug diagnosis loop.
- Switched skills to a tool-agnostic "tracker" instead of naming a specific issue tracker.

## [0.1.0] - 2026-07-06

### Added

- Initial release: flat `/nxs:*` command skills (`plan`, `exec`, `review`, `plancheck`, `bug`, `rnd`, `dialectic`, `wrong`, `explain`, `userdoc`, `techdoc`, `recommit`, `clean`).
- Background (tier 3) rule skills loaded by relevance.
- Autonomous read-only agents for the review and plan lenses.
