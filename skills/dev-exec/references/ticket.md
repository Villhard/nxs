# TICKET

Read this reference before writing or executing a ticket. `dev-exec` owns these rules and the [ticket template](../assets/ticket.md). Tickets are optional; a small clear request needs no artifact.

## TEMPLATE

Before writing, read the template and use its shape: title, `**What to build:**`, `**Blocked by:**`, optional `**Branch:**`, `**Status:**`, acceptance criteria as `- [ ]` lines, then `## Done when`. Put relevant source paths, selected finding IDs and required checks in the behavior or criteria; do not invent a second metadata protocol.

Copy `## Done when` verbatim, in English, whatever language the rest of the ticket uses. It names the executor, prerequisites and completion outcome rather than duplicating its complete instructions. Existing tickets retain their execution text and any `Do not commit` prohibition unless a specific revision is separately approved; the new template does not migrate them.

## NUMBERING

A ticket defaults to `.scratch/<feature-slug>/issues/NN-<slug>.md`; reuse an established explicit location. Read every existing issue, including decision files and rejected work, before allocating numbers. `NN` is `01` when `issues/` is empty or absent, otherwise one past the highest existing number. Number new tickets in dependency order, so a newly created blocker carries a lower number than what it blocks. Never renumber or regenerate existing tickets.

## FIELDS

- `**Blocked by:**` names numbers first - `01`, or `01, 03` - with a title optional after each number. Write `None (can start immediately)` only when no dependency remains; an unknown dependency never becomes `None`. `resolved` is the gate to start, not evidence of the result: `## Done when` has the executor confirm each blocker's result in the working tree before editing.
- `**Branch:**` uses an explicitly approved branch when supplied; otherwise propose `<type>/<feature-slug>`, shaped by the project's branch rule, with `<type>` from the work (`feat`, `fix`, `refactor`, `chore`, `docs`). A project without a branch rule still gets the proposal. Show it for approval before saving; the user may change or drop it. A ticket without it runs on the current branch. Preserve existing branch restrictions and never silently reconcile them by rewriting history.
- `**Status:**` starts as `ready-for-agent`, or `needs-info` only when an explicitly authorized draft has an isolated open `[NEEDS CLARIFICATION: ...]` in its own body. A material open question in the feature's `spec.md` or `root-cause.md` stops new ticket production until answered. `ready-for-human` and `resolved` are execution states, never creation defaults. After a human step, the human sets `ready-for-human` back to `ready-for-agent` and resumes the selected executor, which verifies actual evidence. `wontfix` requires a user decision or an existing ticket's explicit exception; non-reproduction alone never silently rejects new work.
- The checkboxes are observable acceptance criteria, checked only after verification. Keep implementation steps in the approved plan, not a `### Task` section. Preserve existing review-origin non-reproduction rules only where that ticket already grants them; otherwise document the finding and missing evidence without removing its criteria or claiming a fix.
- No `## Parent` section and no back-link: the shared feature directory is the whole link to the spec or root cause.
