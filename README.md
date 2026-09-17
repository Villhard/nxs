# nxs

A GitHub plugin marketplace for Claude Code and Codex.

| Plugin | Use it to |
| --- | --- |
| [dev](plugins/dev/README.md) | Shape, plan, implement, review, and commit development work. |

## Install

Connect the marketplace once, then install the plugin.

**Claude Code**

```bash
claude plugin marketplace add Villhard/nxs
claude plugin install dev@nxs
```

**Codex**

```bash
codex plugin marketplace add Villhard/nxs
codex plugin add dev@nxs
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
| Invoke | `/dev:<command>` | Select the plugin skill; CLI/IDE: `/skills` or the `$` picker |

Codex global paths follow `CODEX_HOME` when customized. `AGENTS.override.md` takes precedence over `AGENTS.md`; `CLAUDE.md` is not a default Codex instruction filename. See the official [instruction](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [configuration](https://learn.chatgpt.com/docs/config-file/config-basic), [permission](https://learn.chatgpt.com/docs/agent-configuration/rules), and [skill](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills) guides.

For one Codex CLI session: `codex --sandbox workspace-write --ask-for-approval on-request`. Claude Code permission syntax does not transfer to Codex. Install `rg`, `fd`, and `jq` separately if needed.

After setup changes, start a new session. Ask the agent which instruction files it loaded and which `SKILL.md` it uses.

## Compatibility

Both clients use shared skills and agent roles with native named-agent and generic `collaboration` launch adapters. Six commands require explicit invocation; `commit` remains eligible for natural-language commit requests. A generic prompt does not enforce the native role's tool allowlist.

Verification on 2026-09-17 for `dev` 0.25.0:

| Client | Verified | Not established |
| --- | --- | --- |
| Claude Code CLI 2.1.273 | Plugin validation and discovery of seven commands and six named roles | Complete native workflows; the isolated session had no login |
| Codex CLI 0.154.0 | Temporary installation, skill discovery, actual request assembly for explicit-only selection and the commit exception | Model behavior and complete CLI workflows; the isolated session had no login |
| Collaboration-enabled session | Synthetic fresh-worker tasks and correction, five-role full review in groups, fix and two-role re-check | Native tool-allowlist enforcement, complete exec recovery and quick-review workflows |

Installation and request assembly do not establish complete workflow compatibility. See the [launch contract](plugins/dev/references/agent-launch.md) and [client scenarios](plugins/dev/tests/client-scenarios.md).

## Update

Refresh the catalog, update the installed snapshot, then start a new session.

**Claude Code**

```bash
claude plugin marketplace update nxs
claude plugin update dev@nxs
claude plugin list
```

For project/local installations, run `plugin update` from that project with `--scope project` or `--scope local`; the default is user scope.

**Codex**

```bash
codex plugin marketplace upgrade nxs
codex plugin add dev@nxs
codex plugin list --marketplace nxs
```

Neither client needs an uninstall first. GitHub-backed installations use published snapshots; edits in another checkout do not update them. Check the configured source with `claude plugin marketplace list` or `codex plugin marketplace list`.

For local previews and authoring, see [CONTRIBUTING.md](CONTRIBUTING.md).
