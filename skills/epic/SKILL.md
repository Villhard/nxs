---
description: Chart a foggy effort too big for one session or one brief into a map of investigation items and implementation tasks, then resolve one unknown or hand one ready task to /nxs:plan per session - the epic entry point. Use for a large multi-session feature, a greenfield area, or an open-ended effort where the decomposition itself is not yet visible.
argument-hint: "[loose idea | tracker key | epic name | map path]"
---

# /nxs:epic

Chart a map of a foggy effort too big for one session, resolve its unknowns one at a time, and chart the cleared way as tasks handed to `/nxs:plan` one by one. The epic entry point. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:epic multi-tenant billing platform

Leading words used throughout: the **destination** (where the effort is heading), the **map** (the single index artifact), the **frontier** (open questions takeable now), the **tasks** (the charted route of implementation chunks), the **fog of war** (what you can tell is coming but cannot yet specify).

## STANCE (CHART, DON'T BUILD)

- epic is planning under fog, not execution. It writes no feature code and runs no build; implementation happens through `/nxs:plan` and `/nxs:exec`, one task at a time.
- An epic is a higher abstraction than a task. It gives each task a goal - a direction - and no more; the concrete implementation is found by `/nxs:plan` at its own level, against the code as it is when the task is taken.
- Produce decisions and directions, not deliverables. The pull to just do the work is the signal you have reached the edge of the map - hand off, do not charge the destination.
- One action per session. Charting is one session; after that, each session does exactly one thing: resolve one Frontier item or hand one ready task to `/nxs:plan`.
- The route is charted when nothing is left to decide; the epic is done when every task is done.
- For a bug surfaced along the way, `/nxs:bug`.

## WHEN EPIC, NOT RND

- `/nxs:rnd` shapes one task you can hold in a single session to a plan-ready brief. epic is for the effort you cannot: the decomposition itself is unknown, the work spans many sessions, the destination is wrapped in fog.
- If charting surfaces no fog - the way is already clear, the whole effort fits one session - you do not need an epic. Stop and route to `/nxs:rnd` or `/nxs:plan`.

## THE MAP

A single markdown file, the canonical artifact: `docs/epics/YYYYMMDD-<slug>.md`; when the epic carries a tracker identifier, `docs/epics/YYYYMMDD-<EPIC-KEY>-<slug>.md`. The epic's key names the map only: it does not flow down to the briefs / plans its tasks spawn - each task is its own entity, named by its own key if it has one. An index, not a store: the map gists each closed decision and links to where the detail lives (a brief, an ADR, a findings note), so a decision lives in exactly one place and the map never restates it.

```markdown
# Epic: <name>

- Date: YYYY-MM-DD
- Status: active | complete
- Tracker: <the epic's own key / URL - omit the line if none>

## Destination

<what reaching the end looks like - the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it first.>

## Notes

<domain; skills each session should consult; standing preferences for this effort.>

## Frontier

<!-- open questions; each is takeable when its blockers are all closed -->

### <item title>

- Type: decide | research | spike | prep
- Mode: HITL | AFK
- Blocked by: <titles, or "none">
- Question: <the decision or investigation this item resolves>

## Tasks

<!-- the charted route - implementation chunks; each converts to a plan once its blockers are done -->

### <task title>

- Goal: <what the task delivers and why - direction toward the destination, not implementation; one or two lines>
- Blocked by: <task and / or Frontier item titles, or "none">
- Tracker: <the task's own key - omit the line if none>
- Status: blocked | ready | planned | done
- Plan: <link to its plan under docs/plans/ - added at handoff>

## Decisions so far

<!-- the index - one line per closed item, enough to judge relevance, linking the artifact that holds the detail -->

- <closed item title> -> <one-line gist of the answer> (<link to brief / ADR / findings note - omit when the gist is the whole record>)

## Not yet specified

<!-- fog of war: in-scope questions you can see coming but cannot yet phrase sharply; graduate into Frontier items or Tasks as decisions clear the fog -->

## Out of scope

<!-- work ruled beyond the destination; never graduates -->
```

## ITEM TYPES

Every Frontier item is HITL (worked with the user, who owns the decisions) or AFK (the agent drives it alone). Mode is fixed at charting, so a work session knows without re-deriving whether to engage the user or run autonomously.

- **decide** (HITL) - a decision the user owns. Three ways to resolve, lightest first: the user answers directly in-session (the map's gist line is the whole record); `/nxs:dialectic` (two concrete options head to head); `/nxs:rnd` (the question needs shaping into a brief). Record a significant one through the `decision-log` gate. The default type.
- **research** (AFK) - knowledge outside the working directory: docs, third-party APIs, prior art. Resolve via an explorer subagent (the in-plugin default), or the external `deep-research` skill if available (OPTIONAL EXTERNAL, not shipped with nxs); the artifact is a findings note in the map's notes folder, linked from the map.
- **spike** (HITL or AFK) - a design question best answered by throwaway code (does this state model or logic feel right). Build it per the spike approach in `plan-conventions`; keep the answer as a findings note in the map's notes folder, delete the code.
- **prep** (HITL or AFK) - manual work that must happen before a decision can be made (provision access, move data so its shape is visible). It does rather than decides, and earns its place by unblocking a decision. The agent drives it alone where it can; otherwise it hands the user a precise checklist.

## TASKS

The charted route: implementation chunks, each carrying a Goal - where the chunk is heading and why - not an implementation. `/nxs:plan` finds the concrete how at its own level, against the code as it is when the task is taken; a completed blocker changes reality and may shift the next task's direction, which is why the Goal is re-checked at handoff.

- Tasks graduate from the fog and from resolved decisions like Frontier items do; charting may seed the obvious ones immediately.
- Statuses: blocked (a blocker is open) -> ready (every blocker done / closed) -> planned (handed to `/nxs:plan`, Plan link recorded) -> done (its plan executed).
- Blocked by may name tasks and open Frontier items alike.
- Hard rule: never create a plan for a task while any of its blockers is open.

## FOG OF WAR

The map is deliberately incomplete: do not chart what you cannot yet see. Beyond the frontier lies the fog - decisions you can tell are coming but cannot pin down, because they hang on questions still open. Write them loosely in **Not yet specified**. Resolving a frontier item clears the fog ahead of it, graduating whatever is now specifiable into fresh Frontier items or Tasks - one at a time, until the way to the destination is clear.

Fog or item? The test is whether you can state the question sharply now, not whether you can answer it. Sharp -> a Frontier item or a Task (even if blocked). Not sharp -> Not yet specified.

## OUT OF SCOPE

The destination fixes the scope; work beyond it is out of scope, not fog, and never graduates. When an item or task turns out to sit past the destination - mis-scoped in while charting, or exposed by a resolution - close it and leave one line in **Out of scope** with the reason. It stays out of Decisions so far, which records only what was actually resolved.

## INVOCATION

The argument picks the mode. An existing path, or a name / slug matching a map in `docs/epics/`, -> work that map. No argument: exactly one map with `Status: active` -> confirm it and work it; none or several -> list them and ask. Anything else (a loose idea, a tracker key, a pasted ticket) -> chart a new map.

### Chart the map

1. If the input is a tracker key / URL / pasted ticket, run the `intake` background skill first to parse structure and separate facts from assumptions. The extracted key names the map and stops at the epic boundary (see THE MAP).
2. Name the destination. A short clarify pass (one question at a time, facts read from the code, decisions put to the user) to pin what this effort is finding its way to. The destination fixes scope, so it is settled first.
3. Map the frontier, breadth-first: fan out across the whole space rather than deep on one thread, surfacing the open decisions and the first items takeable now. If this surfaces no fog, stop - you do not need an epic (see WHEN EPIC, NOT RND).
4. Write the map: header, Destination, and Notes filled; Decisions so far empty; the fog sketched into Not yet specified; the items you can specify now under Frontier with Type / Mode / Blocked-by. Where the way is already clear, seed Tasks with their Goals and Blocked-by edges.
5. Stop. Charting is one session; do not also resolve or hand off.

### Work the map

1. Load the map - the low-res view, not every linked artifact. Sync task statuses: for each planned task, check its plan (all checkboxes `[x]`, git evidence) and mark it done; ask the user when unclear. Then recompute blocked -> ready where every blocker is done / closed.
2. Choose one action: the item or task the user named; else hand off the first ready task; else resolve the first Frontier item whose blockers are all closed.
3. Task handoff: re-check the Goal against Decisions so far and the current code - a done blocker may have shifted the direction; adjust the wording if it did. Route to `/nxs:plan` with the Goal and links to the relevant map decisions. Set Status: planned and record the Plan link.
4. Item resolution: resolve by its Type (ITEM TYPES), invoking the skills Notes names. Record it: move the item from Frontier to Decisions so far as a one-line gist, linking its artifact when one exists (brief / ADR / findings note); a resolution with no durable artifact stays gist-only - the map line is the record.
5. Graduate any fog the answer made specifiable into fresh Frontier items or Tasks, clearing it from Not yet specified. If the answer reveals an item or task sits past the destination, rule it out of scope. If it invalidates other items, update or remove them.
6. Close: when Frontier and Not yet specified are empty and every task is done, set `Status: complete`, announce the epic is done, and point to `/nxs:clean` for archiving.
7. Stop after one action.

## ARTIFACT

The map at `docs/epics/YYYYMMDD-<slug>.md` (with the epic's key: `YYYYMMDD-<EPIC-KEY>-<slug>.md`), updated each session. Findings notes from research and spike items live in the map's notes folder - `docs/epics/YYYYMMDD-<slug>/<item-slug>.md`, named after the map file - and are linked from Decisions so far. Durable writes spawned by items - a brief via `/nxs:rnd`, an ADR via the `decision-log` gate - live in their own homes and are linked from the map, never restated in it. Task plans live under `docs/plans/` per `/nxs:plan`'s own naming, linked from the task's Plan line.

## RULES

- Chart, don't build - decisions and directions, not deliverables; no feature code, no build.
- One action per session: resolve one item or hand off one ready task, never more.
- Never create a plan for a task while any of its blockers is open.
- The epic's key names the map only; a task's brief / plan is named by the task's own key, if any.
- The map is an index - detail lives in its artifact (brief / ADR / findings note); a gist-only line is the record when no artifact exists.
- Refer to items and tasks by title, never by a bare number.
- Fog stays fog until its question is sharp; scope beyond the destination is out of scope, not fog.

## DIFFERENTIATION

- `/nxs:epic` - foggy effort bigger than one session; charts a map of investigation items and implementation tasks, one action per session - resolve an unknown or hand a ready task to `/nxs:plan`; decisions and directions, not deliverables.
- `/nxs:rnd` - shape one session-sized task to a plan-ready brief (CLARIFY / EXPLORE / STRESS).
- `/nxs:plan` - decompose a shaped task into sequenced vertical-slice tasks.
- `/nxs:bug` - investigate a bug to a confirmed root cause.

## NEXT

A ready task -> `/nxs:plan` (the epic hands the goal, the plan finds the implementation), then `/nxs:exec`. A now-specifiable chunk that needs shaping first -> `/nxs:rnd`, whose brief feeds `/nxs:plan`. For a bug surfaced on the map -> `/nxs:bug`. Every task done -> the epic closes; `/nxs:clean` archives the map and its notes folder.
