## nxs

- Project specs: when executing a ticket, before changing a file, list the repository root and every ancestor directory of that file (`ls -a <dir>`) for `SPEC.md` and `.SPEC.md` by exact name, and read each one found, root first. Find them only through these listings: content search misses a `.SPEC.md` kept out of Git, and a case-insensitive filesystem opens `spec.md` for `SPEC.md`. Only `/dev-spec` edits specs.
- Branches: `<type>/<short-description>`, with `<type>` one of `feat`, `fix`, `refactor`, `chore`, `docs`. A branch rule in the project's instructions wins.
