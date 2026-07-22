---
description: Intake a task that carries an identifier - a tracker key/URL or a pasted ticket - extract structure, separate facts from assumptions, classify task vs bug, and route. The identifier also names the downstream plan / brief. Background knowledge, not a user command.
user-invocable: false
---

# TASK INTAKE

Load when a task carries a tracker key or URL (e.g. `PROJ-1234`) or comes as a pasted ticket. Background knowledge, not a user-invocable command. Consumed by `/nxs:rnd` and `/nxs:bug`: run this first, then hand control back to the flow. The extracted identifier also names the downstream plan / brief so they stay navigable by it.

## READ THE TICKET

- Key or URL: read the ticket through a tracker API / integration if one is available. If not, ask the user to paste the ticket text.
- Pasted text: work from it directly.

Do not invent the ticket's content from the key. If it cannot be read, say so, ask for the text, and continue from what is pasted.

## EXTRACT

From the ticket pull: the problem in one sentence; the expected behavior and context; acceptance criteria; type (task or bug); links and dependencies; comments and attachments; the identifier.

Priority counts as a fact only when the ticket states it.

## FACTS VS ASSUMPTIONS

Facts are what the ticket or the code states directly. Assumptions are what you infer - implied behavior, a guess at the root cause, scope, or consumers. Mark every assumption explicitly and never let one pass as a fact.

## TASK VS BUG

| type | signals | route |
|---|---|---|
| task | new functionality, refactoring, migration, improvement | `/nxs:rnd` |
| bug | broken behavior, regression, error | `/nxs:bug` |

If the type is unclear, ask rather than guess.

## UNKNOWNS

- Acceptance criteria not specified -> record as unknowns and either ask or formulate candidates for confirmation. Do not start planning a nontrivial task without clear AC.
- Constraints - what must not break (compatibility, performance budget, deadline, dependencies) - are called out separately.
- Unknowns rank above the plan; close them with a question before planning.

## OUTPUT

Emit a structured summary - problem, identifier, acceptance criteria (or unknowns), facts, assumptions, constraints, unknowns, type, next step - then hand control to the routed flow. Do not plan the solution during intake.
