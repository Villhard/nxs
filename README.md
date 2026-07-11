# nxs

An opinionated plan -> exec -> review loop for Claude Code, packaged as a plugin. You get a reviewable plan as the source of truth, task-by-task execution by a single write-capable worker, and multi-lens code review - with commit / plan / review conventions enforced from one place instead of re-explained in every prompt.

Why install it over ad-hoc prompts: the workflow is fixed and named (`/nxs:plan`, `/nxs:exec`, `/nxs:review`), the conventions live in single-source background skills that every command shares, and human review gates stay in the loop - plan review before auto-exec, code review before commit.

## Quickstart

One task through the loop:

```
/nxs:rnd add rate limiting to the public API   # shape a fuzzy task into a plan-ready brief
/nxs:plan                                        # turn the brief into sequenced, verifiable tasks
/nxs:plancheck                                   # multi-lens read-only review of the plan
/nxs:exec                                         # implement one task, then stop for you to commit
#   ...or /nxs:exec auto                          # run all remaining low-risk tasks
/nxs:review                                       # review the diff before you commit
/nxs:clean                                        # archive the finished plan
```

## Commands

14 flat `/nxs:<name>` commands:

| command | when to use |
| --- | --- |
| `plan` | Decompose a task, brief, or tracker input into sequenced, verifiable vertical-slice tasks - the source of truth for execution. |
| `exec` | Execute a plan task by task and write the code; default runs one task then stops, `auto` runs all remaining low-risk tasks. |
| `review` | Review a diff (staged, branch vs base, file, or PR) and report confirmed BLOCK / NIT findings without editing code. |
| `plancheck` | Multi-lens read-only review of a plan before execution; run after `plan` and always before `exec auto`. |
| `bug` | Investigate a bug to a confirmed root cause before any fix - the tracked-bug entry point. |
| `rnd` | Think a fuzzy task, feature idea, or open question through to a plan-ready brief - the tracked-task entry point. |
| `dialectic` | Compare two concrete approaches head to head, or steelman-then-attack a single claim, for an honest trade-off verdict. |
| `epic` | Chart a foggy multi-session effort into a map of investigation items, then hand off to `rnd` or `plan`. |
| `wrong` | Stop a stuck or thrashing approach and find a genuinely different alternative. |
| `explain` | Explain a diff, file, function, flow, or subsystem from zero, scaling depth to the target - understanding, not review. |
| `userdoc` | Produce end-user how-to documentation for a feature, drafted locally and published to Confluence. |
| `techdoc` | Write technical documentation for maintainers from the branch / plan / diff, drafted locally and published to Confluence. |
| `recommit` | Rewrite the branch's local commits into clean atomic groups without changing the final tree - git-only, never pushes. |
| `clean` | Archive completed plans and superseded briefs after you approve the moves - relocates docs only, never deletes. |

## Model

Three tiers:

1. Global `~/.claude/CLAUDE.md` - tool-level always-on rules (output language, style, token economy, CLI tools, safety). Hand-authored by you, NOT shipped by this plugin - each user provides their own (see Setup). The plugin's skills rely on it for output style and for the safety rules some skills delegate to it: for example `commit-conventions` keeps its secret / force-push safety in your global rules, not in the skill.
2. Command skills (`/nxs:<name>`) - the 14 flat commands listed above. Modes are rare and inferred: `exec` (default / auto) and `explain` (depth). All others are single-mode.
3. Background skills (`user-invocable: false`) - 8 shared rules loaded by relevance, hidden from the `/` menu: `commit-conventions`, `plan-conventions`, `review-protocol`, `verify`, `decision-log`, `intake`, `doc-draft`, `stress-test`.

Agents (`agents/*.md`) - one write-capable `worker` (used by `/nxs:exec`; the only agent that writes) plus read-only subagents in two classes:

- Tool-enforced read-only - tools limited to Read / Grep / Glob, so they cannot write or run shell: the four `plan-*-reviewer` lenses (used by `plancheck`) and the four `review-*-reviewer` lenses (used by `review`).
- Prompt-level read-only - keep Bash to run read-only shell (git history, repro) but write nothing: `explorer` and `diagnose-investigator`.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest (name: nxs)
  marketplace.json     # plugin marketplace
skills/
  <name>/              # command skill -> /nxs:<name>
    SKILL.md
    reference/         # heavy detail, loaded on demand
  <background-name>/    # background skill (user-invocable: false)
agents/
  <name>.md            # subagent (worker + read-only reviewers / explorer)
```

## Setup

1. Install the plugin:
   ```
   claude plugin marketplace add Villhard/nxs
   claude plugin install nxs@nxs
   ```

2. **Global rules (your own)**. The skills defer output language / style to your global `~/.claude/CLAUDE.md`, and `commit-conventions` delegates secret / force-push safety there. The plugin does not ship a block (plugins cannot write `~/.claude/CLAUDE.md`), so set up your own global conventions as you prefer. Without a tier-1 `~/.claude/CLAUDE.md` the skills still run, but they lose the delegated secret / force-push / destructive-op protections and fall back to the default output style. Copy `examples/CLAUDE.md.sample` to `~/.claude/CLAUDE.md` as a starting point - it carries the active safety block the skills assume, with the language / style / tooling extras commented out for you to enable.

3. **Optional - permissions**. The skills prefer `rg` / `fd` / `jq`. Allow them in `~/.claude/settings.json` to avoid prompts, or just allow them on first use. Plugins cannot ship permissions.

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
