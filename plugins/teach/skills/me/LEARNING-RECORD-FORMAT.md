# LEARNING RECORDS

Learning records live in `learning-records/`, numbered `0001-<slug>.md` upward. They are the decision record of this course: what the user actually knows, and why that changes what comes next. Reading them, alongside `OBSERVATIONS.md`, is how the next step gets picked.

Create the directory when the first record is written, not before.

These records are the settled half of what is known about the user. The unsettled half lives in `OBSERVATIONS.md`: gaps, stumbles, and claims not yet tested. A record is what an observation turns into once it closes, and the observation is deleted in the same move.

## TEMPLATE

```md
# {What was learned or established}

{One to three sentences: what the user can now do, and what it changes about future
sessions.}
```

That is the whole format. One paragraph is a complete record. The value is the fact that this is now known, not the filling of sections.

## OPTIONAL LINES

Add these only when they carry weight, which is rarely:

- `Status: superseded by LR-NNNN` in frontmatter, once an earlier understanding turns out to be wrong.
- **Evidence** - how the user showed it: a question answered cold, an exercise completed, experience they cited. Worth having when the claim may be revisited.
- **Implications** - what this opens up or rules out, when that is not obvious.

## WHEN TO WRITE ONE

- **The user demonstrated something non-trivial.** Not exposure - evidence they can use the idea correctly. This raises the floor.
- **The user disclosed prior knowledge.** "I already do X." Record it, and record how deep they claim it goes, so nothing gets re-taught.
- **A misconception was corrected.** The highest-value kind: it predicts where they will stumble on neighbouring topics.
- **The mission shifted because of something learned.** Update `MISSION.md` in the same turn and cross-link it.

## WHEN NOT TO

- Material that was merely covered. Coverage is not learning; wait for evidence.
- A term already defined in `GLOSSARY.md`. That is the glossary's job.
- Session logs. These are not a journal.
- Anything still open. A gap, a stumble, or a claim you have not tested belongs in `OBSERVATIONS.md` until there is evidence to close it.

## NUMBERING AND SUPERSESSION

Take the highest number in `learning-records/` and add one.

When a later record contradicts an earlier one, mark the old one superseded rather than deleting it. How the understanding moved is itself worth knowing.
