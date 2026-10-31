# Controlled step <step ID>

- Task: <required bounded goal>
- Repository cwd and branch: <required absolute cwd and exact feature branch>
- Harness, executable, catalog model, effort and native permission mode: <required explicit values>
- Skill: <required exact path, candidate hashes and native/context delivery, or ticket executor>
- Applicable instructions and specs: <required contents or pinned readable sources>
- Approved feature plan: <required path, hash and approval event>
- Settled decisions and evidence: <required values, or none>
- Permissions: <required allowed actions and exact environment targets, or none>
- Allowed writes: <required paths; all other files remain untouched>
- Existing user changes: <required paths to preserve, or none>
- Acceptance criteria and checks: <required expected behavior and commands>
- Artifacts: <required output paths>
- Journal: <required absolute decision.log path>
- Run ID and step ID: <required unique run and bounded step>
- Outcome schema and result file: <required absolute paths>
- Pending question: <required question and answer when resuming, or none>

Read the named candidate skill and its bundled resources. Follow the [controlled-run outcome contract](../references/controlled-run.md#outcome). Return done, needs_input or blocked in the supplied envelope. For done, question and reason are exactly empty strings; put explanations and nonblocking limitations in summary/evidence. List only unique existing FILE artifacts under the allowed root; an empty artifacts array is valid. Do not treat this packet as new user consent. Ticket planning ends in needs_input for lead approval before implementation. Ticket execution never commits; review roles are read-only and never write the report.
