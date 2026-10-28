# nxs

## Architecture

- Project specs record the intent behind the product or a module that the code does not show. `dev-spec` is their only writer; `dev-rnd`, `dev-bug` and `dev-review` only read them, under one reader contract in the shared `references/project-specs.md`.
- Specs follow the directory tree: a root spec and module specs beside their modules, with no links between specs and no graph to validate.
- Feature records under `.scratch/` hold what was planned; specs hold what was built. `dev-spec` writes from the diff, with the feature's `spec.md` and `root-cause.md` as context only.
- `dev-bug` classifies a confirmed cause against the glossary, decision records and specs. A behavior a record decided is a change of decision and goes to `dev-rnd`, not to a fix ticket. A spec silent or wrong about the fixed behavior is corrected by `dev-spec` after the fix lands, never by the fix ticket, so a spec never states behavior that was not built.
- `dev-review` reports a diff that contradicts a spec; behavior no spec mentions yet is `dev-spec` work, not a finding.
- `dev-setup` makes the settings the other dev skills assume but never create: an executor reads project specs on its path, ticket `**Branch:**` follows a branch rule, "the full test suite and linter" in `Done when` names real commands, and `.scratch/` stays out of Git. `global` writes them into one user source, `~/.agents/AGENTS.md`, that Claude Code, Codex and OpenCode all load; `project` writes them into the repository's instruction file. It is the only skill that writes client instructions, under the exception in `CONTRIBUTING.md`.
- `dev-setup` owns only template sections, `## nxs` and, in `global`, `## Engineering skill defaults`: one heading each, rewritten in place on a repeat. Every other line belongs to the user, and a rule stated there counts as covered instead of being repeated.
- `dev-setup global` installs companion mattpocock/skills by bundle and writes their tracker and domain-doc config so their tickets land in `.scratch/` in the nxs ticket format and statuses. Its tracker template copies `dev-rnd`'s `Done when` block, and the checker keeps the copy identical.

## Known limitations

- Hidden `.SPEC.md` files exist only in the working tree where they were written: a linked worktree, a fresh clone or `git clean -x` does not have them. Accepted because the user works in one checkout in projects that forbid committed specs.
- `dev-spec` does not see work already committed on the base branch.
- `dev-spec` excludes every `SPEC.md` from built work, so a change to a foreign `SPEC.md` is not seen as work either.
- A line the user edits inside a `dev-setup` owned section is proposed back to the template wording on the next run; custom rules belong outside the section.
- `dev-setup` bundle membership and skill dependencies are kept by hand in its bundles template: names are checked against the upstream listing, but a dependency upstream adds or drops goes unnoticed.

## Rationale

- Feature records are local, and the glossary and decision records hold terms and decisions, not module intent: without specs the next session re-derives or contradicts it.
- Hidden mode exists for projects where specs may not be committed.
- Readers find specs by exact name in a directory listing because search is unreliable for them: `rg`, also with `--hidden`, and the Claude Code Grep tool were verified to miss a `.SPEC.md` excluded through `info/exclude`. Codex and OpenCode search is unverified.
- `dev-spec` skips a foreign `SPEC.md` without asking because nxs has no place to remember an answer, so the question would return on every run.
- `dev-setup` never replaces an instruction file that holds content: it merges the content into the source through the approved diff and links the path only after the merge is checked. Losing a user's instructions is the costly failure of a setup command.
- `dev-setup` counts a mattpocock skill as installed only from a lock entry with that source, so a user's same-name skill is never overwritten.
- `dev-setup` offers no commit-message rules because `dev-commit` owns the format, and never offers `setup-matt-pocock-skills` because `dev-setup global` writes that config. `to-spec` and `to-tickets` sit in the recommended Core bundle as the bridge from grilling to a spec, since `dev-rnd` accepts only a spec path as a shortcut past its own interview.
