---
name: nxs-setup
description: Prepare an approved package for a scoped agent setup goal or project configuration, or report readiness.
argument-hint: "[global|project|goal] [--readiness]"
disable-model-invocation: true
---

# /nxs-setup

Audit a concrete setup goal, project instructions or shared global configuration. Keep useful project-spec reading, branch conventions, actual check commands and private local artifacts aligned with the requested scope. Tickets and saved feature records are optional, not prerequisites for development. Show one exact diff package, write only what the user approves, then stop. Setup is a separate support operation, not a required development stage.

Accepted input: `project`, `global` or a concrete goal; `project --readiness` and `global --readiness` run a report-only audit.

Example: /nxs-setup project

Suggest the next command at a handoff; never start it automatically.

Handle `project --readiness` and `global --readiness` before normal setup: read [readiness](references/readiness.md), report and stop. Require an explicit mode with this flag. Skip the setup audit, questions, proposal, writes and checks. Ordinary setup below retains its approval, repeat and decline contract.

## CONTRACT

Every setup scope follows these rules. Each mode's STANCE names the files it writes, its owned sections and its questions; its AUDIT names the files whose headings it counts and when it has nothing to propose.

- Approval: write nothing before the user approves the shown diff, and write exactly that diff, or a diff changed as the user asked and shown again. On decline, write nothing and report that every file is unchanged.
- Owned section: it runs from its heading line to the line before the next `#` or `##` heading, or to the end of the file. More than one heading of an owned section across the audited files stops the run: name the files and line numbers; the user merges them by hand.
- Repeat: an owned section is rewritten in place, and the diff proposes only the lines that change; a line edited inside it goes back to the audited line. Every byte outside the sections the diff touches stays as it was, including the file's final newline state.
- Custom rules belong outside the owned sections, where the audit reports a rule that states an owned line as covered, with the line that states it. When the user changes a line inside an owned section while approving, say that the next run proposes the audited line again and offer to put the custom rule outside the section instead.
- An audit with nothing to propose shows no diff: report "already set up" and stop.
- After writing, run the mode's CHECK and fix what fails before reporting.
- Report a missing item; never invent a command, rule or skill name to fill it.
- Reconcile source and target changes before applying the package. A stale diff cannot overwrite concurrent edits; show and obtain approval for uncovered revisions. Preserve unrelated bytes, symlinks and settings, and keep secrets and private configuration out of shared files.
- Do not install, update or remove skills, add client hooks, migrate user task records or rewrite personal configuration merely because source contracts changed. Report relevant installation provenance separately; source presence and wiring do not prove native registration or workflow compatibility.

## MODE

| Input | Action |
| --- | --- |
| `project --readiness` or `global --readiness` | Run only the bundled readiness report and stop |
| `project` | Run the steps below |
| `global` | Follow [global setup](references/global.md); consult the [capability map](references/capabilities.md) |
| Concrete goal | Follow GOAL below |
| No argument | Ask for the intended project or concrete setup goal |
| Unsupported input | Ask for a concrete scope and stop |

## GOAL

For a specific instruction, document or setting, audit the named target and relevant existing sources. Ask only for missing material scope or authority. Read [writing for agents](references/writing-for-agents.md) for agent instructions. Show one complete package of exact file diffs, target paths and setting changes, including privacy consequences, then obtain approval of that package. A narrow goal never implies project or global setup. Preserve unrelated bytes, symlinks and settings; do not copy secrets or private configuration into shared files. Decline writes nothing; an already-current audit stops without a proposal. Apply exactly the approved package and verify the resulting changes.

## STANCE

This section through NEXT is the `project` mode. Read [writing for agents](references/writing-for-agents.md) when proposing instructions.

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
