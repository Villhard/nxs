---
description: Commit existing changes in atomic groups when the user invokes /dev:commit or asks to commit work outside /dev:exec and /dev:fix. Do not activate for commit discussions or for staging and commits owned by those workflows.
argument-hint: "[optional scope hint]"
---

# /dev:commit

Commit existing changes in atomic groups, outside `/dev:exec` and `/dev:fix`. Their internal staging and commits follow their own rules and never invoke this command.

Accepted input: an optional scope hint. Without one, consider all existing changes for grouping. Stop on foreign or unclear ownership; "all changes" does not override the exclusions below.

Example: /dev:commit

## STANCE

Commit what is there. Keep working-file bytes unchanged throughout the command, not only at the end. Never temporarily remove unrelated edits, commit the file and restore them; never repair an overbroad commit by rewriting files and amending it. Writing code, running the build, and changing behavior belong elsewhere. `git push`, `--force`, and MR / PR creation stay out of this command - push only on a later explicit request.

## PROCEDURE

1. Read `git status`, unstaged and staged diffs, and untracked files. Establish the requested scope and record the original staged content before changing the index.
2. Classify the current state using the table below and name the selected case with its paths before any write. A selected path is **mixed** when its working-tree diff against HEAD contains another logical change. It stays mixed even if a patch could stage only the requested hunk: `commit --only` takes working-tree bytes, not that partial staged version.
3. If another group is staged and any selected path is mixed, stop now. Report both the staged foreign paths and the mixed path; ask the user to separate the changes. Do not create a patch, stage a hunk, alter files or commit. This case has no automatic isolation procedure.
4. For the remaining cases, group by logical change - one group per `feat` / `fix` / `refactor` / `chore` / `docs` unit. Separate a refactor from a feat or a fix even inside one file. For each group, in dependency order:
   - read both diffs for every selected path: a path may contain intended staged content and unrelated unstaged edits;
   - choose the index case below before staging. Never silently unstage, overwrite or include another group's content;
   - inspect the exact proposed commit diff, then commit with the specified command. Never use `git add -A` or `git add .`.
5. Verify that out-of-scope working and staged content was preserved. Report commits made and anything left uncommitted, with reasons.

| Index and selected paths | Action |
| --- | --- |
| Index is empty or contains only this group | Stage explicit intended paths or separable hunks. Verify the entire staged diff, then `git commit -m "<type>(<scope>): <subject>"`. Leave unrelated unstaged hunks untouched. |
| Other groups are staged; every changed hunk in each selected path belongs to this group | For a new untracked file, read its complete content and stage only that new path first; `--only` requires known paths. Inspect `git diff HEAD -- <selected paths>` as the proposed commit. Use `git commit --only -m "<type>(<scope>): <subject>" -- <selected paths>`; it commits those working-tree paths and retains other staged paths. Already tracked paths need no staging first. |
| Other groups are staged and a selected path mixes groups, or ownership is uncertain | Stop before changing the index; name the mixed paths and request separation or clarification. Do not use an alternate index, stash or whole-file commit to bypass this boundary. |

Example: a requested fix entirely in `limits.py` can use `--only` while an unrelated `README.md` remains staged. An intended fix sharing `limits.py` with unrelated unstaged edits cannot use a whole-file `git add` or `commit --only`.

## MESSAGE FORMAT

```
<type>(<scope>): <subject>
```

Single line, no body unless explicitly requested. Subject as short as possible and fully lowercase, abbreviations included ("seo", not "SEO"). Types: `feat` (new functionality), `fix` (bug fix), `refactor` (no behavior change), `chore` (deps, configs), `docs` (documentation).

Plain simple verbs: add, fix, remove, update, show, hide, validate. Never tighten, strengthen, refine, streamline, leverage, harden.

## RULES

- one commit is one logical change;
- do not commit unrelated files, large generated artifacts, foreign-branch files, or merge artifacts;
- do not amend a published commit;
- `--no-verify` only with explicit approval;
- after a failed hook, inspect the resulting state. No commit is assumed to exist. If fixing code is needed, stop and report it; once corrected, retry with a normal commit, never amend a prior commit;
- branches are `<type>/<short-desc>`, or `<type>/vr/<short-desc>` for work branches.

## STOP CONDITIONS

- nothing to commit;
- a secret, a credential, a large generated artifact, a foreign-branch file, or a merge artifact in the diff;
- a hunk spanning two logical changes that will not split cleanly;
- a group whose type or scope is unclear.

With nothing to commit, report a successful no-op without a question. For other stops, name the concrete blocker and request the missing choice or action.

## NEXT

Changes committed. `git push` only when you explicitly ask for it.
