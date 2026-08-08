---
description: Commit the current working changes - splits them into atomic commits with conventional messages. Use on any request to commit work made outside /nxs:exec, and before running `git add` or `git commit` by hand.
argument-hint: "[optional scope hint]"
---

# /nxs:commit

Commit what is already in the working tree, split into atomic commits. For edits made by hand, outside `/nxs:exec`.

Accepted input: an optional hint to narrow the scope or guide the grouping. With nothing given, commit the whole working tree.

Example: /nxs:commit

## STANCE

Commit what is there. Writing code, running the build, and changing behavior belong elsewhere. `git push`, `--force`, and MR / PR creation stay out of this command - push only on a later explicit request.

## PROCEDURE

1. Read the state: `git status`, `git diff`, `git diff --staged`, and untracked files.
2. Group by logical change - one group per `feat` / `fix` / `refactor` / `chore` / `docs` unit. Separate a refactor from a feat or a fix even inside one file.
3. For each group, in dependency order:
   - stage exactly that group with `git add <specific files>`, never `git add -A` or `git add .`; for a file mixing groups, stage the hunks with `git add -p`;
   - check the staged diff matches the group;
   - `git commit -m "<type>(<scope>): <subject>"`.
4. Report the commits made, one line each, plus anything left uncommitted and why.

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
- after a failed pre-commit hook, make a NEW commit with the fix rather than amending;
- branches are `<type>/<short-desc>`, or `<type>/vr/<short-desc>` for work branches.

## STOP CONDITIONS

- nothing to commit;
- a secret, a credential, a large generated artifact, a foreign-branch file, or a merge artifact in the diff;
- a hunk spanning two logical changes that will not split cleanly;
- a group whose type or scope is unclear.

On any of these - stop and ask rather than guessing.

## NEXT

Changes committed. `git push` only when you explicitly ask for it.
