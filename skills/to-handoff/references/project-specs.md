# PROJECT SPECS

Read this reference before using project specs. It is the reader contract: `dev-lead`, `dev-rnd`, `dev-bug` and `dev-review` read specs; only `dev-spec` writes them.

## FILES

A project spec is a durable Markdown file that records the intent behind the product or one module: purpose, boundaries, contracts, known limitations and rationale the code does not show. It is named `SPEC.md` when the project commits specs, or `.SPEC.md` when the specs are the user's private local notes kept out of Git. The root spec sits at the repository root; a module spec sits in the module's directory.

A `SPEC.md` is a project spec only when every `##` heading in it is one of `Goal`, `Architecture`, `Purpose`, `Ownership`, `Boundaries`, `Contracts`, `Known limitations` and `Rationale`. Any other `SPEC.md`, for example a protocol spec, is a foreign document.

## LISTING

List the specs of the repository from its root:

```bash
git ls-files -z --cached --others --exclude-standard -- ':(glob)**/SPEC.md' ':(glob)**/.SPEC.md'
git ls-files -z --others --ignored --exclude-standard --directory   # keep entries whose basename is .SPEC.md
```

Count foreign `SPEC.md` files out. The repository mixes both kinds when the rest holds a `SPEC.md` and a `.SPEC.md`, in one directory or in different ones.

## READING

- For each affected path, list the repository root and every ancestor directory of the path (`ls -a <dir>`), and take a spec only when the listing holds the exact basename `SPEC.md` or `.SPEC.md`. Never open `<dir>/SPEC.md` directly: a case-insensitive filesystem returns `spec.md` for it. Content search misses `.SPEC.md` excluded from Git, and a file-name search may list copies inside ignored directories, so never locate specs by search.
- Read the root spec first and the nearest spec last. Treat their statements like recorded decisions in a glossary or decision record: use their terms, and surface a contradiction with the spec path instead of diverging silently.
- A statement marked `(unconfirmed)` is not a recorded decision.
- A foreign `SPEC.md` on the path is context, not recorded decisions.
- Run LISTING once. When the repository mixes both kinds, read the specs on the path as usual and tell the user that the repository mixes `SPEC.md` and `.SPEC.md` and that one kind must be renamed or removed by hand; continue.
- Never create or edit a spec. Their absence is normal: do not ask about it.
