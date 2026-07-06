# nxs

Nexus workflow skills for Claude Code, packaged as a plugin: dev / rnd / std / doc flows as `/nxs:*` commands, background rule skills, and read-only reviewer / explorer agents plus one write-capable worker.

## Model

Three tiers:

1. Global `~/.claude/CLAUDE.md` - tool-level always-on rules (output language, style, token economy, CLI tools, safety, pointer to project `docs/.ai/*`). Hand-authored by you, NOT shipped by this plugin - each user provides their own (see Setup). The plugin's skills rely on it for output style and for the safety rules some skills delegate to it: for example `commit-conventions` keeps its secret / force-push safety in your global rules, not in the skill.
2. Command skills (`/nxs:<flow>-<action>`) - the workflows: 7 dev, 5 rnd, 4 std, 4 doc, plus `init` and `help`.
3. Background skills (`user-invocable: false`) - shared rules loaded by relevance, hidden from the `/` menu: `commit-conventions`, `plan-conventions`, `review-protocol`, `verify`, `domain-language`, `note-conventions`, `decision-log`, `jira-intake`.

Agents (`agents/*.md`) - one write-capable `worker` (used by `/nxs:dev-exec`) and read-only subagents: `explorer`, `diagnose-investigator`, four `plan-*-reviewer` lenses, four `review-*-reviewer` lenses.

## Layout

```
.claude-plugin/
  plugin.json          # plugin manifest (name: nxs)
  marketplace.json     # plugin marketplace
skills/
  <flow>-<action>/     # command skill -> /nxs:<flow>-<action>
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

2. **Global rules (your own)**. The skills defer output language / style to your global `~/.claude/CLAUDE.md`, and `commit-conventions` delegates secret / force-push safety there. The plugin does not ship a block (plugins cannot write `~/.claude/CLAUDE.md`), so set up your own global conventions as you prefer. Without them the skills still run - just in the default output style and without those delegated safety rules.

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
