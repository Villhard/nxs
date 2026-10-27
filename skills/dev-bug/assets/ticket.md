# <NN>: <Ticket title>

**What to build:** <the end-to-end behavior this ticket makes work, from the user's perspective, not a layer-by-layer implementation list>

**Blocked by:** <the numbers and titles of the tickets that gate this one, or "None (can start immediately)">

**Branch:** <optional: the branch this work goes on; drop the line when there is none>

**Status:** ready-for-agent

- [ ] <acceptance criterion>
- [ ] <acceptance criterion>

## Done when

Execute this ticket directly, for example with `/plan <this file>`.

- Stop and ask if **Status** is not `ready-for-agent`, a ticket in **Blocked by** is not `resolved`, or this ticket or its feature's `spec.md` / `root-cause.md` has an open `[NEEDS CLARIFICATION: ...]`.
- If **Branch** is set, work on that branch: switch to it, or create it from the current HEAD when missing. Stop and ask if the switch fails.
- If the work needs a migration, a dependency install or an external check, set **Status** to `ready-for-human`, name what is needed under `## Comments` and stop.
- Close when the project's full test suite and linter pass and every criterion above is verified against the running code: check each one and set **Status** to `resolved`.
- Add one line under `## Comments` per decision or deviation.
- Do not commit.
