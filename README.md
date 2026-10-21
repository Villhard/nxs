# nxs

A plugin marketplace for Claude Code and Codex.

| Plugin | Use it to |
| --- | --- |
| [dev](plugins/dev/README.md) | Shape features and bugs into tickets, review and commit development work. |

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

**OpenCode**

OpenCode 2 does not install Claude Code plugins; the dev installer copies the plugin into the OpenCode config directory. It needs Python 3:

```bash
git clone https://github.com/Villhard/nxs.git
python3 nxs/plugins/dev/opencode/install.py
```

Remove it with `python3 nxs/plugins/dev/opencode/install.py --uninstall`.

Skip registration if `nxs` is already configured. Start a new session, then follow the [dev workflow](plugins/dev/README.md).

## Update

**Claude Code**

```bash
claude plugin marketplace update nxs
claude plugin update dev@nxs
```

For project/local installations, run the update from that project with `--scope project` or `--scope local`.

**Codex**

```bash
codex plugin marketplace upgrade nxs
codex plugin add dev@nxs
```

**OpenCode**

```bash
git -C nxs pull
python3 nxs/plugins/dev/opencode/install.py
```

Start a new session after updating; restart OpenCode. Local checkout edits do not update an installed plugin.

## Client setup

Configure the client using its official guide: [Claude Code settings](https://code.claude.com/docs/en/settings), [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic) or [OpenCode config](https://opencode.ai/v2/docs/config/).

For local previews and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md).
