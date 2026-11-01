# EXECUTION CONTEXT

Read before inspecting input. Execute an implementation ticket or clear text request; optionally prepare tickets when useful or requested.

## INPUT AND LOCATION

- For a supplied ticket path, read that exact file. Missing or unreadable input stops; never reinterpret it as a clear request. Resolve its established feature directory and read applicable `spec.md` and `root-cause.md` when present. Read [ticket rules](ticket.md) and the linked template for field/status meaning; preserve the supplied ticket's existing execution text and prohibitions. Existing records provide context, not independent authorization.
- A bare or Markdown-bold `Type:` field marks decision work, including `Type: task`; preserve it and the map/history and stop before implementation. An explicit distinct implementation ticket or request may coexist in an established map directory without converting its decision files.
- For clear text, use the supplied request and relevant session decisions; create no ticket, spec or task directory solely to execute it. If durable artifacts are useful and authorized, reuse an explicit feature path or unambiguous established task, or choose a descriptive directory under `.scratch/`. Inspect the destination first and preserve existing content. A branch alone never selects the feature. For source evidence, optional decomposition or ticket production, read [work preparation](work-preparation.md); do not require a feature spec for a clear request.
- Read remote input through an available read interface or supplied content before using it. Establish source identity, applicable decisions and dependencies rather than guessing from a key, URL or ready label. Known open remote blockers require verified local mappings; unknown/unmapped evidence stops affected execution. Never treat remote issue numbers as local ticket IDs or change remote state as a side effect of local execution.

## TICKET GATES

Read the actual ticket, each named local blocker and applicable feature records. An open `[NEEDS CLARIFICATION: ...]` in the ticket, feature `spec.md` or `root-cause.md` stops implementation for an answer; quoted marker syntax in instructions is not an open question.

| State | Action |
| --- | --- |
| Ticket status is not `ready-for-agent` | Stop and ask; do not reopen resolved/rejected work or override ready-for-human. |
| A named blocker is not `resolved` | Stop and ask; do not resolve or execute the blocker here. |
| Ticket has `**Branch:**` | Switch to it, or create it from current HEAD when absent. Stop and ask if switching fails. Preserve unrelated working/index changes; no forced switch, stash or reset. |
| Ticket has no branch | Stay on the current branch. A clear request also stays there unless its approved scope specifies another branch. |
| Required blocker result exists after branch selection | Inspect its actual code/artifacts and run a focused relevant check within the authorized testing scope; append one Comments line naming the evidence before the first implementation edit. A prohibited or unavailable required check leaves the prerequisite unverified. |
| Required result is absent, reverted or unverifiable | Write one Comments line naming the missing prerequisite, then stop. Never merge, cherry-pick or implement it. |

Branch names, status and ancestry do not prove that a result exists. A carried or squashed result may pass by working-tree evidence; a reverted result fails even when its original commit is an ancestor. A branch switch requires repeating the result inspection on the selected tree.

## HUMAN STEPS

An install, migration or external action requires approval covering the concrete action and target, and native permissions; direct scoped authorization needs no coordination packet. Inspect observable effects first if the action may already have occurred. When approval or permission is missing, set an applicable ticket to `ready-for-human`, append the action and expected checkable evidence under Comments, and stop the affected work. For a clear request, report the same in dialogue without inventing a ticket. An authorized but unavailable or unverifiable result remains a blocker; record the expected evidence and pending human step rather than claiming success.

After the human completes the step, resets a ticket to `ready-for-agent` and resumes, verify the actual result in the current environment. A Comments claim alone is not evidence. Do not repeat the human action. If the result is still absent or unverifiable, return the ticket to ready-for-human with the remaining evidence and stop again.
