---
description: Git commit and push conventions - load before any git add, git commit, or git push. Commit message format, atomicity, never-commit items, push restrictions. Background knowledge, not a user command.
user-invocable: false
---

# COMMIT CONVENTIONS

Load before any `git add` / `git commit` / `git push`. Workflow rules, not a user-invocable command. Destructive-op and secret safety is enforced by the global tier-1 block, not here.

## THE GATE

- `/nxs:exec` may run `git add` / `git commit` only after verify passed and the review round came back with zero BLOCK findings.
- Under a **no commits** instruction: no `git add`, no `git commit`.
- Outside exec: do not run git writes - propose the message as text to copy.
- `git push` only on explicit user request. Never `--force` / `--force-with-lease`. Never create an MR / PR automatically.
- `--no-verify` only with explicit approval.

## COMMIT MESSAGES

Plain English, A1-B1 level. Simple verbs: add, fix, remove, update, show, hide, validate. Do NOT use B2+ verbs: tighten, strengthen, refine, streamline, leverage, harden.

```
<type>(<scope>): <subject>
```

Single line, no body unless explicitly requested. Subject as short as possible, fully lowercase (including abbreviations: "seo", not "SEO").

Types: `feat` (new functionality), `fix` (bug fix), `refactor` (no behavior change), `chore` (deps, configs), `docs` (documentation).

One commit = one logical change. Separate refactor from feat / fix.

## BRANCHES

```
<type>/<short-desc>
<type>/vr/<short-desc>    # work branches
```

`/vr/` prefix for work branches; personal ones without it.

## STAGING AND GENERAL RULES

- prefer `git add <specific files>` over `git add -A` / `git add .`; check the diff before commit;
- do not commit unrelated files, large generated artifacts, foreign-branch files, or merge artifacts;
- do not amend published commits;
- HEREDOC for a commit message only if the user explicitly asked for a multi-line body; default is `-m "<subject>"`;
- after a failed pre-commit hook: create a NEW commit with the fix, do not amend.
