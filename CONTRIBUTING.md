# CONTRIBUTING

Read these shared rules and the relevant plugin's rules: [dev](plugins/dev/CONTRIBUTING.md) or [std](plugins/std/CONTRIBUTING.md). `CLAUDE.md` and `AGENTS.md` are equivalent entry points.

## STRUCTURE

Everything bundled lives under `plugins/<name>/`; root files are not bundled.

```text
.claude-plugin/marketplace.json
plugins/<name>/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json     # explicit Codex manifest; currently std only
  skills/<skill>/SKILL.md
  README.md CONTRIBUTING.md CHANGELOG.md
```

Create a plugin only for a distinct subject; otherwise extend the existing plugin. Include:

- A Claude Code manifest with `name`, `description`, initial `version: "0.1.0"`, `author`, `license`, `repository`, and plugin-directory `homepage`.
- For explicit Codex metadata, a manifest with matching name/version and `skills: "./skills/"`. Use one shared skill implementation for shared behavior.
- README, CHANGELOG, and plugin-specific CONTRIBUTING when needed. Add agents or other components only when required and supported by the intended client.
- A catalog entry with `name`, `source: "./plugins/<name>"`, `category`, and `description`; link the plugin from the root README.

## STYLE AND SAFETY

Write concise English with ASCII hyphens and straight quotes. Use UPPERCASE headings in instructions, including skill references, agents, CONTRIBUTING, CLAUDE, and AGENTS. Use sentence case in README and CHANGELOG. Fenced artifact templates retain their required heading case.

Before committing to this public repository, remove private paths/remotes, tracker keys/URLs, secrets, environment values, personal contact details, and raw session output. Use neutral placeholders such as `<user_home>`, `<github_owner>/<repo>`, and `PROJ-123`.

## VERSIONS

Plugins version independently; root files have no version. Every bundled edit, including documentation, requires matching versions in all plugin manifests and a new CHANGELOG entry. Preserve history; use Keep a Changelog with newest entries first.

An unchanged contract is a patch. During `0.x`, contract changes require a minor release. Declare stability at `1.0.0`; subsequent breaking changes require a major release. Plugin CONTRIBUTING defines its contract. Renaming a plugin changes its command and agent names.

## CHECKS

From the repository root:

```bash
bash .github/scripts/lint-house-style.sh
claude plugin validate --strict .
claude plugin validate --strict plugins/dev
claude plugin validate --strict plugins/std
git diff --check
```

Also run the Frontmatter lint shell block in [CI](.github/workflows/ci.yml). Every skill needs a nonempty `description`; `user-invocable`, if present, must be boolean. GitHub CI runs house-style/frontmatter and strict Claude Code catalog/plugin validation.

Pass untracked Markdown paths explicitly to the house-style script. Check links, anchors, instruction-heading case, and the final diff, including new files.

For `std`, additionally run `validate_plugin.py` from Codex's `plugin-creator` system skill and `quick_validate.py` from `skill-creator`. Resolve their installed locations locally. Check matching manifests and shared skill discovery in both clients. These Codex checks are local, outside current CI; report missing validators as unverified.

For behavior changes, use temporary projects and the plugin's scenarios. Record installation, discovery, and complete workflow results separately. Documentation-only changes need source, command, and link checks, without repeating full workflows.

## LOCAL DEVELOPMENT AND RELEASE

Run previews from the checkout root; replace `std` with `dev` as needed.

**Claude Code**

```bash
claude --plugin-dir ./plugins/std
```

Restart after edits.

**Codex**

Use a temporary home for the local package; the checked CLI has no `--plugin-dir`:

```bash
nxs_preview_home=$(mktemp -d)
CODEX_HOME="$nxs_preview_home" codex plugin marketplace add "$PWD"
CODEX_HOME="$nxs_preview_home" codex plugin add std@nxs
CODEX_HOME="$nxs_preview_home" codex plugin list --marketplace nxs
CODEX_HOME="$nxs_preview_home" codex
```

The temporary home has no usual authentication or global settings; sign in if needed. Project instructions still apply. Repeat `plugin add` after a versioned edit and start a new session. Remove the preview directory when finished; keep its credentials out of git.

For releases, publish the version, then follow [updates](README.md#update). Do not replace configured marketplaces or update installed plugins during source edits unless requested.
