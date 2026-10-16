# COMMIT FORMAT

Read this reference before writing a commit. `commit` and `exec` follow it; the calling command owns what goes into each commit.

## MESSAGE

```
<type>(<scope>): <subject>
```

Single line, no body unless explicitly requested. Subject as short as possible and fully lowercase, abbreviations included ("seo", not "SEO"). Types: `feat` (new functionality), `fix` (bug fix), `refactor` (no behavior change), `chore` (deps, configs), `docs` (documentation).

Scope names the area the commit changes: a module, a plugin, or in a notes repository the topic or skill name. Prefer a scope already used in `git log --oneline -20`.

Plain simple verbs: add, fix, remove, update, show, hide, validate. Never tighten, strengthen, refine, streamline, leverage, harden.

## GIT RULES

- stage explicit paths or hunks; never `git add -A`, `git add .` or `git add -f`;
- inspect the exact staged diff before committing;
- never `--force`; `--no-verify` only with explicit approval;
- never amend a published commit;
- after a failed hook, inspect the resulting state. No commit is assumed to exist. If fixing code is needed, stop and report it; once corrected, retry with a normal commit, never amend a prior commit.
