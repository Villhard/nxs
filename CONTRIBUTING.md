# CONTRIBUTING

Read these shared rules and the [dev rules](plugins/dev/CONTRIBUTING.md). `CLAUDE.md` and `AGENTS.md` are equivalent entry points.

## STRUCTURE

Root files describe the marketplace. Installed plugin content lives under `plugins/<name>/`:

```text
.claude-plugin/marketplace.json
plugins/<name>/
  .claude-plugin/plugin.json
  .codex-plugin/plugin.json    # optional
  skills/<skill>/SKILL.md
  skills/<skill>/references/   # optional
  skills/<skill>/assets/       # optional
  skills/<skill>/scripts/      # optional
  README.md CONTRIBUTING.md CHANGELOG.md
```

Create a plugin only for a distinct subject. Its Claude Code manifest needs `name`, `description`, `version`, `author`, `license`, `repository` and a plugin-directory `homepage`. Optional Codex metadata uses the same name/version and `skills: "./skills/"`. Add a catalog entry with `name`, `source`, `category` and `description`, and link the plugin from the root README.

## STYLE AND SAFETY

Write concise English with ASCII hyphens and straight quotes. Use UPPERCASE instruction headings and sentence case in README and CHANGELOG. Artifact templates retain their required headings.

Keep private paths/remotes, tracker identifiers, secrets, environment values, personal contact details and raw session output out of public changes. Use neutral examples.

## INSTRUCTION CONTRACTS

README explains how to use the plugin; CONTRIBUTING explains how to change it. Skills, roles and references own the full execution contract. Link to those rules instead of retelling them in guides. Keep model names and evaluation results out of guides.

- State inputs, entry checks, ordered actions, outputs, stops and handoffs. Put exceptions beside the affected step; use tables for competing states.
- Give descriptions a concrete trigger, result and distinction from neighboring commands. Separate invocation from discussion and internal operations.
- Mark required and optional template fields. Preserve structural names and distinguish completed requirements from removed ones.
- Make installed skills self-contained through bundled resources read at the point of use. Root documents are not runtime context.
- Reuse user authorization within its scope. Report missing evidence explicitly.
- Test normal use and plausible misreadings through actions and artifacts. Line count and structural lint do not prove instruction quality.

## VERSIONS

Plugins version independently; root files have no version. Every bundled edit, including documentation, metadata and file modes, needs a release bump, matching manifest versions and a dated CHANGELOG entry. Start new plugins at `0.1.0`. Keep every past version heading and date, newest first; past entries may be condensed but never dropped.

A CHANGELOG entry lists what changed under Keep a Changelog headings (`Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`). One line per bullet, naming the command, role or artifact that changed. No introductory paragraphs, rationale, before/after comparisons or file listings: the commit and the owning instruction carry those.

An unchanged contract is a patch. During `0.x`, contract changes require a minor release; after `1.0.0`, breaking changes require a major release. Each plugin defines its versioned contract.

## CHECKS

Run from the repository root with Git, Bash, Python 3 and Claude Code available:

```bash
bash .github/scripts/check-marketplace.sh
python3 .github/scripts/test_check_marketplace.py
bash .github/scripts/lint-house-style.sh
claude plugin validate --strict .
claude plugin validate --strict plugins/dev
git diff --check
```

The checker supports three read-only comparisons:

| Arguments | Compared state |
| --- | --- |
| none | Working files against HEAD |
| `--staged` | Index against HEAD |
| `--base REF --head REF` | Two Git snapshots |

The first two require HEAD. See the [checker](.github/scripts/check-marketplace.py) and [CI](.github/workflows/ci.yml) for validation and snapshot selection. Metadata checks use a limited YAML subset; native validation is still required. Link checks do not cover anchors or every Markdown form: inspect links, headings and the final diff yourself. Pass untracked Markdown paths explicitly to the style script.

The optional [Claude Code hook](.claude/hooks/check-version-bump.sh) checks the index. Stage first and use a plain `git commit -m "..."`; combined commands, pathspecs and options such as `--only` or `--amend` are rejected. Run the checker directly in Codex.

If a plugin has a Codex manifest, also run the installed `plugin-creator` validator and `skill-creator` quick validator. Report unavailable checks. For behavior changes, use disposable projects and the plugin's scenarios; documentation-only edits need source, command and link checks, not repeated workflows.

## LOCAL DEVELOPMENT AND RELEASE

From the checkout root:

**Claude Code**

```bash
claude --plugin-dir ./plugins/dev
```

**Codex**

```bash
nxs_preview_home=$(mktemp -d)
CODEX_HOME="$nxs_preview_home" codex plugin marketplace add "$PWD"
CODEX_HOME="$nxs_preview_home" codex plugin add dev@nxs
CODEX_HOME="$nxs_preview_home" codex
```

The temporary Codex home has no usual authentication or global settings; sign in if needed. Project instructions still apply. Repeat `plugin add` after versioned edits. Restart either client after changes and remove the temporary home when finished, keeping credentials out of Git.

Publish the version before [updating installations](README.md#update). Do not update installed plugins or replace configured marketplaces during source edits unless requested.
