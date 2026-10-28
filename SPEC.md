# nxs

## Architecture

- Project specs record the intent behind the product or a module that the code does not show. `dev-spec` is their only writer; `dev-rnd`, `dev-bug` and `dev-review` only read them, under one reader contract in the shared `references/project-specs.md`.
- Specs follow the directory tree: a root spec and module specs beside their modules, with no links between specs and no graph to validate.
- Feature records under `.scratch/` hold what was planned; specs hold what was built. `dev-spec` writes from the diff, with the feature's `spec.md` and `root-cause.md` as context only.
- `dev-bug` classifies a confirmed cause against the glossary, decision records and specs. A behavior a record decided is a change of decision and goes to `dev-rnd`, not to a fix ticket. A spec silent or wrong about the fixed behavior is corrected by `dev-spec` after the fix lands, never by the fix ticket, so a spec never states behavior that was not built.
- `dev-review` reports a diff that contradicts a spec; behavior no spec mentions yet is `dev-spec` work, not a finding.

## Known limitations

- Hidden `.SPEC.md` files exist only in the working tree where they were written: a linked worktree, a fresh clone or `git clean -x` does not have them. Accepted because the user works in one checkout in projects that forbid committed specs.
- `dev-spec` does not see work already committed on the base branch.
- `dev-spec` excludes every `SPEC.md` from built work, so a change to a foreign `SPEC.md` is not seen as work either.

## Rationale

- Feature records are local, and the glossary and decision records hold terms and decisions, not module intent: without specs the next session re-derives or contradicts it.
- Hidden mode exists for projects where specs may not be committed.
- Readers find specs by exact name in a directory listing because search is unreliable for them: `rg`, also with `--hidden`, and the Claude Code Grep tool were verified to miss a `.SPEC.md` excluded through `info/exclude`. Codex and OpenCode search is unverified.
- `dev-spec` skips a foreign `SPEC.md` without asking because nxs has no place to remember an answer, so the question would return on every run.
