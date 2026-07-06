---
description: Parse a Jira key, URL, or pasted ticket - extract structure, separate facts from assumptions, classify task vs bug, and route to the right flow - load on a Jira key, URL, or pasted ticket. Background knowledge, not a user command.
user-invocable: false
---

# JIRA INTAKE

Load on a Jira key, URL, or pasted ticket. Background knowledge, not a user-invocable command. Consumed by `/nxs:rnd-brainstorm` (task entry point) and `/nxs:dev-diagnose` (bug entry point): when either receives a Jira input, run this intake first, then hand control back to the flow.

## INPUT DETECTION

Recognize three input shapes:

- Jira key - a project key plus a number, e.g. `PROJ-1234`.
- Jira URL - a link to a ticket in a Jira instance.
- Pasted ticket text - the ticket body pasted directly, or any task / bug description.

What to do per shape:

- Key or URL: if a Jira API / integration is available, read the ticket through it. If none is available, ask the user to paste the ticket text.
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
- comments and attachments - read them if present.

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
| task | new functionality, refactoring, migration, improvement | `/nxs:rnd-brainstorm` |
| bug | broken behavior, regression, error | `/nxs:dev-diagnose` |

If the type is unclear, ask the user rather than guessing.

## ACCEPTANCE CRITERIA, CONSTRAINTS, UNKNOWNS

- Acceptance criteria - if not specified, record them under unknowns and either ask the user or formulate candidates for confirmation. Do not start on a plan without clear AC when the task is nontrivial.
- Constraints - what must not be broken: compatibility, performance budget, deadline, dependencies. Call these out separately.
- Unknowns - open questions that need clarification, including missing acceptance criteria. Unknowns rank above the plan; close them with a question to the user (or an explorer) before planning.

## OUTPUT

Emit a structured summary, then hand control to the routed flow:

- problem - one sentence;
- acceptance criteria - a list, or unknowns if absent;
- facts - what is known for certain;
- assumptions - what was inferred, each marked;
- constraints - what must not break;
- unknowns - open questions;
- type - task or bug;
- next step - `/nxs:rnd-brainstorm` for a task, `/nxs:dev-diagnose` for a bug.

Do not try to plan the solution during intake, and do not treat guesses as facts. Surface the structure and the open questions, then route.
