# FEATURE DIRECTORY

Read this reference before reading feature input or writing a feature artifact. `dev-rnd` and `dev-bug` apply the sections that fit their input; each command keeps its own gates and outputs.

## LOCATION

One feature is one local directory under `.scratch/`. `<feature-slug>` is two to four lowercase english words from the request or report, hyphenated; a tracker key names the directory instead - `.scratch/<KEY>-<slug>/` - so the feature stays navigable by the key. Write into the directory the input names when it has one.

Never write into a `.scratch/<x>/` that holds a `map.md`: that directory holds another tool's decision work. Pick another slug and say why in one line.

## LOCAL STORAGE

Always save Markdown under `.scratch/`. Do not look up repository/global tracker preferences or ask for a storage backend or separate local-storage consent. An unrelated tracker preference does not redirect this workflow. Content approval and the command's own gates still apply. Do not change settings, run setup or publish/synchronize remote issues.

## TRACKER INPUT

A tracker key or URL is read before anything else through an available read interface; otherwise ask the user to paste the ticket. Never infer its content from the key.

For remote input, establish the source identity, applicable parent decisions/comments (or that no parent applies) and blocker state through an available read interface or supplied content. Ask for missing facts; a key, a ready label or an omitted blocker field is not evidence of no blockers. A known open remote blocker needs a verified mapping to a local ticket in the target feature; retain that local dependency and use the local resolution rules. Never interpret a remote issue number as a local ticket number or resolve a local ticket from a remote label. Unknown or unmapped blockers prevent a ready handoff. Verified closed remote blockers may be recorded as satisfied context.

## EXTERNAL SPEC

Keep a source spec unchanged. Reuse an existing local feature `spec.md` in place. For a source outside the target feature, include preserving its applicable content - decisions, exclusions, testing requirements and answers - in the proposed local `spec.md` before approval to write. Copy a compatible spec unchanged; adapt another layout to the headings of the [spec template](../assets/spec.md), keeping Problem Statement and Solution and omitting only empty optional sections. Inspect the target first: reuse an identical existing spec, but a different existing spec requires a concrete revision decision, never an overwrite. Apply LOCATION before any copy.

Check unresolved questions in the source as well as local documents. Approval of a spec does not clear an open question, and only new contradictory evidence reopens a settled decision.

## DOMAIN DOCUMENTS

A project may keep a domain glossary and decision records - typically `GLOSSARY.md` or `GLOSSARY-MAP.md` at the root and `docs/adr/`, or wherever project instructions point. When they exist, read the entries for the affected area and use the glossary's terms, not a synonym it avoids. Their absence is normal: do not ask about it. Never create or edit these files.
