# GIT CONVENTIONS (reference)

Loaded on demand from `commit-conventions` when the case needs the full rules. Destructive-op and secret safety is enforced by the global tier-1 block, not here.

## COMMIT MESSAGES

Plain English, A1-B1 level. Simple verbs: add, fix, remove, update, show, hide, validate. Do NOT use B2+ verbs: tighten, strengthen, refine, streamline, leverage, harden.

Format:

```
<type>(<scope>): <subject>
```

Single line. No body unless explicitly requested. Subject as short as possible, fully lowercase (including abbreviations: "seo", not "SEO").

Types: `feat` (new functionality), `fix` (bug fix), `refactor` (no behavior change), `chore` (deps, configs), `docs` (documentation).

## BRANCHES

```
<type>/<short-desc>
```

or for work branches:

```
<type>/vr/<short-desc>
```

`/vr/` prefix for work branches; personal ones without it.

## MANUAL VS AUTO MODE

Manual / default mode: do NOT run `git add` / `git commit` / `git push`; propose a commit message.

auto mode: `git add` / `git commit` allowed after verify + full review; `git push` NOT allowed; MR / PR creation NOT allowed; `--no-verify` NOT allowed without explicit approval.

auto mode under a no-commit instruction: no `git add` / `git commit` / `git push`; run verify + full review after each task.

## STAGING

- prefer `git add <specific files>` over `git add -A` / `git add .`;
- check the diff before commit.

## GENERAL RULES

- Do not commit unrelated files, large generated artifacts, foreign-branch files, or merge artifacts.
- Do not amend published commits.
- Do not skip hooks without explicit approval.
- HEREDOC for a commit message only if the user explicitly asked for a multi-line body; default is `-m "<subject>"` single line.
- After a failed pre-commit hook: create a NEW commit with the fix, do not amend.
