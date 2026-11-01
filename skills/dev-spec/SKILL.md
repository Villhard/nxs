---
name: dev-spec
description: Record material built-work contracts in project SPEC.md or private .SPEC.md from the intended changes, including relevant checkpoints and uncommitted work. Optional after implementation or review; no durable change means no edit. Not for planning new behavior or finding defects.
argument-hint: "[feature dir]"
disable-model-invocation: true
---

# /dev-spec

On explicit invocation or an instruction explicitly covering this operation, bring project specs in line with built work, then stop. This is optional: record material intent the code alone does not show, not an obligatory artifact for every task.

Accepted input: an optional feature directory `.scratch/<feature-slug>/`, with supplied task/review/checkpoint context when available. Without a feature directory, use the intended-work evidence and relevant code; do not invent a directory or feature spec.

Before reading specs, read [project specs](references/project-specs.md): it owns the file names and the reading rules this command shares with the other commands.

Example: /dev-spec .scratch/rate-limiting

Suggest the next command at a handoff; never start it automatically.

## STANCE

- In normal task execution, `dev-spec` is the exclusive writer of project `SPEC.md` and `.SPEC.md`. Write only those files and, in hidden mode, the one private-spec exclude line. Never code, a glossary, decision records, `.scratch/` artifacts, the index or commits. Preserve unrelated spec edits.
- Within the authorized operation, amend settled content without a separate content-approval round; the user reviews the diff. Reuse mode/scope approval already supplied.
- Ask about mode once when needed before the first spec (MODE). Missing or conflicting scope/baseline evidence needs clarification or an incomplete stop, not an inferred choice. Uncertain content may be marked `(unconfirmed)` inline; that mark cannot excuse uncertain input coverage.
- Record what was built, not what was planned: the covered net work and current code decide, while `spec.md`, `root-cause.md`, tickets and review follow-ups provide context, not proof of implementation.

## INPUT

Work from the repository root (`git rev-parse --show-toplevel`). Take a supplied feature directory exactly as given; missing or unreadable explicit input stops. Resolve task identity, requirements, intended scope and baseline from supplied task/review/checkpoint evidence or an explicitly agreed boundary. Never infer task ownership or match tickets from a branch name alone. Preserve an explicitly narrower scope; label its limits rather than silently widening it.

Absent an agreed baseline, detect `origin/HEAD`, else the existing `main` or `master`; stop on ambiguity. Resolve its merge-base with HEAD and pin the resulting commit OID as the candidate baseline. Built-work evidence includes:

- `git diff --no-ext-diff --no-textconv <baseline-OID> --` - committed, staged and unstaged net changes through the working tree;
- the staged and unstaged diffs separately, so index-only work or cancellation between index and working tree is not silently omitted;
- `git ls-files -z --others --exclude-standard` and the relevant new files' actual contents.

An existing nonempty index never restricts this scope to staged changes. Reconcile a selected staged version that differs materially from disk before recording it as built behavior. Exclude `.scratch/` and project spec files from built-work input so repeats do not consume their own output. A foreign `SPEC.md` is not a project spec; preserve it as context and never amend it.

For checkpoints, read repository, branch, pre-checkpoint HEAD, each commit and parent OID, approved scope, changed paths and remaining changes. Validate identities and requirements against actual Git and current code before MODE or any write. Verify that every relevant intended change is represented in the selected net input; ancestry or a path list alone is insufficient because later edits may cancel or replace it. A checkpoint already on the normal base is omitted even if unrelated work makes the default diff nonempty. Use an explicitly agreed earlier baseline supported by task evidence, including for work already committed on the base branch; if none is established, ask or stop incomplete rather than claiming no durable change.

Pin the selected baseline, requirement sources and actual change snapshot before deriving content: repository/branch, HEAD, staged/unstaged diffs and relevant untracked bytes. Separate foreign work by evidence, not by moving it. If intended work is omitted, foreign changes cannot safely be distinguished, input evidence is missing or coverage is uncertain, stop incomplete and identify the uncertainty. Never write a partial spec or report "nothing durable changed" as if the intended task were covered. Never stage, stash, reset, switch branches or rewrite foreign work to manufacture scope. Reconcile changed source/snapshot evidence before any spec write or final no-op conclusion; retain the pinned scope in the report without requiring a new artifact.

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

Only after intended-work coverage is established, when nothing in spec terms changed, make no edit, ask no mode question and report "nothing durable changed" for the selected scope. Never invent content to show activity or use no-op to hide omitted checkpoints, missing evidence or skipped modules.

## AMEND

1. With an undecided mode and a material fact to record, ask once: visible `SPEC.md`, eligible for a separately authorized commit, or hidden `.SPEC.md`, private and local, with the cost from MODE. Reuse an explicit choice already covering this repository. If the user declines, change nothing and report the declined save, not "nothing durable changed".
2. Hidden mode: when `git check-ignore -q -- .SPEC.md` exits non-zero, append `.SPEC.md` on its own line to `"$(git rev-parse --path-format=absolute --git-common-dir)/info/exclude"`, adding a newline first when the file does not end with one, and creating its directory if needed. Check again; stop if the file is still not ignored.
3. Amend top-down: the root spec, then module specs. Create a root spec only when the work established a product or architecture fact; a module spec without a root spec is normal. Create a module spec only for a module the work touched, only with what the work established, in the directory of a genuine boundary - not one per directory. Before creating a spec, list its directory (`ls -a`): when it holds a foreign `SPEC.md` or a case variant of either name, such as `spec.md`, `Spec.md` or `.spec.md`, create nothing there and report the module as skipped with that file name.
4. Use the headings of [project spec](assets/project-spec.md): all optional, only settled ones written, in that order; `## Goal` and `## Architecture` only in the root spec. Edit prose in place.

Content rules:

- State intent, not inventory: no restated code, no file listings, no plans, versions or "later" lists.
- Settled content only, no placeholders. Mark an inference `(unconfirmed)` where it stands.
- Each fact once: the spec that owns it states it, others name that spec's path.

## CHECK

Every amended spec matches the selected built work and current code. Touched specs do not contradict each other, the glossary or decision records, and their links resolve. Preserve foreign edits; if a contradiction requires an out-of-scope decision, stop the affected write and name it. Reconcile any change to the pinned input; do not silently write against stale evidence. Respect explicit verification limits and report NOT RUN work without claiming a complete verification.

## NEXT

Report paths created/changed, the selected scope and baseline with checkpoint coverage and verification limits, or a covered "nothing durable changed" no-op. Name any `(unconfirmed)` content, skipped modules/case variants, foreign `SPEC.md` files left unchanged and unresolved coverage. A skipped material contract is incomplete, not a complete spec update. In visible mode, suggest `dev-commit` only for remaining intended changes requiring a separately authorized commit; never stage or commit. In hidden mode, keep private specs out of Git. A handoff never starts another skill automatically.
