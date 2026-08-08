# nxs

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and one multi-agent review gate over the finished branch.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/nxs:plan`, `/nxs:exec`, `/nxs:review`), each command is self-contained, and the human stays in the loop - you approve the plan before execution and the review runs before you push.

## Quickstart

One task through the loop:

```
/nxs:rnd add rate limiting to the public API   # shape a fuzzy task into a plan-ready brief
/nxs:plan                                      # turn the brief into sequenced tasks
/nxs:exec                                      # run the plan to the end, one commit per task
/nxs:review                                    # five reviewers over the branch, fixes committed
```

## Commands

Six flat `/nxs:<name>` commands:

| command | when to use |
| --- | --- |
| `rnd` | Think a fuzzy task, feature idea, or open question through to a plan-ready brief - the task entry point. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the bug entry point. |
| `plan` | Decompose a task, brief, or ticket into sequenced tasks with checkboxes, then self-check the plan against the repository. |
| `exec` | Execute the plan task by task and write the code, committing each finished task. |
| `review` | Review the branch with five parallel agents, verify every finding, fix what is confirmed, and commit. |
| `commit` | Commit the current working changes, split into atomic commits - for edits made outside `exec`. |

## Model

Two tiers, nothing in between:

1. Global `~/.claude/CLAUDE.md` - always-on rules (output language, style, safety). Hand-authored by you, NOT shipped by this plugin (see Setup). The commands defer output style and the safety rules on secrets and destructive operations to it, so they fire even when no skill loads.
2. The six commands above. Each is self-contained: no shared background skills, no `reference/` files, no cross-skill injection. A rule lives in exactly one file.

The contract between `plan` and `exec` is two structural tokens: a `### Task N:` heading and `- [ ]` checkboxes. `exec` takes the first task section with open checkboxes and does not require anything else inside it.

A SessionStart hook (`hooks/`) injects the `using-nxs` discipline so a session checks for the right command before acting - the commands fire on their trigger without being typed by name.

Agents (`agents/*.md`) - one write-capable `worker` used by `/nxs:exec`, the only agent that writes, plus five read-only reviewers used by `/nxs:review`:

| agent | lens |
| --- | --- |
| `review-quality` | bugs, edge cases, error handling, leaks, races, security skim |
| `review-implementation` | goal reached, wiring, completeness, scope creep |
| `review-testing` | coverage over the changed code, fake tests, test quality |
| `review-simplification` | over-engineering this branch introduces |
| `review-documentation` | docs the change needs or made stale, plan checkboxes |

## Artifacts

One story is one whole unit of work, and it gets one directory under `docs/nxs/stories/` in the current repository:

- `/nxs:rnd` -> `docs/nxs/stories/YYYYMMDD-<slug>/brief.md`
- `/nxs:bug` -> `docs/nxs/stories/YYYYMMDD-<slug>/root-cause.md`
- `/nxs:plan` -> `plan.md` beside it, the whole directory archived by hand to `docs/nxs/stories/completed/`
- `/nxs:exec` -> code changes, updated checkboxes, one commit per task
- `/nxs:review` -> fixes committed as `fix: address review findings`

With a tracker key the directory carries it: `YYYYMMDD-<KEY>-<slug>/`. These are local working files - keep `docs/` out of git if you do not want them committed.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest (name: nxs)
  marketplace.json     # plugin marketplace
skills/
  <name>/SKILL.md      # command skill -> /nxs:<name>, self-contained
agents/
  worker.md            # the single write-capable agent
  review-*.md          # five read-only reviewers
hooks/                 # SessionStart hook -> injects the using-nxs discipline
  hooks.json
  session-start.sh
  using-nxs.md
```

## Setup

1. Install the plugin:
   ```
   claude plugin marketplace add Villhard/nxs
   claude plugin install nxs@nxs
   ```

2. **Global rules (your own)**. The commands defer output language and style to your global `~/.claude/CLAUDE.md`, along with secret safety and destructive-op confirmation. The plugin does not ship a block (plugins cannot write `~/.claude/CLAUDE.md`), so set up your own. Without them the commands still run, but they lose those delegated protections and fall back to the default output style.

3. **Optional - permissions**. The skills prefer `rg` / `fd` / `jq`. Allow them in `~/.claude/settings.json` to avoid prompts. Plugins cannot ship permissions.

4. Restart Claude Code so the plugin snapshot and the global rules load.

## Dev loop

The installed plugin reads a cached snapshot, not the live repo, so a session picks up repo edits only after the snapshot is refreshed and the session restarts.

```
# simplest - reinstall (no version bump)
claude plugin uninstall nxs@nxs && claude plugin install nxs@nxs

# or version-based
# bump "version" in .claude-plugin/plugin.json, then:
claude plugin marketplace update nxs
claude plugin update nxs@nxs
```

A restart is required either way. `claude plugin validate --strict .` checks the manifest and skills before install.
