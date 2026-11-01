# EXECUTION CONTEXT

Read before inspecting input or choosing a journal. Execute an implementation ticket or clear text request; ticket creation and decision shaping are separate intents.

## INPUT AND LOCATION

- For a supplied ticket path, read that exact file. Missing or unreadable input stops; never reinterpret it as a clear request. Resolve its established feature directory, read applicable `spec.md` and `root-cause.md` when present, and retain its `decision.log`. Read [ticket rules](ticket.md) and the linked template for field/status meaning and the shared executor contract; preserve the supplied ticket's existing execution text and prohibitions. This does not authorize creating or rewriting tickets.
- A bare or Markdown-bold `Type:` field marks decision work, including `Type: task`; preserve it and the map/history and stop before implementation. An explicit distinct implementation ticket or request may coexist in an established map directory without converting its decision files.
- For clear text, use the supplied request and relevant session decisions; create no ticket or spec solely to execute it. Reuse an explicit feature path or unambiguous established task. Otherwise choose a descriptive two-to-four-word lowercase hyphenated task directory under `.scratch/` for journal records. Inspect the destination first, preserve existing content and use a distinct directory if it belongs to another task. Ask only when task identity remains ambiguous. A branch alone never selects the feature or journal.
- Read remote input through an available read interface or supplied content before using it. Establish source identity, applicable decisions and dependencies rather than guessing from a key, URL or ready label. Known open remote blockers require verified local mappings; unknown/unmapped evidence stops affected execution. Never treat remote issue numbers as local ticket IDs or change remote state as a side effect of local execution.

## TICKET GATES

Read the actual ticket, each named local blocker and applicable feature records. An open `[NEEDS CLARIFICATION: ...]` in the ticket, feature `spec.md` or `root-cause.md` stops implementation for an answer; quoted marker syntax in instructions is not an open question.

| State | Action |
| --- | --- |
| Ticket status is not `ready-for-agent` | Stop and ask; do not reopen resolved/rejected work or override ready-for-human. |
| A named blocker is not `resolved` | Stop and ask; do not resolve or execute the blocker here. |
| Ticket has `**Branch:**` | Switch to it, or create it from current HEAD when absent. Stop and ask if switching fails. Preserve unrelated working/index changes; no forced switch, stash or reset. |
| Ticket has no branch | Stay on the current branch. A clear request also stays there unless its approved scope specifies another branch. |
| Required blocker result exists after branch selection | Inspect its actual code/artifacts and run a focused relevant check; append one Comments line naming the evidence before the first implementation edit. |
| Required result is absent, reverted or unverifiable | Write one Comments line naming the missing prerequisite and journal the blocker, then stop without asking. Never merge, cherry-pick or implement it. Controlled use returns `blocked` with that evidence. |

Branch names, status and ancestry do not prove that a result exists. A carried or squashed result may pass by working-tree evidence; a reverted result fails even when its original commit is an ancestor. A branch switch requires repeating the result inspection on the selected tree.

## HUMAN STEPS

For a required dependency install, migration or external check that is undone or unverifiable, set a ticket to `ready-for-human`, append the needed action and expected checkable evidence under Comments, journal it and stop. For a clear request, record the same pending action/evidence in dialogue and the journal without inventing a ticket. Do not perform the human step yourself.

After the human completes the step, resets a ticket to `ready-for-agent` and resumes, verify the actual result in the current environment. A Comments claim alone is not evidence. Do not repeat the human action. If the result is still absent or unverifiable, return the ticket to ready-for-human with the remaining evidence and stop again.

Only in a complete controlled context, an approved feature plan naming both the action and its exact target authorizes performing and verifying that action. An unnamed/unapproved action follows the human-step path. An authorized but unavailable or unverifiable result remains a blocker. Relay missing authorization through lead; a packet carries existing consent and grants no new consent.
