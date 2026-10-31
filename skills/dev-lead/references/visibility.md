# VISIBLE STATUS AND QUESTIONS

Read before publishing progress, opening a questionnaire, waiting for a result or recovering UI state. These are lead-only mechanics bundled beside the runner. Import `status` and `approval` from this skill's discovered scripts directory in the same persistent interpreter that holds `runner.controller(feature)`. Public calls require that ownership in the calling thread. The bounded waiter is a child CLI process, never another controller or agent.

## STATUS

Call `status.publish(feature, event_id, progress, identity)` at each stage/action change. Use the verified saved lead identity, never worker environment variables or GUI `active`. Required progress fields:

| Field | Value |
| --- | --- |
| `stage`, `step_id`, `action` | Explicit nonempty lead-supplied text |
| `reason` | Current waiting/blocker text, or empty string |
| `current_run` | Exact saved run ID, or `None` |
| `accepted_tickets` | Distinct `{ticket, event_id}` entries referencing lead `ticket.implementation.accepted` events with matching ticket paths and nonempty evidence |
| `last_commit` | `{head, event_id}` referencing a lead `ticket.checkpoint.accepted` event with matching HEAD and evidence, or `None` |

The lead independently checks work before writing those acceptance/checkpoint events. Helpers validate their references; a checkbox, worker outcome or submitted answer cannot accept work. A heartbeat is not semantic progress. `publish` appends `progress.changed` before rendering; repeating an ID with different content fails. `status.refresh(feature, identity)` updates the UTC observation time without appending `progress.changed`. A changed, tree-confirmed HUD specification is saved as `hud.owned` before its derived cache, so cache loss retains exact ownership evidence. `status.reconcile(feature, identity)` rebuilds from journal semantics and checks the referenced run/HEAD. Report its stale references instead of advancing from them.

Readable `research/dev-lead/status.md` contains stage, ticket/step, action, reason, accepted ticket count/IDs, current run, last verified commit and separate UTC observation/semantic timestamps. No completion percentage is inferred. `presentation.json` is a derived UI cache. Both stay ignored and out of Git.

HUD message/detail are plain text limited to 256 characters each; the complete action/reason remains in status.md. Open/update uses explicit socket/window/session with `--position top-right --spinner-style dot`; dot enables the spinner itself. Updates repeat all presentation options. Native theme colors remain unchanged.

Inspect `overlay`, `htmlOverlays`, `paneOverlays`, `ask` and `hud` before painting. Existing overlays/asks and pending owned questions suppress HUD writes, while local status continues updating. Changed or unknown HUD ownership is preserved. To adopt a manual HUD the lead knows it owns, call `status.adopt_hud(feature, event_id, identity, exact_observed_hud)` with the entire actual tree specification; labels are insufficient. Do not adopt another user's panel to make a heartbeat succeed.

When a question closes or a restart drops UI, refresh from reconciled durable state and restore the active owned HUD only in a free slot. Lost HUD replies are observed before another update. The protocol has no atomic compare-and-swap against concurrent user changes. Return/report an ownership conflict rather than claiming stronger isolation. On `ui: error`, report the actual diagnostic in the conversation and point to status.md; the helper saves the HUD command/response when a write was attempted. Socket permissions do not imply a missing app. Never silently disable active visibility.

After completing the work and recording handoff, publish final progress with `current_run: None`, then call `status.finish(feature, event_id, identity)` while still holding the controller. It requires no pending questionnaire and durably ends presentation for that exact progress event. It closes only the tree-confirmed owned HUD with explicit socket/window/session, retaining the final status file and journal. Check `ui: cleared` before releasing ownership; report preserved foreign/covered UI or an unconfirmed close. A recorded close intent is never replayed after a lost response: refresh/reconcile observe its result. Cache loss cannot restore a finished HUD. Resuming work requires a new explicit progress event.

## PREPARE ONE ROUND

The lead groups independent unresolved questions, retaining settled authorization. Workers return questions through their outcome; they never open user UI. Use:

```python
question = {
    'text': 'Which behavior should the affected section use?',
    'step_id': 'ticket-2', 'purpose': 'decision', 'scope': 'affected section',
    'artifact': None, 'worker_run': None,
    'fields': [{'name': 'choice', 'label': 'Behavior',
                'options': ['Keep current behavior', 'Revise this section'], 'required': True}],
}
approval.prepare(feature, 'question-1', question, identity)
waiter = approval.open(feature, 'question-1', timeout=1800)
```

An empty `options` list creates a textarea; otherwise the field is a radio group. There is no selected decision default. Required flags are explicit, field names are unique, and all outside text is HTML-escaped. `artifact`, when present, is `{path, sha256}` for an existing feature-local artifact. An originating `worker_run` is its exact saved ID; prepare verifies a reconciled `needs_input` native session and records harness/session identity. The form's existence is not approval.

One active unconsumed round is allowed. `prepare` writes immutable question/form files and journal evidence under `research/dev-lead/questions/<id>/`. `open` records intent before starting one `approval.py wait --question <question.json> --timeout <seconds>` process. Retain/reap its returned Popen handle with `waiter.poll()` and, once exited, `waiter.wait()`. Its durable exclusive claim and OS lock prevent duplicate waits even after death. The child captures only:

```text
<agtermctl> session overlay open --html <form.html> --js --block --follow --target <lead-session> --window <lead-window> --socket <lead-socket> --json
```

It preserves raw output, PID/group, intent and exit evidence under `wait/`, with no workflow decision or controller acquisition. A timeout stops that CLI group; it does not prove the page closed, expire consent or permit another open.

## REMAIN ACTIVE

Keep the lifetime controller while the questionnaire is pending. Call `approval.poll(feature, question_id)` and `status.refresh(feature, identity)` immediately and at most 60 seconds apart. Nominally schedule a tick every 20 seconds against monotonic time, subtracting time already spent on calls; do not add a full sleep after a slow tick. Individual UI IPCs are bounded to 5 seconds. Limit harness waits to 20 seconds, inspect every returned state and report timing/errors promptly. This active scheduling belongs to the lead, not a helper workflow loop.

`poll` returns observed prepared/pending/submitted/consumed/dismissed/uncertain state and waiter/process evidence. It validates and journals a submitted answer once; it never approves, reopens, launches, cleans up or chooses a stage. Reap the waiter when stopped. A pending page may still be queried after its bounded waiter timed out. Read the exact page outcome, never the unqualified program overlay result:

```text
<agtermctl> session overlay result --page <page-id> --window <lead-window> --socket <lead-socket> --json
```

The `--json` response is `ok/result/pageOutcome {pageID,outcome,value?}`. Submitted `value` is a JSON string decoded into the named-answer object. Exit 0 submitted, exit 2 dismissed and exit 1 pending must agree with the outcome; exit 1 plus an error is not pending. Validate page identity and all required names/values. `parse_outcome(..., direct=True)` is only for explicitly selected non-JSON blocking-open captures with documented direct `{pageID,outcome,value}` output; the transport itself always uses the nested JSON route. No arbitrary envelope search or silent compatibility fallback occurs. Retained finished outcomes are limited to 32; `no such page` leaves missing evidence, never permission to approve or reopen.

On submission, interpret the saved answer in the same active turn. Record a lead `decision` or `approval` event with `question_id` and `answer_event_id: <question-id>:answer`, then call `approval.consume(feature, question_id, decision_event_id)`. Repeating that same use is idempotent; another decision for the same answer fails. Genuine approval must pin the question's exact current `artifact`, `plan_sha256` and `scope`. Only the lead decides that the answer actually grants it. Submission, nonempty text, revision, dismissal and elapsed time never imply approval.

Revisions reopen only their affected scope. Journal that decision, consume that answer, clarify and prepare a new round without discarding unaffected approvals. Do not send a final handoff because a form opened, a revision arrived or a bounded CLI expired. Continue coordination without waiting for a new user message. Only explicit pause/cancel or an actual blocker may end the wait; journal a handoff naming question/page state, processes, answer/use evidence and the next action.

`purpose: probe` is for an authorized presentation probe only. Its form self-submits the first fixture options after eight seconds, is labeled "no approval", and may not pin an approval artifact. Consume its answer only against `probe.observed`. A probe cannot grant feature approval or choose a workflow action.

## RECOVERY

After losing a controller, confirm its process stopped before acquiring one replacement. Call `approval.reconcile(feature, question_id)` before opening anything; it observes the existing wait/page and repairs answer state, without replay. Reconcile status and report failures in the conversation.

| Durable boundary | Recovery |
| --- | --- |
| Progress event before render/cache | Rebuild status; inspect ownership before restoring HUD |
| Open intent before spawn observation | Inspect claim, waiter/PID/group, raw output and exact form-path page association; unknown effects stay uncertain |
| Existing pending page | Recover its pageID in the pinned session and continue polling, with no second open |
| Submitted before capture/answer | Read durable CLI output or exact page outcome and validate the same answer |
| Receipt/answer file before journal | Verify pinned question/page/raw receipt; append one answer event |
| Answer event before cache/use | Rebuild cache and interpret the already-saved answer once |
| Use before continuation | Reconcile the lead's recorded intended run ID before taking its selected action |
| Prepared continuation before launch | Follow existing exact `resume.intent`/immutable run records, never prepare a duplicate |

For a worker continuation, the lead decision records its intended unique continuation run ID and exact question/answer reference before `runner.prepare(..., resume_from=prior_run)`. Include the saved answer in the prompt and preserve the prior harness/native session. `answer.used` records interpretation, not launch completion; runner intent/process/claim evidence determines whether the selected effect occurred. A directory/spec orphaned before continuation intent requires inspection rather than another reservation. Existing runner reconciliation, one-time continuation, stopped-process and cleanup guards remain authoritative. No `--last`, automatic replay, alternative lifecycle or stage selection is added.
