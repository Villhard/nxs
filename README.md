# nxs

A Claude Code plugin marketplace. One plugin lives here, versioned and released on its own.

| plugin | what it gives you |
| --- | --- |
| [`dev`](plugins/dev) | An opinionated plan -> exec -> review loop. Seven flat `/dev` commands, a single write-capable worker, five review agents over the finished branch. |

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
  dev/                 # plugin, own version and CHANGELOG
.github/               # CI, house-style linter, PR template
```

Adding a plugin, house style, and the release rules are in [CONTRIBUTING.md](CONTRIBUTING.md).
