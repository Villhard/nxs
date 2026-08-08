# nxs

A Claude Code plugin marketplace. Two plugins live here, versioned and released independently.

| plugin | what it gives you |
| --- | --- |
| [`dev`](plugins/dev) | An opinionated plan -> exec -> review loop. Six flat `/dev` commands, a single write-capable worker, five review agents over the finished branch. |
| [`teach`](plugins/teach) | `/teach` turns the current directory into a teaching workspace that survives between sessions: a mission, curated sources, numbered lessons, and a record of what you have learned. |

## Install

```
claude plugin marketplace add Villhard/nxs
claude plugin install dev@nxs
claude plugin install teach@nxs
```

Restart Claude Code so the plugin snapshots load. Each plugin's README covers its own setup.

## Layout

```
.claude-plugin/
  marketplace.json     # the two plugin entries
plugins/
  dev/                 # plugin, own version and CHANGELOG
  teach/               # plugin, own version and CHANGELOG
.github/               # CI, house-style linter, PR template
```

Adding a plugin, house style, and the release rules are in [CONTRIBUTING.md](CONTRIBUTING.md).
