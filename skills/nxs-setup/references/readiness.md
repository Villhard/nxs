# LEAD READINESS REPORT

Read only for `project --readiness` or `global --readiness`. Audit the current cwd and selected harness, report in the conversation, then stop. This route skips normal setup entirely, including its upstream listing. It never proposes/applies a setup diff, installs dependencies, writes instructions/configuration/skills/hooks/ignore rules, changes Git state, or launches workers or UI. Updating this skill does not run setup. Ordinary setup and manual dev skills remain available when readiness is incomplete.

## INPUT AND BOUNDS

Use the explicitly selected harness/executable, otherwise the identifiable active client: Codex, Claude Code or OpenCode. If selection is unknown, report `unknown` and the input needed; never substitute a client. Only the selected CLI is required. Resolve cwd and executable paths; record probe time, commands, exit codes and actual errors without credentials or raw session dumps.

Use native read-only discovery tools when they expose the required evidence, or the selected transport below. Bound simple probes to 5 seconds and the complete native catalog exchange to 30 seconds. Start any discovery subprocess in its own process group, drain stdout/stderr while waiting, limit retained output to 16 MiB, and stop/reap only that group on completion/error/timeout. Never send a task prompt, run an installation, or change permissions to make discovery succeed. A restriction is a diagnosis, not permission to bypass it. Native CLI caches are not a promise of whole-filesystem read-only isolation.

Taskless readiness creates no report file, task directory, journal or status installation. In a controlled task, save evidence only where its packet authorizes it. Do not copy lead naming, UI, cleanup or orchestration rules into user instructions. Do not require another installed skill or a developer checkout to execute this reference.

## REQUIREMENTS

Inspect independently so one missing item does not hide the others. Preserve errors when later probes depend on a missing prerequisite.

| Requirement | Read-only probe and interpretation | Remedy when incomplete |
| --- | --- | --- |
| Git | Resolve `git`, run `--version`. For project mode also run `rev-parse --show-toplevel` at cwd; distinguish outside-repository from Git failure. Global mode may report outside-repository without requiring repository creation. | Make Git available, fix the observed execution error, or select the intended repository for project use. Never init/configure it. |
| Native subagents | Inspect the exposed tools and their schemas for a fresh-context agent, a complete prompt, a completion wait, model/effort selection, a read-only boundary and continuation. Record each capability separately; a familiar tool name alone is not evidence. | Select a client route that exposes the required capabilities, or report the missing capability and stop the affected step. Never install, emulate or fall back to a nested CLI runner. |
| Selected CLI | Resolve the selected executable; run its `--version`. Use the calling cwd for catalog discovery, not another client's catalog. | Restore that executable/access/authentication as the observed error requires. Do not install every client or silently fall back. |
| Skills | Discover `nxs-lead`, `dev-review`, `dev-spec`, `dev-commit` and each explicitly selected route skill individually. Record enabled state, exact source path and SHA256 of SKILL.md and bundled resources, excluding interpreter caches. Reject unreadable/escaping resources and ambiguous candidates; do not expose their contents in the report. | Missing after successful complete discovery: make the required skill available to the selected client. Disabled: enable the intended entry separately. Unknown path, partial/error catalog or restriction: fix that exact discovery issue and rerun. A same-name file or installation lock is not native registration. |
| Models | List actual catalog identifiers and advertised efforts/variants; validate a requested model/effort only if supplied. Never select one here. Empty/malformed/failed catalogs are incomplete discovery. Absent effort metadata means native behavior is unspecified by that metadata; invent neither support nor a model/effort called default. | Resolve the actual auth/catalog/transport error, or separately choose an advertised model/effort. Availability does not prove worker execution or permission enforcement. |

Report a failed/malformed reply separately from a missing member in a successfully read inventory. Continue other independent checks when one capability is unavailable; this is an audit, not entry into lead coordination.

## NATIVE CATALOGS

Use only the selected subsection. All exchanges stay within the deadline above; malformed replies, authentication errors, timeouts, wrong cwd and incomplete catalogs remain `discovery_failed`. Do not replace failure with a filesystem scan or guess.

### CODEX

Start `<selected-executable> app-server --stdio` at cwd. Send newline-delimited JSON with unique IDs:

```json
{"id":1,"method":"initialize","params":{"clientInfo":{"name":"nxs-readiness","version":"1"}}}
```

Require that matching response's `result`, with no `error`, then send `{"method":"initialized"}`. Request `skills/list` with `{"cwds":["<absolute-cwd>"],"forceReload":true}`. Require exactly one `result.data` row for cwd, an empty errors list and well-formed skill entries with name, absolute path and boolean enabled. Pin each selected resource's actual bytes; multiple same-name paths need explicit identification, not first-match selection.

Request `model/list` with `{"limit":100}`; follow each non-null `nextCursor` with a new request using that cursor. Reject empty/repeated/invalid cursors and partial results. Read `data[].model` and `supportedReasoningEfforts[].reasoningEffort`; preserve missing effort metadata as unknown support. Match IDs and keep protocol errors separate from successful empty skill results. Stop the discovery server without creating a thread or running `exec`.

### CLAUDE CODE

Start `<selected-executable> -p --input-format stream-json --output-format stream-json --verbose --permission-mode dontAsk --tools ''` at cwd. Send only an Agent SDK initialize control request:

```json
{"type":"control_request","request_id":"1","request":{"subtype":"initialize"}}
```

Require `type: control_response`, matching `response.request_id`, `response.subtype: success` and `response.response` metadata. Read `commands` and `models`; model identifiers are `value`, efforts are `supportedEffortLevels` when present. Send no user message. Stop/reap the transport after metadata.

Command names alone do not establish registered source paths. Report native path visibility unconfirmed unless the client supplies exact path evidence. An explicitly supplied candidate root may be inspected and hashed for pinned context delivery, provided its name is registered and not disabled; label it `context`, never native registration. Do not guess roots or let disk presence override a missing/disabled command. If exact candidate evidence is unavailable, report the missing evidence and remedy, not ready.

### OPENCODE V2

Start `<selected-executable> serve --hostname 127.0.0.1 --port 0` at cwd with a random per-process `OPENCODE_PASSWORD`; retain any configured username, otherwise use the native username `opencode`. Keep credentials in memory and out of evidence. Parse the process's actual loopback HTTP address; a guessed port or another running server is insufficient.

Make authenticated HTTP GET requests, using Basic authentication and query `location[directory]=<absolute-cwd>`. Each response must have matching `location.directory` and `data`, without an error envelope. Poll `/api/plugin` until `opencode.skill`, `opencode.config.skill` and `opencode.tool.skill` all have `state.status: active`. Failed plugins are errors; unsettled plugins at the deadline are incomplete discovery, not absent skills.

Then read `/api/model`, `/api/agent` and `/api/skill`. Require the `build` agent; evaluate its ordered matching `permissions` for action `skill` and each resource ID (last matching rule wins; unspecified permission remains ask). A deny is disabled, ask is not verified permission to launch. Skills use `id`, `path` and content; hash readable local resources, label virtual builtin content separately. Virtual content cannot establish an exact installed local candidate. Include only enabled chat models, using `providerID/id` and advertised `variants[].id`; absent variants do not authorize invented effort support. Stop/reap the private server after discovery.

## REPORT AND STOP

Show timestamp, cwd, selected harness/executable and one row per requirement: actual value/status, evidence command/source, exact missing item or error, and remedy. Distinguish `verified`, `missing`, `disabled`, `discovery_failed` and `unknown`; report unexecuted probes with their reason. A successful complete catalog is required before claiming absence. Never collapse permission failure, partial results or unconfirmed paths into missing.

Say ready only for the audited prerequisites of the selected route when all required observations succeed. Otherwise report missing requirements and incomplete checks separately. This report does not verify native workers, read-only enforcement, full workflow compatibility or another client's route. Suggest any remedy without performing it, and stop without a setup proposal or automatic handoff.
