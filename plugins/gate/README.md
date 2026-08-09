# gate

A planning artifact is a decision you sign off on. This plugin makes you sign it before it reaches disk: a `PreToolUse` hook on `Write` opens the pending content in the [revdiff](https://github.com/umputun/revdiff) TUI, and whatever you annotate comes back to the agent as a blocking denial.

It is the same loop [`revdiff-planning`](https://github.com/umputun/revdiff) runs on `ExitPlanMode`, moved from the built-in plan mode onto files, so a brief, a plan, or a ticket written by any skill goes through the same gate.

> **This plugin is a front-end for revdiff and does nothing without it.** The `revdiff` binary must be in `PATH`, and the review needs an overlay terminal. Install revdiff first: `brew install umputun/apps/revdiff`, or see the [releases](https://github.com/umputun/revdiff/releases). Without it every `Write` simply passes through unreviewed.

## What it gates

Matched against the repository-relative path:

| pattern | written by |
| --- | --- |
| `docs/nxs/stories/*/brief.md` | `/dev:rnd` |
| `docs/nxs/stories/*/root-cause.md` | `/dev:bug` |
| `docs/nxs/stories/*/plan.md` | `/dev:plan` |
| `.scratch/*/*.md` | `to-spec`, `wayfinder` |
| `.scratch/*/issues/*.md` | `to-tickets` |

Every other `Write` passes through untouched: the hook contributes no permission decision at all, so the normal flow decides. Widening or narrowing the gate means editing `GATED_PATTERNS` in `scripts/artifact-review-hook.py`.

`Edit` is deliberately not gated. A gate on every small correction turns the review into a toll booth, and the artifacts this plugin cares about are written whole.

## The loop

1. The agent calls `Write` on a gated path.
2. The hook writes the pending content to a temp snapshot and opens revdiff over your session.
3. Annotations, if any, go back as the denial reason. The file is not written.
4. The agent revises and writes again. This round compares against what you just read, so you see only what changed.
5. A clean review lets the `Write` through.

The baseline for the compare is the snapshot of the last round, or the file already on disk when there was no earlier round. A first draft is read whole. Nothing is stored inside the artifact itself, so the compare chain leaves no marker in the file.

## Review as long as you need

The hook declares `"timeout": 345600` and waits four days for the launcher. That number is the point of running the review from a hook at all: the `revdiff` skill drives the same launcher through the Bash tool, and Claude Code caps a Bash call at 10 minutes, so a long review there loses the channel back to the session (the annotations survive on disk, but somebody has to read them back). Nothing here is on a Bash call, so a review that takes an hour is an hour the hook spends waiting.

## Failing open

A `Write` is never lost because the review could not run. Missing `revdiff`, no overlay terminal, a launcher that crashes, a review that times out - each one lets the `Write` proceed and prints a `gate:` note to stderr saying the artifact went unreviewed.

## Install

```
claude plugin marketplace add Villhard/nxs
claude plugin install gate@nxs
```

Requires `python3`, the `revdiff` binary in `PATH`, and agterm or tmux for the overlay.

## Overriding the launcher

The bundled `launch-artifact-review.sh` handles agterm and tmux, which is what this setup runs. For any other terminal, drop your own launcher into the user layer - it wins over the bundled one and needs no fork:

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}/scripts"
cp "${CLAUDE_PLUGIN_ROOT}/scripts/launch-artifact-review.sh" "${CLAUDE_PLUGIN_DATA}/scripts/launch-artifact-review.sh"
chmod +x "${CLAUDE_PLUGIN_DATA}/scripts/launch-artifact-review.sh"
```

A non-executable file in the user layer counts as absent, so `chmod -x` disables an override without deleting it. There is no project-level layer on purpose: the hook fires in every repository this runtime opens, and a repo-controlled executable would run arbitrary code on a routine `Write`.

**Launcher contract.** Arguments are `<pending-file> <label>`, plus `<baseline-file>` in compare mode. Print the captured annotations to stdout, nothing to approve. Exit 10 for annotations, 0 for clean, anything else is a failure that fails open.

`revdiff-planning`'s own launcher covers tmux, zellij, herdr, kitty, wezterm, cmux, ghostty, iTerm2, and emacs vterm, and its argument order differs - `<new> [<old>]`, with no label. Adapt rather than symlink.

## Layout

```
.claude-plugin/
  plugin.json
hooks/
  hooks.json                    # PreToolUse -> Write
scripts/
  artifact-review-hook.py       # path filter, snapshot, decision
  resolve-launcher.sh           # user layer -> bundled
  launch-artifact-review.sh     # agterm and tmux overlay
```
