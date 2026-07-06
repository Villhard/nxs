---
description: Rewrite the current branch's local commit history into clean, atomic, logically-grouped commits without changing the final tree - explicit-only, git-only, never pushes. Use before opening a PR when the branch has noisy history (per-task commits, WIP, fixups) and you want a clean sequence while the working tree stays byte-for-byte identical.
argument-hint: "[base ref]"
---

# /nxs:dev-recommit

Rewrite the local-only commit history of the current branch into a clean, logical sequence of commits. Self-contained skill. Output language and response style come from global rules, not this file.

## INVARIANT

Reorganize the branch's commits into clean, atomic, logically-grouped commits while the final working tree stays byte-for-byte identical. The end state after the rewrite must produce the exact same tree as before it - only the commit history in between changes. Verify this: the new `git rev-parse HEAD^{tree}` MUST equal the tree hash saved before the rewrite, and `git diff --exit-code <old-head-sha> HEAD` must be empty with a clean working tree.

## GUARDS

- EXPLICIT-ONLY - runs only when the user asks. Never auto-invoked, never run in auto or background mode. If reached from an auto/background context, refuse and tell the user to call `/nxs:dev-recommit` directly.
- GIT-ONLY - touches only git history. No source, config, formatting, generated-file, lockfile, or test edits beyond the staging that commit grouping needs. Do not change file contents.
- NEVER pushes - no `git push`, no `--force`, no `--force-with-lease`, at any step. `git fetch` is allowed; push is not.

## PROCEDURE

1. Inspect state.
   - Determine the current branch.
   - Require a clean working tree and no in-progress rebase / merge. If there are uncommitted changes or an in-progress operation, STOP and report; do not stash automatically.
2. Determine BASE.
   - BASE = the `[base ref]` argument if given, otherwise the merge-base of the current branch and the default remote branch (`origin/main` or `origin/master`).
   - If the base branch is ambiguous, STOP and show the options; do not guess.
3. Verify the range is safe to rewrite.
   - The range is `BASE..HEAD`; every commit in it must be local-only.
   - Compare `git rev-list --count BASE..HEAD` with `git rev-list --count BASE..HEAD --not --remotes`.
   - If the counts differ, ABORT: at least one in-range commit is already on a remote (published/shared history).
4. Save rollback info.
   - Save the current HEAD SHA and `git rev-parse HEAD^{tree}`.
   - Create a backup branch `backup/<branch>-before-history-cleanup-<timestamp>`.
5. Analyze and propose the grouping.
   - Review `git log --oneline --reverse BASE..HEAD`, `git diff --stat BASE...HEAD`, `git diff --name-status BASE...HEAD`.
   - Group the final diff into logical units: one coherent intent per commit; keep mechanical/generated changes separate; prefer fewer clean commits over fragile micro-commits.
   - Show the planned grouping and get the user's approval before rewriting.
6. Rewrite (git-only).
   - Reorder / squash / split into the approved logical commits, e.g. `git reset --mixed BASE` then stage each group into a new commit, or an equivalent interactive-rebase-style rewrite. Do not edit file contents.
   - Write each message per `commit-conventions`.
7. Verify the tree is unchanged.
   - The new `git rev-parse HEAD^{tree}` MUST equal the saved tree hash, and `git diff --exit-code <old-head-sha> HEAD` must be empty with a clean working tree.
   - If the tree differs, immediately restore from the backup branch / old HEAD SHA and report.
8. Report the summary (see OUTPUT FORMAT).

## SAFETY

This uses history-rewriting git operations. Confirm the grouping with the user before running them (step 5), create the backup branch first (step 4), and abort if any in-range commit is already pushed (step 3). Never force-push; never rewrite published or shared history without explicit user confirmation. The destructive-op and force-push safety is enforced by the global tier-1 block - it applies here in full; this section does not restate it.

## COMMIT MESSAGES

The new commit messages follow `commit-conventions` (format, atomicity, one commit = one logical change). Reference it by name before writing any commit.

## OUTPUT FORMAT

```text
recommit summary
- original HEAD: <sha>
- new HEAD: <sha>
- backup branch: backup/<branch>-before-history-cleanup-<timestamp>
- old commits: <list>
- new commits: <list>
- final tree hash identical: yes
- pushed: no
```

## NEXT

History cleaned -> open the PR yourself (this skill never pushes). For a standalone code review of the branch -> `/nxs:dev-review`. To archive finished plans / stale briefs (docs, not git history) -> `/nxs:dev-cleanup`.
