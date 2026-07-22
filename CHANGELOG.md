# Changelog

All notable changes to the `nxs` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.10.0] - 2026-07-22

### Changed

- Brief files are named after the command that writes them: `rnd` -> `docs/nxs/briefs/YYYYMMDD-<slug>-rnd.md`, `bug` -> `docs/nxs/briefs/YYYYMMDD-<slug>-bug.md` (the tracker-key forms gain the same suffix). Replaces a scheme where `bug` tagged its file by content (`-root-cause`) and `rnd` tagged nothing at all, so the file name now says which command produced it.
- The suffix is a category tag, not a rename of the artifact: in prose the `bug` output is still a "root-cause brief", and `## SOURCE ARTIFACTS` still carries a `Root-cause brief:` line. Nothing reads the suffix - briefs are resolved by path - so files written under the old scheme keep working.
- `plan-conventions`: the source-artifact line names the "root-cause brief" that `bug` writes, instead of calling it a "diagnosis". The artifact had two names across the repo; `plan` and `plancheck` already used this one.

## [0.9.2] - 2026-07-22

### Removed

- `review/reference/smell-baseline.md` - the Fowler smell definitions it injected into two lenses are textbook material the model already knows. The simplification lens keeps one line saying the vocabulary applies and that a smell is a candidate, not a violation.

### Changed

- The review flow says less and relies more on what the model brings: 700 lines down to 494 with no change in behavior. Gone are the sections that only stated where other sections live, the tables restating that `must` blocks and `should` does not, the per-lens matrices explaining how each lens differs from the other three, and the focus-area entries that defined ordinary words.
- What stays is what the model cannot infer about this project: where the standards live, how to find the source artifact, the citation each axis finding carries, and three calls that are easy to get wrong - negative-only assertions, complexity judged against the task, and the ban on demanding a case matrix.

## [0.9.1] - 2026-07-22

### Changed

- `review`, `plancheck`: a finding is now `Issue:` / `Impact:` / `Fix:` - what is wrong, what it costs, what to change. The quoted excerpt is gone; a NIT is a single line and several nits fold into one summary line, so they stop competing with the blocking findings for attention.
- `review-protocol`: verification is four steps - read the code with its context, confirm it is real, check it is not already handled, check it is not deliberate. Confirmed findings are reported, everything else is discarded rather than downgraded. Replaces the longer evidence checklist that had grown around the same job.
- `plan-reviewer`: checks the plan against the repository instead of grading its form. It confirms the paths exist, follows the change outward to find the places the plan never mentions, and carries a `Repo:` line with the command it ran. Checkbox counts, title wording, and slicing style are explicitly out of scope.
- Review lenses no longer restate how they differ from each other; one line replaces the cross-referenced matrix each of them carried.
- `CONTRIBUTING.md` is now in English, so the whole repo is one language.

## [0.9.0] - 2026-07-22

Cut the plugin back to its core loop. The workflow is `rnd` / `bug` -> `plan` -> `plancheck` -> `exec` -> `review` and nothing else; everything that was not being used, or that duplicated what the harness already does, is gone. 41 files and ~2980 lines became 22 files and ~1690.

Breaking: commands were removed and artifact paths moved. `0.x` is initial development - the public contract is not stabilized, so a breaking change is a minor bump. See CONTRIBUTING / VERSIONING.

### Removed

- Commands `dialectic`, `wrong`, `epic`, `explain`, `clean`, `recommit`, `techdoc`, `userdoc`.
- Background skills `stress-test` (its four steps are inlined in `rnd`), `doc-draft`, `decision-log` (a significant decision is now recorded in the plan or brief itself).
- Agents `explorer` (the built-in Explore agent is equivalent) and `diagnose-investigator` (`bug` investigates in the main context).
- `exec`: the default / auto mode split. `exec` now always runs the plan to the end with the same gates; a single task is an ordinary prompt, not a mode. The `no commits` instruction is unchanged.

### Changed

- `plancheck`: the four `plan-*-reviewer` lens agents and the plan protocol addendum collapse into one `plan-reviewer` agent that covers scope, structure, testing, and risk in a single pass.
- `exec`: `reference/auto.md`, `reference/worker-mode.md`, and `reference/tdd.md` fold into `SKILL.md`, which no longer states the worker model three times.
- `commit-conventions`: `reference/git-conventions.md` folds into `SKILL.md`; the mode matrix collapses to one gate.
- `intake`: trimmed to reading a tracker ticket and routing to `rnd` or `bug`.
- Artifacts moved from `docs/plans/` and `docs/briefs/` to `docs/nxs/plans/` and `docs/nxs/briefs/`.
- `CONTRIBUTING.md`: dropped the ARTIFACT PATHS table that duplicated each skill's own path line.

## [0.8.0] - 2026-07-22

### Added

- `plan-conventions`: an optional `## CONVENTIONS` plan section - the rules and shared steps every task in the plan follows (code style and naming for the work, a procedure repeated per task, standing preferences for this effort). Detail specific to one task stays in that task.

### Changed

- `exec`: the worker launch contract passes the task, its acceptance criteria, and a conventions set (the plan's `## CONVENTIONS` plus the project rules and standing directives the orchestrator works under). The set is assembled once per run and reused verbatim; a clean worker context does not carry conventions, so what is not passed does not reach the code.
- `worker`: follows the conventions passed in its prompt and matches the surrounding code where they are silent, instead of inventing a style of its own.

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
