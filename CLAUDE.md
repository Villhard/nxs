# CLAUDE

Rules for working in this repository. `CONTRIBUTING.md` is the full text; read it, and the plugin's own `CONTRIBUTING.md`, before the first edit under `plugins/`.

## BEFORE COMMITTING

Every edit to bundled content - `skills/`, `agents/`, manifests - bumps `version` in that plugin's `plugin.json` and adds an entry to that plugin's `CHANGELOG.md`, in the same change. A commit that edits a plugin and leaves the version alone is incomplete.

Which part of the version moves is decided by the CONTRACT, not by the size of the diff and not by the commit type. Each plugin defines its contract in its own `CONTRIBUTING.md`: for `dev` it is command names and arguments, agent names, artifact paths, the handoff headings, and the git gates. Wording inside a `SKILL.md` and an agent's criteria are internal, so they are a patch.

Nothing at the repository root carries a version, this file included.

## HOUSE STYLE

ASCII `-` and straight quotes only. Run `.github/scripts/lint-house-style.sh` before pushing - it checks every git-tracked `*.md`.

Files the model loads as instructions - `SKILL.md`, `agents/*.md`, `CONTRIBUTING.md`, this file - use UPPERCASE headings at every level. Files a human reads on GitHub - `README.md`, `CHANGELOG.md` - use sentence case.
