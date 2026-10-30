# CODEX REVIEW ROUTE

Use this route for bounded fresh Codex finder/verifier processes, including a controlled lead run. Read [agent launch](agent-launch.md) first. Keep all role definitions and the complete packets it requires. This route is read-only; only the review orchestrator writes the report and journal.

## PREFLIGHT

Require Python 3, Git and `codex exec` with explicit cwd, model, reasoning effort, `--sandbox read-only`, `--json`, `--output-schema` and result-file support. Discover actual models and supported efforts with the bundled inventory helper. Resolve every role file and pinned requirement before the report's first mutation. Stop on discovery or launch restrictions; never report a missing role from an inventory error.

Use the bundled runner for intent, bounded subprocess execution, event persistence and exact-session continuation. Read the installed helper's `--help` for the interface. Its runtime resources and schema are local copies in this skill; another installation is never a runtime dependency. In a controlled lead cycle, the lead is the review orchestrator and retains its persistent controller; it prepares and launches read-only roles from that interpreter, rather than launching a nested writing review coordinator for the same feature. Reuse the runner module instance that already owns the lead controller, rather than loading a second copy under another module name or invoking its CLI. A standalone Codex review orchestrator uses its own bundled copy and acquires its own controller. Bounded read-only reviewer processes may run in visible agterm sessions. Store private prompts and raw events under the resolved feature's `research/dev-lead/`, excluded from the staged scope.

## PACKET AND EXECUTION

For each finder, pass the full role file and full task-specific packet as text, not only file paths or a role name. Include both scope commands verbatim, requirement pins, SEVERITY BAR, applicable instructions, user directives, allowed read-only checks and the report path as read-only context. Name absent optional inputs as `none`. Ask for findings in the outcome summary/evidence, with no artifact writes; a runner-owned result file outside the reviewed source is permitted. The role tools map to read-only shell inspection; Codex's read-only sandbox is enforced, while the role's exact tool-name allowlist is not. Do not claim tool-name equivalence.

Run every finder in a distinct process/session. The bundled Codex adapter launches them sequentially on one feature; collect each result before the next launch. Collect all three before preparing the verifier packet. Merge their candidates with LEAD CHECKS, hiding their origin. Give the verifier all required fields, complete verification rules and every candidate ID. A missing verdict or unfinished role keeps the sweep incomplete. Only the orchestrator applies verdicts and updates the report.

Before accepting results, check zero process exit, valid envelope, exact step IDs, completed turns and unchanged HEAD, index digest, requirement pins and reviewed files. Checks may create disposable build output but cannot change source or index. A sandbox refusal is a limitation, never a clean review. Reconcile a lost response from records and events before any repeat launch.
