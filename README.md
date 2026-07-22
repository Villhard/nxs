# nxs

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and multi-lens code review - with commit, plan, and review conventions enforced from one place instead of re-explained in every prompt.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/nxs:plan`, `/nxs:exec`, `/nxs:review`), the conventions live in single-source background skills that every command shares, and human review gates stay in the loop - plan review before execution, code review before commit.

## Quickstart

One task through the loop:

```
/nxs:rnd add rate limiting to the public API   # shape a fuzzy task into a plan-ready brief
/nxs:plan                                        # turn the brief into sequenced, verifiable tasks
/nxs:plancheck                                   # read-only review of the plan
/nxs:exec                                        # run the plan to the end, with gates on every task
/nxs:review                                      # review the diff before you commit
```

## Commands

Six flat `/nxs:<name>` commands:

| command | when to use |
| --- | --- |
| `rnd` | Think a fuzzy task, feature idea, or open question through to a plan-ready brief - the task entry point. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the bug entry point. |
| `plan` | Decompose a task, brief, or tracker input into sequenced, verifiable vertical-slice tasks - the source of truth for execution. |
| `plancheck` | Read-only review of a plan before execution; run after `plan` and before `exec`. |
| `exec` | Execute a plan task by task and write the code, with verify, review, and a commit after each task. |
| `review` | Review a diff (staged, branch vs base, file, or PR) and report confirmed BLOCK / NIT findings without editing code. |

## Model

Three tiers:

1. Global `~/.claude/CLAUDE.md` - tool-level always-on rules (output language, style, safety). Hand-authored by you, NOT shipped by this plugin (see Setup). The skills rely on it for output style and for the safety rules some of them delegate to it: `commit-conventions` states the git gate itself, but leaves secret safety and destructive-op confirmation to your global rules, which fire even when no skill loads.
2. Command skills (`/nxs:<name>`) - the six commands above. Single-mode; `exec` takes an optional natural-language `no commits`.
3. Background skills (`user-invocable: false`) - five shared rule sets loaded by relevance, hidden from the `/` menu: `plan-conventions`, `review-protocol`, `verify`, `commit-conventions`, `intake`.

Agents (`agents/*.md`) - one write-capable `worker` (used by `/nxs:exec`; the only agent that writes) plus five read-only lenses whose tools are limited to Read / Grep / Glob, so they cannot write or run shell: `plan-reviewer` (used by `plancheck`) and the four `review-*-reviewer` lenses (used by `review`).

## Artifacts

Working artifacts live under `docs/nxs/` in the current repository:

- `/nxs:rnd` -> `docs/nxs/briefs/YYYYMMDD-<slug>-rnd.md`
- `/nxs:bug` -> `docs/nxs/briefs/YYYYMMDD-<slug>-bug.md`
- `/nxs:plan` -> `docs/nxs/plans/YYYYMMDD-<slug>.md`, archived by hand to `docs/nxs/plans/completed/`
- `/nxs:plancheck`, `/nxs:review` -> chat only
- `/nxs:exec` -> code changes plus updated plan checkboxes

With a tracker key the name carries it: `YYYYMMDD-<KEY>-<slug>.md`. These are local working files - keep `docs/` out of git if you do not want them committed.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest (name: nxs)
  marketplace.json     # plugin marketplace
skills/
  <name>/              # command skill -> /nxs:<name>
    SKILL.md
    reference/         # heavy detail, loaded on demand
  <background-name>/   # background skill (user-invocable: false)
agents/
  <name>.md            # subagent (worker + read-only lenses)
examples/              # filled sample artifacts, as the skills write them
  plan-sample.md
  brief-sample.md
```

## Setup

1. Install the plugin:
   ```
   claude plugin marketplace add Villhard/nxs
   claude plugin install nxs@nxs
   ```

2. **Global rules (your own)**. The skills defer output language and style to your global `~/.claude/CLAUDE.md`, and `commit-conventions` delegates secret safety and destructive-op confirmation there. The plugin does not ship a block (plugins cannot write `~/.claude/CLAUDE.md`), so set up your own global conventions. Without them the skills still run, but they lose the delegated secret and destructive-op protections and fall back to the default output style.

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
