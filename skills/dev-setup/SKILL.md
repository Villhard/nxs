---
name: dev-setup
description: Set up agent instructions for the dev skills when the user explicitly invokes /dev-setup. `global` wires Claude Code, Codex and OpenCode to `~/.agents/AGENTS.md` and adds the `## nxs` section and accepted working rules, and installs the chosen mattpocock/skills bundles with their tracker config; `project` writes a repository `## nxs` section with the branch rule and check commands and keeps `.scratch/` out of Git. Each mode audits, shows one diff and writes only after approval. Not for discussing instructions; dev-spec records project specs and dev-rnd shapes work.
argument-hint: "[global|project]"
disable-model-invocation: true
---

# /dev-setup

Give the user's agents and a repository the settings the other dev skills rely on: an executor reads project specs on its path, tickets name a `**Branch:**` from the project's branch rule, a ticket's `Done when` runs "the full test suite and linter", and feature records under `.scratch/` stay out of Git. Audit, show one diff, write only what the user approves, then stop.

Accepted input: `project` or `global`.

Example: /dev-setup project

Suggest the next command at a handoff; never start it automatically.

## MODE

| Input | Action |
| --- | --- |
| `project` | Run the steps below |
| `global` | Read [global mode](references/global.md) and follow it instead of the sections below |
| No argument, inside a Git repository (`git rev-parse --show-toplevel` succeeds) | Ask once: `project` for this repository or `global` for the user's agent instructions; then act on the answer as above |
| No argument, outside a Git repository | `global` |
| Anything else | Name the accepted values and stop |

## STANCE

This section through NEXT is the `project` mode.

- Write only the target instruction file, a new `CLAUDE.md` holding `@AGENTS.md`, and one `.scratch/` ignore line. Never code, other instruction files, the index or commits.
- Write nothing before the user approves the shown diff, and write exactly that diff. A declined diff leaves every file unchanged.
- Own one `## nxs` section in the target file. A repeat rewrites that section in place; every byte outside it stays as it was.
- The section belongs to the skill: the next run replaces an edit inside it with the audited line. Custom rules belong outside it, where the audit reports a branch rule as covered (AUDIT step 3).
- Questions: the mode, only when no argument was given, and the approval of the diff. Report a missing item; never invent a command or rule to fill it.

## AUDIT

Work from the repository root. Read before proposing anything; record each item as found, with its source path, or missing.

1. Instruction files: list the root (`ls -a`) for `AGENTS.md` and `CLAUDE.md` by exact name, and note a symlink and its target. Choose the target with the first matching row:

   | Found | Target |
   | --- | --- |
   | Exactly one `## nxs` heading in either file | That file |
   | More than one `## nxs` heading across both files | Stop: name the files and line numbers; the user merges them by hand |
   | One file is a symlink to the other | The symlink's target |
   | `CLAUDE.md` contains the line `@AGENTS.md` | `AGENTS.md` |
   | `AGENTS.md` only | `AGENTS.md` |
   | `CLAUDE.md` only | `CLAUDE.md` |
   | Both, independent | `AGENTS.md`; name `CLAUDE.md` as the alternative in the approval question |
   | Neither | Create `AGENTS.md` and a `CLAUDE.md` that holds `@AGENTS.md` |

   Edit a symlink's target, never the link itself. Never create a second instruction file next to an existing one.

2. The `## nxs` section: it runs from the `## nxs` line to the line before the next `#` or `##` heading, or to the end of the file. Read it; the repeat proposes only the lines that change.

3. Branch rule: read the instruction files and `CONTRIBUTING.md` for a stated branch naming rule, and list existing branches (`git for-each-ref --format='%(refname:short)' refs/heads refs/remotes`).

   - A rule stated outside the `## nxs` section: report it as covered with the line that states it; the `Branches:` line names that file instead of restating the rule.
   - No stated rule, and most existing branches follow one other pattern: propose that pattern and say it was inferred from branch names.
   - Otherwise: propose `<type>/<short-description>` with `<type>` one of `feat`, `fix`, `refactor`, `chore`, `docs`.

4. Check commands: find the test suite, linter and type checker commands. Read each source that exists:

   | Source | What counts |
   | --- | --- |
   | `Makefile`, `justfile` | Targets or recipes for testing, linting and type checking (`test`, `lint`, `typecheck`, `check` and similar names): `make <target>`, `just <recipe>` |
   | `package.json` | `scripts` entries for the same purposes, run with the package manager its lock file shows |
   | CI config (`.github/workflows/*.yml`, `.gitlab-ci.yml` and other CI files in the root) | Commands its steps run |
   | `pyproject.toml` | Tool configuration (`[tool.pytest.ini_options]`, `[tool.ruff]`, `[tool.mypy]`, `[tool.pyright]` and similar), run the way the lock file or CI shows, such as `uv run pytest` |

   Propose the command from the first source in that order; when sources disagree, list each in the audit. A Make or just target that only calls the tool counts as one command. A purpose with no command is missing: the section drops its line.

5. `.scratch/`: run `git check-ignore -q .scratch/`. Exit 0 means ignored and nothing to propose; exit 1 means unignored; any other exit stops with the error.

## PROPOSE

Show, in one message:

1. The audit: each item found, with its source, or missing.
2. One unified diff of every proposed write:
   - the `## nxs` section in the shape of [project section](assets/project-section.md), appended at the end of the target file after one blank line, or replacing the existing section's lines in place;
   - for no instruction file, the new `AGENTS.md` holding the section and the new `CLAUDE.md` holding `@AGENTS.md`;
   - for an unignored `.scratch/`, the line `.scratch/` in `.git/info/exclude`: private to this clone, recommended. Name `.gitignore` as the alternative: shared with everyone who clones the repository.
3. One question: approve the diff, approve it with `.gitignore` or the other target file, change specific lines, or decline. A line changed inside `## nxs` holds only until the next run, which proposes the audited line again: when the user changes one, say so and offer to put the custom rule outside the section instead.

An audit that finds the section current and `.scratch/` ignored proposes no diff: report "already set up" and stop.

## WRITE

On approval of the diff, or of a diff changed as the user asked and shown again:

1. Write the instruction file changes. Keep every byte outside the `## nxs` section, including the file's final newline state.
2. Ignore line: for `.git/info/exclude` use `"$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"`, creating the directory when missing. Append `.scratch/` on its own line, adding a newline first when the file does not end with one. The same applies to `.gitignore`.

On decline, write nothing and report that every file is unchanged.

## CHECK

- The target file has exactly one `## nxs` heading, and a diff against its pre-write content touches only that section.
- A created `CLAUDE.md` holds `@AGENTS.md`.
- `git check-ignore -q .scratch/` exits 0 when an ignore line was approved.

Fix what fails before reporting.

## NEXT

Report the files changed or "nothing written", the items still missing, and where the ignore line went. When a tracked file changed, suggest `/dev-commit`.
