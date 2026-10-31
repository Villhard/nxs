# LOCAL PROGRESS AND QUESTIONS

Read before publishing progress, asking the user a question, waiting for an answer or recovering local state. These mechanics are lead-only. They write ordinary files under `research/dev-lead/`; they do not open a HUD, start a waiter or own a terminal.

## PROGRESS

At each stage or action change, rewrite `research/dev-lead/status.md`. Keep it readable and include:

- stage and step ID;
- action, in one sentence;
- reason for waiting or the current blocker, or `none`;
- current run ID, or `none`;
- accepted tickets, each with its `ticket.implementation.accepted` event ID;
- the last verified commit checkpoint and HEAD, or `none`;
- an observation timestamp and a separate semantic timestamp.

The lead independently checks work before writing an acceptance or checkpoint event. A checkbox, a subagent outcome or a submitted answer cannot accept work. A timestamp refresh is not semantic progress.

The status file is the durable view. There is no HUD, overlay, page or terminal ownership to preserve, adopt or close. If the host exposes its own progress UI, use it only as a presentation of this file; the file remains authoritative.

## ASK

Group independent unresolved questions into one round. Preserve settled authorization and do not repeat a decision. An internal technical choice is not a user question.

Record the exact question in `decision.log` before asking, with a unique question ID, step ID, scope, the artifact path and hash when approval is involved, and the options. Ask through the host's native question or dialog tool when one is exposed; otherwise ask in the conversation. Do not start a background process to carry the question.

Each field has a name, a label, options and a required flag. Options are behavior choices, never a preselected decision. A free-text answer uses an empty options list. If the answer is an approval, pin the exact artifact, content hash and scope in the journal before consuming it.

One active unconsumed question round is allowed. A submitted answer is recorded as `question.answered`, then interpreted in the same turn. Only the lead decides whether an answer grants approval; submission, nonempty text, revision, dismissal and elapsed time do not. Consume the answer with a decision or approval event that references the answer event.

A revision reopens only its affected scope. Keep unaffected approvals. Do not treat a new question as permission to start another workflow stage.

## AUTO

An explicitly selected auto mode is defined by its own contract. It may prepare a standalone local HTML defense for a decision; opening the file is a user or host action, not a server, network call or new dependency. Its approval is recorded in the journal like any other. Auto never turns a missing answer into consent.

## REMAIN ACTIVE

While a question is pending, keep the lead active and wait through the host's question or completion mechanism. There is no fixed polling loop and no child waiter process. If the host cannot keep the turn open, record a handoff naming the question, the answer needed and the next action, and stop.

## RECOVERY

After an interruption, read `decision.log` and the saved question records before reopening anything. Reconcile the question text, options, answer event and whether that answer was consumed. Never reopen or replay a consumed answer, and never infer approval from a missing reply.

Rebuild `status.md` from journal events and current evidence. Report stale references instead of advancing from them. If the host lost the question UI, ask again only when no answer was recorded; a recorded answer is used once.
