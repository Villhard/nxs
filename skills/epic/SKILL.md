---
description: Chart a foggy effort too big for one session or one brief - name the destination, map its unknowns as investigation items, resolve them one at a time until the way is clear, then hand off to /nxs:rnd or /nxs:plan. The epic entry point. Use for a large multi-session feature, a greenfield area, or an open-ended effort where the decomposition itself is not yet visible.
argument-hint: "[loose idea | tracker key | epic name | map path]"
---

# /nxs:epic

Chart a map of a foggy effort too big for one session, resolve its unknowns one at a time until the way to the destination is clear, then hand off to `/nxs:plan`. The epic entry point. Self-contained skill. Output language and response style come from global rules, not this file.

Leading words used throughout: the **destination** (where the effort is heading), the **map** (the single index artifact), the **frontier** (items takeable now), the **fog of war** (what you can tell is coming but cannot yet specify).

## STANCE (CHART, DON'T BUILD)

- epic is planning under fog, not execution. Each item resolves one decision or investigation; the map is done when nothing is left to decide before planning or doing. It writes no feature code and runs no build.
- Produce decisions, not deliverables. The pull to just do the work is the signal you have reached the edge of the map - hand off, do not charge the destination.
- One item per session. Charting is one session; resolving is one item per session. Never resolve more than one item in a run.
- The next step off the map is `/nxs:rnd` (shape a now-clear chunk to a brief) or `/nxs:plan` (decompose it). For a bug surfaced along the way, `/nxs:bug`.

## WHEN EPIC, NOT RND

- `/nxs:rnd` shapes one task you can hold in a single session to a plan-ready brief. epic is for the effort you cannot: the decomposition itself is unknown, the work spans many sessions, the destination is wrapped in fog.
- If charting surfaces no fog - the way is already clear, the whole effort fits one session - you do not need an epic. Stop and route to `/nxs:rnd` or `/nxs:plan`.

## THE MAP

A single markdown file, the canonical artifact: `docs/epics/YYYYMMDD-<slug>.md`. An index, not a store: it gists each closed decision and links to where the detail lives (a brief, an ADR, a spike findings note), so a decision lives in exactly one place and the map never restates it.

```markdown
# Epic: <name>

## Destination

<what reaching the end looks like - the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it first.>

## Notes

<domain; skills each session should consult; standing preferences for this effort; link to the tracker ticket if there is one.>

## Frontier

<!-- open items; each is takeable when its blockers are all closed -->

### <item title>

- Type: decide | research | spike | task
- Blocked by: <titles, or "none">
- Question: <the decision or investigation this item resolves>

## Decisions so far

<!-- the index - one line per closed item, enough to judge relevance, linking the artifact that holds the detail -->

- <closed item title> -> <one-line gist of the answer> (<link to brief / ADR / spike>)

## Not yet specified

<!-- fog of war: in-scope questions you can see coming but cannot yet phrase sharply; graduate into Frontier items as decisions clear the fog -->

## Out of scope

<!-- work ruled beyond the destination; never graduates -->
```

## ITEM TYPES

Every item is HITL (worked with the user, who owns the decisions) or AFK (the agent drives it alone).

- **decide** (HITL) - a decision the user owns. Resolve via `/nxs:rnd` (shape a sub-chunk to a brief) or `/nxs:dialectic` (two concrete options head to head); record a significant one through the `decision-log` gate. The default type.
- **research** (AFK) - knowledge outside the working directory: docs, third-party APIs, prior art. Resolve via `deep-research` or an explorer subagent; the artifact is a findings note linked from the map.
- **spike** (HITL or AFK) - a design question best answered by throwaway code (does this state model or logic feel right). Build it per the spike approach in `plan-conventions`; keep the answer, delete the code.
- **task** (HITL or AFK) - manual work that must happen before a decision can be made (provision access, move data so its shape is visible). It does rather than decides, and earns its place by unblocking a decision. The agent drives it alone where it can; otherwise it hands the user a precise checklist.

## FOG OF WAR

The map is deliberately incomplete: do not chart what you cannot yet see. Beyond the frontier lies the fog - decisions you can tell are coming but cannot pin down, because they hang on questions still open. Write them loosely in **Not yet specified**. Resolving a frontier item clears the fog ahead of it, graduating whatever is now specifiable into fresh Frontier items - one at a time, until the way to the destination is clear and no items remain.

Fog or item? The test is whether you can state the question sharply now, not whether you can answer it. Sharp -> a Frontier item (even if blocked). Not sharp -> Not yet specified.

## OUT OF SCOPE

The destination fixes the scope; work beyond it is out of scope, not fog, and never graduates. When an item turns out to sit past the destination - mis-scoped in while charting, or exposed by a resolution - close it and leave one line in **Out of scope** with the reason. It stays out of Decisions so far, which records only the route actually walked.

## INVOCATION

Two modes. Either way, never resolve more than one item per session.

### Chart the map

User invokes with a loose idea.

1. If the input is a tracker key / URL / pasted ticket, run the `intake` background skill first to parse structure and separate facts from assumptions.
2. Name the destination. A short clarify pass (one question at a time, facts read from the code, decisions put to the user) to pin what this effort is finding its way to. The destination fixes scope, so it is settled first.
3. Map the frontier, breadth-first: fan out across the whole space rather than deep on one thread, surfacing the open decisions and the first items takeable now. If this surfaces no fog, stop - you do not need an epic (see WHEN EPIC, NOT RND).
4. Write the map: Destination and Notes filled, Decisions so far empty, the fog sketched into Not yet specified, and the items you can specify now listed under Frontier with their Blocked-by edges.
5. Stop. Charting is one session; do not also resolve items.

### Work the map

User invokes with a map (path). An item is optional - without one, you pick the next decision, not the user.

1. Load the map - the low-res view, not every linked artifact.
2. Choose the item: the one the user named, else the first Frontier item whose blockers are all closed.
3. Resolve it by its Type, invoking the skills Notes names. If in doubt, run an `/nxs:rnd` clarify pass.
4. Record the resolution: move the item from Frontier to Decisions so far as a one-line gist linking its artifact (brief / ADR / spike / findings note).
5. Graduate any fog the answer made specifiable into fresh Frontier items, clearing it from Not yet specified. If the answer reveals an item sits past the destination, rule it out of scope. If it invalidates other items, update or remove them.
6. Stop after one item.

## ARTIFACT

The map at `docs/epics/YYYYMMDD-<slug>.md`, updated each session. Durable writes spawned by items - a brief via `/nxs:rnd`, an ADR via the `decision-log` gate, a spike findings note - live in their own homes and are linked from the map, never restated in it.

## RULES

- Chart, don't build - decisions, not deliverables; no feature code, no build.
- One item per session; never resolve more than one.
- The map is an index - a decision lives in one place (its brief / ADR / spike), the map gists and links.
- Refer to items by title, never by a bare number.
- Fog stays fog until its question is sharp; scope beyond the destination is out of scope, not fog.

## DIFFERENTIATION

- `/nxs:epic` - foggy effort bigger than one session; charts a map of investigation items and resolves one per session, decisions not deliverables.
- `/nxs:rnd` - shape one session-sized task to a plan-ready brief (CLARIFY / EXPLORE / STRESS).
- `/nxs:plan` - decompose a shaped task into sequenced vertical-slice tasks.
- `/nxs:bug` - investigate a bug to a confirmed root cause.

## NEXT

The way is clear -> `/nxs:rnd` to shape a now-specifiable chunk into a brief, or `/nxs:plan` straight to decomposition if it is already plan-ready. A brief or plan then runs through `/nxs:exec`. For a bug surfaced on the map -> `/nxs:bug`.
