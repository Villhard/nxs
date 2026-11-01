# <NN>: <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list>

**Blocked by:** <the numbers and titles of the tickets that gate this one, or "None (can start immediately)">

**Branch:** <optional: the branch this work goes on; drop the line when there is none>

**Status:** ready-for-agent

- [ ] <acceptance criterion>
- [ ] <acceptance criterion>

## Done when

Execute this ticket directly with `/dev-exec <this file>`.

- Start only when **Status** is `ready-for-agent`, every **Blocked by** ticket is `resolved`, material questions are answered and required prerequisite results are verified in the selected working tree. Respect **Branch** and preserve unrelated changes; status or history alone proves no result.
- Implement only within an approved concrete plan. An install, migration or external action needs approval covering the action and exact target plus native permissions; otherwise record the human step and expected evidence under `## Comments`, set **Status** to `ready-for-human` and stop the affected work. Verify the actual result when the human returns the ticket to `ready-for-agent`; never repeat an uncertain action.
- Close only after every criterion, the project's full test suite, linter and other required checks pass: check the criteria and set **Status** to `resolved`. Record exact verification, missing checks and meaningful decisions or deviations under `## Comments`; prohibited or unavailable verification leaves the ticket unresolved.
- Commits are optional and require explicit authorization for their scope through `dev-commit`. Preserve any existing `Do not commit` instruction. Report actual checkpoint identities, remaining work and verification limits; a commit alone does not complete this ticket.
