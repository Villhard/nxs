---
name: dev-setup
description: Set up agent instructions when the user explicitly invokes /dev-setup. `global` wires clients to shared instructions and installs approved skill bundles; `project` proposes repository rules and checks. Both write only an approved diff. Add `--readiness` to either explicit mode for a report-only audit of the selected lead environment, without setup writes or installs. Not for discussing instructions; dev-spec records project specs and dev-rnd shapes work.
argument-hint: "[global|project] [--readiness]"
disable-model-invocation: true
---

# /dev-setup

Give the user's agents and a repository the settings the other dev skills rely on: an executor reads project specs on its path, tickets name a `**Branch:**` from the project's branch rule, a ticket's `Done when` runs "the full test suite and linter", and feature records under `.scratch/` stay out of Git. Audit, show one diff, write only what the user approves, then stop.

Accepted input: `project` or `global`, optionally followed by `--readiness`.

Example: /dev-setup project

Suggest the next command at a handoff; never start it automatically.

Handle `project --readiness` and `global --readiness` before normal setup: read [readiness](references/readiness.md), report and stop. Require an explicit mode with this flag. Skip the setup AUDIT, questions, diff, upstream bundle listing, INSTALL, WRITE and CHECK. Ordinary setup below retains its approval, repeat and decline contract.

## CONTRACT

Both modes follow these rules. Each mode's STANCE names the files it writes, its owned sections and its questions; its AUDIT names the files whose headings it counts and when it has nothing to propose.

- Approval: write nothing before the user approves the shown diff, and write exactly that diff, or a diff changed as the user asked and shown again. On decline, write nothing and report that every file is unchanged.
- Owned section: it runs from its heading line to the line before the next `#` or `##` heading, or to the end of the file. More than one heading of an owned section across the audited files stops the run: name the files and line numbers; the user merges them by hand.
- Repeat: an owned section is rewritten in place, and the diff proposes only the lines that change; a line edited inside it goes back to the audited line. Every byte outside the sections the diff touches stays as it was, including the file's final newline state.
- Custom rules belong outside the owned sections, where the audit reports a rule that states an owned line as covered, with the line that states it. When the user changes a line inside an owned section while approving, say that the next run proposes the audited line again and offer to put the custom rule outside the section instead.
- An audit with nothing to propose shows no diff: report "already set up" and stop.
- After writing, run the mode's CHECK and fix what fails before reporting.
- Report a missing item; never invent a command, rule or skill name to fill it.

## MODE

| Input | Action |
| --- | --- |
| `project --readiness` or `global --readiness` | Run only the bundled readiness report and stop |
| `project` | Run the steps below |
| `global` | Read [global mode](references/global.md) and follow it instead of the sections below |
| No argument, inside a Git repository (`git rev-parse --show-toplevel` succeeds) | Ask once: `project` for this repository or `global` for the user's agent instructions; then act on the answer as above |
| No argument, outside a Git repository | `global` |
| Anything else | Name the accepted values and stop |

## STANCE

This section through NEXT is the `project` mode.

- Write only the target instruction file, a new `CLAUDE.md` holding `@AGENTS.md`, and one `.scratch/` ignore line. Never code, other instruction files, the index or commits.
- Owned section (CONTRACT): one `## nxs` section in the target file. A branch rule outside it is reported as covered in AUDIT step 3.
- Questions: the mode, only when no argument was given, and the approval of the diff.

## AUDIT

Work from the repository root. Read before proposing anything; record each item as found, with its source path, or missing.

1. Instruction files: list the root (`ls -a`) for `AGENTS.md` and `CLAUDE.md` by exact name and resolve each with `realpath`. Names with the same `realpath` are one real file: read it and count its `## nxs` headings once. Choose the target with the first matching row:

   | Found | Target |
   | --- | --- |
   | Exactly one `## nxs` heading across the real files | The real file that holds it |
   | More than one `## nxs` heading across the real files | Stop as CONTRACT says, naming the real files |
   | Both names resolve to one real file | That real file, the symlink's target |
   | `CLAUDE.md` contains the line `@AGENTS.md` | `AGENTS.md` |
   | `AGENTS.md` only | `AGENTS.md` |
   | `CLAUDE.md` only | `CLAUDE.md` |
   | Both, independent | `AGENTS.md`; name `CLAUDE.md` as the alternative in the approval question |
   | Neither | Create `AGENTS.md` and a `CLAUDE.md` that holds `@AGENTS.md` |

   Edit a symlink's target, never the link itself. Never create a second instruction file next to an existing one.

2. The `## nxs` section, bounded as CONTRACT says: read it.

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
3. One question: approve the diff, approve it with `.gitignore` or the other target file, change specific lines, or decline.

The audit has nothing to propose when the section is current and `.scratch/` is ignored.

## WRITE

On approval (CONTRACT):

1. Write the instruction file changes.
2. Ignore line: for `.git/info/exclude` use `"$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"`, creating the directory when missing. Append `.scratch/` on its own line, adding a newline first when the file does not end with one. The same applies to `.gitignore`.

## CHECK

- The target file has exactly one `## nxs` heading, and a diff against its pre-write content touches only that section.
- A created `CLAUDE.md` holds `@AGENTS.md`.
- `git check-ignore -q .scratch/` exits 0 when an ignore line was approved.

## NEXT

Report the files changed or "nothing written", the items still missing, and where the ignore line went. When a tracked file changed, suggest `/dev-commit`.
