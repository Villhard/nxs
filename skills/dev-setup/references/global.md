# GLOBAL MODE

Read this when `/dev-setup` runs `global`. It wires Claude Code, Codex and OpenCode to one source of user instructions, `~/.agents/AGENTS.md`, adds the `## nxs` section the dev skills rely on, adds the rule groups the user accepts, installs the skill bundles the user chooses and writes their configuration. Audit, ask for the rule groups and bundles, show one diff, write only what the user approves, then stop.

`~` is `$HOME`. Work with absolute paths built from it.

## STANCE

- Write only the source, the three client instruction files, the three docs files under `~/.agents/docs/` and the parent directories they need; install skills only through the skills CLI command of INSTALL. Never project files, client settings, other installed skills, the index or commits.
- Write nothing before the user approves the shown diff, and write exactly that diff. A declined diff leaves every file unchanged and installs nothing.
- Never replace a client file that holds content: merge its content into the source through the diff first, and link it only after that write is checked.
- In the source, own the `## nxs` section, the `## Engineering skill defaults` section and the rule group sections the user accepted. A repeat rewrites those sections in place; every byte outside the touched sections stays as it was.
- `## nxs` and `## Engineering skill defaults` belong to the skill: the next run replaces an edit inside them with the template. Custom rules belong outside them, where the audit reports a rule that states a `## nxs` bullet as covered (AUDIT step 3).
- Questions: the mode, only when SKILL.md MODE asked it, the rule groups and bundles, in one round, and the approval of the diff. Report a missing item; never invent a rule or a skill name to fill it.

## AUDIT

Read before proposing anything; record each item as found, with its path, or missing.

1. Source `~/.agents/AGENTS.md`: missing, a regular file, or a symlink. Resolve a symlink with `realpath` and edit its target, never the link. Missing means the diff creates it.

2. Clients: inspect each path with `ls -la` and resolve symlinks with `realpath`. A path is wired when its `realpath` equals the source's `realpath`, checked before anything else, or when it matches the Wired column. Choose the proposal with the first matching row:

   | Client | Path | Wired |
   | --- | --- | --- |
   | Claude Code | `~/.claude/CLAUDE.md` | Holds the line `@~/.agents/AGENTS.md` (or `@` and the source's absolute path), or resolves to the source |
   | Codex | `~/.codex/AGENTS.md` | Symlink that resolves to the source |
   | OpenCode | `~/.config/opencode/AGENTS.md` | Symlink that resolves to the source |

   | Found | Proposal |
   | --- | --- |
   | Wired | Nothing. A source that is a symlink to a client file makes that file the source's real file: it is written as the source and never merged or linked |
   | Missing | Claude Code: create the file holding `@~/.agents/AGENTS.md`. Codex, OpenCode: the symlink to the source's absolute path |
   | Codex or OpenCode broken symlink | Replace it with the symlink; nothing to merge |
   | Codex or OpenCode file, or symlink to another file, with content byte-identical to the source | Replace it with the symlink; nothing to merge. A link's former target stays untouched |
   | Claude Code file without the import | Insert `@~/.agents/AGENTS.md` as its first line, followed by one blank line; keep the rest. The file is the user's Claude-only layer |
   | Codex or OpenCode regular file, or symlink to another file | Merge its content into the source (step 4), then replace the path with the symlink. A link's former target stays untouched unless it is a client path: a Codex or OpenCode file takes its own row; `~/.claude/CLAUDE.md` has its content, without the import line, merged and is rewritten to hold only `@~/.agents/AGENTS.md`, so Claude Code does not load the text twice |

3. The `## nxs` section in the source: it runs from the `## nxs` line to the line before the next `#` or `##` heading, or to the end of the file. More than one `## nxs` heading across the source and the content to merge stops the run (content linked without a merge is not counted): name the files and line numbers; the user merges them by hand. Build the expected section from [global section](../assets/global-section.md), one decision per bullet, from the source and the content to merge outside `## nxs`:

   | That text | The bullet |
   | --- | --- |
   | States its rule, in any wording | Covered: not written; report it with the line that states it |
   | Contradicts it | Not written; report it with the conflicting line |
   | Neither | Written |

   Expected section with no bullet left and no section found: no `## nxs` section is created. A found section is compared with the expected one; a repeat proposes only the lines that change: a line edited inside the found section goes back to the expected one, and a bullet already in the found section that became covered stays and is reported as covered with the line that states it.

4. Merge: group the client files to merge by `realpath` and merge each real file once. Take its content without its owned sections, `## nxs` and `## Engineering skill defaults`, which the source's sections replace (steps 3 and 7). Append it to the end of the source after one blank line, verbatim, under its own heading `## Merged from <real path>`, so an owned section that ends the source never runs over it. Lines the source already holds stay in the merged text: the user removes duplicates in the diff.

5. Rule groups: read [rule groups](../assets/rules.md). For each rule, decide from the source and the content to merge whether it is already stated, in any wording, or contradicted. A stated rule is not offered; a contradicted rule is not offered and is reported with the conflicting line. A group with no rule left is reported as covered and not offered.

6. Bundles: read [skill bundles](../assets/bundles.md).
   - Installed: a skill is installed when `~/.agents/.skill-lock.json` lists its name under `skills`, or `<name>/SKILL.md` exists under `~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/` or `~/.config/opencode/skills/`. Record the source of each mark.
   - Upstream: run `npx skills@latest add mattpocock/skills -l` and take the skill names it lists. A bundle name missing from the listing is reported as missing upstream and dropped from its bundle. A failed listing verifies no name: report the error; the bundles are still offered, and INSTALL runs no command.
   - A bundle whose remaining skills are all installed is reported as installed and not offered. Every other bundle is offered with its purpose line, its `Needs:` line, its skills, and each installed one marked; a bundle with `Recommended.` is marked as recommended.
   - Each skill under "Never offered" that is installed is reported as installed; nothing is installed or removed.

7. Engineering config: needed when a bundle skill is installed, one is chosen in BUNDLES, or the content to merge holds a `## Engineering skill defaults` section. Compare:
   - the `## Engineering skill defaults` section in the source (bounded like `## nxs`) with [engineering section](../assets/engineering-section.md); more than one such heading stops the run like `## nxs`;
   - each of `~/.agents/docs/issue-tracker.md`, `triage-labels.md` and `domain.md` with its template: [issue tracker](../assets/issue-tracker.md), [triage labels](../assets/triage-labels.md), [domain](../assets/domain.md). Resolve a symlink with `realpath` and edit its target.

   Record each as current, missing or changed. Not needed: propose nothing for it.

## RULE GROUPS AND BUNDLES

When at least one group or bundle is offered, ask one question before the diff: for each offered group, show its remaining rules and ask accept, edit or decline; for each offered bundle, show its purpose, its recommended mark and `Needs:` line, and its skills with the installed marks, and ask install or decline. An edit takes the user's wording for that group's rules. Skip the question when nothing is offered.

Accepted rules go into the source:

- a `## <group>` section with the template heading, appended at the end of the source after one blank line, in template order, before a newly appended `## Engineering skill defaults` or `## nxs` section;
- when the source already has a `## <group>` heading by that exact name, the rules are appended at the end of that section instead.

A chosen bundle adds its uninstalled skills to the install list and makes the engineering config needed (step 7). Then add dependencies: for each skill on the install list, each skill its `needs` names that is neither installed nor on the list joins the list, marked "required by <skill>" with the first skill that needs it; repeat for each added skill. A dependency missing upstream is reported with the skill that needs it and not added. Every group and bundle declined adds no rule lines and no install; the diff still holds the wiring, the `## nxs` section and the engineering config when they are missing.

## PROPOSE

Show, in one message:

1. The audit: the source, each client with its state and proposal, the `## nxs` section as current, missing or changed with its covered and conflicting bullets, the rule groups as accepted, declined or covered, with any conflict, the bundles as chosen, declined or installed, with names missing upstream, each added dependency as `<name>: required by <skill>` and installed "Never offered" skills, and the engineering config items as current, missing or changed.
2. One unified diff of every proposed write: the source changes (merged content, rule groups, the `## Engineering skill defaults` section and the `## nxs` section, each appended at the end of the source after one blank line in that order or replacing an existing section's lines in place), each docs file created or edited, each created or edited Claude Code file, and each symlink as `<path> -> <source absolute path>`, marking a replaced file and its merged source lines. An existing docs file is shown as its own diff against the template, never as a replacement.
3. The install command of INSTALL, when the install list is not empty, followed by each added dependency as `<name>: required by <skill>`.
4. One question: approve the diff and the install, change specific lines, or decline. A line changed inside `## nxs` or `## Engineering skill defaults` holds only until the next run, which restores the template: when the user changes one, say so and offer to put the custom rule outside the section instead.

An audit with every client wired, the `## nxs` section current or fully covered, no accepted rule, no chosen bundle and the engineering config current or not needed proposes no diff: report "already set up" and stop.

## WRITE

On approval of the diff, or of a diff changed as the user asked and shown again:

1. Run INSTALL.
2. Write the source, creating `~/.agents/` when missing. Keep every byte outside the touched sections, including the file's final newline state.
3. Check that the source holds every merged line from step 4 of AUDIT. Stop on a mismatch, before any link: the client files are still in place.
4. Write each approved docs file, creating `~/.agents/docs/` when missing.
5. Write the Claude Code file, and create each symlink with `mkdir -p <parent>` and `ln -sfn "$HOME/.agents/AGENTS.md" <path>`, replacing symlinks before regular files. Right before each `ln -sfn`, compare `realpath <path>` with `realpath "$HOME/.agents/AGENTS.md"`: when they are equal, skip the path; it is already wired.

On decline, write nothing, install nothing and report that every file is unchanged.

## INSTALL

The install list holds the uninstalled, upstream-verified skills of the chosen bundles in bundle order, then the added dependencies in the order they were added. Run once, with every name after one `-s`:

```bash
npx skills@latest add -g mattpocock/skills -s <name> <name> ... -a claude-code codex opencode -y
```

Then check that `~/.agents/.skill-lock.json` lists each name. When `npx` is unavailable, the command fails, a name is still missing, or the upstream listing failed in AUDIT, report the exact command for the user to run and continue with the next WRITE step.

## CHECK

- The source has at most one `## nxs` heading, none only when every bullet was covered, and at most one `## Engineering skill defaults` heading; a diff against its pre-write content touches only the merged content, the accepted group sections and those two sections.
- Every client path is wired as AUDIT step 2 defines it.
- No accepted rule appears twice in the source.
- Each written docs file matches the approved diff.

Fix what fails before reporting.

## NEXT

Report the files changed or "nothing written", each client's wiring, the merged files, the declined, covered and conflicting rules and `## nxs` bullets, the installed skills, and any install command left for the user. Suggest `/dev-setup project` inside a repository.
