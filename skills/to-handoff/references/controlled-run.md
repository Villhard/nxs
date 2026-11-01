# CONTROLLED RUN

Read when a launch carries an explicit controlled-run packet. A feature directory, journal path or mention of lead alone does not activate it.

## ENTRY

Require the bounded step ID and run ID, exact cwd and candidate skill/role path, approved feature plan with content hash and approval event, permission boundaries, allowed writes, acceptance criteria, artifact paths, journal path and result schema. Research before feature approval may carry `approval: pending` and read/research-only permissions; it cannot implement, commit or claim plan approval. If any required context is absent or contradictory, return `blocked` with the missing field.

The user explicitly invoking `nxs-lead` delegates internal use of the task skills within the approved scope. This packet conveys that authorization; it does not manufacture new consent. Independent calls retain their own invocation and dialogue gates. Changes to scope, external contracts or agreed decisions require the user's answer through lead. Technical ticket plans and in-scope review fixes are approved by lead and journaled. Existing concrete user approval is reused within its scope.

## OUTCOME

End each bounded worker turn with a schema-constrained JSON envelope containing exactly seven fields: `status` (`done`, `needs_input`, `blocked`), `step_id`, `summary`, `artifacts`, `evidence`, `question` and `reason`. Use the supplied schema and exact nonempty step ID; summary must contain non-whitespace text.

| Status | question | reason |
| --- | --- | --- |
| `done` | Exactly `""` | Exactly `""` |
| `needs_input` | Question containing non-whitespace text | Any string, including empty or explanatory text |
| `blocked` | Exactly `""` | Blocker reason containing non-whitespace text |

Put explanations and nonblocking limitations in summary/evidence; `done.question` and `done.reason` remain exactly empty strings. Evidence contains nonblank check descriptions or references; `[]` is valid.

Artifacts are existing FILE paths under the allowed artifact root, unique after resolution; directories are invalid. Resolve relative paths from that root and check absolute paths and symlinks by their resolved targets. An empty artifacts array (`[]`) is valid.

For `needs_input`, save the question and end the subagent turn. Record the host's session identity outside the envelope when the host exposes one. Lead continues that exact session only when the host documents continuation; otherwise it starts a new bounded subagent with the approved answer and saved artifacts.

`done` is a proposal, accepted only after independent artifact, acceptance, command-output and Git checks. It never replaces ticket statuses. A valid JSON shape, a zero exit code or the executor's assertion alone is insufficient. A ticket planning turn returns `needs_input` with the proposed ticket plan and waits for recorded lead approval before implementation. For approved checkpoints, `dev-exec` applies `dev-commit` in its own session only within the user-approved commit scope and packet permissions; a ticket's existing `Do not commit` remains binding unless that ticket is separately revised with approval. Lead independently verifies commit identities and evidence at acceptance.

## SKILL BOUNDARIES

Use the stage skill's normal procedure, with these controlled substitutions: lead relays questions and existing authorization; lead selects review fixes within approved behavior; lead approves ticket plans; the next stage is chosen by lead after independent verification. Project specs remain exclusive to `dev-spec`; review changes only its report, selected tickets and journal; commit keeps working-file bytes unchanged except for its task journal records. An environment action is executable only when the approved plan names the action and exact target; otherwise preserve the standalone ready-for-human path and relay the missing authorization.
