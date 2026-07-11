---
description: Git commit and push conventions - load before any git add, git commit, or git push. Commit message format, atomicity, mode gating, never-commit items, push and force-push restrictions. Background knowledge, not a user command.
user-invocable: false
---

# COMMIT CONVENTIONS

Load before any `git add` / `git commit` / `git push`. Workflow rules, not a user-invocable command. Destructive-op and secret safety is enforced by the global tier-1 block, not here.

## CORE

Mode gating - the operational gate before any git write:

- Manual / default mode: do NOT run `git add` / `git commit` / `git push` - propose the message as text to copy.
- auto mode: `git add` / `git commit` allowed only after verify + full review; push never.
- auto under a no-commit instruction: no `git add` / `git commit` / `git push`.
- `git push` only on explicit user request.

One commit = one logical change. Separate refactor from feat / fix.

Full rules live once in `reference/git-conventions.md` - commit format, the A1-B1 verb allow-list and B2+ ban-list, the type list, the full manual-vs-auto mode matrix, branch naming, staging, the never-commit list, the failed-hook rule, and HEREDOC usage. Read it when writing a message or when the case needs the detail.
