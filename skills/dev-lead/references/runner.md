# RUNNER

The installed `scripts/` directory contains Python 3 standard-library mechanics. Use its absolute path from skill discovery, never a guessed installation path. Each CLI has `--help`; CLI calls protect individual operations. A coordinating lifetime additionally holds one `runner.controller(feature)` context in a persistent Python process across every step. A second owner fails through the operating system lock. Release that context only at handoff or completion.

## DISCOVER

```text
python3 <skill>/scripts/inventory.py --harness <codex|claude|opencode> --cwd <repo> --output <feature>/research/dev-lead/inventory.json
```

Resolve the selected CLI executable in the calling shell and pass its absolute path with `--executable` when the GUI process has a different PATH. `prepare` freezes any executable it can resolve before handing the command to agterm. Check both cwd skill status and model status. Use `skill_status` to distinguish enabled, disabled, missing, discovery failure and explicit candidate context. Select exact candidate paths and retain their hashes. A same-name installed copy is insufficient. `prepare` checks the selected model/effort against the catalog; unsupported values stop before launch.

Choose the active harness explicitly in both discovery and `prepare(..., harness=..., executable=...)`; never fall back to another client after an error. Codex uses `skills/list` and paginated `model/list`. Claude uses the Agent SDK stream-json initialize control exchange for commands/models. Its command names do not prove which file is registered: native sources without path evidence stay unconfirmed. To use a known candidate, pass its exact skills root with `--skill-root` and select its exact path in prepare. `skill_status` then reports `context`, not native `enabled`: the runner embeds the candidate SKILL.md text with its absolute resource base and pins all resource hashes. This explicit delivery route does not register or install a skill, and never claims that a same-name installed copy is the candidate. A missing or disabled registry name cannot enable it. Name this delivery mode in the approved feature plan. Unconfirmed native visibility remains a discovery failure, not an absent skill. OpenCode v2 uses a private authenticated loopback server, waits for its skill plugins, then reads native model, agent and skill catalogs through HTTP. The private server is stopped after discovery; credentials remain in memory. Virtual builtin skills have content hashes but cannot replace exact local candidate resources. Discovery errors remain errors.

Use only advertised efforts/variants. If Claude metadata or an OpenCode model omits them, select Python `None` (CLI `--effort default`) to retain the native default; do not infer support from another client. Save the harness, executable, model, effort, permissions and exact candidate paths in each packet. Only the selected CLI must be installed. Claude protocol fixtures do not establish live CLI compatibility.

| Harness | Output and continuation | Permission boundary |
| --- | --- | --- |
| Codex | JSON events, output schema and result file; exact thread UUID | Native read-only/workspace-write sandbox, approval policy never |
| Claude Code | stream-json success result with structured_output; exact session UUID | Existing native rules, dontAsk for reading and acceptEdits for approved writing; no bypass |
| OpenCode v2 | JSON events; strict final-message JSON checked locally; exact ses ID verified with session.get before resume | Existing build-agent permissions; no auto approval; unavailable permission yields a blocked run |

For Claude/OpenCode read-only workers, macOS sandbox-exec denies writes throughout the resolved repository, including writes from shell tools, while allowing the CLI's session/cache storage elsewhere. It is source protection, not full filesystem isolation; missing enforcement stops launch. Writing workers retain the native client's permissions, not an emulated Codex sandbox. Prompt path restrictions are not an OS allowlist. A native session never migrates between harnesses. Another coordinator may read the shared journal and reconcile, then resume through the saved harness; starting a different harness is a new bounded step after the prior effect is known.

## HOLD OWNERSHIP

Use a persistent Python interpreter through the client's terminal/session tool, then submit mechanics calls to that same interpreter. The lead continues choosing every action. For example, start Python with the installed scripts on `sys.path`, import `runner`, `inventory` and `mechanics`, then enter:

```python
owner = runner.controller(feature)
owner.__enter__()
```

Keep that interpreter alive while coordinating. Calls to `prepare`, `launch`, `reconcile` and `verify` in the same thread reuse its ownership. `owner.__exit__(None, None, None)` releases it. A one-shot `prepare` followed by an unrelated controller process does not establish lifetime ownership. After losing the interpreter, check whether it is alive and reconcile its recorded runs before acquiring a new controller; never start a competing owner.

## LAUNCH AND CONTINUE

`runner.prepare(task, run_id, step_id, cwd, inventory, model, effort, sandbox, prompt, artifact_root, ...)` reserves a unique run ID and saves immutable context, schema, selected skill identities and initial Git evidence. Use `workspace-write` for writing workers and `read-only` for finder/verifier runs. Keep task records ignored under the explicit feature directory. They must not enter completion snapshots or commits.

`runner.launch(run)` saves intent before creating the visible agterm session. Confirm its returned session ID and actual process in `agtermctl tree --json`. The worker writes raw event bytes, stderr, session ID, PID, command, timeout and exit status while streaming terminal output. A failed or lost IPC response is uncertain; never call launch again for that run ID. Session creation uses `--wait`; restoring a terminal may rerun its initial command, so the durable run claim must reject duplicate execution.

`runner.reconcile(run)` compares saved records, current process ownership, events, result and Git state. `needs_input` includes the saved question and session ID. Record the answer/approval, then prepare a new unique run with `resume_from=previous_run`; this keeps the exact native session ID and harness and consumes the question once. Do not use `--last`. A structured `blocked` result with a saved session may resume only after lead records `<previous-run-id>:resolution` with evidence resolving its cause; a failed CLI without a validated saved outcome is not this route. A failed or uncertain run is reconciled, never silently replaced with a new run ID.

## ACCEPTANCE

`runner.verify(run, commands, verifier)` runs separate explicit command argv lists after a proposed `done`, retaining actual stdout, stderr and exit codes and pinning artifact hashes and Git state. The lead first inspects the artifact contents and every criterion; these checks cannot be replaced by schema validation. Failed or interrupted checks retain evidence and do not authorize automatic repetition of a potentially mutating command. Changed source, index, HEAD, immutable artifacts or check output invalidates a saved completion. A decision.log artifact and its derived journal-state.json cache pin the existing journal prefix; the cache must match authoritative events. Later valid append-only events do not invalidate it, and rewriting its prefix does. After inspecting stale evidence, the lead may explicitly verify again with a new `attempt_id`; old check outputs and reports remain in their attempt directories. An unknown or failed mutating check is reconciled before a new attempt. After an ungraceful interruption, inspect tool subprocesses as well as wrapper/CLI PIDs; `acknowledge-stopped` rejects a surviving recorded process group. If an escaped or unobserved tool process cannot be ruled out, keep the run uncertain.

The outcome CLI checks schema fields, exact step, required question/blocker and artifact containment/existence. A result outside its allowed root, malformed stream, missing result or unfinished turn remains invalid or blocked. Ticket statuses remain unchanged by helpers.

## JOURNAL AND COMMIT RECOVERY

Use `journal.py append <decision.log> <event-id> <kind> '<JSON object>'` for semantic events. Include timestamp, step ID, concise decision/question/answer and evidence links in the data. Use `recover` to rebuild state after append succeeded but state replacement was interrupted. Identical event retries are idempotent; conflicting IDs and torn records stop for reconciliation without truncating history.

While holding lifetime ownership, import the bundled `commit` module in the same persistent interpreter and call `commit.intent(feature, operation_id, cwd)` before authorized `dev-commit`, then `commit.reconcile(feature, operation_id, cwd)` after response loss. The CLI equivalents apply only outside a held lifetime controller; another process cannot reuse its lock. Reconciliation identifies a direct-child HEAD only when its parent, committed tree, index, branch and working files match intent. `committed_observed` is evidence to inspect, not an instruction to commit again. Unchanged HEAD or a later/unrelated commit stays uncertain. This helper never commits, rewrites history or chooses the next action.
