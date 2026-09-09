# CONTRIBUTING

`CLAUDE.md` and `AGENTS.md` are the client entry points for these repository rules. Each plugin sets its own authoring rules on top of these, in its own `CONTRIBUTING.md`, and those apply to that plugin alone: [dev](plugins/dev/CONTRIBUTING.md) and [std](plugins/std/CONTRIBUTING.md).

## LAYOUT

```
.claude-plugin/
  marketplace.json     # shared catalog, one entry per plugin
plugins/
  <name>/
    .claude-plugin/
      plugin.json      # name, version, description
    .codex-plugin/     # present in std; not currently shipped by dev
      plugin.json      # Codex metadata; points at the shared skills directory
    skills/<skill>/SKILL.md
    README.md CHANGELOG.md
.github/               # CI, house-style linter, PR template
LICENSE
```

Everything a plugin ships lives under its own directory. Nothing at the repository root is bundled into any plugin.

## ADDING A PLUGIN

1. `plugins/<name>/.claude-plugin/plugin.json` - `name`, `description`, `version` starting at `0.1.0`, `author`, `license`, `repository`, `homepage` pointing at the plugin directory.
2. For an explicit Codex manifest, add `.codex-plugin/plugin.json` with the same name/version and `skills: "./skills/"`; `std` is the current example. Keep one shared skill implementation when behavior is shared. Document and verify platform-specific components instead of assuming that installation proves compatibility.
3. Content in the client-discovered directories: `skills/`, plus agents or other components only when the plugin needs them and the intended client supports them.
4. `README.md` and `CHANGELOG.md` in the plugin directory.
5. An entry in `.claude-plugin/marketplace.json` with `name`, `source: "./plugins/<name>"`, `category`, `description`.
6. `CONTRIBUTING.md` in the plugin directory, once the plugin has authoring rules of its own worth stating.

A plugin gets its own directory when its subject does not belong to an existing plugin. A new command inside an existing subject is an addition to that plugin, not a new plugin.

## VERSIONING

Plugins version independently. An edit to bundled content, including plugin documentation, bumps `version` and adds an entry to that plugin's `CHANGELOG.md` (Keep a Changelog, newest section on top). Keep every manifest shipped by that plugin at the same name/version; `std` has two, `dev` currently has one. Documentation fixes are patches when the contract is unchanged. Preserve historical changelog entries. Nothing at the repository root carries a version.

What counts as a contract, and therefore as a minor rather than a patch, is defined per plugin. Renaming a plugin is a contract change: it renames every command and agent it ships.

## HOUSE STYLE

Markdown uses ASCII `-` and straight quotes only. Em-dash, en-dash, horizontal bar, minus sign, and typographic or angle quotes are rejected. `.github/scripts/lint-house-style.sh` enforces this over every git-tracked `*.md`; run it before pushing.

Headings split by reader, not by level. Anything the model loads as instructions - `SKILL.md`, the files a skill links to, `agents/*.md`, `CONTRIBUTING.md` - uses UPPERCASE headings at every level, `#` through `###`. Anything a human reads on GitHub - `README.md`, `CHANGELOG.md` - uses sentence case. A heading inside a fenced block belongs to the artifact being templated and keeps whatever case that artifact needs.

## PUBLIC SAFETY

This repository is public. Before committing, strip local paths like `/Users/<name>`, private git remotes, real tracker keys and URLs, secrets, tokens, `.env` values, colleague names and emails, and raw session or tool output. Swap in neutral placeholders: `<user_home>`, `<github_owner>/<repo>`, `PROJ-123`.

## VERIFICATION

GitHub CI runs two jobs in `.github/workflows/ci.yml`:

- House style plus frontmatter: every skill needs a non-empty `description`; `user-invocable`, when present, must be a boolean.
- Strict Claude Code validation of the marketplace and every plugin directory.

Run the same checks locally from the repository root:

```bash
bash .github/scripts/lint-house-style.sh
claude plugin validate --strict .
claude plugin validate --strict plugins/dev
claude plugin validate --strict plugins/std
```

Run the workflow's Frontmatter lint shell block as well; it is the source of that check. Pass new Markdown paths explicitly to the house-style script before they are tracked. Check relative links, instruction-heading case, and `git diff --check`, including new files before committing.

Codex-specific checks are additional local checks, not part of the current GitHub CI. For `std`, use the `validate_plugin.py` and `quick_validate.py` validators supplied with Codex's `plugin-creator` and `skill-creator` system skills when available. Resolve them from the installed skill locations rather than committing machine-specific paths. Check matching manifest names/versions and that both clients discover the same `teach` implementation. Report a missing validator as unverified, not as a pass.

Document compatibility at the level exercised: catalog acceptance, installation, skill discovery, and complete workflows are separate checks. A manifest validator does not exercise learning or named-agent delegation. Use temporary projects for behavior checks and follow each plugin's verification scenarios when behavior changes. Documentation-only changes need source/command/link checks, not another full dialogue or execution run.

## LOCAL DEVELOPMENT AND RELEASE

### CLAUDE CODE

From the checkout root, run `claude --plugin-dir ./plugins/std` (replace `std` with `dev` for that plugin). This loads local content for the session without changing the configured marketplace. Restart the preview after edits.

### CODEX

The checked Codex CLI has no `--plugin-dir` option. Test the complete local package with a temporary Codex home, leaving the normal installation and configuration alone. Run from the checkout root:

```bash
nxs_preview_home=$(mktemp -d)
CODEX_HOME="$nxs_preview_home" codex plugin marketplace add "$PWD"
CODEX_HOME="$nxs_preview_home" codex plugin add std@nxs
CODEX_HOME="$nxs_preview_home" codex plugin list --marketplace nxs
CODEX_HOME="$nxs_preview_home" codex
```

Replace `std@nxs` with `dev@nxs` to load `dev`. The temporary home does not copy your usual authentication or global settings; sign in if required and configure only the test settings needed. Local project instructions still apply. Inspect the installed version before exercising a skill. Repeat `plugin add` after a versioned source change and start a new session. This verifies package loading; `dev` agent delegation still needs a separate workflow check. Keep temporary credentials out of commits and remove the preview directory when finished.

### INSTALLED RELEASES

For cached installations, first verify the configured source with `claude plugin marketplace list` or `codex plugin marketplace list`. A GitHub source sees published changes; editing a different local checkout does not update it. Refreshing a catalog alone does not update the installed plugin snapshot. Use the [installation and update instructions](README.md#update) after publishing the new version. Do not replace a user's configured marketplace or reinstall their plugins as part of a documentation or source edit unless requested.
