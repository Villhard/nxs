## nxs

- Project specs: before changing a file, list the repository root and each ancestor directory for `SPEC.md` and `.SPEC.md` by exact name and read each found, root first. Only /dev-spec edits project specs.

- Branches: <required: the branch rule from AUDIT step 3>
- Tests: <optional: the full test suite command; drop the line when none was found>
- Lint: <optional: the linter command; drop the line when none was found>
- Typecheck: <optional: the type checker command; drop the line when none was found>

A ticket's "full test suite and linter" means the commands above. Missing, prohibited or unavailable required checks remain unverified, not passed.
