# LEARNING RECORDS

Learning records live in `learning-records/`, numbered `0001-<slug>.md` upward. They are the decision record of this course: what the user actually knows, and why that changes what comes next. Reading them, alongside `OBSERVATIONS.md`, is how the next step gets picked.

Create the directory when the first record is written, not before.

These records are the settled half of what is known about the user. The unsettled half lives in `OBSERVATIONS.md`: gaps, stumbles, and claims not yet tested. Closing an observation deletes its line, but creates no record by itself. A record is written only for a corrected misconception, a closed plan node, or a mission revision.

## TEMPLATE

```md
---
Date: 2026-08-25
Units: [0042]
Evidence: chat mastery check for PLAN.md node 2
---

# {What was learned or established}

{One to three sentences: what the user can now do, and what it changes about future
sessions.}
```

`Date`, `Units`, and `Evidence` are required frontmatter on every record. `Date` is the date of the evidence or mission revision; for a node or misconception it is the date of the successful check. `Units` is a list of one or more theory unit ids, or `[]` when the record concerns no theory unit. `Evidence` is one line naming the check, practice, lesson, corrected misconception, or mission revision that closed the record; it may point to chat when no file exists. There is no required practice path. A failed check is recorded in `OBSERVATIONS.md`, not here.

The paragraph is one to three sentences, up to about 80 words. The value is the fact that this is now known, not the filling of sections.

## OPTIONAL LINES

Add these only when they carry weight, which is rarely:

- `Status: superseded by LR-NNNN` in frontmatter, once an earlier understanding turns out to be wrong.
- **Implications** - what this opens up or rules out, when that is not obvious.

## WHEN TO WRITE ONE

- **A plan node closed.** The mastery check supplies the evidence and its record id goes into `PLAN.md`.
- **A misconception was corrected.** The independent attempt supplies the evidence and closes that observation.
- **The mission shifted because of something learned.** Update `MISSION.md` in the same turn and cross-link it.

## WHEN NOT TO

- Material that was merely covered. Coverage is not learning; wait for evidence.
- A term already defined in `GLOSSARY.md`. That is the glossary's job.
- Session logs. These are not a journal.
- A disclosed prior-knowledge claim. Until an independent attempt verifies it, keep it in `OBSERVATIONS.md`.
- Anything still open. A gap or a stumble belongs in `OBSERVATIONS.md` until there is evidence to close it.

## NUMBERING AND SUPERSESSION

Take the highest number in `learning-records/` and add one.

When a later record contradicts an earlier one, mark the old one superseded rather than deleting it. How the understanding moved is itself worth knowing.
