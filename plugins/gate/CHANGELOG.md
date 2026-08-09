# Changelog

All notable changes to the `gate` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-09

First release. `revdiff-planning` gates the plan the built-in plan mode produces, and nothing gated the artifacts a skill writes to disk - a brief, a plan, or a ticket landed on the first try, and the read happened afterwards, if at all. This plugin puts the same review in front of the `Write`.

### Added

- `hooks/hooks.json` - a `PreToolUse` hook on `Write`.
- `scripts/artifact-review-hook.py` - filters by path, snapshots the pending content, runs the review, and returns annotations as a blocking denial. A `Write` outside `GATED_PATTERNS` gets no permission decision at all, so the normal flow is untouched. Everything that can go wrong fails open with a `gate:` note on stderr.
- `scripts/launch-artifact-review.sh` - the overlay launcher for agterm and tmux.
- `scripts/resolve-launcher.sh` - the user layer beats the bundled launcher, with no project layer, since the hook fires in any repository the runtime opens.

The compare baseline is keyed by a hash of the target path rather than by a marker inside the content, which is what `revdiff-planning` needs for `ExitPlanMode`. An artifact is a file the user keeps, so the rolling chain leaves nothing in it.

The hook waits four days on the launcher. Claude Code caps a Bash call at 10 minutes, which is what a review driven from the `revdiff` skill runs into; a hook carries its own `timeout` and is not on that path, so the length of a review is the user's business.
