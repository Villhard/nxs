# nxs

A plugin marketplace for Claude Code and Codex. Plugins are versioned and released independently.

| plugin | what it gives you |
| --- | --- |
| [`dev`](plugins/dev) | An opinionated plan -> exec -> review loop. Seven flat `/dev` commands, a single write-capable worker, five review agents over the finished branch. |
| [`std`](plugins/std) | Conversational learning from books and courses, with trusted sources, a mission, and durable progress. |

## Install

```
claude plugin marketplace add Villhard/nxs
claude plugin install dev@nxs
```

Restart Claude Code so the plugin snapshot loads. The plugin's README covers its own setup.

## Layout

```
.claude-plugin/
  marketplace.json     # one entry per plugin
plugins/
  dev/                 # development workflow
  std/                 # conversational learning; own version and CHANGELOG
.github/               # CI, house-style linter, PR template
```

Adding a plugin, house style, and the release rules are in [CONTRIBUTING.md](CONTRIBUTING.md).
