# Issue tracker: Local Markdown

Local artifacts are optional. A small clear request needs no spec, ticket, task directory or journal. When durable records are useful and authorized, reuse established project paths; the defaults below stay private under `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`.
- An optional feature description is `spec.md`, saved directly by `rnd-grill` after content/scope approval. It is not a project `SPEC.md` or `.SPEC.md` and is not a prerequisite for a clear request.
- `dev-exec` owns optional implementation tickets, one file per ticket at `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. A new ticket takes `NN` one past the highest existing number in `issues/`, including decision files and rejected work; use `01` only when the directory is empty or missing. Never renumber or regenerate existing tickets.
- Triage state is the `**Status:**` line near the top of each implementation ticket; `~/.agents/docs/triage-labels.md` maps role names to values.
- Execution notes append under `## Comments`. Preserve identities, branch restrictions, source records and prior history. Existing `Do not commit` instructions remain binding unless a specific revision is separately approved.

## Local ticket format

Use the ticket rules and template bundled with `dev-exec`, not another installed skill's resources. Saving tickets requires approval covering their content and destination; it does not approve implementation.

- Keep the title `# NN: <title>`, `**What to build:**`, `**Blocked by:**`, optional `**Branch:**`, `**Status:**`, then observable acceptance criteria as `- [ ]` lines.
- `**Blocked by:**` names local ticket numbers, or `None (can start immediately)` only when no dependency remains. Unknown evidence is never `None`; a resolved status still needs the actual prerequisite result in the selected working tree.
- Propose `**Branch:**` from the approved branch or project rule, otherwise `<type>/<feature-slug>` with `feat`, `fix`, `refactor`, `chore` or `docs`. Show it before saving; the user may change or drop it. No branch field means the current branch, not permission to override existing restrictions.
- New `**Status:**` is `ready-for-agent`, or `needs-info` for an explicitly authorized draft with an isolated `[NEEDS CLARIFICATION: ...]` in its own body. Material open questions in the feature records stop new executable ticket production.
- After the criteria, copy this block verbatim and in English from the `dev-exec` template:

````markdown
## Done when

Execute this ticket directly with `/dev-exec <this file>`.

- Start only when **Status** is `ready-for-agent`, every **Blocked by** ticket is `resolved`, material questions are answered and required prerequisite results are verified in the selected working tree. Respect **Branch** and preserve unrelated changes; status or history alone proves no result.
- Implement only within an approved concrete plan. An install, migration or external action needs approval covering the action and exact target plus native permissions; otherwise record the human step and expected evidence under `## Comments`, set **Status** to `ready-for-human` and stop the affected work. Verify the actual result when the human returns the ticket to `ready-for-agent`; never repeat an uncertain action.
- Close only after every criterion, the project's full test suite, linter and other required checks pass: check the criteria and set **Status** to `resolved`. Record exact verification, missing checks and meaningful decisions or deviations under `## Comments`; prohibited or unavailable verification leaves the ticket unresolved.
- Commits are optional and require explicit authorization for their scope through `dev-commit`. Preserve any existing `Do not commit` instruction. Report actual checkpoint identities, remaining work and verification limits; a commit alone does not complete this ticket.
````

Existing bare or bold `Type:` decision records, including `Type: task`, are not implementation tickets. Preserve them, their answers, maps, statuses and history; do not execute, relabel or silently convert them. This template does not migrate existing artifacts.

## Save or read a local record

Use an explicit or established path before the defaults. A request to save locally never authorizes publishing or synchronizing remote tracker state. Read a referenced ticket at its actual path; an ambiguous issue number needs clarification. Keep private data, secrets and raw conversations out of saved records.

Optional resumable context belongs to `dev-exec`, normally `handoff.md` in an established feature. It distinguishes accepted, open and unverified state, actual verification and the next authorized action; saving starts no subsequent skill.

## Scope

This is an optional global default for repositories without their own tracker conventions. Project instructions win. Setup changes only the exact approved guidance, not existing tickets, journals, prototypes or task history.
