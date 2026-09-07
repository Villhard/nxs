# dev

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and one multi-agent review gate over the finished branch.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/dev:plan`, `/dev:exec`, `/dev:review`), each command is self-contained, and the human stays in the loop - you approve the plan before execution and the review runs before you push.

## Quickstart

One ticket through the loop:

```
/dev:rnd add rate limiting to the public API   # a spec plus the tickets cut from it, under .scratch/
/dev:plan                                      # plan the next ticket into sequenced tasks
/dev:exec                                      # run one ticket to the end, one commit per task
/dev:review                                    # review the branch and write review.md
/dev:fix                                       # apply the saved findings and record the outcome
```

## Commands

Seven flat `/dev:<name>` commands:

| command | when to use |
| --- | --- |
| `rnd` | Shape a fuzzy request, feature idea, or open question into a spec and the tickets cut from it - the entry point for new work. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the entry point for a bug report. |
| `plan` | Decompose one ticket into sequenced tasks with checkboxes, written into the ticket itself, then self-check the plan against the repository. |
| `exec` | Take the next unblocked ticket, execute its tasks and write the code, committing each finished task and marking the ticket resolved. |
| `review` | Review the diff and write `review.md`, changing no code, index or commits. Pass a ticket path or feature directory to name requirements. Add `quick` for two reviewers with wider duties; otherwise five, or a direct pass for a trivial diff. |
| `fix` | Read the saved report, verify its currency and open findings, apply the confirmed fixes, commit code alone and record the outcome. Critical or major fixes get a two-agent re-check. |
| `commit` | Commit the current working changes, split into atomic commits - for edits made outside `exec`. |

## Model

Two tiers, nothing in between:

1. Global `~/.claude/CLAUDE.md` - always-on rules (output language, style, safety). Hand-authored by you, NOT shipped by this plugin (see Setup). The commands defer output style and the safety rules on secrets and destructive operations to it, so they fire even when no skill loads.
2. The seven commands above. Each is self-contained: no shared background skills, no `reference/` files, no cross-skill injection. A rule lives in exactly one file.

Commands hand work to the next one through five minimal contracts: `plan` reads a ticket by its `**What to build:**` line and its acceptance criteria, reads a spec by its `## Implementation Decisions` and `## Testing Decisions` headings, reads a root cause by its `## Root cause` and `## Fix direction` headings, and `exec` finds the work in a ticket by two structural tokens - a `### Task N:` heading and `- [ ]` checkboxes - plus the optional `## Conventions` section it hands to every worker, and it drives the ticket's `**Status:**` and `**Blocked by:**` lines with execution history in `## Comments`. The fifth contract is `review -> fix`: the report carries the reviewed scope, mode, pinned requirements, findings, dismissals and follow-ups. Nothing beyond those contracts crosses between them.

Six of the seven commands carry `disable-model-invocation: true`, so they run only when you type them. The workflow is yours to pick, not the model's to guess, and the plugin stays out of the way when you drive a session by hand or through another planning tool. `commit` is the exception: it fires on its own trigger, since "commit this" is a request to commit rather than a request for a command.

Agents (`agents/*.md`) - one write-capable `worker` used by `/dev:exec` and `/dev:fix`, the only agent that writes, plus five read-only reviewers used by `/dev:review`:

| agent | lens |
| --- | --- |
| `review-quality` | bugs, edge cases, error handling, leaks, races, security skim |
| `review-implementation` | goal reached, wiring, completeness, scope creep |
| `review-testing` | coverage over the changed code, fake tests, test quality |
| `review-simplification` | over-engineering this branch introduces |
| `review-documentation` | docs the change needs or made stale, ticket checkboxes |

## Features and tickets

One feature is one directory under `.scratch/<feature-slug>/` in the current repository: a feature document and the tickets cut from it. One ticket is one whole unit of work - a vertical slice, sized to a single fresh context window. With a tracker key the directory carries it, `<KEY>-<slug>/`, and the key names the directory, never the files inside it.

| command | writes | where |
| --- | --- | --- |
| `rnd` | spec, plus one ticket per slice | `spec.md`, `issues/NN-<slug>.md` |
| `bug` | root cause | `root-cause.md` |
| `plan` | `## Conventions` and `## Implementation`, appended to one ticket | `issues/NN-<slug>.md` |
| `exec` | the ticket's status, checkboxes and execution notes in Comments | `issues/NN-<slug>.md` |
| `review` | report | `review.md` (fallback below) |
| `fix` | finding results and fix outcome | the same `review.md` |

`review` writes `.scratch/<feature-slug>/review.md` for one matching feature, or `.scratch/reviews/<branch-slug>/review.md` when there is none. Several matching features require a choice. `fix` updates that same report after committing code as `fix: address review findings`; the report stays outside the commit, even when tracked. `commit` writes no artifact.

Run `/dev:review quick` to request two reviewers explicitly. The report says `quick`; it is not a full review gate. Quality also covers tests and implementation also covers docs and simplification. A fix re-check uses their original bounds, with critical and major findings only.

A repeated review asks before sweeping a current, complete, unfixed report again. `fix` stops when the scope or requirements changed, the sweep or an earlier fix is unfinished, or unrelated worktree changes would enter the fix. Run review again after a stale or unfinished report. An already-applied report runs no worker; an empty report or findings all dropped by verification make no commit. Each new sweep overwrites the report and carries open follow-ups forward as not re-verified.

A `- [ ]` line means two things inside a ticket, and its position decides which. Above `## Implementation` it is an acceptance criterion, written when the ticket is created and flipped once by `exec` after the last task is green. Inside a `### Task N:` section it is a unit of work, written by `plan` and flipped by `exec` as that task passes.

The `**Status:**` line carries one of seven values: `needs-triage`, `needs-info`, `ready-for-agent`, `claimed`, `ready-for-human`, `resolved`, `wontfix`. Two commands write it, each its own transitions. `plan` writes `needs-info` while an open `[NEEDS CLARIFICATION: ...]` marker sits in the ticket and `ready-for-agent` once the last one is answered. `exec` writes the execution transitions - `claimed` when it takes the ticket, `ready-for-human` or `needs-info` when it stops on something it cannot clear, `resolved` when every task is green and every criterion verified. `resolved` records verified implementation; execution notes and git show whether its close was committed. It does not claim a review happened. `wontfix` is yours to write by hand, and it is the only manual state act left.

`exec` picks the next ticket itself: numeric order, `ready-for-agent`, with every number on its `**Blocked by:**` line already `resolved` and its close finished. Interrupted work takes priority. Pass a ticket path to override; a fully completed `resolved` ticket passed this way is reopened, after `exec` names which criteria and task checkboxes it reopens and you confirm. One ticket per run.

Inside a ticket, `exec` hands each worker the task plus the acceptance criteria that task serves, checks the task's diff against its checkboxes before committing it, and runs the full suite and the linter once itself at the close. A worker's own test run is not repeated when it was the exact command the task names, run after the worker's last edit.

Worker decisions and deviations that affect later work are saved with their reasons in the ticket's Comments. Each subsequent worker receives the notes relevant to its task. The same section records the current task, git mode, starting commit, verification results and remaining step.

After an interruption, invoke `/dev:exec` again. The orchestrator checks the stopping point once, before selecting more work; workers do not check previous tasks. Checked boxes with uncommitted code can resume at validation or commit, and an existing task commit is not repeated. An interrupted final close is finished without reopening completed criteria. The recorded `no commits` mode survives a new session. Foreign changes or uncertain ownership stop automatic recovery, and old tickets without notes resume only when their state is unambiguous.

This is the local-markdown layout of the `.scratch/` issue tracker, so the files stay readable by any toolchain that speaks it, and this plugin writes them with nothing else installed. It implements that layout only - no `gh` or `glab` dependency - and in a repository configured for GitHub or GitLab it names the tracker and asks before writing locally. Do not re-run an external slicing skill over a feature whose tickets already carry `## Implementation`: it rewrites those files and every plan in them is gone.

These are local working files - keep `.scratch/` out of git if you do not want them committed, and `exec` will commit the code alone and say so once when they are ignored.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest (name: dev)
skills/
  <name>/SKILL.md      # implements the /dev:<name> command, self-contained
agents/
  worker.md            # the single write-capable agent
  review-*.md          # five read-only reviewers
```

## Setup

1. Install the plugin:
   ```
   claude plugin marketplace add Villhard/nxs
   claude plugin install dev@nxs
   ```

2. **Global rules (your own)**. The commands defer output language and style to your global `~/.claude/CLAUDE.md`, along with secret safety and destructive-op confirmation. The plugin does not ship a block (plugins cannot write `~/.claude/CLAUDE.md`), so set up your own. Without them the commands still run, but they lose those delegated protections and fall back to the default output style.

3. **Optional - permissions**. The skills prefer `rg` / `fd` / `jq`. Allow them in `~/.claude/settings.json` to avoid prompts. Plugins cannot ship permissions.

4. Restart Claude Code so the plugin snapshot and the global rules load.

## Dev loop

The installed plugin reads a cached snapshot, not the live repo, so a session picks up repo edits only after the snapshot is refreshed and the session restarts.

```
# simplest - reinstall (no version bump)
claude plugin uninstall dev@nxs && claude plugin install dev@nxs

# or version-based
# bump "version" in plugins/dev/.claude-plugin/plugin.json, then:
claude plugin marketplace update nxs
claude plugin update dev@nxs
```

A restart is required either way. `claude plugin validate --strict plugins/dev`, run from the repository root, checks the manifest and skills before install.
