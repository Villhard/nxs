---
description: Git commit and push conventions - load before any git add, git commit, or git push. Commit message format, atomicity, mode gating, never-commit items, push and force-push restrictions. Background knowledge, not a user command.
user-invocable: false
---

# COMMIT CONVENTIONS

Load before any `git add` / `git commit` / `git push`. Workflow rules, not a user-invocable command. Destructive-op and secret safety is enforced by the global tier-1 block, not here.

## CORE

- Commit format: `<type>(<scope>): <subject>` - single line, no body unless explicitly requested.
- Subject fully lowercase (including abbreviations: "seo", not "SEO"), as short as possible.
- A1-B1 verbs only: add, fix, remove, update, show, hide, validate. No B2+ verbs (tighten, refine, streamline, leverage, harden).
- Types: `feat`, `fix`, `refactor`, `chore`, `docs`.
- One commit = one logical change. Separate refactor from feat / fix.
- Manual / default mode: do NOT run `git add` / `git commit` / `git push` - propose the message as text to copy.
- auto mode: `git add` / `git commit` allowed only after verify + full review; push never.
- auto under a no-commit instruction: no `git add` / `git commit` / `git push`.
- `git push` only on explicit user request.
- Do not commit unrelated files, large generated artifacts, foreign-branch files, or merge artifacts.
- After a failed pre-commit hook: create a NEW commit with the fix, do not amend.

Full mode matrix, branch naming, staging, and HEREDOC rules: read `reference/git-conventions.md` when the case needs it.
