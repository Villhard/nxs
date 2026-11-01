# FEATURE DIRECTORY

Read this reference before reading feature input or writing a feature artifact. Apply the sections that fit the input; `rnd-debug` keeps its own gates and outputs.

## LOCATION

Reuse an explicit or established feature directory before choosing a new one. For new diagnostic artifacts, use `.scratch/<feature-slug>/`, with two to four lowercase English words from the request or report, hyphenated; a tracker key prefixes the slug - `.scratch/<KEY>-<slug>/`. A source under a feature's `research/` belongs to that feature, not a new nested directory. Ask when several tasks, destinations or owners fit; a branch alone does not establish task identity.

Inspect the destination before writing. A `map.md` or typed decision record is existing context, not permission to alter it and not a reason to force a separate workflow. Save diagnosis in the selected feature only when ownership and scope are clear. Preserve map/decision files, identities, answers and history; do not claim, renumber, convert or reset decision tickets. Ask or choose a distinct destination if another worker's ownership conflicts.

## LOCAL STORAGE

Save new diagnostic Markdown under `.scratch/` by default; reuse an explicitly supplied existing diagnostic artifact in place. Create only the diagnosis and useful probe evidence, not prerequisite feature specs, tickets or journals. Do not look up repository/global tracker preferences or ask for a storage backend or separate local-storage consent. An unrelated tracker preference does not redirect this workflow. The skill's own approval and preservation gates still apply. Do not change settings, run setup or publish/synchronize remote issues. Keep secrets, private configuration and raw session transcripts out of saved evidence.

## TRACKER INPUT

A tracker key or URL is read before anything else through an available read interface; otherwise ask the user to paste the ticket. Never infer its content from the key.

For remote input, establish the source identity, applicable parent decisions/comments (or that no parent applies) and relevant blocker state through an available read interface or supplied content. Ask for missing facts; a key, a ready label or an omitted blocker field is not evidence of no blockers. Preserve known prerequisites and their required results; if local tickets already represent them, retain their identities and verified mapping. Do not manufacture a local ticket to diagnose the failure. Never interpret a remote issue number as a local ticket number or resolve a local ticket from a remote label. Unknown or unsatisfied prerequisites prevent claiming affected work ready; verify the actual needed result rather than relying on status alone. Independent safe diagnosis can continue within its authorization. Record verified closed blockers with their supporting evidence.

## SOURCE PRESERVATION

Read an existing feature `spec.md`, decision or external source as evidence without copying or rewriting it. Carry applicable intent, conditions, answers, exclusions, testing requirements and source links into the diagnosis where relevant. Saving `root-cause.md` requires no intermediate feature spec. A separately requested feature-description or domain-record save belongs to `rnd-grill`; project specs remain `dev-spec`-owned.

Check unresolved questions in the source as well as local documents. Approval of a spec does not clear an open question, and only new contradictory evidence reopens a settled decision.

## DOMAIN DOCUMENTS

A project may keep a domain glossary and decision records - typically `GLOSSARY.md` or `GLOSSARY-MAP.md` at the root and `docs/adr/`, or wherever project instructions point. When they exist, read the entries for the affected area and use the glossary's terms, not a synonym it avoids. Their absence is normal: do not ask about it. Never create or edit these files.

Project specs are domain documents too: read them per [project specs](project-specs.md).
