# dev

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and one multi-agent review gate over the finished branch.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/dev:plan`, `/dev:exec`, `/dev:review`), each command is self-contained, and the human stays in the loop - you approve the plan before execution and the review runs before you push.

## Quickstart

One ticket through the loop:

```
/dev:rnd add rate limiting to the public API   # a spec plus the tickets cut from it, under .scratch/
/dev:plan                                      # plan the next ticket into sequenced tasks
/dev:exec                                      # run one ticket to the end, one commit per task
/dev:review                                    # five reviewers over the branch, findings reported
/dev:review fix                                # same, and the confirmed findings get fixed
```

## Commands

Six flat `/dev:<name>` commands:

| command | when to use |
| --- | --- |
| `rnd` | Shape a fuzzy request, feature idea, or open question into a spec and the tickets cut from it - the entry point for new work. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the entry point for a bug report. |
| `plan` | Decompose one ticket into sequenced tasks with checkboxes, written into the ticket itself, then self-check the plan against the repository. |
| `exec` | Take the next unblocked ticket, execute its tasks and write the code, committing each finished task and marking the ticket resolved. |
| `review` | Review the branch with five parallel agents, verify every finding, and report it. Writes nothing unless you add `fix`, which applies the confirmed findings and re-checks its own work with two agents. |
| `commit` | Commit the current working changes, split into atomic commits - for edits made outside `exec`. |

## Model

Two tiers, nothing in between:

1. Global `~/.claude/CLAUDE.md` - always-on rules (output language, style, safety). Hand-authored by you, NOT shipped by this plugin (see Setup). The commands defer output style and the safety rules on secrets and destructive operations to it, so they fire even when no skill loads.
2. The six commands above. Each is self-contained: no shared background skills, no `reference/` files, no cross-skill injection. A rule lives in exactly one file.

Commands hand work to the next one through four minimal contracts: `plan` reads a ticket by its `**What to build:**` line and its acceptance criteria, reads a spec by its `## Implementation Decisions` and `## Testing Decisions` headings, reads a root cause by its `## Root cause` and `## Fix direction` headings, and `exec` finds the work in a ticket by two structural tokens - a `### Task N:` heading and `- [ ]` checkboxes - plus the optional `## Conventions` section it hands to every worker, and it drives the ticket's `**Status:**` and `**Blocked by:**` lines. Nothing beyond that crosses between them.

Five of the six commands carry `disable-model-invocation: true`, so they run only when you type them. The workflow is yours to pick, not the model's to guess, and the plugin stays out of the way when you drive a session by hand or through another planning tool. `commit` is the exception: it fires on its own trigger, since "commit this" is a request to commit rather than a request for a command.

Agents (`agents/*.md`) - one write-capable `worker` used by `/dev:exec`, the only agent that writes, plus five read-only reviewers used by `/dev:review`:

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
| `exec` | the ticket's `**Status:**` line and its checkboxes | `issues/NN-<slug>.md` |

`review` and `commit` write nothing here - what they produce lands in git. `review` leaves nothing at all unless you ask for `fix`, and then commits as `fix: address review findings`.

A `- [ ]` line means two things inside a ticket, and its position decides which. Above `## Implementation` it is an acceptance criterion, written when the ticket is created and flipped once by `exec` after the last task is green. Inside a `### Task N:` section it is a unit of work, written by `plan` and flipped by `exec` as that task passes.

The `**Status:**` line carries one of seven values: `needs-triage`, `needs-info`, `ready-for-agent`, `claimed`, `ready-for-human`, `resolved`, `wontfix`. After the ticket is created `exec` is the only command that writes it - `claimed` when it takes the ticket, `resolved` when every task is green and every criterion verified. `resolved` says the tasks ran green at that commit; it does not claim a review happened. `wontfix` is yours to write by hand, and it is the only manual state act left.

`exec` picks the next ticket itself: numeric order, `ready-for-agent`, with every number on its `**Blocked by:**` line already `resolved`. Pass a ticket path to override. One ticket per run.

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
