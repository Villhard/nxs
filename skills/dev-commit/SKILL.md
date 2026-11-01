---
name: dev-commit
description: Commit existing changes in atomic groups when the user invokes /dev-commit or asks to commit work, including requests with limits such as "commit only X" or "leave Y staged". Use this skill for every commit instead of a direct git commit. Do not activate for commit discussions.
argument-hint: "[optional scope hint]"
---

# /dev-commit

Commit existing changes in atomic groups within explicit authorization. An approved `dev-exec` checkpoint may apply this procedure in the same session; it does not start a nested client or bypass any boundary.

Accepted input: an optional scope hint or explicitly approved checkpoint scope. Without one, consider all existing changes for grouping, not as permission to include foreign work. Stop on foreign or unclear ownership; "all changes" does not override the exclusions below. A ready ticket, implementation approval without commits or a saved handoff alone does not authorize a commit. An existing `Do not commit` instruction remains binding unless a specific revision is separately approved.

Example: /dev-commit

## STANCE

Commit what is there. Keep working-file bytes unchanged throughout the command, not only at the end. Never temporarily remove unrelated edits, commit the file and restore them; never repair an overbroad commit by rewriting files and amending it. Writing code, running the build, and changing behavior belong elsewhere. `git push`, `--force`, and MR / PR creation stay out of this command - push only on a later explicit request. Reconcile an interrupted or uncertain commit against actual Git state before proceeding; never repeat it automatically.

## PROCEDURE

1. Read `git status`, unstaged and staged diffs, and untracked files. Establish the requested scope and applicable commit authorization before any index write. Record pre-commit HEAD and the original staged content; distinguish intended task changes from foreign work and retain any supplied checkpoint/baseline context. Missing authority stops the affected commit, not permission to widen it.
2. Classify the current state using the table below and name the selected case with its paths before any write. A selected path is **mixed** when its working-tree diff against HEAD contains another logical change. It stays mixed even if a patch could stage only the requested hunk: `commit --only` takes working-tree bytes, not that partial staged version.
3. If another group is staged and any selected path is mixed, stop now under the third row of the table below: report both the staged foreign paths and the mixed path and ask the user to separate the changes. This case has no automatic isolation procedure.
4. For the remaining cases, group by logical change - one group per `feat` / `fix` / `refactor` / `chore` / `docs` unit. Separate a refactor from a feat or a fix even inside one file. For each group, in dependency order:
   - read both diffs for every selected path: a path may contain intended staged content and unrelated unstaged edits;
   - choose the index case below before staging. Never silently unstage, overwrite or include another group's content;
   - inspect the exact proposed commit diff, then commit with the specified command.
5. Verify resulting commit and parent OIDs, actual changed paths and approved scope, and that out-of-scope working and staged content was preserved. Report commits made and remaining staged, unstaged and untracked task work, identifying foreign content separately and giving reasons for anything left uncommitted. A successful hook or ancestry check alone proves neither scope nor preservation. If a commit's existence or effects are uncertain, reconcile actual HEAD, history and index before any retry; report uncertainty instead of replaying it.

| Index and selected paths | Action |
| --- | --- |
| Index is empty or contains only this group | Stage explicit intended paths or separable hunks. Verify the entire staged diff, then `git commit -m "<type>(<scope>): <subject>"`. Leave unrelated unstaged hunks untouched. |
| Other groups are staged; every changed hunk in each selected path belongs to this group | For a new untracked file, read its complete content and stage only that new path first; `--only` requires known paths. Inspect `git diff HEAD -- <selected paths>` as the proposed commit. Use `git commit --only -m "<type>(<scope>): <subject>" -- <selected paths>`; it commits those working-tree paths and retains other staged paths. Already tracked paths need no staging first. |
| Other groups are staged and a selected path mixes groups, or ownership is uncertain | Stop before changing the index; name the mixed paths and request separation or clarification. Do not use an alternate index, stash or whole-file commit to bypass this boundary. |

Example: a requested fix entirely in `limits.py` can use `--only` while an unrelated `README.md` remains staged. An intended fix sharing `limits.py` with unrelated unstaged edits cannot use a whole-file `git add` or `commit --only`.

## RULES

Before the first commit, read [commit format](references/commit-format.md); every message and staging step follows its MESSAGE and GIT RULES.

- one commit is one logical change;
- unrelated files stay out of every commit; large generated, foreign-branch and merge artifacts stop the command under STOP CONDITIONS.

## STOP CONDITIONS

- nothing to commit;
- a secret, a credential, a large generated artifact, a foreign-branch file, or a merge artifact in the diff;
- a hunk spanning two logical changes that will not split cleanly;
- a group whose type is unclear.

With nothing to commit, report a successful no-op without a question. For other stops, name the concrete blocker and request the missing choice or action.

## NEXT

For a standalone commit, stop after the report from step 5. When `dev-exec` applies this procedure as an explicitly authorized checkpoint in the same session, return the result to the calling execution instead; it verifies the checkpoint before continuing. This exception does not authorize a commit, bypass any stop condition or start a nested command. `git push` waits for a later explicit request.
