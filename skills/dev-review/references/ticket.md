# TICKET

Read this reference before writing a ticket. `to-tickets` owns these rules and the template; `dev-review` and `dev-exec` bundle identical copies and keep their own gates.

## TEMPLATE

Before writing, read the [ticket template](../assets/ticket.md) and write each ticket exactly in that shape: title, `**What to build:**`, `**Blocked by:**`, optional `**Branch:**`, `**Status:**`, acceptance criteria as `- [ ]` lines, then `## Done when`.

Copy `## Done when` verbatim, in English, whatever language the rest of the ticket uses. `dev-exec` reads that block when executing a ticket. Never edit, shorten or translate it. Existing tickets retain their execution text and any `Do not commit` prohibition unless a specific revision is separately approved; the new template does not migrate them.

## NUMBERING

A ticket is `.scratch/<feature-slug>/issues/NN-<slug>.md`. `NN` is `01` when `issues/` is empty or absent, otherwise one past the highest existing number. Number new tickets in dependency order, so a blocker always carries a lower number than what it blocks. Never renumber existing tickets.

## FIELDS

- `**Blocked by:**` names numbers first - `01`, or `01, 03` - with a title optional after each number. Write `None (can start immediately)` only when no dependency remains; an unknown dependency never becomes `None`. `resolved` is the gate to start, not evidence of the result: `## Done when` has the executor confirm each blocker's result in the working tree before editing.
- In an explicit controlled-run context, every new ticket uses the approved feature branch. Reconcile existing branches instead of silently rewriting their history. Outside that context, `**Branch:**` always proposes `<type>/<feature-slug>`, shaped by the project's branch rule when one exists, with `<type>` from the work (`feat`, `fix`, `refactor`, `chore`, `docs`), unless the writing command sets its own `<type>` or value. A project without a branch rule still gets the line. Tickets of one feature may therefore name different branches. The user may change or drop the line; a ticket without it runs on the current branch.
- `**Status:**` is `ready-for-agent`, or `needs-info` when an open `[NEEDS CLARIFICATION: ...]` marker sits in this ticket's own body. A marker still open in the feature's `spec.md` gates the whole feature: write no tickets until it is answered. `ready-for-human` and `resolved` are written by the executor under `## Done when`, never at creation. After the human step, the human sets `ready-for-human` back to `ready-for-agent` and reruns the selected executor on the ticket. `wontfix` is set by the user, or by the executor only under the first criterion of a ticket from `dev-review` when none of its findings reproduced.
- The checkboxes are acceptance criteria, flipped once when the ticket closes. Under the first criterion of a ticket from `review`, the executor removes the criteria of a finding that did not reproduce, so a later review never checks them. Never write a `### Task` heading or an implementation checkbox in a new ticket: harness plan mode writes its plan in the chat.
- No `## Parent` section and no back-link: the shared feature directory is the whole link to the spec or root cause.
