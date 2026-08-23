# MISSION.md

The mission is the concrete outcome the user wants. It sits at the workspace root and every teaching decision traces back to it: what to teach next, which sources to chase, which exercise to build.

## TEMPLATE

```md
# Mission: {topic}

## Why
{One to three sentences. The real-world thing the user is chasing, and what changes for
them once they can do it. "To understand X" is not an outcome - keep asking until you
reach the thing underneath it.}

## Success looks like
- {Something specific the user will be able to do, observable enough to test}
- {Another one}

## Constraints
- Deadline: {date}, when there is one
- Budget: {N} hours per week, when there is one
- {Other constraints: equipment, how they prefer to learn}

## Out of scope
- {Adjacent topics deliberately left alone, so lessons stop drifting toward them}
```

## RULES

- **One mission per workspace.** Two unrelated topics are two directories.
- **Concrete beats abstract.** "Half marathon in October" over "get fitter". "Ship a Rust CLI my team uses" over "learn Rust".
- **Interview before writing.** If the user cannot say why, ask until they can. A wrong mission steers every future session wrong, and a missing one at least stays honest.
- **Rewrite when the goal moves.** Confirm the change with the user, update this file, and write a learning record for it.
- **Keep it under a screen.** Past that it has stopped being a compass and turned into a plan.
- **Deadline and budget get their own bullets, when they exist.** Plain values, not prose - `Deadline: {date}` and `Budget: {N} hours per week` - so `PLAN.md` can do arithmetic against them. Neither applies to this course? Nothing about time gets enforced; the plan still gets built, just without a fit-check.
- **`Success looks like` lines may carry `[core]`.** Untagged lines default to `extra`. This is decided in the intake interview as each line comes up - see `SKILL.md` PROCEDURE step 2. An older `MISSION.md` without tags gets asked once, at the first `PLAN.md` build (step 4). After intake, a tag changes only through the rewrite-when-the-goal-moves rule above, with the user's confirmation.
