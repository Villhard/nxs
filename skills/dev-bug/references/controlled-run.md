# CONTROLLED RUN

Read when a launch carries an explicit controlled-run packet. A feature directory, journal path or mention of lead alone does not activate it.

## ENTRY

Require the bounded step ID and run ID, exact cwd and candidate skill/role path, approved feature plan with content hash and approval event, permission boundaries, allowed writes, acceptance criteria, artifact paths, journal path and result schema. Research before feature approval may carry `approval: pending` and read/research-only permissions; it cannot implement, commit or claim plan approval. If any required context is absent or contradictory, return `blocked` with the missing field.

The user explicitly invoking `dev-lead` delegates internal use of the task skills within the approved scope. This packet conveys that authorization; it does not manufacture new consent. Independent calls retain their own invocation and dialogue gates. Changes to scope, external contracts or agreed decisions require the user's answer through lead. Technical ticket plans and in-scope review fixes are approved by lead and journaled. Existing concrete user approval is reused within its scope.

## OUTCOME

End each bounded worker turn with a schema-constrained JSON envelope: `status` (`done`, `needs_input`, `blocked`), `step_id`, `summary`, `artifacts`, `evidence`, `question` and `reason`. Use the supplied schema and exact step ID. List only existing artifacts within allowed paths. `needs_input` includes the saved question and finishes the process; `blocked` names the cause. Persist the session ID outside the envelope too, from session events. Lead resumes only that session after recording the answer.

`done` is a proposal, accepted only after independent artifact, acceptance, command-output and Git checks. It never replaces ticket statuses. A valid JSON shape, a zero exit code or the executor's assertion alone is insufficient. A ticket planning turn returns `needs_input` with the proposed ticket plan and waits for recorded lead approval before implementation. A source-changing ticket executor never commits.

## SKILL BOUNDARIES

Use the stage skill's normal procedure, with these controlled substitutions: lead relays questions and existing authorization; lead selects review fixes within approved behavior; lead approves ticket plans; the next stage is chosen by lead after independent verification. Project specs remain exclusive to `dev-spec`; review changes only its report, selected tickets and journal; commit keeps working-file bytes unchanged except for its task journal records. An environment action is executable only when the approved plan names the action and exact target; otherwise preserve the standalone ready-for-human path and relay the missing authorization.
