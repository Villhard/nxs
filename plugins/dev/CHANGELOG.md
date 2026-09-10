# Changelog

All notable changes to the `dev` plugin are documented in this file. The plugin was called `nxs` until 0.17.0; entries below that version use the old name and are left as written.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.23.4] - 2026-09-10

### Changed

- Move rnd and plan templates into skill-local assets and document optional supporting resources; artifact contracts and workflow gates are unchanged.

## [0.23.3] - 2026-09-10

### Changed

- Rewrite guides concisely, centralize client setup, and link detailed contracts to their source instructions; behavior is unchanged.

## [0.23.2] - 2026-09-10

### Changed

- Add concrete Codex setup, skill invocation, and isolated local preview instructions alongside the Claude Code workflow; plugin behavior is unchanged.

## [0.23.1] - 2026-09-10

### Changed

- Document installation in both clients and the limits of the unverified named-agent workflow in Codex.
- Clarify command routing, no-commit execution, review scope, automatic commit activation, and snapshot updates; workflow behavior is unchanged.

## [0.23.0] - 2026-09-07

### Added

- Exec saves substantive worker decisions and deviations in the ticket's Comments and passes applicable notes to later workers, including across sessions.
- Exec records the current task, git mode, starting commit and remaining step. A repeated invocation reconciles interrupted work once at entry, including checked tasks awaiting a commit and interrupted ticket closes. Completed tasks are not re-reviewed between workers.

### Changed

- A resume preserves `no commits` and permits only changes attributable to the interrupted work. Ambiguous or foreign changes stop before staging; an unfinished close is handled before reopening a resolved ticket or taking a dependent ticket.
- Execution notes share existing ticket writes and task commits. Ignored tickets keep their records on disk; tracked tickets use the task commit as their receipt without another bookkeeping commit.

## [0.22.2] - 2026-09-07

### Changed

- Rnd shows the current behavior, likely change points and reusable code before discussing approaches, and saves findings with code references and reasons in the spec.
- Plan carries applicable decisions, exclusions and their reasons into task text or Conventions, checks that workers can use them without the conversation or full spec, and avoids repeating answered questions unless new evidence contradicts them.

## [0.22.1] - 2026-09-07

### Changed

- Review and fix use the same severity bar, passed to every sweep and re-check reviewer. Test and documentation findings need concrete consequences; executable instructions are rated by what their consumer does wrong.
- Verification traces reachable triggers through callers and guards, cites evidence, and separates demonstrated defects from inferred consequences. Expensive or risky fixes remain in Findings with their cost under Fix.
- Quality findings name the demonstrated mechanism and check its preconditions. Unclear, misleading or misspelled identifiers and test names are minor; equally clear synonym preferences and other style alone are not findings.

## [0.22.0] - 2026-09-06

### Added

- `skills/fix/SKILL.md` - `/dev:fix` consumes a saved report without repeating the sweep, checks scope and requirement pins, verifies open findings, and commits code alone before recording the outcome. Incomplete attempts and unrelated worktree changes stop before another fix; empty reports make no commit.
- `skills/review/SKILL.md` - `review.md` preserves confirmed findings, dismissal reasons and open follow-ups across sessions. Incomplete-first writes and a final currency check prevent an interrupted or stale sweep from becoming an applicable report.
- `skills/review/SKILL.md`, `agents/review-quality.md`, `agents/review-implementation.md` - explicit `quick` uses two reviewers with wider duties and records that mode, so a small review need not launch five agents or masquerade as a full gate.

### Changed

- `skills/review/SKILL.md` - writes only the report; an unchanged complete unfixed report asks before another sweep. `skills/fix/SKILL.md` owns the bounded re-check, preserving the original base after staged changes are committed.
- `agents/review-quality.md`, `agents/review-implementation.md` - `review_phase: recheck` keeps original bounds and critical/major severity; a report path is context, never permission for an agent to write it.
- `README.md`, `CONTRIBUTING.md` - document seven commands, the report schema and state gates, and the `review -> fix` handoff. `skills/exec/SKILL.md` and `skills/plan/SKILL.md` send users to the separate commands.
- `.claude-plugin/plugin.json` - version 0.22.0 and seven-command description; the repository `README.md` and `.claude-plugin/marketplace.json` carry the same command count.

- `skills/review/SKILL.md` - test runs may create disposable caches and build output while source, tracked files and index stay untouched; the testing lens can still execute tests. `skills/review/SKILL.md`, `skills/fix/SKILL.md` and `CONTRIBUTING.md` use plain-text fields and only the disk/index sources the producer actually writes.

### Removed

- `skills/review/SKILL.md` - `fix` as a review argument; `/dev:fix` now applies the saved report without paying for a second sweep.

## [0.21.0] - 2026-09-06

State transitions that produced a wrong result, and the repeated work between a worker and its orchestrator. Found in a joint read of the plugin with Codex; the two contract decisions that came out of the same read - persisting the review history and a two-agent sweep - are not in this release and wait on a separate decision.

### Added

- `skills/exec/SKILL.md` - a `resolved` ticket passed as the argument is a reopen, not a skip: `exec` names the criteria the change invalidated and the task checkboxes that reopen with them, asks, then flips those and sets `claimed`. `/dev:review` had promised this reopen since 0.20.0 and `exec` had no such path.
- `skills/exec/SKILL.md` - each worker receives the acceptance criteria its task serves, as `Serves:` lines in plain text, never as checkboxes. Before the commit the orchestrator checks the task's changes, recorded against the worktree state before the worker, against the task's checkboxes and those lines: every checkbox with its evidence - a diff, a command result, or observed behavior - nothing in the diff that serves none, one correction to the same worker, then a stop. A criterion spanning several tasks is verified at the close, not at every task on the way.
- `skills/review/SKILL.md` - a ticket path or feature directory as an argument names the goal outright, for a repository where `.scratch/` is ignored and the branch carries no ticket file to read it from.
- `agents/worker.md` - `Serves:` lines explained, and `Verify:` reports each command exactly as run and whether it ran after the last edit, so the orchestrator can decide not to run it again.

### Changed

- `skills/exec/SKILL.md` - the close moves before the last task's commit. It had been written after the loop, on top of a commit already made, so "rides the final task's commit" could not hold without an amend.
- `skills/exec/SKILL.md` - a test command the worker reports as the exact one the task names, passing, run after its last edit, is not run again. `not run`, a failure, a narrower command, or any doubt still runs it. The full suite and the linter run once, by the orchestrator, at the close; a plan no longer carries a task for them.
- `skills/plan/SKILL.md` - the `3-7 tasks` floor and ceiling go; a task exists only when the work has that unit. The template's `### Task N: Verify acceptance criteria` block goes with it, and the last checkbox of a task names that task's test command, never the whole suite.
- `skills/plan/SKILL.md` - a small single-step request is offered a direct edit and is never routed to `/dev:exec`, which stops on a ticket without `## Implementation`.
- `skills/plan/SKILL.md` - clearing the last `[NEEDS CLARIFICATION]` marker in `spec.md` flips only the `needs-info` tickets with no marker and no open question of their own. `plan` is now stated as the writer of `needs-info` and `ready-for-agent`, and of nothing else on the status line; README and CONTRIBUTING said `exec` was the only writer while `plan` had written those two values since 0.20.0.
- `skills/review/SKILL.md` - for the `staged` scope, `git rev-parse HEAD` is recorded before launch and every pass after a fix commit diffs `<base>..<tip>`. The re-check had been handed `git diff --staged` after the commit, which is an empty diff.
- `skills/review/SKILL.md`, `agents/review-implementation.md`, `agents/review-documentation.md` - the tickets a branch resolved come from `git diff --name-only <base>...HEAD -- .scratch`, `--cached` for `staged`, not from `git log`, whose subjects carry no ticket key; only tickets at `resolved` in the reviewed state count, and the prompt names where to read each one from - the index or the fix commit for `staged`, disk otherwise - so a reviewer holds staged code to the staged requirements and not to a working tree that moved on.
- `skills/review/SKILL.md` - the third re-check ends the run with what it still confirms reported as unresolved; the branch is not called ready.
- `skills/bug/SKILL.md` - the `3-5 hypotheses` floor goes: as many as there are checkable alternatives, one when a probe already confirmed it. The worked example no longer ends in "move to a queue" as the only right answer; the fix direction is the smallest change the evidence at that layer supports.
- `README.md`, `CONTRIBUTING.md` - the status line's writer per value, the reopen, `Serves:` in the `plan -> exec` and ticket contracts, and the new `review` argument.

## [0.20.1] - 2026-09-05

### Changed

- Worker results optionally include `Decisions` and `Deviations` with reasons. `/dev:exec` and `/dev:review fix` carry them into final reports, including unfinished runs, without changing worker authority or stop and approval rules.
- `/dev:review` keeps finding verification and fix history in the current run's context and passes it to both re-check agents. Prior conclusions are checked against current code and may be challenged with new evidence.
- These are internal instruction changes; public commands and ticket formats remain unchanged.

## [0.20.0] - 2026-08-29

The story dies and a ticket becomes the unit of work. Every artifact moves to `.scratch/<feature-slug>/`, the local-markdown layout of the issue tracker the wider toolchain already uses, and the plan stops being a file: it becomes two sections inside the ticket it plans.

This is a merge, not an integration. Knowledge lives in one place, and that place is the tracker's own layout. `/dev:rnd` writes `spec.md` with the seven headings the external spec skill writes, then cuts the work into vertical slices and writes each as `issues/NN-<slug>.md` from that toolchain's local ticket template, byte for byte, blocking edges included. `/dev:bug` writes `root-cause.md` beside it with all nine headings unchanged. `/dev:plan` appends `## Conventions` and `## Implementation` to one ticket. Nothing is converted at a boundary, because nothing crosses one: with the external skills installed the same files come out, and without them this plugin writes all of it alone and the flow stays complete.

The two altitudes were the hard part. A vertical slice and a story turned out to be the same object - one whole unit of work, demoable on its own, sized to one fresh context window - so `story` was a duplicate term and it goes. What survives is three levels with one home each: the feature is the directory, the ticket is the unit of work, the task is a `### Task N:` block inside it. A ticket IS a story, so a plan does not become a ticket and a ticket does not become a plan.

The dangerous token is `- [ ]`. In a ticket header it is an acceptance criterion; under `## Implementation` it is a unit of work `exec` executes. Position is the only discriminator, so it is enforced mechanically instead of restated in prose: `plan` refuses a ticket that already carries `### Task` headings and checks that no checkbox sits between `## Implementation` and `### Task 1:`, `exec` announces the task count it found before launching the first worker, and a worker never receives the criteria block at all. Left unenforced, an `exec` that scanned the whole ticket would hand acceptance criterion 1 to a worker as a single implementation step, flip it, and leave a ticket that looks executed while no real task ever ran.

Artifacts also stay current now, which is what the old `completed/` move never managed. `exec` sets `**Status:** claimed` before the first worker, flips task checkboxes per commit, and on the last green task verifies every acceptance criterion and sets `**Status:** resolved` - the token every `**Blocked by:**` line in the directory waits on. Seven status values, none invented: the five canonical triage roles plus `claimed` and `resolved`, borrowed from the tracker doc's own wayfinding operations, so a reader that has never heard of this plugin still reads an nxs ticket correctly.

### Added

- `skills/rnd/SKILL.md` - slicing. After the spec it cuts the work into vertical slices and writes `issues/NN-<slug>.md` for each, numbered from 01 in dependency order, blockers first, from the local ticket template verbatim: `**What to build:**`, `**Blocked by:**`, `**Status:**`, then the acceptance criteria. No `## Parent` section, because the local template has none. One ticket is the normal outcome for small work and gets no ceremony and no second code path. The ticket template lives here and nowhere else.
- `skills/exec/SKILL.md` - the frontier walk. Resolve the feature, read `issues/` in numeric order, skip any file carrying a `Type:` line, offer a `claimed` ticket with open tasks before taking a new one, then take the first `ready-for-agent` ticket that has an `## Implementation` section and whose every `**Blocked by:**` file carries `resolved`. A blocker naming a file that does not exist is a stop, never a satisfied edge. One ticket per run; the run ends by naming the next takeable ticket, and says the feature is complete when the ticket it just resolved was the last unresolved one.
- `skills/exec/SKILL.md` - the status writes. `claimed` after the clean-worktree check and before the first worker, carried into task 1's commit rather than paying its own, so a crash before task 1 still leaves a legible ticket on disk. `resolved` on the last green task, riding that task's commit. `ready-for-human` when the run ends on something only a human can clear, `needs-info` when it ends on an unclear requirement, each with one line under `## Comments`. A red suite writes no status and leaves the ticket `claimed`, because a retry is what clears it.
- `skills/{rnd,plan}/SKILL.md` - the tracker-config check before the first write into a new feature directory: the repository's `docs/agents/issue-tracker.md`, then the global default at the same relative path, then local markdown. That last fallback is what the wider toolchain itself defaults to, so it is copied rather than chosen. In a repository configured for GitHub or GitLab neither command picks silently: it names the tracker, names the duplication cost in one sentence, and the user chooses. Neither command ever writes that config file or runs a setup skill.
- `skills/{rnd,bug,plan}/SKILL.md` - never write into a `.scratch/<x>/` that holds a `map.md`. That directory is another skill's effort; pick a different slug and say why in one line.
- `skills/plan/SKILL.md` - three self-check bullets: `rg "### Task" <ticket>` returns nothing before the append, no `- [` line sits between `## Implementation` and `### Task 1:` after it, and a ticket may name only lower numbers on its `**Blocked by:**` line, so a cycle cannot be authored and `exec` needs no cycle detection.

### Changed

- `skills/rnd/SKILL.md` - the artifact becomes `.scratch/<feature-slug>/spec.md` with seven headings taken verbatim from the external spec skill: `## Problem Statement`, `## Solution`, `## User Stories`, `## Implementation Decisions`, `## Testing Decisions`, `## Out of Scope`, `## Further Notes`. The brief skeleton is gone, and the options with their rejection reasons, the stress verdict and the clarifications log move under `## Further Notes`. `## STANCE`, `## CLARIFY`, `## EXPLORE` and `## STRESS` are untouched - the thinking is the reason to type `/dev:rnd` instead of the external skill.
- `skills/bug/SKILL.md` - the smallest diff of the three, and the only handoff that survives verbatim. `root-cause.md` moves to `.scratch/<feature-slug>/`, all nine headings stay, the `YYYYMMDD-` prefix and the `- Date:` line go, the `- Tracker:` line stays because a bug usually has a real external key, and a `spec.md` already in the directory is not touched. It still writes no ticket: reach a confirmed cause, then stop.
- `skills/plan/SKILL.md` - the input is a ticket path and the output is appended to that ticket. `## Overview`, `## Acceptance criteria` and `## Context` go: the ticket already carries the first two, and `exec` never passed `## Context` to a worker, so it reached no code. With no `issues/` at all it creates `01-<slug>.md` from four fields named in prose and plans into it. An existing `## Implementation` is never replaced silently, and a `claimed` or `resolved` ticket is never re-planned without asking, because its task checkboxes are execution history.
- `skills/exec/SKILL.md` - `## RESOLVE THE PLAN` becomes `## RESOLVE THE TICKET`. Step 5 commits code and ticket together when git tracks the ticket, commits the code alone when `.scratch/` is gitignored and says so once, and never uses `git add -f`: the on-disk ticket, not git, is what a resume reads. A decision that contradicts the spec's `## Implementation Decisions` becomes a stop condition rather than making `exec` a writer of the spec.
- `skills/review/SKILL.md`, `agents/review-implementation.md`, `agents/review-documentation.md` - the goal comes from the ticket's `**What to build:**` line and its acceptance criteria, and the ticket path replaces the plan path in the launch contract. `## RESOLVE THE SCOPE` is untouched, since review resolves a git diff and never an artifact tree, and the `no stated goal` fallback stands for a branch nobody planned. `review-documentation` now reads two checkbox sets under different rules. New, and stated once: `review` writes no `**Status:**` line in either mode, so a re-opened ticket is `/dev:exec <ticket path>` asking first, not review deciding.
- `agents/worker.md` - unchanged, deliberately. A worker that knew about tickets would be a second writer of the status line.
- `CONTRIBUTING.md` - `story` and `brief` leave the ubiquitous-language table; `feature`, `ticket`, `spec`, `status` enter, and `checkbox` splits into `task checkbox` and `acceptance criterion`. The handoff section carries four contracts. `## ARTIFACT PATHS` is rewritten around `.scratch/`, and the rule that `exec` writes no artifact gains the write-versus-mutate distinction it now needs. The playbook records `rnd` as the next split candidate.
- `README.md` - `## Stories` becomes `## Features and tickets`: the layout, the checkbox positional rule, the seven status values and who writes each, the frontier rule, and the declaration that this plugin implements the local-markdown layout only and ships no `gh` or `glab` dependency.

### Deprecated

- The story directory - gone from the plugin entirely. No command writes there, reads there, or names it, and no legacy branch was kept: the only such directory left in practice held no `plan.md`, so a branch guarding it would never have fired once. Nothing is renamed, moved, or converted either, and there is no migration command: converting a story into a ticket means inventing acceptance criteria the old plan wrote as prose, and a tool that guesses acceptance criteria is worse than no tool. An unfinished old plan is finished by hand or dropped. This reverses the 0.17.0 decision to freeze the string, which existed to keep old stories visible to `plan` and `exec`; with nothing new landing there, there is nothing left to keep visible.

### Fixed

- `CHANGELOG.md` - the 0.19.1 entry claimed the link from a story back to its spec "rides through that ticket's own `## Parent`". The local ticket template has no `## Parent` section; that section exists only in the variant written for a real tracker. The shared feature directory is the whole link, and after this release nothing needs a second one.

## [0.19.2] - 2026-08-11

### Added

- `agents/review-quality.md` - a `## WHAT THE DIFF TOOK AWAY` section. For every deleted or replaced line the agent names the invariant it held and looks for where the new code re-establishes it, and for every changed function it greps the callers to see what the change costs them. The agent read what the diff adds and had nothing to say about what it removes, which is where a dropped guard or a narrowed validation hides.

### Changed

- `agents/review-quality.md` - the enclosing function of a hunk is read in full and its unchanged lines count, since a change re-exposes them. `## CORRECTNESS` keeps its six categories and adds the traps by name - falsy-zero, `==` coercion, mutable default args, a nil-map write, a range variable captured, float equality, DST drift, a narrowed lock scope, a predicate with a side effect. A named trap is something to look for; a category is something to agree with.
- `agents/review-testing.md` - `## TEST QUALITY` covers setup and teardown that do not match, in both directions: what a test stands up and never takes down, and what a teardown removes without a setup that created it.

## [0.19.1] - 2026-08-11

### Changed

- `skills/{rnd,bug,plan}/SKILL.md` - the `- Tracker:` line of the brief, the root cause, and the plan accepts the path of a local ticket beside a tracker key or URL. A story that came out of `to-tickets` had no way to name what it implements, because the line asked for a tracker and the ticket is a file under `.scratch/`; the link back to the spec rides through that ticket's own `## Parent`.

## [0.19.0] - 2026-08-09

`/dev:review` reviews. It no longer edits anything unless asked, and when asked it stops paying full price for every pass.

Reviewing someone else's PR is a normal use of this command, and until now the command answered that by rewriting their branch. Reporting is the whole command by default: nothing edited, nothing staged, nothing committed. `fix` in the arguments opts into changing code, and that word is the only thing that does. A command that writes by default and needs a flag to stay quiet gets it backwards, because the run where the flag is forgotten is the destructive one.

Fix mode picks up three things from [cc-thingz](https://github.com/umputun/cc-thingz) `planning:exec`, which runs the same shape of pipeline inside an interactive session. The passes are named by purpose rather than counted: the **sweep** launches five agents on the diff as it arrived, and the **re-check** launches two, critical and major only, to answer whether the fixes broke something. A re-check exists only after fixes landed, so report mode is one sweep and no more. The run ends on severity instead of on activity - the agents have always reported `Severity: critical | major | minor` and the command simply never read the field. And the fixes move into a `dev:worker`, so reading files and editing them stops happening in the session that also has to hold the whole review.

What fix mode deliberately gives up: a pass that confirmed only minor findings fixes them and stops, so those fixes go unverified. That is the trade cc-thingz makes, and a minor fix is small enough to be worth it.

`## VERIFY` stays in the main session. Handing the decision of what is real to an agent is a different philosophy, not an optimization, and it is not in this release.

### Added

- `skills/review/SKILL.md` - a `## STANCE` section and the `fix` argument. Without it the command is read-only over any diff, including a PR that is not yours; with it the confirmed findings are applied, committed, and re-checked. The mode is announced before anything launches, so a run that will write is never a surprise, and fix mode over a diff the user does not own is a stop condition.
- `skills/review/SKILL.md` - a `## REPORT` section, which is where a default run ends. It names the dismissed findings in one line so a discarded candidate stays visible.

### Changed

- `skills/review/SKILL.md` - `## LAUNCH THE AGENTS` describes the sweep and the re-check by what each is for. `## VERIFY` carries the agent's severity forward instead of re-ranking by consequence, and forbids lowering a finding to end the pass. `## FIX AND COMMIT` becomes `## FIX`, delegates to one `dev:worker`, and gates the re-check on a confirmed critical or major.
- `agents/worker.md` - a list of confirmed review findings counts as a unit of work alongside a plan task. Without this its scope rule reads as plan tasks only.
- `README.md` - the quickstart shows both modes, and the command table and `## Stories` section state that `review` leaves nothing behind unless asked.
- `skills/exec/SKILL.md`, `skills/plan/SKILL.md` - the `## NEXT` pointers name `/dev:review fix` beside `/dev:review`, since a branch you just executed is the case where applying the findings is the point. `exec` also says out loud that neither starts on its own, which has been true since 0.18.0 made the workflow commands type-only and is easy to assume otherwise from a line that reads like a handoff.

### Fixed

A multi-agent pass over the skillset for contradictions found eight, six after merging. These are them.

- `skills/review/SKILL.md`, `agents/review-*.md` - the scope selector now reaches the agents. `## RESOLVE THE SCOPE` resolves to exactly two commands, a history one and a diff one, the launch contract carries them verbatim, and all five agents run what they are given instead of a hardcoded `git diff <base>...HEAD`. Until now `argument-hint` advertised selectors that nothing downstream consumed, so `/dev:review staged` silently reported on the whole branch. `staged` resolves to `git diff --staged` against the last commit, a path narrows the branch scope, and the `PR / MR URL` selector is gone - someone else's branch is reviewed by checking it out, which the no-selector case already covers, and `gh pr diff` would have bought a dependency for a case nobody runs.
- `skills/review/SKILL.md`, `agents/review-implementation.md`, `agents/review-documentation.md` - the plan path AND the goal are conditional, matching what a branch handed to you actually offers. The goal comes from the plan or from what the user said when invoking; with neither, the prompt carries `no stated goal` and nothing is manufactured from commit messages or the branch name, because an invented goal becomes a requirement the reviewer holds the code to. `review-implementation` then skips requirement coverage, requirement edge cases and the scope-creep section, says which it skipped, and reviews what stands without a requirement: wiring, completeness, data flow. The goal sentence joins its list of allowed requirement sources, so the ban on reconstructing requirements from git history stays intact. `review-documentation` skips its plan section when no plan came. Both agents previously asserted the plan path was always present, which is false on the first-class case of a branch nobody planned.
- `skills/exec/SKILL.md` - "the one command that changes project code" becomes "the command that turns a plan into code". Fix mode in `review` writes too.
- `skills/plan/SKILL.md`, `CONTRIBUTING.md`, `README.md` - `## Conventions` joins the `plan -> exec` contract, since `exec` has always passed it to every worker while both documents said only two tokens crossed. `plan` also gains the sources to fill it from - the brief's chosen approach, the patterns of the surrounding code, what the user said this session - and an instruction not to copy in what CLAUDE.md already covers, which `exec` passes separately.
- `CONTRIBUTING.md` - `sweep`, `re-check` and `fix mode` get rows in the ubiquitous-language table. The rule above it now asks for a row whenever one is missing rather than demanding it precede the skill, which was a rule nobody could keep.
- `CHANGELOG.md` - the `## [0.18.0]` heading is back. The 0.19.0 entry had replaced it, leaving a whole release filed under the wrong version.

## [0.18.0] - 2026-08-09

The plugin stops routing the user and waits to be called. Five commands become type-only and the SessionStart hook is gone.

The hook existed to make the commands fire without being typed, which only makes sense when this plugin is the whole workflow. It is not: work larger than one story starts in another toolchain, and small work is faster in the built-in plan mode. In both cases the injected discipline pulled toward a `/dev:` command that did not belong, and the pull was strongest exactly where the workflows met - `/dev:plan` invoked inside plan mode cannot write its artifact at all, since plan mode blocks the write the whole command exists to perform.

`commit` keeps model-invocation. "Commit this" is a request to commit rather than a request for a command, and its description has carried that trigger since 0.16.1.

### Changed

- `skills/{rnd,bug,plan,exec,review}/SKILL.md` - `disable-model-invocation: true`. Each one is invocable only as `/dev:<name>`; none appears in the model's skill listing, and no skill or agent can call them. `skills/commit/SKILL.md` is unchanged.
- `skills/{rnd,bug,plan}/SKILL.md` - the tracker-ticket rule returns to the three commands that accept a key, one line after `Accepted input`: read the ticket through the tracker, ask for a paste when it is unreachable, never infer its content from the key. It moved to the hook in 0.11.0 and had no other home.
- `CONTRIBUTING.md` - `disable-model-invocation: true` joins the command frontmatter template as the default, with `commit` named as the single exception. The layout, the tiers, and the "when to add something new" sections drop the hook.
- `README.md` - the `## Model` section states that five commands are type-only and why; the layout block drops `hooks/`.

### Removed

- `hooks/` - `hooks.json`, `session-start.sh`, and `using-dev.md`. Of what the discipline carried, the artifact-naming rule was already duplicated in `rnd`, `bug`, and `plan`, the commit trigger lives in the `commit` description, and the ticket-reading rule moves back into the three skills. What is left, "check for a command before acting" and the red-flag list, is what this release deliberately drops.

## [0.17.0] - 2026-08-08

The repository stops being one plugin that happens to declare a marketplace and becomes a marketplace that holds several. `nxs` was both the marketplace and the only plugin in it, so the name carried no information once a second plugin arrived. The marketplace keeps the name; the plugin takes the one that says what it does. Every command reads `/dev:plan` instead of `/nxs:plan`, and the plugin moves from the repository root into `plugins/dev/`.

The artifact path does not follow. Stories written as `docs/nxs/stories/` live in repositories this plugin does not control, and renaming the directory would hide every one of them from `plan` and `exec`. `docs/nxs/` is a fixed string from here on, documented as such rather than kept in sync with the plugin name.

### Changed

- `.claude-plugin/plugin.json` - `name` becomes `dev`, which renames all six commands and all six agents. `homepage` points at the plugin directory rather than the repository root.
- `skills/*/SKILL.md`, `agents/*.md` - `/nxs:<name>` becomes `/dev:<name>`, and the agents `/dev:exec` and `/dev:review` spawn become `dev:worker` and `dev:review-*`.
- `hooks/using-nxs.md` becomes `hooks/using-dev.md`; `hooks/session-start.sh` reads the new filename and names the `dev` plugin in the context it injects.
- `CONTRIBUTING.md` - scoped to this plugin. The layout section describes `plugins/dev/`, and the repository-wide rules (house style, public safety, how a plugin is added) move to the root `CONTRIBUTING.md`. A new paragraph in `## ARTIFACT PATHS` records why `docs/nxs/` keeps the old name.
- `README.md` - moved out of the repository root into the plugin, and covers the plugin only. The root README now describes the marketplace.

### Fixed

- `agents/review-simplification.md` - the `description` was an unquoted YAML scalar containing `introduces: needless`, which made the whole frontmatter block fail to parse. The agent loaded with no `name`, no `description`, and no `tools`. Quoting the value fixes it; `claude plugin validate` now catches this class of error, which is how it surfaced.

## [0.16.1] - 2026-08-08

`/nxs:commit` was the one command a user reaches without naming it. "Commit this" is a request to commit, not a request for a command, and the description only answered the question a user asks when browsing the `/` menu - "what does this do" - not the one the model asks when reading a plain sentence: does this apply right now. The `using-nxs` hook already listed the trigger as easy to miss, which is a hook compensating for a description that does not carry its own trigger.

### Changed

- `skills/commit/SKILL.md` - the `description` names the trigger it fires on: any request to commit work made outside `/nxs:exec`, and a hand-run `git add` or `git commit`. The body is untouched.

## [0.16.0] - 2026-08-08

One term, one meaning. The vocabulary had drifted while the plugin shrank to six commands, and two words were carrying two jobs each. `task` meant both the work a user arrives with and a numbered block in a plan - the collision sat inside one sentence of `/nxs:plan`'s own description, "decompose a task ... into sequenced tasks". `brief` meant both the artifact `rnd` writes and the one `bug` writes: `plan` called the second a "root-cause brief", `bug` called it "the brief" twice in its own body, and the file on disk is `root-cause.md`. Meanwhile `story` - the concept that names the directory - appeared in `plan`, `exec`, `using-nxs`, and the README, but in neither of the two commands that create one.

A closed vocabulary now lives in `CONTRIBUTING.md` and every file obeys it. `task` is a `### Task N:` block and nothing else; the incoming work is a `request`. The three artifacts are named after their files: brief, root cause, plan. An artifact is a durable markdown file in a story - commits, flipped checkboxes, follow-ups, and the review report are not artifacts and get no home on disk.

Archiving loses its owner on purpose. It was stated three times and differently - in `plan`'s `## ARTIFACT`, in `exec`'s `## NEXT`, and in the README - and it belongs to none of them: `exec` is an executor and `review` is a quality gate, while the decision that a story is finished is the user's, made after reading the plan. Moving a story to `completed/` is now documented as a user action and no command mentions it. `exec` keeps skipping `completed/` when it resolves the latest plan, which is a resolution rule, not archiving.

### Changed

- `CONTRIBUTING.md` - a new `## UBIQUITOUS LANGUAGE` section holds the twelve-term table and the rule that a term enters it before it appears in a skill. `## THE PLAN CONTRACT` becomes `## THE HANDOFF CONTRACTS` and covers all three handoffs instead of one. `## ARTIFACT PATHS` names the three artifacts in a table and states that `exec`, `review`, and `commit` write none and grow no `## ARTIFACT` section.
- `skills/rnd/SKILL.md` - `task` becomes `request` throughout, including the `## Task` heading of the brief skeleton, which becomes `## Request`. The `## ARTIFACT` section names the story, defines the slug, and fixes `YYYYMMDD` as the day the story is created rather than the day of a later write.
- `skills/bug/SKILL.md` - "the brief" becomes "the root cause" in both places. `## ARTIFACT` replaces its prose list of contents with the fixed heading skeleton `/nxs:plan` now reads, and gains the same story, slug, and date rules as `rnd`.
- `skills/plan/SKILL.md` - reading the source artifact by its headings becomes the first step of `## PROCEDURE`, which is what `rnd` already promised on its side and nothing enforced on this one. Input is a request, a brief, or a root cause. A story that already holds a `plan.md` is not overwritten silently.
- `skills/exec/SKILL.md`, `hooks/using-nxs.md`, `README.md` - `skill` becomes `command` in user-facing text; `skill` stays only for the file that implements one. The README `## Artifacts` section becomes `## Stories` and separates the three artifacts from what `exec` and `review` leave in git.
- `agents/review-implementation.md` - a requirement may come from the root cause, which was missing from the list of sources.

### Removed

- The archiving rule from `skills/plan/SKILL.md` and `skills/exec/SKILL.md`. It survives as a described user action in `README.md` and `CONTRIBUTING.md`.

## [0.15.0] - 2026-08-08

The plugin loses a whole layer. It had grown to 2348 lines across seven commands, four background skills, six `reference/` files, and four agents, and one rule lived in several of them at once: changing the shape of a plan task meant editing `plan/SKILL.md`, `plan-conventions/SKILL.md`, `reference/plan-template.md`, and `exec/SKILL.md` together. The architecture now follows [ralphex](https://github.com/umputun/ralphex): flat self-contained files, narrow single-subject agents, the output format stated at the end of each agent instead of a shared protocol injected into it, and a contract between plan and execution reduced to two structural tokens. 822 lines of skills and agents, no background tier at all.

The review gate moves too. It used to run inside `exec` after every task, with two lenses, an acceptance comparison, a cap of five fix rounds, and stalemate detection to keep it from looping. Now `exec` runs the plan straight through, committing each green task, and `review` runs once over the finished branch with five agents in parallel - and it fixes what it confirms instead of only reporting it.

### Changed

- `skills/review/SKILL.md` - launches five agents in one message, merges duplicates, verifies every candidate against the code, fixes the confirmed ones, and commits `fix: address review findings`. A round that fixed something runs again, because fixes introduce problems; a round with zero findings ends the pass, and three rounds is the ceiling. Injection is gone: agents fetch the diff themselves and carry their own output format.
- `skills/plan/SKILL.md` - absorbs `plancheck` and the whole `plan-conventions` tree. It carries the plan template with one filled example, the decomposition rules (3-7 tasks, each one working unit with its tests, dependencies running forward), and a self-check against the repository as its last step instead of a separate command and a separate agent.
- `skills/exec/SKILL.md` - the cycle is pick, delegate, validate, flip checkboxes, commit. It absorbs the `verify` discipline as one step that runs the commands the task names, and the commit format from `commit-conventions`. Stop conditions go from thirteen to seven.
- `skills/commit/SKILL.md` - absorbs `commit-conventions`: message format, types, atomicity, staging hygiene, git safety.
- `skills/rnd/SKILL.md` - same three steps, without the internal Impact times Uncertainty scoring, the coverage-category table, and the one-loop-back rule.
- `skills/bug/SKILL.md` - ten phases become eight, the seven feedback-loop types become one sentence, and evidence-request mode becomes one paragraph.
- `agents/worker.md` - drops the enumerated list of destructive operations, which the global tier already covers, and the `AC:` line from its result block.
- `hooks/using-nxs.md`, `README.md`, `CONTRIBUTING.md` - six commands, two tiers, no background skills or `reference/` directories.

### Added

- `agents/review-quality.md`, `review-implementation.md`, `review-testing.md`, `review-simplification.md`, `review-documentation.md` - five read-only reviewers, one subject each, self-contained. Every one fetches the branch diff itself, states its own bounds and what the other agents own, and ends with a `## WHAT TO REPORT` block. `review-simplification` names the over-engineering patterns it looks for rather than describing the idea.

### Removed

- The background tier: `skills/plan-conventions/` (with `plan-template.md`, `tdd.md`, `vertical-slice.md`), `skills/review-protocol/`, `skills/verify/`, `skills/commit-conventions/`, and `skills/review/reference/`. Everything they held now lives in the one command or agent that uses it.
- `/nxs:plancheck` and `agents/plan-reviewer.md` - the plan self-check runs inline at the end of `/nxs:plan`.
- `agents/review-quality-reviewer.md` and `agents/review-fit-reviewer.md`, replaced by the five narrow reviewers.
- The four development approaches (`default`, `TDD`, `tracer-bullet`, `spike`) with `exec`'s TDD mode and the `## DEVELOPMENT APPROACH` section. Tests are written with the code; `exec` branches on nothing.
- The review step inside `exec`'s task cycle, with its five-round cap and stalemate detection. Nothing loops there anymore.
- `## SOURCE ARTIFACTS` (a `Tracker:` line in the plan header replaces it), `## COMPLEXITY TRACKING`, the mandatory `Test cases` block, and per-task success criteria.
- `examples/` - the filled plan and brief samples, and the plancheck fixtures they calibrated. The worked example now sits inside the template in `plan/SKILL.md`.

## [0.14.0] - 2026-07-31

A plan task is now a capability, not a step. `/nxs:exec` pays a fixed toll per task - a fresh worker with a cold context, a verify run, a two-lens review to zero BLOCK, an AC comparison, a commit - so a plan that splits one capability into five technical steps costs about five times what the same capability costs as one slice. Every rule in the repo pushed toward that split: the sizing rule targeted five checkboxes, the vertical-slice reference asked for "many thin slices, not a few thick ones", and all three worked examples taught fine-grained slicing, one of them sliced horizontally by layer despite the rule forbidding it. The bar moves to 2-5 tasks for a typical feature with 7 as the ceiling, and a boundary now has to earn itself. Nothing about rigor moves: a task still carries Test cases, success criteria, and a verification step, and that step now names the project's actual command instead of saying "run tests".

### Changed

- `skills/plan-conventions/SKILL.md` - a task is one complete capability carried through every layer it needs, not "one function, one endpoint, one component". `## TASK SIZING, DECOMPOSITION, SEQUENCING` states the 2-5 / 7 counts and the five criteria that license a split: parts release independently, carry different risk, change different public contracts, need different verification strategies, or one task would be too large to review in a single pass. Touching different files or layers is explicitly not one of them.
- `skills/plan-conventions/reference/vertical-slice.md` - the registration example becomes two complete slices instead of three validation cases, a second anti-pattern block names the cost of splitting one capability by step, and a reviewability check says when a slice is the right size: what capability was added, how it is verified, what contracts changed, what risk remains, all answerable from one task.
- `skills/plan-conventions/reference/plan-template.md` - the worked task is a cross-layer capability with a Files block spanning migration, service, and API, replacing the single-file hashing utility.
- `skills/plan-conventions/reference/tdd.md` - a larger slice means more RED -> GREEN -> REFACTOR cycles, never a longer one.
- `skills/plan/SKILL.md` - step 4 asks for the fewest vertical slices the split criteria justify and defers the counts to `plan-conventions`.
- `skills/exec/SKILL.md` - the commit rule moves into cycle step 6 and covers both ways a task gets split at commit time, by layer and by TDD micro-cycle. The large-diff stop condition now measures against the task's Files block and goal, so a diff matching a deliberately large slice is expected rather than a stop. The review-fix cap goes from 3 rounds to 5: a stalled task now holds a whole capability of uncommitted work, and rounds that make no progress are already cut by stalemate detection.
- `skills/plancheck/reference/plan-review-policy.md` - slicing is a NIT, reported once for the group with the merge named, never a BLOCK. It covers both over-splitting and cutting by layer, which used to be judged in two places at once. `agents/plan-reviewer.md` drops `task size` and the slicing clause from its NOT-YOUR-JOB list so the injected policy is not overridden; checkbox counts, titles, and section order stay dropped.
- `examples/plan-sample.md` - the pagination plan collapses from three layer tasks (params -> repository -> handler) to the single slice it always was.
- `README.md` - plan tasks are a story's end-to-end increments, not its atomic steps.

### Removed

- The `~5 checkboxes per task` target with its split-at-8 and merge-at-2 thresholds, and the slice-size bound that repeated it in `reference/vertical-slice.md`. Task size is governed by the split criteria and the reviewability check; a checkbox count never described a capability.
- `exec`'s `commit granularity` bullet in TDD MODE, folded into cycle step 6 where the commit already happens.

## [0.13.1] - 2026-07-28

Prompt cleanup against Anthropic's skill-authoring and prompt-engineering guidance. Nothing about the workflow changes: same commands, same agents, same artifact paths, same gates. What changes is that a rule is now stated once. The corpus had drifted from `CONTRIBUTING`'s own placement rule - read-only was declared five times on the review path, TDD and vertical-slice discipline lived in three files each, and four `## RULES` sections were compressed restatements of the body above them. Every deleted sentence was checked against a surviving home before it went.

### Removed

- The `## RULES` recap sections in `rnd`, `bug`, `plan`, `plancheck`, and `verify`. Every bullet restated the body; the two that did not (no destructive commands, no aborting on the first failure) moved into `verify`'s procedure.
- `exec`'s `## WHAT EXEC NEVER DOES`, `## AC VERIFICATION`, and `## REFERENCE SKILLS`. The first duplicated the stop conditions and execution discipline, the second restated cycle step 5, and the third re-listed skills already named at the point of use. Git safety keeps a line of its own in `## STANCE`, since a safety gate should not depend on a background skill loading.
- `plan-conventions`'s `## TDD LOOP (essence)` and `## VERTICAL SLICE (essence)`. A skill file points at its references rather than summarizing them first - the one-line pointers in `## DEVELOPMENT APPROACH` and `## TASK SIZING` carry it now.
- The `Self-contained skill. Output language and response style come from global rules` line from all seven command skills, and `Workflow rules, not a user-invocable command` from all four background skills. Both are already carried by frontmatter.
- The duplicate template rules and COMPLEXITY TRACKING table in `reference/plan-template.md`, which restated `plan-conventions`. The filled example row moved up to the table's single home.

### Changed

- The reviewer agent files trade their essayistic voice for plain imperative: the rule stays, the aphorism justifying it goes.
- `hooks/using-nxs.md` drops the `<EXTREMELY-IMPORTANT>` wrapper and "this is not negotiable" for a direct opening sentence. The command triggers and the red-flag phrases are unchanged.
- One term per concept: the actor that classifies findings is the orchestrator everywhere, and a review subagent is a lens.
- `reference/plan-template.md` gains a table of contents, being over 100 lines.
- `exec`'s description no longer retells its own workflow, per `CONTRIBUTING`'s rule on descriptions.

## [0.13.0] - 2026-07-28

Review gets its bar, its lenses, and its report reworked together. `/nxs:plancheck` had no plan-shaped definition of a BLOCK, so it borrowed the code-shaped one and called every omission a block; it has one now, and it is the only place plan severity is written down. Four code lenses become two, cut by reading mode rather than by severity: one reads the execution paths the diff touches and the tests over them, the other surveys the diff against its requirements and the rest of the project. And both reports now open with the verdict instead of ending with it.

### Added

- `skills/plancheck/reference/plan-review-policy.md` - what `/nxs:exec` actually is as an executor, the plan-shaped BLOCK / NIT / DROP bar, and the calls that are easy to get wrong. Read by the orchestrator and injected into the lens beside `review-protocol`.
- `examples/plancheck-fixtures/` - two plans written against this repository, one carrying a single real blocker among plausible bait and one carrying none, with the expected verdicts kept in `examples/plancheck-fixtures.md` so they cannot leak into a review.
- `agents/review-fit-reviewer.md` - what the change is missing or never wired up, and what it carries beyond what the task asked for: over-engineering, duplication, dead code, scope creep. Replaces `review-implementation-reviewer` and `review-simplification-reviewer`.
- `skills/review/reference/review-axes.md` - where this project keeps its standards, how to find the source artifact, and the citation each axis finding carries. Split out of `review-policy.md` so a lens is never handed a procedure for finding artifacts it must not go looking for.

### Changed

- A plan BLOCK means the wrong end state ships and no gate catches it: the task's Test cases, the `verify` run, the review of that task's diff, the acceptance criteria, and exec's stop conditions all read as passing with the wrong result in place. A gap one of those catches is a NIT. A fix that adds a sentence to the plan and leaves the resulting code identical is neither.
- `/nxs:plancheck` classifies and `nxs:plan-reviewer` proposes unlabeled candidates. The verify step now runs two gates - the `Repo:` command reproduces, and no named gate catches the consequence - instead of re-running the command alone. Every candidate carries a mandatory `Impact:` naming an end state after execution, not a property of the document.
- `nxs:plan-reviewer` drops the line making every unlisted dependent a BLOCK, and the line rewarding the check that finds the most. It no longer reports open `[NEEDS CLARIFICATION]` markers - the orchestrator already checks them mechanically.
- `plan-conventions` states what a plan must contain and no longer assigns review severity to it. The Files block and Test cases stay mandatory; whether a missing one is worth reporting is `/nxs:plancheck`'s call.
- `nxs:review-quality-reviewer` also owns test coverage and test quality, and interleaves the two questions: read a path, then read what tests it, before moving to the next path. A bug and the missing test for it are one finding, with the test named in `Fix:`.
- `reference/review-policy.md` is the lens payload now: `/nxs:review` injects it into both lenses beside `review-protocol`, the way `/nxs:plancheck` injects `plan-review-policy.md`. It holds only what a lens acts on - where a requirement may come from, when scope creep costs something, and the three classification calls that are easy to get wrong.
- The rules the agent files stated in their own words - complexity judged against the task, never asking for a case matrix, and requirements coming from the artifact rather than from the reviewer - live in the policy alone.
- Lens selection has two cases: a trivial or non-code diff gets one direct orchestrator pass and no subagents, anything with logic gets both lenses in parallel.
- `dedup` names the collision two lenses actually produce: the fit lens and the Spec axis on one unmet requirement, and a bug reported apart from the test that would have caught it.
- `/nxs:exec` reviews a task diff with both lenses or the direct pass, not with a set sized to the change.
- The report `/nxs:review` and `/nxs:plancheck` print opens with the verdict, the counts and the scope, so the size of the problem is the first thing read; the provenance that used to head the report is now its last line. A block is an anchor, one sentence naming the cause and what it costs, and a `Fix:` line - `Issue:` and `Impact:` split one sentence in two and made the second half restate the first. Nits get a line each instead of one comma-separated run. The candidate format the lenses hand the orchestrator is unchanged: naming an impact is a bar on writing a finding, not on reading one.

### Removed

- `agents/review-implementation-reviewer.md`, `agents/review-testing-reviewer.md`, `agents/review-simplification-reviewer.md`. Anything spawning them by name breaks; `nxs:review-quality-reviewer` and `nxs:review-fit-reviewer` replace them.

## [0.12.0] - 2026-07-28

The artifacts of one unit of work now live together. `docs/nxs/briefs/` and `docs/nxs/plans/` give way to one directory per story, holding the brief and the plan side by side and archived as a whole.

### Added

- A read-only fallback in the Spec axis: with no `docs/nxs/stories/` present, review still finds a plan under `docs/nxs/plans/` and a brief under `docs/nxs/briefs/`. Compatibility only - nothing is ever written to the old layout - and removable in a later release. Existing files stay where they are; there is no migration.

### Changed

- Artifact paths: `/nxs:rnd` writes `docs/nxs/stories/YYYYMMDD-<slug>/brief.md`, `/nxs:bug` writes `root-cause.md`, and `/nxs:plan` writes `plan.md` into the same directory, creating it when there is no prior brief. A tracker key names the directory, never the files inside it.
- Archiving moves the whole story directory to `docs/nxs/stories/completed/`, still on explicit user confirmation only.
- `/nxs:plancheck` and `/nxs:exec` resolve the latest story that contains a `plan.md`; an explicit argument may be a story directory or a plan file. The `argument-hint` of `plan`, `plancheck`, and `exec` changes accordingly.
- `## SOURCE ARTIFACTS` records a tracker key or URL and nothing else - the brief is a sibling and needs no pointer - and is omitted without one.
- The Spec axis resolves a story's plan and its sibling brief in one step instead of two.

## [0.11.0] - 2026-07-23

Simplify the architecture: every non-command skill is now a plain rules contract, and a SessionStart hook makes the commands fire on their trigger. The `intake` dispatcher is gone, and a real `/nxs:commit` command commits working changes.

### Added

- `/nxs:commit` - commit the current working changes, split into atomic commits with conventional messages, for edits made outside `/nxs:exec`.
- A SessionStart hook (`hooks/`) that injects the `using-nxs` discipline so a session checks for the right command before acting.

### Changed

- `commit-conventions` is a pure convention now: message format, atomicity, staging hygiene, and git safety. The exec-specific gate (commit only after verify and a zero-BLOCK review, the `no commits` mode) lives in `/nxs:exec`, which already owned it.
- `rnd`, `bug`, `plan` drop their `INTAKE` sections; the tracker-ticket rule (read the ticket, name the artifact by its key) moved to the `using-nxs` hook.
- `verify` points at `/nxs:exec` as the owner of the commit gate.

### Removed

- The `intake` background skill. Its ticket-reading rule moved to the hook; its task/bug routing is dropped - the entry command is the user's choice.

## [0.10.1] - 2026-07-22

An audit for name conflicts and dead terms. No command, argument, path scheme, or gate changed; the contract is where it always was, and this release makes the files agree with it.

### Fixed

- The plan's source-artifact section has one name again: `## SOURCE ARTIFACTS`. `plan-conventions`, its template, and the sample plan called it `Context / source artifacts`, while `/nxs:plan` wrote and `/nxs:plancheck` plus the review spec axis read `## SOURCE ARTIFACTS` - so the section a plan carried was not the one its readers looked for. It is written only when a source artifact exists, which is what `/nxs:plan` already did.
- `review` and `plancheck` point at the protocol as `${CLAUDE_SKILL_DIR}/../review-protocol/SKILL.md`. The old relative path resolved against the user's project instead of the plugin, where the file is not, so every lens could answer `protocol missing` instead of reviewing. Both orchestrators carry a fallback: the path does not resolve -> find the file inside the plugin before spawning anything, and no lens reviews from memory.
- `exec` names the plan's `## DEVELOPMENT APPROACH` section instead of a `Development approach: TDD` line no plan ever writes; TDD mode keys off the section.
- `bug` says it writes no fix and no product code, instead of claiming nothing mutates the repo - the investigation builds probes, adds debug logs, and writes the brief.
- The tier-3 placement rule matches what `commit-conventions` actually holds: security-critical content never lives on tier 3 alone, but the git gate is workflow detail and belongs there. README no longer says the force-push ban was moved out of the skill.
- `plan-conventions` drops its second copy of the plan path (`yyyymmdd-<task-name>.md` against `YYYYMMDD-<slug>.md` everywhere else). The path lives only in the `## ARTIFACT` section of `/nxs:plan`.
- Section names and order match the template: `Implementation`, and acceptance criteria are no longer described as "right after Overview" when source artifacts sit between them.
- The strict task template carries the `Success:` line the conventions require and the sample plan writes, and its example file paths have extensions.
- `intake` lists `/nxs:plan` as a consumer, which it has been all along.

### Removed

- `examples/epic-sample.md` and `examples/adr-sample.md`. `epic` went in 0.9.0 and its sample still pointed at `decision-log` and the pre-0.9.0 `docs/plans/` path; no command has written an ADR since `decision-log` went.
- The output block `plan-reviewer` duplicated from `plancheck` byte for byte. The agent now follows the injected protocol like the four review lenses, so its verdict is `CLEAN | FINDINGS` and `plancheck` alone owns the user-facing `APPROVE | NEEDS CHANGES` report.

### Changed

- `rnd` and `bug` are the task and bug entry points, not the "tracked-task" and "tracked-bug" ones - both accept input that carries no tracker key.
- CONTRIBUTING documents agent frontmatter (`name`, `description`, `tools`), and the repo layout lists `examples/`, `.github/`, `CHANGELOG.md`, and `LICENSE`.
- The plan archive folder is stated once, in `plan-conventions`; `exec` and the task template point at that rule instead of repeating the path. CONTRIBUTING says why: where an artifact goes after it is written is not a write path, so the `## ARTIFACT` rule does not cover it.

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
