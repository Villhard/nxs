# DIRECT SAVING

Read when saving is requested or consuming tracker input. Saving is optional and happens directly within rnd-grill; no decision/spec/ticket chain or journal is required.

## SOURCE AND DESTINATION

Read explicit local input first; missing or unreadable input stops the affected work. Read a tracker key or URL through an available read interface, otherwise ask for pasted content. Never infer content from an identifier. Establish source identity, applicable parent decisions/comments (or evidence that none apply), and relevant blockers. A ready label or omitted blocker field is not evidence of readiness. Unknown prerequisites prevent a ready handoff, not an explicitly approved draft. Keep verified prerequisites and their required results explicit; local/remote identifiers and status alone do not prove those results exist.

Use an explicit or established destination before defaults. A decision in a feature's `research/` belongs to that feature, not a new nested feature. Ask when multiple tasks, paths or owners fit; a branch alone does not establish ownership. For new local records use `.scratch/<feature-slug>/` with a short lowercase hyphenated slug; a tracker key can prefix it. Do not consult unrelated storage preferences, run setup or publish/synchronize remote records.

Read source records and existing targets before proposing any write. Preserve applicable decisions, conditions, defaults, answers, exclusions, rationale, testing requirements, feedback and open questions. Keep external sources unchanged; layout adaptation is not permission to drop source content. Existing maps and typed decision records are context, not implementation tickets or authorization to convert them. Reuse their identity without modifying their histories merely to create a new result.

## PROPOSE AND APPROVE

Show proposed content, exact destination, state (agreed or unfinished/draft) and any readiness limits. For an existing result, show the concrete revision instead of regenerating it. Distinguish facts, assumptions, proposals, accepted conclusions, feedback and unanswered questions. An explicitly requested unfinished result may preserve specific questions; approval to save them never answers them.

Identify approval covering each write's actual content, destination and scope. A request to save authorizes preparation, not unseen conclusions. Reuse exact applicable approval; otherwise ask and wait before writing. Show glossary/ADR entries as separate concrete proposals under [domain modeling](domain-modeling.md); approval of one does not approve another. A domain-only request needs no decision wrapper or feature directory. Declining a proposal leaves its files unchanged. HTML approval alone requests no save and approves no unseen Markdown or domain changes.

## OUTPUT SHAPES

Choose only the useful record, not one of every kind:

- Decision: default `research/decision.md`, using [decision template](../assets/decision.md). Keep agreed/unfinished state, scope, conclusions and reasons, proposals/alternatives, evidence, feedback/open questions and next authorized action. Preserve earlier rationale when approved revisions supersede a conclusion.
- Feature description: default `spec.md`, using [feature template](../assets/spec.md). Keep its seven permitted `##` headings in order; Problem Statement and Solution are required, other sections may be omitted only when empty. Put behavior, conditions, defaults, integrated answers and acceptance checks in Solution; current findings, interfaces, constraints and project-record links in Implementation Decisions; check requirements in Testing Decisions; exclusions in Out of Scope; source identity, approval scope, feedback and remaining `[NEEDS CLARIFICATION: <question>]` entries in Further Notes when they do not fit an affected section. Keep draft state explicit within those headings. This local lowercase feature record is not a project `SPEC.md` or `.SPEC.md` and describes no completed implementation merely because it was saved.
- Research, survey or design: use a concise evidence report under `research/`, such as `<topic-slug>.md`, `architecture-audit.md` or `<module-slug>-design.md`. Include the relevant result elements from [evidence methods](evidence-methods.md), without forcing a separate decision or feature file.
- Questionnaire: default `research/questionnaire-<recipient-slug>.md`, using [questionnaire rules](questionnaire.md) and [template](../assets/questionnaire.md). Preserve question identities, exact wording, existing and partial responses, attribution and unresolved blockers. Preparation and approval never authorize sending, contacting anyone or supplying answers.
- Domain records: only approved glossary entries or worthwhile ADRs under the project's existing conventions and the domain rules. Project specs remain exclusive to `dev-spec`.

Copy a compatible authorized source feature spec unchanged when useful, or adapt it while preserving applicable content. Do not duplicate an existing local feature spec merely to satisfy a default path. Record source paths/URLs and relevant versions or supplied snapshots; distinguish inspected source from an observation. Use an exact content hash only when pinning a mutable source is useful or requested, identify what it hashes, and never treat a hash as approval. For byte-identical reuse/copy, carry source context in the response without rewriting the file merely to attach metadata.

## WRITE, PRESERVE AND RETURN

Check current source and target before writing. Reconcile concurrent changes and obtain approval for uncovered revisions; never overwrite another worker's changes based on a stale proposal. Identical results are a no-op. Preserve manual additions, links, earlier evidence and history; broad save permission does not authorize removal. Keep secrets, private configuration and raw transcripts out of artifacts and out of external services.

Write only approved content. Re-read saved files to confirm the approved state, source links, requirements, acceptance checks, remaining questions and preservation of existing material. Report paths, revisions/no-ops, declined entries and exact limits. No event IDs, approval hashes, locks or run-state artifacts are required.

Sufficient agreed scope can go directly to a separately authorized `dev-exec`, with or without a feature record. Carry source identity, approved scope, intent, concrete prerequisites, evidence and unresolved questions. An unknown or unsatisfied prerequisite prevents claiming the affected work ready; verify actual needed results rather than relying on status alone. Saving never creates tickets, implements a fix, changes Git/settings/installations or implicitly starts another skill.
