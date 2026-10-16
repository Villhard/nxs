# TICKET

Read this reference before writing a ticket. `rnd`, `bug` and `review` create tickets by these rules; each command keeps its own gates for when a ticket may be written.

## TEMPLATE

Before writing, read the [ticket template](../skills/rnd/assets/ticket.md) and write each ticket exactly in that shape: title, `**What to build:**`, `**Blocked by:**`, optional `**Branch:**`, `**Status:**`, acceptance criteria as `- [ ]` lines, then `## Done when`.

Copy `## Done when` verbatim, in English, whatever language the rest of the ticket uses. Harness plan mode sees only the ticket text, so that block is the whole execution contract for `/plan <ticket-path>`. Never edit, shorten or translate it.

## NUMBERING

A ticket is `.scratch/<feature-slug>/issues/NN-<slug>.md`. `NN` is `01` when `issues/` is empty or absent, otherwise one past the highest existing number. Number new tickets in dependency order, so a blocker always carries a lower number than what it blocks. Never renumber existing tickets.

## FIELDS

- `**Blocked by:**` names numbers first - `01`, or `01, 03` - with a title optional after each number. Write `None (can start immediately)` only when no dependency remains; an unknown dependency never becomes `None`.
- `**Branch:**` proposes `<type>/<feature-slug>` by the project's branch rule when one exists, with `<type>` from the work (`feat`, `fix`, `refactor`, `chore`, `docs`), unless the writing command sets its own `<type>` or value. Tickets of one feature may therefore name different branches. The user may change or drop the line; a ticket without it runs on the current branch.
- `**Status:**` is `ready-for-agent`, or `needs-info` when an open `[NEEDS CLARIFICATION: ...]` marker sits in this ticket's own body. A marker still open in the feature's `spec.md` gates the whole feature: write no tickets until it is answered. `ready-for-human` and `resolved` are written by the executor under `## Done when`, never at creation. `wontfix` is set by the user, or by the executor only under the first criterion of a ticket from `review` when none of its findings reproduced.
- The checkboxes are acceptance criteria, flipped once when the ticket closes. Under the first criterion of a ticket from `review`, the executor removes the criteria of a finding that did not reproduce, so a later review never checks them. Never write a `### Task` heading or an implementation checkbox in a new ticket: harness plan mode writes its plan in the chat.
- No `## Parent` section and no back-link: the shared feature directory is the whole link to the spec or root cause.
