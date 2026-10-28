# GLOBAL MODE

Read this when `/dev-setup` runs `global`. It wires Claude Code, Codex and OpenCode to one source of user instructions, `~/.agents/AGENTS.md`, adds the `## nxs` section the dev skills rely on, and adds the rule groups the user accepts. Audit, ask for the rule groups, show one diff, write only what the user approves, then stop.

`~` is `$HOME`. Work with absolute paths built from it.

## STANCE

- Write only the source, the three client instruction files and the parent directories they need. Never project files, client settings, the index or commits.
- Write nothing before the user approves the shown diff, and write exactly that diff. A declined diff leaves every file unchanged.
- Never replace a client file that holds content: merge its content into the source through the diff first, and link it only after that write is checked.
- In the source, own the `## nxs` section and the rule group sections the user accepted. A repeat rewrites those sections in place; every byte outside the touched sections stays as it was.
- Questions: the mode, only when SKILL.md MODE asked it, the rule groups, in one round, and the approval of the diff. Report a missing item; never invent a rule to fill it.

## AUDIT

Read before proposing anything; record each item as found, with its path, or missing.

1. Source `~/.agents/AGENTS.md`: missing, a regular file, or a symlink. Resolve a symlink with `realpath` and edit its target, never the link. Missing means the diff creates it.

2. Clients: inspect each path with `ls -la` and resolve symlinks with `realpath`. A path is wired when it matches the Wired column. Choose the proposal with the first matching row:

   | Client | Path | Wired |
   | --- | --- | --- |
   | Claude Code | `~/.claude/CLAUDE.md` | Holds the line `@~/.agents/AGENTS.md` (or `@` and the source's absolute path), or resolves to the source |
   | Codex | `~/.codex/AGENTS.md` | Symlink that resolves to the source |
   | OpenCode | `~/.config/opencode/AGENTS.md` | Symlink that resolves to the source |

   | Found | Proposal |
   | --- | --- |
   | Wired | Nothing |
   | Missing | Claude Code: create the file holding `@~/.agents/AGENTS.md`. Codex, OpenCode: the symlink to the source's absolute path |
   | Claude Code file without the import | Insert `@~/.agents/AGENTS.md` as its first line, followed by one blank line; keep the rest. The file is the user's Claude-only layer |
   | Codex or OpenCode regular file, or symlink to another file | Merge its content into the source (step 4), then replace the path with the symlink. A link's former target stays untouched |
   | Codex or OpenCode broken symlink | Replace it with the symlink; nothing to merge |
   | Content identical to the source | Replace it with the symlink; nothing to merge |

3. The `## nxs` section in the source: it runs from the `## nxs` line to the line before the next `#` or `##` heading, or to the end of the file. More than one `## nxs` heading across the source and the content to merge stops the run: name the files and line numbers; the user merges them by hand. Compare a found section with [global section](../assets/global-section.md); a repeat proposes only the lines that change.

4. Merge: for each client file to merge, take its content without its own `## nxs` section, which the source's section replaces. Append it to the end of the source after one blank line, verbatim, under a comment line `<!-- merged from <path> -->`. Lines the source already holds stay in the merged text: the user removes duplicates in the diff.

5. Rule groups: read [rule groups](../assets/rules.md). For each rule, decide from the source and the content to merge whether it is already stated, in any wording, or contradicted. A stated rule is not offered; a contradicted rule is not offered and is reported with the conflicting line. A group with no rule left is reported as covered and not offered.

## RULE GROUPS

When at least one group is offered, ask one question before the diff: for each offered group, show its remaining rules and ask accept, edit or decline. An edit takes the user's wording for that group's rules. Skip the question when no group is offered.

Accepted rules go into the source:

- a `## <group>` section with the template heading, appended at the end of the source after one blank line, in template order, before a newly appended `## nxs` section;
- when the source already has a `## <group>` heading by that exact name, the rules are appended at the end of that section instead.

Every group declined adds no rule lines; the diff still holds the wiring and the `## nxs` section when they are missing.

## PROPOSE

Show, in one message:

1. The audit: the source, each client with its state and proposal, the `## nxs` section as current, missing or changed, and the rule groups as accepted, declined or covered, with any conflict.
2. One unified diff of every proposed write: the source changes (merged content, rule groups, the `## nxs` section in the shape of [global section](../assets/global-section.md), appended at the end of the source after one blank line or replacing the existing section's lines in place), each created or edited Claude Code file, and each symlink as `<path> -> <source absolute path>`, marking a replaced file and its merged source lines.
3. One question: approve the diff, change specific lines, or decline.

An audit with every client wired, the `## nxs` section current and no accepted rule proposes no diff: report "already set up" and stop.

## WRITE

On approval of the diff, or of a diff changed as the user asked and shown again:

1. Write the source, creating `~/.agents/` when missing. Keep every byte outside the touched sections, including the file's final newline state.
2. Check that the source holds every merged line from step 4 of AUDIT. Stop on a mismatch, before any link: the client files are still in place.
3. Write the Claude Code file, and create each symlink with `mkdir -p <parent>` and `ln -sfn "$HOME/.agents/AGENTS.md" <path>`.

On decline, write nothing and report that every file is unchanged.

## CHECK

- The source has exactly one `## nxs` heading, and a diff against its pre-write content touches only the merged content, the accepted group sections and the `## nxs` section.
- Every client path matches its Wired column.
- No accepted rule appears twice in the source.

Fix what fails before reporting.

## NEXT

Report the files changed or "nothing written", each client's wiring, the merged files, and the declined, covered and conflicting rules. Suggest `/dev-setup project` inside a repository.
