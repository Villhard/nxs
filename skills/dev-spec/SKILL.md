---
name: dev-spec
description: Record durable project specs from landed work when the user explicitly invokes /dev-spec. Writes SPEC.md, or private .SPEC.md kept out of Git, from the branch diff and an optional feature directory, then stops. Not for discussing specs; dev-rnd shapes new work and dev-review finds defects.
argument-hint: "[feature dir]"
disable-model-invocation: true
---

# /dev-spec

Bring the project specs in line with work that has landed in the working tree, then stop. Specs record what the code alone does not show, so the next session starts from recorded intent instead of re-deriving it.

Accepted input: an optional feature directory `.scratch/<feature-slug>/`. Without one, work from the diff alone.

Before reading specs, read [project specs](references/project-specs.md): it owns the file names and the reading rules this command shares with the other commands.

Example: /dev-spec .scratch/rate-limiting

Suggest the next command at a handoff; never start it automatically.

## STANCE

- Write only project spec files and, in hidden mode, one exclude line. Never code, a glossary, decision records, `.scratch/`, the index or commits.
- Write without an approval round; the user reviews the result in the diff.
- The only question this command asks is the mode, once, before the first spec of a repository (MODE). Uncertain content is written as `(unconfirmed)` inline, never asked.
- Record what was built, not what was planned: the diff decides, `spec.md` and `root-cause.md` are context.

## INPUT

Work from the repository root (`git rev-parse --show-toplevel`). Take the feature only from the argument; never match tickets by branch. A missing or unreadable feature directory stops.

Detect the base: `origin/HEAD`, else the existing `main` or `master`; stop on ambiguity. Built work is the union of:

- `git diff --no-ext-diff --no-textconv <merge-base> --`, with `<merge-base>` from `git merge-base <base> HEAD` - committed, staged and unstaged changes;
- `git ls-files -z --others --exclude-standard` - new untracked files.

Exclude `.scratch/`, `SPEC.md` and `.SPEC.md` from it, so a repeat never treats its own specs as work. An empty result on the base branch stops: work already committed on the base branch is not supported; run on a branch, or before committing.

## MODE

Detect with LISTING from the reference. A foreign `SPEC.md` is not counted here and never amended. Take the first matching row:

| Found | Mode |
| --- | --- |
| A tracked `.SPEC.md`: `git ls-files -z --cached -- ':(glob)**/.SPEC.md'` is not empty | Stop: name it; it is already committed, so the user decides how to remove it from Git |
| Both kinds | Stop: name the files of each kind and tell the user to rename or remove one kind by hand |
| `SPEC.md` files only | visible |
| `.SPEC.md` files only | hidden; an untracked one not yet ignored gets the exclude line under AMEND |
| Neither, and `git check-ignore -q -- .SPEC.md` exits 0 | hidden |
| Neither, otherwise | undecided: ask under AMEND, before the first write |

Hidden mode is the user's private documentation for a project where specs may not be committed. Its cost, stated to the user when the mode is chosen: the files exist only in this working tree, a fresh clone or `git clean -x` loses them, and only the exclude line keeps them out of commits.

## FIND WHAT CHANGED

Read the specs that govern the built work per the reference, then name what changed in spec terms:

- the product goal or architecture: a capability added or removed, a principle or a cross-module decision moved;
- a module: its purpose, ownership, boundary, contract, decision or known limitation;
- a genuinely new module boundary;
- for a bug in the feature's `root-cause.md`: the intended behavior of a `silent` one in the spec that governs the affected path - the nearest existing spec on the path, or a module spec created under AMEND; of a `wrong` one in the record the root cause names, when that record is a spec; the fix ticket leaves that spec unchanged for dev-spec to correct.

A fact already in a glossary or decision record is linked by path, not restated.

## NOTHING DURABLE

When nothing in spec terms changed, make no edit, ask nothing and report "nothing durable changed". Never invent content to show activity.

## AMEND

1. With an undecided mode, ask once: visible `SPEC.md`, committed with the project, or hidden `.SPEC.md`, private and local, with the cost from MODE. Then proceed.
2. Hidden mode: when `git check-ignore -q -- .SPEC.md` exits non-zero, append `.SPEC.md` on its own line to `"$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"`, adding a newline first when the file does not end with one, and creating its directory if needed. Check again; stop if the file is still not ignored.
3. Amend top-down: the root spec, then module specs. Create a root spec only when the work established a product or architecture fact; a module spec without a root spec is normal. Create a module spec only for a module the work touched, only with what the work established, in the directory of a genuine boundary - not one per directory. Before creating a spec, list its directory (`ls -a`): when it holds a foreign `SPEC.md` or a case variant of either name, such as `spec.md`, `Spec.md` or `.spec.md`, create nothing there and report the module as skipped with that file name.
4. Use the headings of [project spec](assets/project-spec.md): all optional, only settled ones written, in that order; `## Goal` and `## Architecture` only in the root spec. Edit prose in place.

Content rules:

- State intent, not inventory: no restated code, no file listings, no plans, versions or "later" lists.
- Settled content only, no placeholders. Mark an inference `(unconfirmed)` where it stands.
- Each fact once: the spec that owns it states it, others name that spec's path.

## CHECK

Every amended spec matches the code as built. Touched specs do not contradict each other, the glossary or decision records, and their links resolve. Fix what fails before reporting.

## NEXT

Report in one or two lines the spec paths created or changed, or "nothing durable changed", any `(unconfirmed)` statement left, modules skipped for a foreign `SPEC.md` or a case variant, with the file name, and foreign `SPEC.md` files on the built work's paths left unchanged. In visible mode suggest `/dev-commit`.
