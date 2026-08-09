# dev

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and one multi-agent review gate over the finished branch.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/dev:plan`, `/dev:exec`, `/dev:review`), each command is self-contained, and the human stays in the loop - you approve the plan before execution and the review runs before you push.

## Quickstart

One story through the loop:

```
/dev:rnd add rate limiting to the public API   # shape a fuzzy request into a plan-ready brief
/dev:plan                                      # turn the brief into sequenced tasks
/dev:exec                                      # run the plan to the end, one commit per task
/dev:review                                    # five reviewers over the branch, findings reported
/dev:review fix                                # same, and the confirmed findings get fixed
```

## Commands

Six flat `/dev:<name>` commands:

| command | when to use |
| --- | --- |
| `rnd` | Think a fuzzy request, feature idea, or open question through to a plan-ready brief - the entry point for new work. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the entry point for a bug report. |
| `plan` | Decompose a request, a brief, or a root cause into sequenced tasks with checkboxes, then self-check the plan against the repository. |
| `exec` | Execute the plan task by task and write the code, committing each finished task. |
| `review` | Review the branch with five parallel agents, verify every finding, and report it. Writes nothing unless you add `fix`, which applies the confirmed findings and re-checks its own work with two agents. |
| `commit` | Commit the current working changes, split into atomic commits - for edits made outside `exec`. |

## Model

Two tiers, nothing in between:

1. Global `~/.claude/CLAUDE.md` - always-on rules (output language, style, safety). Hand-authored by you, NOT shipped by this plugin (see Setup). The commands defer output style and the safety rules on secrets and destructive operations to it, so they fire even when no skill loads.
2. The six commands above. Each is self-contained: no shared background skills, no `reference/` files, no cross-skill injection. A rule lives in exactly one file.

Three commands hand work to the next one, and each handoff is minimal: `plan` reads a brief by its `## Acceptance criteria` and `## Chosen approach` headings, reads a root cause by its `## Root cause` and `## Fix direction` headings, and `exec` finds the work in a plan by two structural tokens - a `### Task N:` heading and `- [ ]` checkboxes. Nothing else crosses between them.

Five of the six commands carry `disable-model-invocation: true`, so they run only when you type them. The workflow is yours to pick, not the model's to guess, and the plugin stays out of the way when you drive a session by hand or through another planning tool. `commit` is the exception: it fires on its own trigger, since "commit this" is a request to commit rather than a request for a command.

Agents (`agents/*.md`) - one write-capable `worker` used by `/dev:exec`, the only agent that writes, plus five read-only reviewers used by `/dev:review`:

| agent | lens |
| --- | --- |
| `review-quality` | bugs, edge cases, error handling, leaks, races, security skim |
| `review-implementation` | goal reached, wiring, completeness, scope creep |
| `review-testing` | coverage over the changed code, fake tests, test quality |
| `review-simplification` | over-engineering this branch introduces |
| `review-documentation` | docs the change needs or made stale, plan checkboxes |

## Stories

One story is one whole unit of work, and it gets one directory under `docs/nxs/stories/` in the current repository. Three commands write an artifact into it, and an artifact is always one markdown file:

| command | artifact | file |
| --- | --- | --- |
| `rnd` | brief | `docs/nxs/stories/YYYYMMDD-<slug>/brief.md` |
| `bug` | root cause | `docs/nxs/stories/YYYYMMDD-<slug>/root-cause.md` |
| `plan` | plan | `docs/nxs/stories/YYYYMMDD-<slug>/plan.md` |

`exec` and `review` write no artifact - what they produce lands in git. `exec` leaves code changes, flipped checkboxes, and one commit per task; `review` leaves nothing at all unless you ask for `fix`, and then commits as `fix: address review findings`. Follow-ups and the review report are spoken to you, not filed.

With a tracker key the directory carries it: `YYYYMMDD-<KEY>-<slug>/`. The key names the directory, never the files inside it.

You move a finished story to `docs/nxs/stories/completed/` yourself, when you decide it is finished. No command does it for you and none will ask - `exec` only knows to skip `completed/` when it looks for the latest plan.

These are local working files - keep `docs/` out of git if you do not want them committed.

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
