---
description: Commit the current working changes - splits them into atomic commits with conventional messages. Use when you want to commit changes made outside `/nxs:exec`.
argument-hint: "[optional scope hint]"
---

# /nxs:commit

Commit the changes already in the working tree, split into atomic commits. Use it for edits you made by hand, outside `/nxs:exec`. Self-contained skill. Output language and response style come from global rules, not this file.

Message format, the atomicity rule, staging hygiene, and git safety come from the `commit-conventions` background skill - load it and follow it. This command owns only the procedure of grouping and committing.

Accepted input: an optional hint to narrow scope or guide grouping; with nothing given, commit the whole working tree split into atomic commits.

Example: /nxs:commit

## STANCE

- Commit what is already there. This command does not write code, run the build, or change behavior - it stages and commits existing changes only.
- One commit = one logical change (`commit-conventions`). Split a mixed working tree into separate commits; do not squash unrelated work into one.
- HITL: never `git push`, never `--force`, never create an MR / PR. Push only on a later explicit request.

## PROCEDURE

1. Read the state: `git status` and `git diff` (staged and unstaged), including untracked files.
2. Group the changes by logical change - one group per `feat` / `fix` / `refactor` / `chore` / `docs` unit. Separate a refactor from a feat / fix even when they touch the same file.
3. For each group, in dependency order:
   - stage exactly that group: `git add <specific files>` (never `git add -A` / `git add .`); for a file that mixes groups, stage the intended hunks with `git add -p`;
   - check the staged diff matches the group;
   - commit with a conventional one-line message (`commit-conventions`): `git commit -m "<type>(<scope>): <subject>"`.
4. Report the commits made - one line each - and anything left uncommitted with the reason.

## STOP CONDITIONS

- nothing to commit (clean tree);
- a secret, credential, large generated artifact, foreign-branch file, or merge artifact in the diff - stop and ask;
- a hunk that spans two logical changes and cannot be split cleanly - ask how to group rather than guess;
- a group whose type or scope is unclear - ask, do not invent.

On any of these - stop and inform the user.

## NEXT

Changes committed. `git push` only when you explicitly ask for it.
