# Controlled step <step ID>

- Task: <required bounded goal>
- Repository cwd and branch: <required absolute cwd and exact feature branch>
- Skill: <required exact path and candidate hashes, or ticket executor>
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

Read the named candidate skill and its bundled resources. Follow controlled-run rules. Return done, needs_input or blocked in the supplied envelope. Do not treat this packet as new user consent. Ticket planning ends in needs_input for lead approval before implementation. Ticket execution never commits; review roles are read-only and never write the report.
