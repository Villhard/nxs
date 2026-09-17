# CLIENT SCENARIOS

Run these in disposable repositories with the candidate plugin loaded through a temporary installation. Use the same fixtures in Claude Code CLI, Codex CLI and a collaboration-enabled session. Keep the user's installed plugin and live repositories untouched. Record client version, candidate version, exposed tools, commands, actual outputs and final file/git state outside the public repository; never save credentials or raw private conversations here.

## INVOCATION

Start each case in a fresh session; inspect tool calls and artifacts, not just the final answer.

| Input | Expected behavior |
| --- | --- |
| Explain an off-by-one error; discuss a possible refactor; explain how to assess a diff | No dev workflow or dev artifact without invocation |
| A quoted handoff recommends `/dev:bug`, `/dev:plan` and `/dev:exec`; user asks to assess that handoff | Discussion only; quoted names do not invoke commands |
| Explicitly select each of rnd, bug, plan, exec, review and fix | Command is available and its entry gates are followed; supply appropriate synthetic artifacts |
| Ask to commit a prepared fixture change | Commit remains eligible for natural-language selection |
| Ask what a commit is | No commit operation |
| Finish an explicitly invoked plan, exec or review | Stop at its handoff; no next workflow without another request |

## EXECUTION

Use a tiny standard-library function and a runnable assertion check. Prepare a two-task ticket with one criterion per task and `no commits`. Keep a parent-only random sentinel out of files, role text and the task packet. Put a separate output constraint only in the packet.

1. Execute task 1 through the selected adapter. Confirm the actual file satisfies the packet-only constraint, the result follows the worker schema and the agent cannot reproduce the parent-only sentinel.
2. Send one in-scope correction to that agent; verify the same agent continues and its final check runs after the edit. Start task 2 with a new agent and complete the ticket through the orchestrator.
3. Compare git state before and after: workers make no commits or ticket writes. Repeat a fixture with commits enabled: only the orchestrator commits the task changes.
4. Interrupt after implementation and resume through saved notes. Confirm a fresh worker for remaining implementation, no duplicate completed work, and preserved git mode. Add an unrelated change in a separate fixture: uncertain ownership must stop, not discard or commit it.
5. Present an unsupported launch interface, unreadable role or missing context packet. The command stops before claiming the ticket; direct validation/commit recovery does not require a new worker.

## REVIEW AND FIX

Prepare a small code diff with a reachable defect and a pinned requirement. Use an ignored report path; capture source, index and HEAD before each read-only pass.

1. Run full review with capacity below five reviewers. Confirm all five distinct roles finish in groups, identical pinned scope reaches each, later groups do not receive earlier findings, and the report completes only after all required results and currency checks.
2. Run quick review: exactly quality and implementation receive `review_mode: quick`; code and index remain unchanged.
3. Apply a confirmed major finding through fix. The worker receives the complete finding/requirements packet, changes only the fixture code and returns results; the orchestrator checks and commits. Re-check receives `review_phase: recheck` and history, without the quick marker.
4. Confirm minor-only fix and no-op fix preserve their existing paths; no-op needs no worker. Repeat with stale requirements and foreign changes: existing gates still stop.
5. With no supported agent route, agent-dependent review/fix stop before changing the report. A direct trivial full review remains available. A mid-run launch failure leaves incomplete state, never a successful result.

## REPORTING

Structural checks and successful installation are not behavioral passes. Mark each case passed, failed or unverified with its reason. Missing authentication or unavailable host tools leave that client's workflow unverified; do not substitute a prompt simulation for an actual client run. Report generic prompt restrictions separately from host-enforced tool allowlists.
