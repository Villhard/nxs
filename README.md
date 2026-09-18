# nxs

A plugin marketplace for Claude Code and Codex.

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

Start a new session after updating. Local checkout edits do not update an installed plugin.

## Client setup

Configure the client using its official guide: [Claude Code settings](https://code.claude.com/docs/en/settings) or [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic).

For local previews and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md).
