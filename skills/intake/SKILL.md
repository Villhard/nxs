---
description: Intake a task that carries an identifier - a tracker key/URL or a pasted ticket - extract structure, separate facts from assumptions, classify task vs bug, and route. The identifier also names the downstream plan / brief for navigation. Background knowledge, not a user command.
user-invocable: false
---

# TASK INTAKE

Load when a task carries an identifier (a tracker key or URL, e.g. `PROJ-1234`) or comes as a pasted ticket. Background knowledge, not a user-invocable command. Consumed by `/nxs:rnd` (task entry point) and `/nxs:bug` (bug entry point): when either receives an identified task or a pasted ticket, run this intake first, then hand control back to the flow. The extracted identifier also names the downstream plan / brief so they stay navigable by it.

## INPUT DETECTION

Recognize three input shapes:

- Identifier key - a project key plus a number, e.g. `PROJ-1234`.
- Tracker URL - a link to a ticket in an issue tracker.
- Pasted ticket text - the ticket body pasted directly, or any task / bug description.

What to do per shape:

- Key or URL: if a tracker API / integration is available, read the ticket through it. If none is available, ask the user to paste the ticket text.
- Pasted text: work from it directly, no fetch needed.

Do not invent the ticket's content from the key. If the ticket cannot be read, tell the user it cannot be read, ask for the text to be pasted, and continue from the pasted text.

## STRUCTURE EXTRACTION

From the ticket (or pasted text) pull:

- title / problem - what needs to be solved, in one sentence;
- description - the expected behavior and context;
- acceptance criteria - measurable completion conditions;
- type - task or bug (see below);
- priority - only if stated; otherwise treat it as an assumption or unknown, never as a fact;
- links - related tickets, dependencies, references;
- comments and attachments - read them if present;
- identifier - the key / id used to name the downstream plan / brief, if any.

## FACTS VS ASSUMPTIONS

Keep the two distinct; never let an assumption pass as a fact.

Facts - what the ticket or the code states directly:

- the described expected behavior;
- a stack trace from the ticket;
- reporter comments;
- acceptance criteria.

Assumptions - what you infer but the ticket does not confirm:

- implied behavior that is not stated explicitly;
- a guess at the root cause before confirmation;
- a guess at priority / scope;
- a guess at consumers.

Mark every assumption explicitly. Do not invent facts.

## TASK VS BUG

| type | signals | route |
|---|---|---|
| task | new functionality, refactoring, migration, improvement | `/nxs:rnd` |
| bug | broken behavior, regression, error | `/nxs:bug` |

If the type is unclear, ask the user rather than guessing.

## ACCEPTANCE CRITERIA, CONSTRAINTS, UNKNOWNS

- Acceptance criteria - if not specified, record them under unknowns and either ask the user or formulate candidates for confirmation. Do not start on a plan without clear AC when the task is nontrivial.
- Constraints - what must not be broken: compatibility, performance budget, deadline, dependencies. Call these out separately.
- Unknowns - open questions that need clarification, including missing acceptance criteria. Unknowns rank above the plan; close them with a question to the user (or an explorer) before planning.

## OUTPUT

Emit a structured summary, then hand control to the routed flow:

- problem - one sentence;
- identifier - the key / id used to name the plan / brief, if any;
- acceptance criteria - a list, or unknowns if absent;
- facts - what is known for certain;
- assumptions - what was inferred, each marked;
- constraints - what must not break;
- unknowns - open questions;
- type - task or bug;
- next step - `/nxs:rnd` for a task, `/nxs:bug` for a bug.

Do not try to plan the solution during intake, and do not treat guesses as facts. Surface the structure and the open questions, then route.
