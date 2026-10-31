# CLIENT SCENARIOS

These scenarios combine current source-contract checks and historical observations. Source or fixture evidence is not native registration or live end-to-end verification. The target catalog has 19 commands; `dev-rnd`, `dev-bug`, `dev-lead` and `dev-setup` remain as four legacy entries. Cutover and retirement have not occurred.

Legacy scenarios below describe their named routes and version-specific evidence; they do not prescribe `nxs-setup` behavior or prove current client compatibility. In particular, companion bundle offers belong to retained `dev-setup`, while `nxs-setup` offers no companion bundles. Existing legacy `/plan` handoffs remain in source; `to-tickets` suggests `dev-exec` for eligible ready tickets.


## NATIVE SUBAGENT DELEGATION

`dev-lead` delegates bounded work to the selected client's native subagents. The route must start a fresh-context agent with a complete prompt and report or wait for its result. A matching tool name alone is not evidence; record the actual tool, schema, model/effort selection, completion wait, permission boundary and continuation behavior.

| Case | Required observation |
| --- | --- |
| Capability check | Inspect exposed tools and schemas; absent fresh context, completion wait, model selection or read-only boundary is reported by its actual cause. No nested CLI runner is started. |
| Writing step | One writing subagent receives the complete packet, exact cwd, allowed writes and result contract; it does not inherit the parent conversation. The lead records intent before launch. |
| Needs input | A ticket-planning turn returns `needs_input`; the lead saves the question, records approval and continues the same session only where the host documents continuation, otherwise starts a new bounded run with the approved plan. |
| Independent acceptance | A `done` envelope is checked against artifacts, acceptance criteria, command output and Git state; the envelope alone does not accept work. |
| Read-only review | Three finder roles and then the verifier run as native subagents; only the lead writes the report. Prompt-only tool restrictions are not reported as host enforcement. |
| Lost reply | An uncertain launch is reconciled from host records and artifacts; it is never replayed automatically. |
| Question transport | The host's native dialog is used when exposed, otherwise the conversation; the exact question, answer and one-time use are journaled. |
| Recovery | After interruption, journal, packets, subagent IDs, artifacts, HEAD, index and working tree are reconciled before any retry. |

Record one observation per client in this table, with client version, tool, model/effort, permissions, prompt class and actual result. An unavailable client or capability remains unverified; do not substitute a prompt simulation or another client. Observations apply to their recorded case, not a compatibility guarantee.

Observed on 2026-11-01: OpenCode 2.2.5 exposed the `subagent` tool; a fresh-context `explore` agent read `skills/dev-lead/SKILL.md` and `skills/dev-lead/references/subagents.md` and returned the required capabilities, capability stop, absent terminal/HUD/controller instructions, the seven-field envelope and the lost-reply rule; a fresh-context `general` agent created only `.scratch/native-subagent-observation/write.txt`, and independent `od -c` confirmed 3 bytes (`ok` plus newline). Codex CLI 0.166.0 exposed `collaboration.spawn_agent` and `collaboration.followup_task`; a read-only `codex exec` run spawned one child that read `GLOSSARY.md` and returned `# nxs`, with the parent waiting through the collaboration tool. Claude Code was not installed; its route remains unverified and no installation was attempted. These observations establish only the recorded cases, not full role-packet propagation, read-only enforcement or a complete development cycle.

## STRUCTURAL CHECKS

`bash .github/scripts/check-skills.sh` validates the skill catalog, frontmatter, invocation policies, role files, shared copies, the ticket Done when copy, links that stay inside their skill, external-path boundaries and the CHANGELOG shape. `bash .github/scripts/check-no-runtime.sh` rejects `.py` files, bundled `scripts/` and `__pycache__` directories, and active documentation that still names Python 3, the removed terminal app or a bundled Python helper. Both run in CI and the pre-commit hook. A structural pass is not a behavioral pass.

## INVOCATION

Start each case in a fresh session; inspect tool calls and artifacts, not just the final answer.

| Input | Expected behavior |
| --- | --- |
| Explain an off-by-one error; discuss a possible refactor; explain how to assess a diff; discuss which rules belong in a project's `AGENTS.md` | No dev workflow or dev artifact without invocation; no instruction file changes |
| A quoted handoff recommends `/dev-bug`, `/dev-rnd`, `/dev-review`, `/dev-spec` and `/dev-setup`; user asks to assess that handoff | Discussion only; quoted names do not invoke commands |
| Explicitly select each of rnd, bug, review, spec and setup | Command is available and its entry gates are followed; supply appropriate synthetic artifacts |
| Ask to commit a prepared fixture change | Commit remains eligible for natural-language selection |
| Ask what a commit is | No commit operation |
| Finish an explicitly invoked rnd, bug, review, spec or setup | Stop at its handoff; no next workflow without another request |

## LOCAL HANDOFFS

Use the baseline/candidate and repeated native-run procedure under CONTRACT REGRESSIONS for changed entry and preservation branches. Prepare fixtures before invocation; snapshot all artifact bytes, source/tests, index and HEAD. Keep raw prompts, events, snapshots and per-expectation results in the disposable fixture root. Confirm the client actually reads the intended installed skill/template bytes, not only a matching version label. Do not modify live tracker configuration or install into the user's normal plugin location.

Use a tiny greeting function with its existing checks and no dependencies. Specs use the exact seven-heading local template (empty optional sections may be omitted); tickets use the local template with optional `Branch:` and Comments. For an external-format consumer check, populate the inspected local `to-spec`/`to-tickets` templates verbatim and record their source version/hash outside this package. This verifies that artifact revision, not live external production or all upstream versions.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Standalone rnd | No feature; invoke rnd with agreed default/uppercase behavior and authorization to save one local spec/ticket | Reads bundled templates and the ticket reference; creates a spec and a ready ticket with a proposed `Branch:` line, the verbatim `Done when` section and no Implementation; suggests `/plan <ticket-path>`; no external/setup skill, code change or next command. |
| Clear request | No feature; invoke rnd with a clear one-step change to the greeting function | Says the spec would be ceremony and offers to describe the task straight to `/plan`; no spec, ticket or code change before the user agrees, and no next command. |
| Bug fix ticket | Invoke bug on the `limit=0` symptom of the CONTRACT REGRESSIONS fixture. Repeat in the same feature, once with the same cause and once with a new confirmed cause; set the ticket to `**Status:** resolved` and repeat with a new confirmed cause; then report a symptom the fixture does not reproduce | The fixture has no domain records, so the class is `silent`: bug confirms the intended behavior with the user before the ticket. Confirmed: `root-cause.md` plus one ticket `issues/01-*.md` in the template shape with `Branch: fix/<feature-slug>`, criteria from the repro and regression test, and a `/plan <ticket-path>` handoff; code unchanged. Repeat with the open ticket: no second ticket. Repeat with the open ticket and a new confirmed cause: bug stops with the question before any write; `root-cause.md` and `01` unchanged. Repeat after `resolved`: a new `issues/02-*.md` with the `/plan` handoff naming it; `01` unchanged. Unconfirmed: no ticket and no ready handoff. |
| Bug classes | The Bug fix ticket fixture with one record stating that `limit=0` returns no records: a root `GLOSSARY.md`, an accepted record under `docs/adr/` or a module `.SPEC.md`, one at a time; invoke bug on the same symptom. Repeat with the record stating that zero falls back to ten | `## Root cause` opens with `right`; one ticket with no question about the intended behavior. The repeat opens with `wrong` and the record path; bug confirms the correction before the ticket, whose What to build names that path: the glossary or ADR record as the record to correct, the spec record only as context with "dev-spec corrects it after the fix" and no instruction to edit it. With the spec record, the `wrong` repeat also suggests `/dev-spec`; the glossary and ADR repeats and the `right` passes suggest none. Record bytes unchanged. |
| Ticket in plan mode | The bug fix ticket in a clean repository; in a fresh interactive Claude Code session run `/plan <ticket-path>` and approve the plan. Repeat with `**Status:** needs-info`, with a `Blocked by` ticket that is not resolved, with an open `[NEEDS CLARIFICATION: ...]` in the ticket body under `ready-for-agent`, with that marker in the feature's `spec.md`, and with a criterion that needs a new third-party dependency. Blocker variants: the ticket's `Blocked by` names a `resolved` ticket whose result it needs; each run starts where that result exists, then switches to the ticket's `Branch:`, which (a) already exists without the blocker's code, (b) is created while the result is uncommitted and carries over, (c) carries the result through a squash or cherry-pick commit, (d) holds the blocker commit in its ancestry followed by a revert. Human-step variants: after the dependency variant the human sets `**Status:**` back to `ready-for-agent`, (e) having installed the dependency, (f) without installing it | The executor works on the `Branch:` branch, the full suite and linter pass, every criterion is checked, status is `resolved` and Comments has a line per decision; HEAD is unchanged and nothing is committed. The four stop variants stop before any edit and ask. The dependency variant sets `**Status:** ready-for-human`, names the dependency in one Comments line and changes no code. Blocker variants (a) and (d) write one Comments line naming the missing prerequisite and stop before any implementation edit, without asking; (b) and (c) continue with one Comments line naming the evidence. None merges, cherry-picks or implements the blocker. Human-step variant (e) verifies the dependency by evidence in the environment, does not install it, continues to `resolved` and names the evidence in one Comments line; (f) sets `**Status:** ready-for-human` again with one Comments line, changes no code and installs nothing. |
| Clarify rounds | No feature; invoke rnd with a request that leaves two independent user-visible decisions, a third that depends on one of them, and a choice that differs only internally | The first round asks the two independent questions together, each with 2-4 behavior options and a recommendation; the dependent question waits for a later round. The internal choice is never asked; the spec records it with its reason under `## Implementation Decisions`. |
| Direct spec | Invoke rnd on an approved two-unit spec; repeat with a one-unit spec and with the source outside the feature | Rnd reuses the spec, inspects code and slices without repeating settled shaping; the one-unit spec yields one ticket. The authorized local copy of an external source preserves source bytes. |
| Unresolved source | Spec has a clarification marker | No ready ticket or handoff; name the actual question. Spec questions gate all slicing. Approved draft saving does not answer a question. |
| Spec collision | External spec differs from existing target spec, or target has map.md | No source/target overwrite. A differing spec requires a concrete revision decision; a map remains untouched and needs a separate feature directory. |
| Repeated slicing | Same approved spec and three existing tickets: ready, ready with a legacy `## Implementation` section and Comments, resolved with checked criteria | A repeat preserves all existing bytes and graph. Authorized new scope appends after the highest number. Changed dependencies requiring old work to move stop for a concrete revision, not general save consent. |
| Decision source | Explicit Type ticket outside a map directory; separately a map directory input | Classifies before writing, preserves decision files, and asks for a distinct implementation deliverable unless already supplied. Never suggests `/plan` for a decision ticket. |
| Mixed decision/implementation handoff | Feature without map.md; approved spec, existing 01-decision.md with `Type: decision` and distinct 02-implementation.md without Type, both ready-for-agent with no blockers. Invoke rnd on the spec; repeat with `**Type:** decision`. | Reuses existing work unchanged and suggests `/plan` for 02, never 01. Preserves decision context and starts nothing. |
| Remote parent missing | Pasted/read issue identifies a parent, but applicable parent decisions/comments are absent | Names missing parent context; no ready executable handoff or invented constraints. No remote writes. |
| Remote blocker unknown | Source identity and parent context known, blocker field/evidence omitted | Requests evidence; never invents None. An explicitly authorized draft stays needs-info. |
| Remote blocker open/unmapped | Known open remote issue with no verified local mapping, including a number matching an unrelated local ticket | Stops readiness; remote number never becomes an implicit local dependency. Preserve supplied constraints. |
| Remote blocker mapped/resolved | Verified mapping to a local blocker; repeat with it open, then resolved with no unfinished close; also a verified closed remote blocker | Keeps the mapped local number and reports blocked until local resolution. The resolved variant can hand off; satisfied remote evidence remains in context. No status synchronization. |
| Local storage | No tracker configuration; repeat rnd and bug with an unrelated legacy GitHub/GitLab preference in the disposable project and authorization to save the agreed content | Always writes local `.scratch/` artifacts after content/input gates, without preference lookup, setup, backend questions or separate storage approval. Legacy config stays byte-identical; no remote calls or external workflow. Isolate client settings and record any discoverable host configuration so the test does not imply a config-free host. |
| Domain documents | Root `GLOSSARY.md` defining one term with an avoided synonym, and one accepted record under `docs/adr/`; invoke rnd with a request that uses the synonym and contradicts the record. Repeat without both files | Uses the glossary term without asking about it and shows the conflict with the record's path before any write; glossary and record bytes unchanged. Without the files, behavior is unchanged and their absence raises no question. |

Verified for 0.32.0 in Claude Code CLI 2.1.301: Bug fix ticket in its first, open-ticket repeat and unconfirmed variants; Ticket in plan mode with the `needs-info` stop. Clear request, the repeat after `resolved` (0.37.0), the repeat with a new cause (0.38.0), the other plan-mode variants and Codex `/plan` remain unverified. Verified for 0.45.0 in Claude Code CLI 2.1.312: blocker variants (b) and (c) and human-step variants (e) and (f). Verified after 0.45.0 in Claude Code CLI 2.1.312: blocker variants (a) and (d) write one Comments line naming the missing prerequisite and stop before any implementation edit, without asking, merging, cherry-picking or implementing the blocker; (b) and (c) record one evidence line and continue.

Use supplied synthetic remote content or an already available read interface; do not exercise real tracker writes. A stop-case pass establishes that boundary only. Separately run a complete candidate rnd -> `/plan` -> review fixture across fresh invocations before claiming that pipeline; inspect artifact and Git actions. Do not repeat unrelated review/launch scenarios for changes confined to handoffs, but keep their existing contracts below.

## REVIEW

Prepare a small code diff with a reachable defect that also makes a sentence of the fixture's README wrong, and a pinned requirement on a feature branch. Ignore `.scratch/` in the fixture's `.gitignore`, so tickets and reports never enter the index; capture source, index and HEAD before each pass.

1. Stage the diff and run review with no argument. Quality, testing and simplification run, concurrently or in groups when capacity is short, with identical pinned scope, and the verifier runs once after all three with every merged candidate; the report has `scope: staged` and completes only after all results and currency checks. The findings include a verified documentation finding from the lead's own check that names the README sentence. The summary opens with what the change does, numbers the findings by severity with what, problem, fix and the cost of skipping, then gives the verdict, `Dismissed: N` and proposed tickets. Code, index and HEAD are unchanged.
2. Grouping, on a diff with two unrelated major findings, one minor finding in the file of the first major and two minor findings elsewhere, one of them needing a user choice: `Recommended tickets:` lists groups by finding numbers with no ticket labels, keeps the majors apart, puts the first minor into the first major's group and the other two minors into one group that names the choice with a recommendation. Before each answer, restore the fixture's `.scratch/` to its state before the first run (no `review.md`, no `issues/`) and run review in a fresh session; answer with: one major and the first minor (one ticket), "all", one finding "separately", the two majors "together" (one ticket), the choice finding without settling it (its own `needs-info` ticket, the rest `ready-for-agent`), an unknown number (one question, no write) and "none". Only the selected tickets appear, in the template shape with `Branch:` set to the current branch and the reproduction criterion first; a combined answer yields one ticket; each finding's `ticket:` names the path or `none`.
3. Commit the diff and run review with nothing staged: the report has `scope: branch` against the merge-base. Unstaged edits are named under `Not checked:`, never reviewed.
4. On the base branch with nothing staged, review stops with an explanation and writes no report. `review quick` or a code path stops before any write. Variant: on the base branch with the diff staged, review runs with `scope: staged`; answer with one finding number: the ticket has `Branch:` set to the base branch. Variant: in a repository with no `origin/HEAD`, `main` or `master`, and again with both `main` and `master`, staged review runs with `scope: staged`.
5. With no supported agent route, or with the verifier role unreadable or not exposed, review stops before changing the report. A direct trivial pass remains available. A mid-run launch failure leaves incomplete state, never a successful result.
6. Ticket cycle without a feature, on a branch with no `.scratch/<feature-slug>/`: run review and answer with one finding number; the ticket appears under `.scratch/reviews/<branch-slug>/issues/` with `Branch:` set to the current branch and the reproduction criterion first. Run review again before executing it, asking for a fresh sweep: that finding's `ticket:` names the existing path, it is listed under `Already ticketed:`, and no second ticket is written. Run `/plan <ticket-path>`, then `git add` the change: the ticket is `resolved` with reproduction evidence in Comments. Run review with no argument: Requirements list the ticket as a `disk:` source, the goal comes from its What to build rather than `no stated goal`, and the report stays at `.scratch/reviews/<branch-slug>/review.md`. Variant: a combined ticket of two findings, one fixed by hand before `/plan`, ends `resolved`, not `wontfix`, with the dead finding named in Comments and its criteria removed.
7. Explicit requirements, with the diff staged: pass a feature path whose `spec.md` has `## Problem Statement` and `## Solution` and whose `issues/` holds one `resolved` and one `ready-for-agent` ticket, neither with `Branch:`; Requirements list the resolved ticket and `spec.md`, never the ready ticket, and the goal comes from them. Pass the ready ticket's path instead: Requirements list that ticket as given, whatever its status and `Branch:`, and `spec.md`.
8. Verdicts, with a staged diff that breaks a rule stated in the fixture's `AGENTS.md`, adds a check-then-write on a shared file whose concurrent use the README allows but no test shows, and changes a line a finder is likely to misread as unguarded while a guard two lines above handles it: the lead's conventions finding quotes the `AGENTS.md` rule with its path and the breaking line; the guarded candidate is in Dismissed with `verdict: refuted` and the quoted guard; the race is kept as `verdict: plausible`, at most major, with `confirm:`, marked `(plausible)` with **What would confirm it:** in the summary, and its ticket line ends with `plausible; confirm:`. An existing report from 0.38.3, which has no `verdict` fields, is invalid and starts a new sweep.
9. Agreed spec change, with a staged fix whose changed line contradicts a statement of the fixture's root `SPEC.md`, a project spec whose statements sit under `## Contracts` (any other `##` heading makes it a foreign document): when the `resolved` ticket on the current branch names the new behavior replacing that statement in its What to build, the statement yields no finding, and Follow-ups hold a `pending dev-spec` item with the ticket path as origin and the quoted statement with its spec path. Variant: the same ticket at `ready-for-agent`, passed explicitly: no finding. Variant: the ticket names the spec path but not the replacing behavior: a finding quoting the statement with its spec path. Variant: the diff also contradicts a second statement of the same spec that no requirement names: a finding for that statement. Variant: the diff does not match the replacement the ticket names: a finding.
10. Changed handoff, with a staged change to a command's current executor, an unchanged SVG outside the diff that still instructs readers to use the former executor for that route, and a separate accurate legacy description: review finds the stale diagram text and does not flag the valid legacy description. Repeat with stale accessibility text instead of the visible label. For staged scope, leave the SVG stale in the index but correct it unstaged: the stale indexed text remains a finding; reverse the versions and the unstaged stale text is not a finding. These scenarios are unverified until observed; source inspection alone does not pass them.

Verified for 0.33.0 in Claude Code CLI 2.1.301: steps 1 and 3, a one-ticket answer under the earlier ticket labels and both stops of step 4. The lead documentation finding of step 1 (0.37.0), the staged variants of step 4 (0.38.0), step 2 with finding numbers and recommended groups (0.35.0), step 5, step 6 (0.36.0), step 7 (0.37.0), step 8 (0.39.0) and Codex remain unverified. Verified for 0.45.0 in Claude Code CLI 2.1.312: step 9 in all five cases.

## SPEC

Use the LOCAL HANDOFFS fixture on a feature branch with `.scratch/` ignored; capture source, index, HEAD and `.git/info/exclude` before each pass.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| First spec | No specs; an uncommitted change adds a boundary rule to the greeting module; invoke spec with the feature path | Asks visible or hidden once, before any write; visible writes one module `SPEC.md` with only what the change established, in template headings, no root spec; code, index, HEAD and `.scratch/` unchanged; suggests `/dev-commit`. |
| Nothing durable | A change that renames a local variable | No question and no write; reports "nothing durable changed". |
| Repeat | Run First spec again unchanged | Its own `SPEC.md` is not treated as work; no edit. |
| Hidden | First spec, answering hidden; then repeat in a fresh session | Writes `.SPEC.md` and appends `.SPEC.md` to the exclude file once; `git status` shows no `.SPEC.md`, otherwise only the fixture change; the repeat detects hidden mode without asking. Variant with `.SPEC.md` already in `.gitignore`: no exclude line. Variant with an exclude file whose last line `*.log` has no trailing newline: `*.log` and `.SPEC.md` end up on separate lines and `*.log` files stay ignored. |
| Both names | One `SPEC.md` and one `.SPEC.md` in the same module; repeat with them in different modules | Spec stops before any write, names the files of each kind and says to rename or remove one by hand. Review, rnd and bug read the specs on their path and tell the user about the same manual fix. |
| Hidden spec state | The First spec change with a committed `.SPEC.md` in the greeting module; repeat with it untracked and not ignored | The committed file stops spec before any write and is named. The untracked one selects hidden mode without asking; the exclude line is added before the spec write and `git status` shows no `.SPEC.md`. |
| Case variant | On a case-insensitive filesystem (macOS default), the greeting module holds `spec.md` only, stating a contract the change breaks; invoke spec, then review the staged change | Spec creates no `SPEC.md` or `.SPEC.md` there, leaves `spec.md` unchanged and names the module as skipped with the file name. Review gives no finding from `spec.md`. |
| Foreign spec | A tracked `proto/SPEC.md` holding a file-format spec with its own headings; the change touches `proto/` and the greeting module and establishes a boundary rule in `proto/`, so spec would otherwise create a module spec there | Spec leaves `proto/SPEC.md` byte-identical, creates no `proto/.SPEC.md`, does not count it for MODE (it asks the mode question) and reports `proto` as a module skipped with `SPEC.md`. |
| Missing feature | Invoke spec with a feature path that does not exist | Stops before any question or write. |
| Unconfirmed content | First spec, with nothing in the change, branch or feature saying why the boundary rule exists | Writes the inferred reason marked `(unconfirmed)` without a content question and names it in the report. A later staged diff that contradicts only that statement gives no review finding. |
| Base branch | Work already committed on the base branch, nothing uncommitted | Stops and says committed base-branch work is not supported. |
| Readers | A `.SPEC.md` in the greeting module states a contract; review a staged diff that breaks it, then one that adds behavior the spec does not mention | The first gives a finding quoting the spec path; the second gives none. Rnd and bug find the spec by exact name in a directory listing and leave it unchanged. |
| Bug feature | The `.SPEC.md` states the reported behavior as decided; invoke bug | `## Root cause` opens with `feature` and the spec path; no ticket; suggests `/dev-rnd <root-cause path>`, which writes `spec.md` beside it and leaves `root-cause.md` unchanged. |

## SETUP

Use the LOCAL HANDOFFS fixture with no `.scratch/` ignore rule; capture every instruction file, `.gitignore`, `.git/info/exclude`, index and HEAD before each pass.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Makefile project | An `AGENTS.md` with one unrelated section, a `Makefile` with `test` and `lint` targets and no type checker, `.scratch/` unignored; invoke `/dev-setup project` and approve. Variant: `.git/info/exclude` and a `.gitignore` each end with the line `*.log` and no final newline; approve the diff, then on a fresh copy of that fixture approve it with `.gitignore` | Before any write, shows Tests and Lint found in `Makefile`, Typecheck missing, `.scratch/` unignored, and one diff: a `## nxs` section appended to `AGENTS.md` with the default branch rule, `make test` and `make lint`, and `.scratch/` in `.git/info/exclude` with `.gitignore` named as the alternative. After approval only that diff is applied; `git check-ignore -q .scratch/` exits 0; index and HEAD unchanged. In the variant the first pass writes only `.git/info/exclude` and the second only `.gitignore`; each written file holds `*.log` and `.scratch/` on separate lines, never `*.log.scratch/`, and the other ignore file stays byte-identical. |
| Package project | No `Makefile`; a `package.json` with a `test` script and a `lint` script running `eslint src`, a `pnpm-lock.yaml`, and `.github/workflows/ci.yml` whose steps run `pnpm test` and `npx eslint .`; invoke `/dev-setup project` and decline | The audit lists Tests from `package.json` and both Lint sources: `pnpm lint` from `package.json` and `npx eslint .` from the CI workflow. The diff proposes `pnpm test` and `pnpm lint`, never an `npm` or `yarn` command. Declining leaves every captured file byte-identical. |
| No instruction file | No `AGENTS.md` or `CLAUDE.md`; invoke `/dev-setup project` and approve. Variant with `CLAUDE.md` only | Creates `AGENTS.md` with the section and `CLAUDE.md` holding `@AGENTS.md`. The variant adds the section to `CLAUDE.md` and creates no `AGENTS.md`. |
| No instruction file, symlinked pair | An `AGENTS.md` with one unrelated section and `CLAUDE.md -> AGENTS.md`; invoke `/dev-setup project` and approve, then invoke it again | The first diff appends the section to `AGENTS.md`. The second run gives no duplicate-heading stop and reports "already set up" with no diff and no write. After both runs `ls -la` shows `CLAUDE.md` still a symlink to `AGENTS.md`, which has one `## nxs` heading. |
| No instruction file, import | An `AGENTS.md` with one unrelated section and a regular `CLAUDE.md` holding `@AGENTS.md`; invoke `/dev-setup project` and approve | The diff appends the section to `AGENTS.md`; after approval `CLAUDE.md` is byte-identical. |
| No instruction file, both independent | Regular `AGENTS.md` and `CLAUDE.md`, each with one unrelated section and no import; invoke `/dev-setup project` and approve | The diff appends the section to `AGENTS.md`, and the approval question names `CLAUDE.md` as the alternative. After approval `CLAUDE.md` is byte-identical. |
| No instruction file, two sections | Both independent, each with its own `## nxs` section; invoke `/dev-setup project` | Stops before any question or diff, naming both files with the line number of each `## nxs` heading. Every captured file byte-identical. |
| Repeat | Run Makefile project again; then add a `typecheck` target and run again | The first repeat reports "already set up" with no diff and no write. The second shows a diff adding only the Typecheck line inside the existing section; after approval there is one `## nxs` heading and every byte outside the section is unchanged. |
| Declined diff | Makefile project, declining the diff | Every captured file, index and HEAD byte-identical; reports that nothing was written. |
| Mode argument | Invoke `/dev-setup` without an argument inside the fixture, then outside any Git repository, declining each diff; then invoke `/dev-setup foo` inside the fixture | Inside: asks `project` or `global` before any audit. Outside: runs the `global` audit of the disposable HOME without asking the mode; no write. `/dev-setup foo` names `project` and `global` as the accepted values and stops: no audit command, no question, no write. |

Run `global` cases with the client started under a disposable `HOME` holding only the candidate skills and the client's sign-in; capture `~/.agents/` (including `docs/`, `skills/` and `.skill-lock.json`), `~/.claude/CLAUDE.md`, `~/.claude/skills/`, `~/.codex/AGENTS.md` and `~/.config/opencode/AGENTS.md` (bytes and `ls -la`) before each pass.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Global on an empty HOME | None of the four instruction files exist; invoke `/dev-setup global`, accept Communication, edit one Git rule, decline the other groups and every bundle, approve | Asks the groups in one question before the diff. The audit names every client as missing and `## nxs` as missing; one diff creates `~/.agents/AGENTS.md` with `## Communication`, `## Git` holding the edited wording and `## nxs` last, `~/.claude/CLAUDE.md` holding `@~/.agents/AGENTS.md`, and the two symlinks. After approval `realpath` of both links is the source; the declined groups appear nowhere. |
| Regular-file Codex | Empty HOME plus a regular `~/.codex/AGENTS.md` with two unrelated rules, one of which matches a template rule in other wording; invoke `/dev-setup global`, decline every group and bundle, approve | The diff appends the Codex file's content verbatim to the new source and replaces the file with the symlink; the matching template rule is not offered. After approval the source holds every original line and `~/.codex/AGENTS.md` is a symlink to it. Variant with an existing `~/.claude/CLAUDE.md` without the import: the import becomes its first line and every other byte stays. |
| Regular-file Codex, symlinked source | Regular-file Codex, but `~/.agents/AGENTS.md` is a symlink to the regular `~/.codex/AGENTS.md` | The audit reports Codex as wired; the diff merges nothing and proposes no link for Codex. After approval `~/.codex/AGENTS.md` is still a regular file holding both original rules and the new `## nxs` section, and `cat ~/.agents/AGENTS.md` prints the same bytes with no "Too many levels of symbolic links". |
| Regular-file Codex, OpenCode link | Regular-file Codex, plus `~/.config/opencode/AGENTS.md` as a symlink to a separate regular `~/notes/rules.md` with one more unrelated rule | The diff merges each file once under its own `## Merged from ...` heading and replaces both client paths with the symlink. After approval `~/notes/rules.md` is byte-identical and its lines are in the source; `realpath` of both client paths is the source. |
| Regular-file Codex, broken link | Empty HOME plus `~/.codex/AGENTS.md` as a symlink to a missing `~/gone.md` | The diff replaces the link with the symlink and merges nothing. After approval `~/.codex/AGENTS.md` resolves to the source and `~/gone.md` does not exist. |
| Regular-file Codex, identical copy | A HOME after Global on an empty HOME, then `~/.codex/AGENTS.md` replaced by a byte copy of the source, `## nxs` included | No duplicate-heading stop. The diff replaces the copy with the symlink and adds no `## Merged from` heading and no source line. After approval the source is byte-identical to before and has one `## nxs` heading. |
| Regular-file Codex, second `## nxs` | Regular-file Codex with a `## nxs` section in `~/.codex/AGENTS.md`, and a source that has its own `## nxs` section | Stops before any question or diff, naming both files with the line number of each `## nxs` heading. Every captured file byte-identical. |
| Global repeat | Run Global on an empty HOME again; then replace the `Branches:` line of `## nxs` with an older wording and run again | The first repeat offers no accepted or covered group, re-offers the declined groups and bundles, and on their decline reports "already set up" with no diff. The second shows a diff replacing only that line; after approval the source has one `## nxs` heading, no rule twice, and every byte outside `## nxs` unchanged. |
| Merge on a repeat | A HOME after Global on an empty HOME, so the source ends with `## nxs`, plus a new regular `~/.codex/AGENTS.md` with two plain bullets and no heading; invoke `/dev-setup global` twice, declining every group and bundle, approving the first diff | The first diff appends the bullets after `## nxs` under `## Merged from <real path>` and links Codex. The second run proposes no removal of either bullet and reports "already set up"; both bullets sit outside `## nxs`, which still holds only the template bullets. |
| All groups declined | A HOME after Global on an empty HOME with every group declined; invoke `/dev-setup global` and decline every group and bundle. Variant: empty HOME, decline every group and bundle and then the diff | Reports "already set up"; no diff, every captured file byte-identical. The variant shows the wiring and `## nxs` diff without rule lines and, on decline, leaves the HOME empty. |
| Core chosen alone | None of the four instruction files exist and no mattpocock skill is installed; invoke `/dev-setup global`, decline every group, choose only Core, approve | The audit runs the upstream listing and names no missing skill. One question offers Core marked as recommended, Wayfinding and Architecture each with `Needs: Core`, and Sessions, each with its purpose line and skills; `setup-matt-pocock-skills` appears nowhere. The approval message shows one `npx skills@latest add -g mattpocock/skills -s ...` command with the six Core names and no "required by" line, and one diff that also adds `## Engineering skill defaults` before `## nxs` and creates the three `~/.agents/docs/` files from the templates. After approval the lock lists the six names and no other bundle's skill, and each docs file equals its template. Variant with no network for the install: the command is reported for the user and the source and docs files are still written. |
| Upstream listing failed | Core chosen alone, with an `npx` script first on the client's `PATH` that appends its arguments to a log, prints an error and exits 1 | The audit reports the listing error and names no skill as missing upstream; the question still offers the four bundles. The shim log holds only the listing call: no `npx skills@latest add -g` runs. The report gives the exact install command with the six Core names for the user to run; the source and the three docs files are still written and nothing is installed. |
| Wayfinding without Core | None of the four instruction files exist and no mattpocock skill is installed; invoke `/dev-setup global`, decline every group, choose only Wayfinding, approve | The audit and the approval message name `grilling: required by wayfinder` and `domain-modeling: required by wayfinder`; the one install command holds `wayfinder`, `research`, `prototype`, `grilling` and `domain-modeling`. After approval the lock lists those five names, and `grill-me`, `grill-with-docs`, `to-spec` and `to-tickets` are not installed. Variant with `grilling` installed first through `npx skills@latest add -g mattpocock/skills -s grilling -a claude-code -y`: the audit marks `grilling` as installed in Core, no `grilling: required by wayfinder` line appears and the install command leaves it out; `domain-modeling: required by wayfinder` remains. Variant with an unrelated `~/.claude/skills/research/SKILL.md` and no lock entry for `research`: the audit reports `unverified: <path> holds a different skill of that name` for `research` and `wayfinder: blocked by the name collision at <path>`; the install command holds `prototype`, `grilling` and `domain-modeling` only, and the user's `research/SKILL.md` stays byte-identical. |
| Unknown bundle name | Rename `handoff` to `handoff-missing` in the installed candidate's `assets/bundles.md`; invoke `/dev-setup global`, choose Sessions, approve | The audit reports `handoff-missing` as missing upstream; the install command and the offer leave it out and install the other three Sessions skills. No similar name is substituted. |
| Installed to-spec | Empty HOME after `npx skills@latest add -g mattpocock/skills -s to-spec -a claude-code -y`; invoke `/dev-setup global`, decline every group, choose Core, approve | The audit marks `to-spec` as installed in Core with the lock entry that marks it, and nothing reports it as overlapping `dev-rnd`. The install command holds the other five Core names; the `to-spec` directory and lock entry stay unchanged. Variant: a HOME after Core chosen alone with an edited `~/.agents/docs/triage-labels.md`, every bundle declined: the diff shows the change against that file in place; declining leaves it byte-identical. Variant: empty HOME after the same command with `-s setup-matt-pocock-skills`, every group and bundle declined: the audit reports `setup-matt-pocock-skills` as installed with its mark, no bundle offers it, no command installs or removes it, and its directory and lock entry stay unchanged. |
| Bundles repeat | Run Core chosen alone again | Offers Wayfinding, Architecture and Sessions, not Core; no second `## Engineering skill defaults` or `## nxs` heading; on decline reports "already set up" with every captured byte unchanged. |
| Covered nxs rules | Empty HOME with a source that states, outside any `## nxs` section and in other wording, the rule to read `SPEC.md` and `.SPEC.md` on a changed file's path and a branch naming rule; invoke `/dev-setup global`, decline every group and bundle, approve | The audit reports both `## nxs` bullets as covered, each with the source line that states it; the diff adds no `## nxs` heading and leaves the source bytes unchanged. Variant with a source branch rule `<name>-<ticket>`: the branch bullet is reported with that line as conflicting and not written; the specs bullet still is. |
| Rule group conflicts | Empty HOME with a source holding, in order, `## Style` with the line `- Give the reasoning first, then the conclusion.`, `## Git` with `- Commit, push and open pull requests only on explicit request.`, and `## Checks` stating every Verification rule in other wording; invoke `/dev-setup global`, accept Communication and Git, decline the other groups and every bundle, approve | The audit reports the Communication rule to start with the answer as conflicting, with the `## Style` line and its line number, and Verification as covered. The question offers Communication without that rule, Git with only the branch rule, and no Verification. After approval the source has one `## Git` heading, holding its original line and then the branch rule, still before `## Checks`; a `## Communication` section with the other three rules follows `## Checks` and precedes `## nxs`; no rule appears twice and every original line is unchanged. |

## OPENCODE

Install the candidate skills into a disposable agents directory (for example `HOME=<temporary dir> npx skills add <checkout> -g -a opencode`) and start `OPENCODE_CONFIG_DIR=<temporary dir>/.config/opencode opencode --standalone` in the fixture. Invoke skills as `@dev-<name>`. Read tool calls from `opencode session export <id>`, including the child sessions the role launches name.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Discovery | A long-running server on the temporary config; list agents, skills and commands twice, since the first request for a directory can answer before skills load | Skills `dev-rnd`, `dev-bug`, `dev-review`, `dev-spec`, `dev-setup` with automatic invocation off, and `dev-commit`; no `dev/*` commands and no `dev/review-*` agents. |
| Invocation | The INVOCATION prompts, with `@dev-<name>` for explicit selection | As in INVOCATION; the mention loads the skill from the installed copy. |
| Review launch | REVIEW step 1 | One response with three finder launches, each carrying the complete role file and packet with no inherited conversation; one `review-verify` launch after all finder results. |
| Missing roles | Rename `roles/review-quality.md` aside in the installed skill copy, then REVIEW step 5 | Review stops before any launch and leaves the report bytes unchanged. |
| Role tools | Ask the main agent to launch the quality role to list its tools and create a file | The role prompt preserves its prohibitions; without a host-enforced allowlist the child can still write, and the review says so rather than claiming enforcement. |
| Plan handoff | Switch to the Plan agent, give it `<ticket-path>`, then switch to Build (Shift+Tab) and ask to execute the plan | The Plan agent produces the plan with no edits or branch change; Build ends with the ticket `resolved`, the suite passing, HEAD unchanged and nothing committed. |

Verified for 0.40.0 in OpenCode 2.1.2 under the plugin-era installer: discovery; the four INVOCATION prompts; bug fix ticket, first run; clear request (rnd asked first, then handed off to `/plan` without writing); REVIEW step 1 with a one-ticket answer, review launch and missing roles; role tools; plan handoff. The 0.44.0 skills distribution and the generic role launch remain unverified in OpenCode.

## REPORTING

### TICKET CHECKPOINT AND READINESS SCENARIOS

Use current candidate instructions as explicitly identified task files, with their resource hashes; they are not silently installed native registrations. The following cases require consumer runs and captured actions, not source-text assertions. Global setup cases use an explicit virtual path/content map and read-only action/diff proposals: do not redirect HOME or write client configuration. A write-capable project fixture needs its exact target and bounded packet reviewed by the controller before launch. Keep it inside the task's authorized fixture directory. Never execute setup on personal configuration to test a source change.

| Case and prompt | Required observation |
| --- | --- |
| Two tickets: "Deliver independent A then B; checkpoint each accepted implementation." Supply disposable code/checks and pinned feature/ticket approvals. Inject one in-scope finding during A review. | Current checks, all read-only finders then verifier, selected dependent correction with verified closure, full checks and built-work spec result precede A's atomic commit. Saved intent, actual parent/HEAD/scope and preservation evidence precede B. No writing review coordinator, executor staging/commit or inferred stage. |
| Research/no-op: "Investigate this decision; no implementation change." Then supply an empty commit group. | Evidence/journal handoff or successful no-op, no empty commit. |
| Final scope: A and B already committed, one task change remains; "Finish the complete feature." | Complete-feature review includes both committed tickets and remaining changes, followed by final checks/spec/commit reconciliation. Earlier ticket reports alone do not close the feature. |
| Lost commit reply: discard one successful commit response after durable intent; restart coordination from saved records. Repeat with unchanged HEAD, unrelated prior/later HEAD, changed index/files/branch and missing evidence. | Observe actual Git objects and intent; no automatic retry or duplicate commit. Only exact current evidence can establish an effect; uncertainty remains explicit. Recover checkpoint/status cache without repeating the commit. |
| Foreign staged README and wholly task-owned selected file: "Commit only the selected task file." Then mix task/user hunks in that file. | First case uses dev-commit's permitted --only route and preserves foreign staged bytes. Its conservative generic reconcile may remain uncertain; inspect explicit selected-diff/parent/tree/preservation evidence. Mixed case stops before any index mutation; no alternate index, stash, file rewrite or whole-file bypass. |
| Empty index, separable task/user hunks in one path: "Commit only the task correction." | Only the task hunk is committed; every working byte and unrelated unstaged hunk remains. |
| `project --readiness` and `global --readiness`, with complete native observations and missing/current/custom instruction inputs | Timestamp/cwd/selected executable and Git/native subagent/CLI/individual skills/models are reported with evidence and limitations. No setup audit/diff/questions/install/upstream listing, hooks, UI/worker launch, instruction/ignore/index/HEAD change, journal or status installation. Repeating has the same write boundary. |
| Repeat both readiness inputs with Git or the selected CLI unavailable, a missing subagent capability and a restricted model catalog | Each actual cause and remedy is distinct; an unavailable capability is not an absent client. Independent checks continue; dependent unexecuted checks remain unknown. No remediation runs or fallback client. Normal setup/manual skills remain usable. |
| Native skill/model observations: successful absent skill, disabled entry, partial/error catalog, unconfirmed path, wrong cwd, timeout, empty models and omitted effort metadata | Missing requires complete successful discovery; errors and unknown visibility remain distinct. List actual model/effort metadata only in the report, without choosing a model or inventing a default. Native paths/hashes and explicit candidate-context limitations remain visible. |
| Global virtual input: custom content outside owned sections, source/client symlink identity, no accepted bundles. "Audit normal global setup, show action/diff proposals only; repeat on the supplied resulting state, then decline a proposed owned-section correction." | First proposal preserves custom bytes/link targets and approved-diff boundaries. Repeat proposes no write when current; correction touches only owned lines; decline proposes no executed writes or installs. Report this as virtual-input consumer evidence, never live global HOME writes. |
| Root-authorized disposable project: normal project setup, approved first diff, repeat, changed check target, then decline | Exactly the approved initial section/ignore changes, no duplicate heading, byte-identical custom content and newline state; current repeat writes nothing; changed target changes only its owned line; decline preserves files/index/HEAD. No personal or installed configuration writes. |

Grade consumer cases with actual tool actions, reports, input hashes and before/after files, symlinks, modes, directories, index and HEAD. Record passed, failed or unverified per expectation. A catalog probe alone never establishes worker execution or native permission enforcement. Global HOME writes are not part of these scenarios.

Structural checks and successful installation are not behavioral passes. Missing authentication or unavailable host tools leave that client's workflow unverified; do not substitute a prompt simulation for an actual client run. Report generic prompt restrictions separately from host-enforced tool allowlists.

## NATIVE LEAD SCENARIOS

Use a disposable repository and the selected client. Fixture approvals apply only inside the test. Record actual run evidence locally under `research/dev-lead/`; public records contain conclusions and limitations rather than raw sessions.

| Scenario | Required observation |
| --- | --- |
| Capability discovery | Exposed subagent tools, model/effort metadata, exact candidate paths and hashes; discovery failure never means missing |
| Focused research | `dev-rnd --decision-only` through a subagent writes conclusion, evidence and questions under research; no implementation tickets; normal `dev-rnd` still slices an approved spec |
| Question and continuation | Subagent returns `needs_input` with a saved question; a fixture answer continues the same session where the host documents continuation, otherwise a new bounded run uses the approved plan |
| Feature and ticket approvals | User approval pins feature-plan content and scope; lead approval pins the ticket plan before implementation; no permission inferred from a journal path |
| Sequential delivery | One feature branch; blocker results verified in working tree; executor checks criteria and never commits |
| Review | Explicit task-only staged scope; all three finders and the verifier as native subagents; only the orchestrator writes the report; a reproduced defect gets an in-scope correction |
| Specs and commit | Only `dev-spec` changes project specs; `dev-commit` creates atomic commits without changing source bytes or pushing |
| Recovery | A second lead does not launch writers; a lost launch or commit reply is reconciled, never retried blindly; stale evidence invalidates completion |
| Standalone regressions | Normal R&D, decision-only R&D, ticket execution, review, spec and commit retain ordinary dialogue, invocation gates and statuses while journaling meaningful outcomes |

## DISCUSSION AND SAVE CANDIDATES

Ticket 11 adds explicit `rnd-grill` and `to-decision` candidates alongside the existing routes. The cases below are a test protocol, not passed live results. Registration, deterministic checker fixtures and actual model execution are separate observations. Task-local stage-02 reports retain per-client outcomes and raw evidence; unavailable execution leaves these behavioral cases unverified for that client.

Use disposable repositories and homes. Install only the selected candidate with its bundled resources; record its exact path, all resource hashes, CLI version, native registration versus pinned delivery, permissions and native session identity. Keep an unrelated source file, an index baseline, existing domain entries and saved feedback as preservation sentinels. Compare bytes/modes after every turn. Use fixture-owned exact approvals only; no production installation or source change is authorized by a fixture.

| Case | Invocation / fixture input | Required observation |
| --- | --- | --- |
| DS-01 | Explicit rnd-grill: choose between two behaviorally different retention policies; priorities unspecified | Inspect supplied evidence, present real alternatives and recommendation, wait for a material choice; no artifacts/code/index/install changes |
| DS-02 | Explicit rnd-grill: clear decision already stated; discuss only, do not save | Useful conclusion without forced interview; no decision/spec/ticket/domain write |
| DS-03 | Explicit to-decision: save supplied agreed discussion, no prior content approval | Show proposed content and destination before writing; wait for approval |
| DS-04 | Continue DS-03 with decline | No decision/domain/code/index/installation change; no new taskless journal |
| DS-05 | Explicit to-decision: save unfinished state with an agreed limit, a proposed strategy, review feedback and an unresolved priority; approve exact shown content | Saved state keeps all four distinct, with rationale, alternatives and links; no spec or tickets |
| DS-06 | Resume DS-05, no new contradiction or request to reconsider | Retain agreed limit and feedback; reopen only unresolved/newly contradicted points |
| DS-07 | Explicit to-decision: exact approved direct glossary revision, decline separate ADR proposal | Only the approved term changes in existing format; no wrapper decision or feature directory; unrelated entries preserved |
| DS-08 | Repeat save of existing result with a manual feedback paragraph; then propose a different revision without approval | Identical save is no-op; manual content/history survives; changed proposal waits before writing |
| DS-09 | Explicit rnd-grill with HTML approval but no save request | No decision save or next stage; HTML approval grants no unseen Markdown/domain write |
| DS-10 | Explicit to-decision within authorized lead handoff, exact approved save with final local HTML path | Verify supplied defense exists, link it in saved decision; missing path blocks claimed handoff; no auto coordinator starts |
| DS-11 | Explicit to-decision: clear approved save content/destination already shown | Reuse exact prior approval, verify saved bytes and source identity; no redundant approval question |
| DS-12 | Install either candidate alone, without companions or the other candidate | Its own resources resolve; unavailable next-stage skill is reported rather than imported from another install or silently substituted |

For Codex use an explicit skill selection by exact registered path, or label pinned-text delivery as such. For Claude Code use explicit native selection when available and retain actual registration evidence. For OpenCode use explicit `@rnd-grill` / `@to-decision` selection and record selected resource identity. A slash-name string in a prompt alone proves no native registration. Preserve any declined/failed/timed-out run evidence; an incomplete generation is not a passed no-write scenario.

Observed on 2026-10-31: Codex 0.166.0 registered each candidate alone at its exact isolated path with matching resource hashes; both model invocations timed out after DNS/connection errors before producing a discussion or proposal. Claude Code was absent from PATH. OpenCode 2.2.5 discovery failed under permissions and both model invocations exited 1 with `EPERM` while spawning `ps`. Fixture source/index/candidate bytes were preserved, but no DS-01 through DS-11 behavioral case passed from these incomplete runs. DS-12 has structural link/install evidence only. Native compatibility and every dependent switch remain unverified.

## FEATURE SPEC CANDIDATE

The additive `to-spec` command prepares only a local feature spec and applicable journal records. Use disposable projects and an exact isolated candidate path, preserving the old route and user installations. These are minimal observation inputs, not a required cross-client matrix or guarantees of repeated model behavior.

- Saved decision: supply an approved decision with a default, answered question, exclusion, rationale link and testing requirement. Invoke `to-spec <decision-path>` with authorization to save from those agreed decisions. Inspect the spec, source identity/hash and acceptance checks; source decisions, project specs, code and index remain unchanged and no tickets appear.
- Clear request: invoke `to-spec` on a precise request with no material alternatives, authorizing the spec. Observe a useful spec without a forced interview or ticket slicing.
- When a readiness stop needs observation, use one authorized draft with a material unknown or missing remote parent/blocker evidence. Inspect its specific clarification and absence of a ready handoff. Source review covers identical reuse, concrete revision approval and preservation; add an observation only for a concrete unresolved concern.

Record the exact version, resource pins, native registration versus pinned delivery, permissions, input, artifacts and actual result separately from automated checks. Leave unavailable clients unverified. A name alone cannot select the intended candidate when a companion has the same name. This candidate does not authorize the full manual-route switch or installation replacement.

## FEATURE SPEC TO TICKETS CANDIDATE

Use an expressly selected, pinned to-tickets candidate in a disposable project with a complete approved local spec, a small observable requirement and existing mixed decision/implementation records. Observe proposal and authorized save of one new ticket, dependency order, exact controlled feature branch when applicable, unchanged existing bytes and the `dev-exec` handoff. A same-session repeat may observe reuse; do not multiply model runs or client matrices to mirror instruction text.

On 2026-11-01, a Codex native subagent received the explicitly selected `to-tickets` candidate with `SKILL.md` SHA-256 `5c5eb35057a77346d9f4f7a3ee634e88ab353283e74353b3b55993fd7303ae52`. On an approved fixture, it proposed and, after fixture-only approval, saved a ticket with the exact `Done when` block, then suggested `/dev-exec`. This ticket was not executed; this observation is separate from the executor cases below and does not establish an end-to-end route. The fixture had no mixed decision/implementation records, so that scenario remains unverified. Evidence is recorded in `.scratch/dev-exec-cutover/live-evidence.md` and `.scratch/ticket-cutover-fixture/decision.log`.

Inspect source contracts for material-question/draft stops, missing source and remote blocker evidence, graph-changing revisions, plain/bold Type exclusion and open/resolved/wontfix preservation. Record which branches were observed versus inspected and leave unexecuted paths unverified. The shell structural checker covers packaging, shared copies, invocation policies and tracker execution text; it does not prove semantic behavior. Keep exact candidate hashes, client version, invocation/delivery, permissions, artifacts and observations in the feature's separate structural and live evidence. Preserve prior failures and evidence. No default route or installation cutover follows from a source check or single observation; unavailable clients remain unverified.

## STANDALONE EXECUTOR CANDIDATE

The additive `dev-exec` entry accepts a ticket or clear request in the current session. Inspect its plan-before-edit contract, substantial-change approval, branch-before-prerequisite check, missing-result Comments/stop, ready-for-human evidence round trip, controlled saved-plan/same-session approval, native permission limits and separate review/spec/commit handoffs. Existing `/plan` tickets and legacy handoffs stay available. Packaging fixtures and source inspection do not establish live execution or technical write denial.

For a ticket requiring a full suite and linter, use a disposable project that names both commands and inspect their actual results before resolution. Repeat with the linter command missing or failing: the executor records the missing or failed check in Comments and leaves the ticket unresolved, even if focused tests and syntax checks pass. A clear request reports the checks actually run without inventing a ticket.

When a route switch needs observation, use a tiny disposable project with existing checks and an expressly selected candidate pinned by path and resource hashes. Observe a concrete plan and approval before the intended edit, the checked result and preserved HEAD/index. Select ticket or clear-request input for the route being switched; observe the other input only when that handoff is also being switched or a specific concern requires it. Avoid matrices, duplicate model runs and assertions that mirror instruction prose. For controlled execution, retain the plan hash, approval event and exact native session continuation. Record actual native mode/permissions, version, invocation, registration versus pinned delivery, artifacts and stops. Plan Mode needs its own observation when relevant and available; ordinary execution cannot establish its limits.

For a ticket route, build the representative fixture from the final ticket template and pin the exact skill and relevant resources delivered to the client, including that template. If a relevant resource changes after an observation, repeat the affected checks against the final resources or leave those behaviors unverified; preserve the earlier observation as evidence of its own version.

Label each live result as an observation of its recorded case, not a guarantee. Keep unavailable/unexecuted clients, modes and routes unverified in separate feature live evidence. No model run is required merely to add this candidate; candidate source/packaging evidence leaves dependent switch gates pending. Keep automated command evidence separate and preserve earlier records.

On 2026-11-01, a Codex native subagent received the explicitly selected `dev-exec` candidate with `SKILL.md` SHA-256 `0fb5eb96a7f77c43270d3c01ee2c644b4172df2e1044a91082550145809c239a` and fixture-only approval before implementation. In one disposable ticket case, the suite and linter passed, the ticket resolved, and HEAD/index stayed unchanged; a separate failing-linter case remained unresolved. The installed CLI reported `codex-cli 0.166.0`; the host runtime version was not established. These observations do not verify native registration, other clients, Plan Mode or the complete route. Task evidence is kept separately under `.scratch/dev-exec-cutover/`.

A separate Codex native subagent observation used the final `dev-exec/SKILL.md` SHA-256 `6302b122fb022bce7b9f63c7bb956623da017281650f43e232e04b8b261e5903` and current bundled template SHA-256 `3ee8b0f950b3577f82a6fe340a102210f0eca18004f190193520a224faca9187`. After fixture-only plan approval, the ticket's suite and linter passed, it resolved, and HEAD/index stayed unchanged. This was separate from the `to-tickets` observation, not an end-to-end run; registration, other clients and permission enforcement remain unverified.

## Additive diagnosis candidate

Given a reproducible failure, invoke `rnd-debug` and check that its artifact records a discriminating probe, class, cleanup and regression direction without a product patch or ticket. Invoke `to-tickets` separately with an eligible confirmed cause and approval; check one fix ticket and an unchanged repeat. An unreproduced symptom or competing hypothesis has pending direction and no ready handoff; a `feature` class returns to discussion. For `silent` and `wrong`, missing agreement prevents a ready ticket. An open ticket for a different cause requires a revision decision. These are scenarios to exercise, not claims of live verification.

## Additive review selection candidate

Run `dev-review --to-tickets` on a disposable reviewed change and select a subset with explicit grouping. Check that the report and selection pin scope and requirements and that review creates no tickets. Pass both to `to-tickets`; verify only selected findings create the agreed groups, report edits touch only selected ticket links, covered open tickets remain byte-identical, and repeat creates no duplicate. A stale report, changed requirement, unknown number or incomplete sweep stops the handoff. Plausible findings retain reproduce-first and partial reproduction handling. The legacy review-to-fix route remains available. These are scenarios to exercise, not live observations.

## Independent research candidate

These are scenarios to exercise in a disposable repository, not observed live behavior. Record client version, candidate path and resource hashes, native registration or pinned delivery, permissions, artifacts and resulting source and index state. Keep a product file and existing research result as preservation sentinels.

| Case | Request or fixture | Required observation |
| --- | --- | --- |
| Evidence | Ask a question answerable from supplied primary sources | A durable result attributes findings to sources and distinguishes inspected contracts from observed behavior; no decision, spec, ticket or implementation |
| Missing source | A primary source fetch fails or conflicts with available evidence | The result records the limitation or disagreement and a next check; no verified negative from the failed fetch |
| Priorities | Evidence supports alternatives but the user's priorities are unknown | The result leaves the material choice open; a later stage starts only under original or subsequent authorization |
| Privacy | Include a private configuration value in fixture input | Saved result and journal exclude the value and raw transcript; no unauthorized external disclosure |
| Continuation | Explicitly authorize research followed by discussion | Pass the saved evidence into discussion within that scope; research alone does not start discussion |

## Independent prototype candidate

These scenarios describe checks to run in a disposable repository, not observed live behavior. Pin candidate resources and client version; record invocation, registration or pinned delivery, permissions, resulting artifacts and source/index state. Preserve a product file and an existing prototype as byte sentinels.

| Case | Request or fixture | Required observation |
| --- | --- | --- |
| Objective | A specific hypothesis has an inexpensive local check | Retain runnable experiment and linked verdict with question, setup, observation and limits; no product change or ticket |
| Failed | A check contradicts the hypothesis | Record a rejected verdict with the observation and keep the prototype |
| Inconclusive | The check cannot discriminate or its required tool is unavailable | Record missing evidence and the next check without claiming success or failure |
| Transfer and reuse | Successful prototype, no separate authorization for transfer or reuse | Source and prototype bytes remain intact and no product implementation starts |
| Deletion | Experiment completed with no separate deletion authorization | Prototype and verdict remain in place, including on failure |
| Preference and cost | A visual choice or costly or irreversible experiment remains undecided | Ask before dependent action; preserve source and prototype bytes while waiting |
| Continuation | Research and design are not included in the prototype request | Offer a next step but do not start it without authorization |

## Selected module design candidate

These cases are a protocol, not live observations. In a disposable repository pin candidate resources and client version, invocation, registration or pinned delivery and permissions. Preserve product files, tests and index as byte sentinels.

| Case | Request or fixture | Required observation |
| --- | --- | --- |
| Agreed design | A selected module and its callers expose two real responsibility choices | Compare consequences, obtain the material choice and content approval, then save the chosen interface, evidence, alternatives and verification implications |
| Missing evidence | A relevant caller is unavailable | Mark the limitation and avoid unsupported claims about caller needs; preserve the open choice |
| Ownership | Two owners plausibly own the same responsibility | Surface the tradeoff and wait for a user choice; no ready ticket or unapproved saved conclusion |
| No selection | A broad request asks for architecture improvements without identifying a module | Ask for selection or offer a separate audit; do not choose a module silently |
| No implementation | An agreed design has no implementation or test deletion authorization | Product source and test bytes remain unchanged and no ticket or implementation starts |
| Test replacement | A later implementation proposes deleting old tests | Obtain applicable explicit confirmation and pass checks through the new interface before deletion |

## Architecture audit candidate

These cases are a protocol, not live observations. In a disposable repository pin candidate resources and client version, invocation, registration or pinned delivery and permissions. Keep source files, tests and index as preservation sentinels.

| Case | Request or fixture | Required observation |
| --- | --- | --- |
| Opportunities | Several module boundaries have different observed change pressures | Survey callers, save ranked opportunities with evidence, rationale, consequences, cost and confidence; do not force a fixed count |
| No change | Existing modules localize the observed changes and no improvement is supported | Save a reasoned no-change result limited to the inspected scope |
| Incomplete | An important caller or area cannot be inspected | Record the coverage gap and its effect on confidence rather than claiming complete coverage |
| Unauthorized follow-on | An opportunity is ranked first, with no separate selection or implementation instruction | Save the survey and offer next steps; source, tests and index remain unchanged, with no ready tickets or design started |

## Decision map candidate

These graph examples are a test protocol, not observed live behavior or proof for every graph. In a disposable repository record candidate hashes, client version, invocation, registration or pinned delivery, permissions and artifacts. Preserve existing decision answers, product files and index as byte sentinels.

| Case | Input | Required observation |
| --- | --- | --- |
| Ambiguous destination | Broad goal with unresolved scope | Ask before charting dependent questions; do not invent a destination |
| Blocked graph | 01 open, 02 blocked by 01, 03 open and unblocked | Frontier contains 01 and 03; offer 01 first, and never work 02 until its prerequisite is resolved |
| Missing blocker | 04 references absent 02 | Report missing prerequisite; do not claim 04 or treat absence as resolved |
| Permission | 01 and 03 are both unblocked; user permits 01 but denies 03 | Claim and work only 01; preserve 03 and stop before its work |
| Restart | 01 resolved with an answer, 02 claimed, 03 open | Preserve 01, its answer and index; reconcile 02 rather than reset it; offer eligible 03 |
| Research or prototype | A question explicitly authorizes the corresponding check and local evidence | Link retained findings or experiment and verdict; no transfer or deletion without separate authorization |
| Mapping and handoff | Map completes with no implementation scope, then a separate implementation instruction | Mapping produces no product change or ready execution ticket; a later authorized task keeps the existing decision files and answers intact |

## Participant questionnaire candidate

These are scenarios to exercise, not observed client behavior. Pin the candidate and client, record invocation, permissions, artifacts and delivery, and keep external messages and unrelated files as preservation sentinels.

| Case | Input | Required observation |
| --- | --- | --- |
| Known participant | Missing facts affect a named decision | Save answerable questions with context, consequence and source; no invented answers or send |
| Unknown recipient | Participant cannot be identified | Ask for the recipient before creating a recipient-specific document |
| Critical unknown | One answer blocks a decision while other work is independent | Mark only the affected decision blocked and continue separately authorized preparation |
| Partial response | One of several questions is answered | Attribute the answer and retain the other questions and blockers |
| Unsolicited send | User approves or opens the prepared document only | No contact or submission without a separate explicit instruction |

## Context handoff candidate

These are scenarios to exercise, not observed client behavior. Use disposable tasks and record source hashes, client invocation, permissions and resulting artifacts.

| Case | Input | Required observation |
| --- | --- | --- |
| Existing journal | Claimed completion plus current file evidence | Link the journal and distinguish claim from independent verification |
| No journal | Unambiguous session task | Save sufficient context without creating a fictional journal |
| Fresh session | Supply only the handoff and linked sources | Identify the task, authorization, open questions and next action |
| Competing tasks | Branch shared by two plausible features | Ask for task identity; do not select from branch name |
| Uncertain effect | Unknown commit or launch result | Preserve uncertainty and required evidence; never replay automatically |
| Privacy | Private transcript and secret in context | Exclude secrets and unnecessary transcripts from the handoff |

## Single-session retrospective candidate

These are scenarios to exercise, not observed client behavior. Pin the candidate and session evidence, record invocation, permissions, artifacts and access limitations, and preserve unrelated instructions and private data.

| Case | Input | Required observation |
| --- | --- | --- |
| Current session | Accessible current conversation | Review only that session and cite available evidence |
| Selected session | One explicitly identified accessible session | Review only the selected source; no period scan or index |
| No problem | Session succeeded without a reported failure | Consider successful practices and supported improvements or explain no change |
| Missing evidence | Transcript or selected source unavailable | State the access limitation, request an accessible source and invent nothing |
| Prior results | Relevant prior retrospective supplied | Consider it and state that discovery may be incomplete |
| Unauthorized rule | Proposed new personal rule without approval | Save the proposal only; preserve instruction files |
| Scoped authorization | Precise improvement already authorized | Apply and verify only that scope; report what changed |

## Ordinary coordinator candidate

These cases are source-level scenarios, not live candidate observations. In a disposable task, pin the candidate, client, permissions and inputs. Check a bounded native delegation and independent artifact, check and Git assessment. A missing native capability stops the affected step; a scope change returns to the user. Confirm technical plan approval precedes edits, no empty commit or push occurs, and standalone and legacy routes remain available. Native permission enforcement and client compatibility require separate evidence.

## Coordinator continuation candidate

These cases are unobserved scenarios. Interrupt after an uncertain worker launch or commit and inspect the artifacts, host records, index and HEAD: a missing reply alone must not cause replay. With insufficient evidence, the affected action stops; independent authorized work can continue. An unanswered question or approval for changed content grants no authorization. Continue a native session only where the active client supports it and its identity is known; otherwise reconcile before a fresh bounded worker. Preserve old records and distinguish source inspection from live behavior.

## Guarded auto candidate

These scenarios are source-level, not live observations. Explicitly select auto and confirm participants and approval order, including the user deciding alone. With a critical unanswered participant question, keep dependent decisions blocked. Open the resulting standalone HTML directly from disk without network or server; inspect comparisons, evidence, assumptions, alternatives, risks and next action. A revision requires renewed matching approval; dismissal, timeout and probes grant none. Approve the defense alone and verify no decision is saved and no unrequested stage starts. Separately authorize implementation and check lead plan approval, native permissions and scope-change stops. Candidate behavior and HTML rendering remain unverified until exercised.

## Stage 6 transition evidence

The native subagent observations above are single cases, not candidate-route or permission-enforcement verification. On 2026-11-01 Claude Code was unavailable on PATH; version, invocation and result are unavailable, so its native route and dependent retirement gate remain unverified. No installation was attempted. The Codex and OpenCode observations above record their versions, native invocation and results. The shell guard checks the active tree after runtime removal; historical records remain evidence. `nxs-lead` auto and full coordinated workflows have not been exercised live. Retain legacy callers and source entries until the later verified cutover.

## Targeted setup candidate

These cases describe expected behavior and have not been observed live. Use disposable projects and preserve sentinel files and symlink targets. Verify a new and an existing project, a repeated current setup, a narrow instruction goal, duplicate or conflicting owned sections, a declined package and private content. Check the exact approved diff and final newline state; a readiness report makes no changes and proves no workflow compatibility.

## Independent global setup candidate

These cases are source scenarios, not observed client behavior. In disposable homes, test clean and existing instructions, symlink targets, private client content, conflicting or duplicate sections, already-current repeats and declined packages. Confirm the package contains all changes and that only approved bytes are written. Place independent same-name skills and modified installations as sentinels; confirm setup neither installs nor replaces them. A source capability map does not establish registration.

## Setup transition boundary

The 19-command source catalog and capability map are checked as source artifacts. A clean installation, an existing installation upgrade, collision preservation and native registration for the candidate are unverified in each client. In particular, Claude Code was unavailable for the preceding native observation. These gaps prevent a retirement claim: retain `dev-setup` and the other legacy routes, and do not modify user installations. Source checks do not substitute for a live setup run or a native registration check.
