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

Installing `nxs@nxs` no longer works: the plugin was renamed to `dev` in `dev` 0.17.0, and the marketplace keeps the name. An existing install should follow the `renames` entry in the manifest on `claude plugin marketplace update nxs`. If it does not, uninstall `nxs@nxs` and install `dev@nxs`.

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
