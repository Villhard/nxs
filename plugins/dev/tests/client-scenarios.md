# CLIENT SCENARIOS

Run these in disposable repositories with the candidate plugin loaded through a temporary installation. Use the same fixtures in Claude Code CLI, Codex CLI and a collaboration-enabled session. Keep the user's installed plugin and live repositories untouched. Record client version, candidate version, exposed tools, commands, actual outputs and final file/git state outside the public repository; never save credentials or raw private conversations here.

Keep host session state needed for same-worker continuation. In Claude Code CLI 2.1.273, `--no-session-persistence` made continuation fail with `No transcript found`; test the ordinary persistent route separately. Record tool permission denials and retries too. A denied helper call followed by an equivalent successful read is different from a blocked workflow or an attempted forbidden write.

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

## LOCAL HANDOFFS

Use the baseline/candidate and repeated native-run procedure under CONTRACT REGRESSIONS for changed entry and preservation branches. Prepare fixtures before invocation; snapshot all artifact bytes, source/tests, index and HEAD. Keep raw prompts, events, snapshots and per-expectation results in the disposable fixture root. Confirm the client actually reads the intended installed skill/template bytes, not only a matching version label. Do not modify live tracker configuration or install into the user's normal plugin location.

Use a tiny greeting function with existing unittest checks and no dependencies. Specs use the exact seven-heading local template (empty optional sections may be omitted); tickets use the five-field local template with optional Conventions, Implementation and Comments. For an external-format consumer check, populate the inspected local `to-spec`/`to-tickets` templates verbatim and record their source version/hash outside this package. This verifies that artifact revision, not live external production or all upstream versions.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Standalone rnd | No feature; invoke rnd with agreed default/uppercase behavior and authorization to save one local spec/ticket | Reads bundled templates; creates a spec and ready ticket with no Implementation; no external/setup skill, code change or next command. A fresh plan invocation consumes that ticket and preserves spec/source bytes. |
| Fresh clear plan | No `.scratch/`; explicitly ask plan to save the same clear request | One ticket with concrete tasks/checks, no pre-existing ticket required; no rnd or exec invocation. |
| Detailed local artifacts | Exact external local templates; two tickets, 02 blocked by 01, applicable exclusions and an agreed no-trimming Comment | Plan enriches only 01 before Comments, carries constraints into tasks/Conventions, and preserves source spec, 02, criteria and blocker fields. |
| Direct one-unit spec | Invoke plan on approved `spec.md`; repeat with the source outside the feature and an explicit target | One planned ticket; source unchanged, applicable content available in local spec and plan; no repeated interview on settled decisions. |
| Direct multi-unit spec | Invoke plan on an approved two-unit spec, then explicitly invoke rnd in a separate session | Plan stops before writing or invoking rnd. Rnd reuses the spec, inspects code and slices without repeating settled shaping. Repeat with an external path; the authorized local copy preserves source bytes. |
| Unresolved source | Spec has a clarification marker, or a ready ticket's Comments contain an unresolved material question | No executable plan/handoff; name the actual question. Spec questions gate all slicing. Approved draft saving does not answer a question. |
| Spec collision | External spec differs from existing target spec, or target has map.md | No source/target overwrite. A differing spec requires a concrete revision decision; a map remains untouched and needs a separate feature directory. |
| Repeated slicing | Same approved spec and four existing tickets: ready/unplanned, planned, claimed with partial checks, resolved with checked criteria and execution notes | A repeat preserves all existing bytes and graph. Authorized new scope appends after the highest number. Changed dependencies requiring old work to move stop for a concrete revision, not general save consent. |
| Decision source | Explicit Type ticket outside a map directory; separately a map directory input | Classifies before writing, preserves decision files, and asks for a distinct implementation deliverable unless already supplied. Never appends Implementation to a decision ticket. Exec's Type exclusion remains. |
| Mixed decision/implementation handoff | Feature without map.md; approved spec, existing 01-decision.md with `Type: decision` and distinct 02-implementation.md without Type, both ready-for-agent with no blockers or Implementation. Invoke rnd on the spec; repeat with `**Type:** decision`. | Reuses existing work unchanged and suggests plan for 02, never 01. Preserves decision context and does not invoke plan. |
| Refactor verification | Green expand/migrate/contract sequence; separately one whose intermediate tickets fail until final integration | Plans the green unit; integration-only-green stops for a compatible breakdown without weakening checks. |
| Remote parent missing | Pasted/read issue identifies a parent, but applicable parent decisions/comments are absent | Names missing parent context; no ready executable handoff or invented constraints. No remote writes. |
| Remote blocker unknown | Source identity and parent context known, blocker field/evidence omitted | Requests evidence; never invents None. An explicitly authorized draft stays needs-info. |
| Remote blocker open/unmapped | Known open remote issue with no verified local mapping, including a number matching an unrelated local ticket | Stops readiness; remote number never becomes an implicit local dependency. Preserve supplied constraints. |
| Remote blocker mapped/resolved | Verified mapping to a local blocker; repeat with it open, then resolved with no unfinished close; also a verified closed remote blocker | Keeps the mapped local number and reports blocked until local resolution. The resolved variant can hand off; satisfied remote evidence remains in context. No status synchronization. |
| Local storage | No tracker configuration; repeat rnd and fresh plan with an unrelated legacy GitHub/GitLab preference in the disposable project and authorization to save the agreed content | Always writes local `.scratch/` artifacts after content/input gates, without preference lookup, setup, backend questions or separate storage approval. Legacy config stays byte-identical; no remote calls or external workflow. Isolate client settings and record any discoverable host configuration so the test does not imply a config-free host. |
| Missing plan diagnosis | Claimed/resolved ticket has no Implementation and no history proving why | Exec stops unchanged, names missing state, and does not attribute it to an unverified producer. |

Use supplied synthetic remote content or an already available read interface; do not exercise real tracker writes. A stop-case pass establishes that boundary only. Separately run a complete candidate rnd -> plan -> exec fixture across fresh invocations before claiming that pipeline; retain `no commits` and inspect worker/artifact/Git actions. Do not repeat unrelated review/launch scenarios for changes confined to handoffs, but keep their existing contracts below.

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

## CONTRACT REGRESSIONS

Compare the released baseline and candidate in separate temporary installations, with identical fixture bytes and user prompts. Use a fresh session per case and repeat each case twice on an available smaller model. Record model, client, package version, prompt, tool calls, exit status, final answer and before/after file, index and HEAD state. Keep credentials, transcripts and the skill-creator comparison viewer outside this repository.

Use a tiny Python standard-library repository: `limits.py` with `resolve_limit(value)` returning `value or 10`, unittest checks for None, zero and a positive number, and AGENTS.md naming the suite and lint commands. No external dependencies. The intended correction is `10 if value is None else value`.

| Case | Setup and invocation | Required observation |
| --- | --- | --- |
| Discussion | Ask to explain a quoted handoff containing command names | No workflow invocation, artifact or code/Git mutation. |
| New plan | No `.scratch/`; explicitly request plan and authorize saving the agreed limit behavior | One new ticket with usable tasks and concrete verification; no implementation or next command. |
| Unconfirmed cause | Root-cause document marks the cause unconfirmed and alternatives still open; invoke plan | Name missing evidence; no executable fix plan or fabricated rejection of alternatives. |
| Feature question | Ready planned ticket; only adjacent spec has a clarification marker; invoke exec | Name the spec question and stop before claims, edits or worker launch. |
| Checked requirements | Resolved ticket has checked criteria, but the reviewed code still replaces zero | Implementation reviewer checks those criteria and reports the broken behavior; files and index unchanged. |
| No-commit recovery | Two completed tasks, attributable uncommitted code, `next: validate; mode: no commits` | Run missing checks, close the ticket, preserve mode and HEAD. |
| Pre-commit interruption | Complete code and tracked ticket, `next: commit`, no receipt commit | Validate current bytes and create exactly one task commit. |
| Post-commit interruption | The same record and code already occur in a completed commit | No repeated worker, completed check or commit; no accidental reopen. |
| Stale fix | Complete report with a disk requirement changed after its recorded hash | Stop unchanged and require review, even when Findings is empty. |
| No-op fix | Current complete report with no open findings | No worker, commit or fix-state fields; unchanged report when no result is added. |
| Staged foreign group | Request only the code fix in one complete file; an unrelated README change is staged | Commit only the selected file; preserve the unrelated working bytes and staged diff exactly. A selected file mixing logical groups stops before changing the index. |

Run the EXECUTION and REVIEW AND FIX scenarios above as well: direct contract checks do not replace fresh-worker isolation, correction, two-task execution, five-role full review, two-role quick review or major-fix re-check. In fix transcripts, verify that internal commits never invoke the standalone commit skill. Check the same boundary during exec.

Grade actions and artifacts, not a promise in the final answer. Use per-expectation `text`, `passed` and `evidence` fields for the skill-creator viewer. Missing model access or unsupported agent tools are unverified capabilities, not passed cases. A current artifact with missing evidence must stop instead of being silently migrated. Publish only a concise, sanitized compatibility summary with the actual limitations.
