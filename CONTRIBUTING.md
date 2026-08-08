# CONTRIBUTING

Rules for the repository. Each plugin sets its own authoring rules on top of these, in its own `CONTRIBUTING.md`, and those apply to that plugin alone: [dev](plugins/dev/CONTRIBUTING.md).

## LAYOUT

```
.claude-plugin/
  marketplace.json     # one entry per plugin
plugins/
  <name>/
    .claude-plugin/
      plugin.json      # name, version, description
    skills/<skill>/SKILL.md
    README.md CHANGELOG.md
.github/               # CI, house-style linter, PR template
LICENSE
```

Everything a plugin ships lives under its own directory. Nothing at the repository root is bundled into any plugin.

## ADDING A PLUGIN

1. `plugins/<name>/.claude-plugin/plugin.json` - `name`, `description`, `version` starting at `0.1.0`, `author`, `license`, `repository`, `homepage` pointing at the plugin directory.
2. Content in the directories Claude Code discovers: `skills/`, and `agents/`, `hooks/`, `commands/` if the plugin needs them.
3. `README.md` and `CHANGELOG.md` in the plugin directory.
4. An entry in `.claude-plugin/marketplace.json` with `name`, `source: "./plugins/<name>"`, `category`, `description`.
5. `CONTRIBUTING.md` in the plugin directory, once the plugin has authoring rules of its own worth stating.

A plugin gets its own directory when its subject does not belong to an existing plugin. A new command inside an existing subject is an addition to that plugin, not a new plugin.

## VERSIONING

Plugins version independently. An edit to bundled content bumps `version` in that plugin's `plugin.json` and adds an entry to that plugin's `CHANGELOG.md` (Keep a Changelog, newest section on top). Nothing at the repository root carries a version.

What counts as a contract, and therefore as a minor rather than a patch, is defined per plugin. Renaming a plugin is a contract change: it renames every command and agent it ships.

Renaming a plugin also needs an entry in the `renames` map of `marketplace.json`, `{"<old>": "<new>"}`, so existing installs follow the rename instead of breaking.

## HOUSE STYLE

Markdown uses ASCII `-` and straight quotes only. Em-dash, en-dash, horizontal bar, minus sign, and typographic or angle quotes are rejected. `.github/scripts/lint-house-style.sh` enforces this over every git-tracked `*.md`; run it before pushing.

## PUBLIC SAFETY

This repository is public. Before committing, strip local paths like `/Users/<name>`, private git remotes, real tracker keys and URLs, secrets, tokens, `.env` values, colleague names and emails, and raw session or tool output. Swap in neutral placeholders: `<user_home>`, `<github_owner>/<repo>`, `PROJ-123`.

## CI

Three checks run on push and pull request, and all three run locally:

```
bash .github/scripts/lint-house-style.sh
claude plugin validate --strict .
claude plugin validate --strict plugins/<name>
```

The workflow also checks that every `plugins/*/skills/*/SKILL.md` carries a non-empty `description` and, when present, a well-formed `user-invocable`.
