# nxs

A GitHub plugin marketplace for Claude Code and Codex.

| Plugin | Use it to |
| --- | --- |
| [dev](plugins/dev/README.md) | Shape, plan, implement, review, and commit development work. |
| [std](plugins/std/README.md) | Study books and courses through dialogue, with sources and saved progress. |

## Install

Connect the marketplace once, then install a plugin. These examples use `std@nxs`; use `dev@nxs` for `dev`, or install both.

**Claude Code**

```bash
claude plugin marketplace add Villhard/nxs
claude plugin install std@nxs
```

**Codex**

```bash
codex plugin marketplace add Villhard/nxs
codex plugin add std@nxs
```

Skip marketplace registration if `nxs` is already configured. If a plugin is missing, refresh the catalog using the matching [update](#update) command. Start a new session after installation.

## Client setup

Keep personal preferences in instruction files and execution permissions in client configuration. Plugins create neither.

| Setting | Claude Code | Codex |
| --- | --- | --- |
| Global instructions | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| Project instructions | `CLAUDE.md` | `AGENTS.md` |
| User configuration | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Project configuration | `.claude/settings.json` | `.codex/config.toml` in a trusted project |
| Execution permissions | Permission rules in settings | Sandbox, approvals, optional `~/.codex/rules/*.rules` |
| Invoke | `/std:teach`, `/dev:<command>` | Select the plugin skill; CLI/IDE: `/skills` or the `$` picker |

Codex global paths follow `CODEX_HOME` when customized. `AGENTS.override.md` takes precedence over `AGENTS.md`; `CLAUDE.md` is not a default Codex instruction filename. See the official [instruction](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [configuration](https://learn.chatgpt.com/docs/config-file/config-basic), [permission](https://learn.chatgpt.com/docs/agent-configuration/rules), and [skill](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills) guides.

For one Codex CLI session: `codex --sandbox workspace-write --ask-for-approval on-request`. Claude Code permission syntax does not transfer to Codex. Install `rg`, `fd`, and `jq` separately if needed.

After setup changes, start a new session. Ask the agent which instruction files it loaded and which `SKILL.md` it uses.

## Compatibility

Both clients accept the catalog. `std` installation, skill discovery, and sample learning dialogues are verified in both, using one shared skill and two manifests. These are spot checks, not a guarantee of lesson accuracy.

`dev` has a Claude Code manifest and named-agent workflow. Codex installation and skill discovery are verified; complete execution, review, and fixes with those agents remain unverified. Installation alone does not establish workflow compatibility.

## Update

Refresh the catalog, update the installed snapshot, then start a new session. Replace `std@nxs` with `dev@nxs` as needed.

**Claude Code**

```bash
claude plugin marketplace update nxs
claude plugin update std@nxs
claude plugin list
```

For project/local installations, run `plugin update` from that project with `--scope project` or `--scope local`; the default is user scope.

**Codex**

```bash
codex plugin marketplace upgrade nxs
codex plugin add std@nxs
codex plugin list --marketplace nxs
```

Neither client needs an uninstall first. GitHub-backed installations use published snapshots; edits in another checkout do not update them. Check the configured source with `claude plugin marketplace list` or `codex plugin marketplace list`.

For local previews and authoring, see [CONTRIBUTING.md](CONTRIBUTING.md).
