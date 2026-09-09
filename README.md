# nxs

A GitHub-hosted plugin marketplace for Claude Code and Codex. Both clients read the same catalog; plugins are versioned and released independently. Choose the plugin for the work you want to do.

| Plugin | What it gives you |
| --- | --- |
| [`dev`](plugins/dev) | A development workflow: seven commands for shaping, investigating, planning, execution, review, fixes, and commits; one worker and five reviewers. |
| [`std`](plugins/std) | Conversational learning from books and courses, with trusted sources, a mission, and durable progress. |

## Compatibility

| Plugin | Claude Code | Codex |
| --- | --- | --- |
| `dev` | The documented workflow uses Claude Code commands, named agents, and global configuration. | Installation and skill discovery are verified. The complete workflow with its named agents has not been verified. |
| `std` | Installation, skill discovery, and sample learning dialogues are verified. | Installation, skill discovery, and sample dialogues with the shared skill are verified. |

Catalog support does not establish that every client runs every plugin component the same way. `std` has manifests for both clients and one shared `teach` skill. `dev` currently ships a Claude Code manifest and agent definitions; its [README](plugins/dev/README.md#compatibility) describes the boundary. Sample dialogues are behavioral spot checks, not a guarantee of factual correctness.

## Install

Connect `nxs` once in each client you use, then install a chosen plugin. The examples install `std`; replace `std@nxs` with `dev@nxs` to install `dev`, or repeat the install step for the other plugin to install both.

### Claude Code

```bash
claude plugin marketplace add Villhard/nxs
claude plugin install std@nxs
```

### Codex

```bash
codex plugin marketplace add Villhard/nxs
codex plugin add std@nxs
```

If `nxs` is already configured, skip the marketplace-add command. For a newly published plugin missing from the catalog, refresh the marketplace using the first command in the matching update section below, then install it. These instructions use the GitHub source; an existing local-checkout source continues to use that checkout.

Start a new session after installation. In Claude Code, invoke `/std:teach` or a `/dev:<command>`. In Codex, select the plugin's skill or ask for it by plugin and skill name; do not assume Claude Code slash-command syntax is identical. Each plugin's README covers its own setup and usage.

## Client setup

Plugins supply workflows. Keep your own language, coding, and confirmation preferences in the instruction files your client reads; neither plugin creates them or grants tool permissions.

| Task | Claude Code | Codex |
| --- | --- | --- |
| Global instructions | `~/.claude/CLAUDE.md` | `~/.codex/AGENTS.md` |
| Project instructions | `CLAUDE.md` in the project | `AGENTS.md` in the project |
| User configuration | `~/.claude/settings.json` | `~/.codex/config.toml` |
| Project configuration | `.claude/settings.json` | `.codex/config.toml` in a trusted project |
| Command permissions | Permission rules in `settings.json` | Sandbox and approval settings; optional command-prefix rules in `~/.codex/rules/*.rules` |
| Choose a plugin skill | `/std:teach` or `/dev:<command>` | Select the installed skill; in CLI/IDE use `/skills` or type `$` and choose the matching plugin entry |

Codex paths above assume the default `CODEX_HOME`. If it is customized, use that directory for global instructions and configuration. `AGENTS.override.md` takes precedence over `AGENTS.md` at the same level; a `CLAUDE.md` file is not a default Codex instruction filename. See OpenAI's [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

For Codex, use [config.toml](https://learn.chatgpt.com/docs/config-file/config-basic) for persistent settings. A one-session CLI example is `codex --sandbox workspace-write --ask-for-approval on-request`. These settings control execution access and approvals; prose in `AGENTS.md` does not replace them. Optional [command rules](https://learn.chatgpt.com/docs/agent-configuration/rules) govern execution outside the sandbox and are not a direct copy of Claude Code permission syntax. `rg`, `fd`, and `jq` need to be available on `PATH`; listing them in instructions does not install them.

Start a new session after changing setup. To verify instruction discovery, ask the agent to list the instruction files it loaded. To verify a skill, select it explicitly and ask which `SKILL.md` it is using. See the [Codex skill invocation guide](https://learn.chatgpt.com/docs/build-skills#how-codex-uses-skills).

## Update

Marketplace refresh fetches the catalog and sources. The next command updates the installed plugin snapshot. Use the pair for your client, replacing `std@nxs` with `dev@nxs` when needed.

### Claude Code

```bash
claude plugin marketplace update nxs
claude plugin update std@nxs
```

### Codex

```bash
codex plugin marketplace upgrade nxs
codex plugin add std@nxs
```

Claude Code defaults to user scope. To update a project or local installation, pass the matching `--scope project` or `--scope local` to `plugin update` from that project.

Codex uses `plugin add` again to install the current version from the refreshed marketplace. Neither workflow requires uninstalling first. Start a new session afterward to load the refreshed skills. Already-running sessions should not be used to judge whether the update took effect.

Check installed versions and enabled status with:

```bash
claude plugin list
codex plugin list --marketplace nxs
```

A GitHub-backed installation reads a cached snapshot, not edits in a separate working checkout. Publishing changes, refreshing the marketplace, and updating an installation are separate actions.

## Layout

```text
.claude-plugin/
  marketplace.json     # shared catalog, one entry per plugin
plugins/
  dev/                 # development workflow; Claude Code manifest and agents
  std/                 # conversational learning; Claude Code and Codex manifests
.github/               # CI, house-style linter, PR template
```

Each plugin owns its skills, documentation, version, and CHANGELOG. Adding a plugin, house style, verification, and release rules are in [CONTRIBUTING.md](CONTRIBUTING.md).
