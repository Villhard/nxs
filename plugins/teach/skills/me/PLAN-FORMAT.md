# PLAN.md

The backbone that survives between sessions: 3 to 5 open nodes, each tied to one line of
`MISSION.md`'s "Success looks like." This is what THE NEXT STEP in `SKILL.md` picks candidates
from, instead of rebuilding direction from nothing each session.

## TEMPLATE

```md
# Plan

1. {skill as an action} -> {Success looks like item} [open] (~2h)
2. {skill as an action} -> {Success looks like item} [in progress] (~1h)
3. {skill as an action} -> {Success looks like item} [done LR-0004]
```

## RULES

- **One line per node**, numbered, 3 to 5 open nodes at a time. A queue, not a syllabus. Keep
  done nodes as stable history.
- **No dates or reasons.** Those already live in `learning-records/` and observations. A node is
  a pointer, with its done record id as the only retained history.
- **Names a skill as an action** the user will be able to perform, never a topic.
- **Points at one line of `MISSION.md`'s "Success looks like."** A node with nothing to point
  to does not belong here.
- **Core lines get nodes first.** An `extra` line earns a node only once every `core` line
  already has one.
- **Status is one of three:** `open`, `in progress`, `done <LR-NNNN>`. `done` carries the
  learning-record id that closed it, nothing more.
- **A node carries a rough hour estimate**, not a date - `(~Xh)` at the end of the line. A
  `done` node does not need one any more.
- **A node closes only at its mastery check.** The check happens in chat, creates no practice
  file, and does not allocate a `unit_id`. See `SKILL.md`'s THE NEXT STEP and format 10 MASTERY
  CHECK in [PRACTICE-FORMAT.md](./PRACTICE-FORMAT.md).
- **A failed late mastery check does not reopen a `done` node.** Its observation starts ordinary
  practice against the gap.
- **A node changes only when an observation, a learning record, or a mission revision
  contradicts it.** Never rewritten on a whim, never filled in ahead of evidence. A budget
  shortfall found while checking fit (below) counts as this too.
- **Building and rebuilding checks fit, when `MISSION.md` states a deadline and a budget.**
  Remaining calendar is weeks to the deadline times hours per week - it shrinks on its own as
  the deadline nears, no separate counter needed. Remaining work is the sum of the hour
  estimates on every node not yet `done`. Short on time: drop `extra` nodes first, then cut the
  format of the remaining `core` nodes to something cheaper (see `PRACTICE-FORMAT.md`) -
  whichever format survives, the node still closes only through the mastery check above;
  cutting depth cuts the path there, never the check itself. `core` still does not fit
  after both cuts: stop and ask the user to demote a specific `core` line to `extra` or extend
  the budget. Never drop `core` silently, and never lower the mastery threshold to make it fit - that
  is a mission revision with its own learning record, not a quiet `done`. No deadline or no
  budget in `MISSION.md`? Skip this check; nothing about time gets enforced. (Carroll 1963, "A
  Model of School Learning," Teachers College Record 64, formalizes degree of learning as time
  spent over time needed; Bloom's mastery learning normally takes the other side of that
  tension, holding the target fixed and letting time float. Holding the mastery threshold and
  cutting scope instead, under a hard deadline, is this plugin's choice built on that tension -
  not a prescription from either source.)
- **Numbers are stable ids.** `OBSERVATIONS.md` may point at a node by number. A number is
  assigned once and never reused - nodes are never renumbered. Keep closed (`done`) nodes in
  `PLAN.md` as stable history; the next new node takes the next free number.
- **Rebuilding the plan is its own visible move**, stated to the user in one line, never a
  silent overwrite.
- **Out of nodes, mission not met:** replan the same way the first set was built. **Out of
  nodes, mission met:** that is a mission conversation, not a plan update - see THE MISSION in
  `SKILL.md`.
