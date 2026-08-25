# Changelog

All notable changes to the `teach` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-08-25

### Added

- Source-led sessions for user-supplied book chapters, course lessons, and transcripts.
  The material is saved in `materials/` and enters the same recall, practice, observation,
  and remediation loop as a generated lesson.
- A stable `unit_id` contract. Generated lessons and supplied materials own the id; linked
  practice reuses it and records the id and theory path in every stored task.

### Changed

- Number allocation now distinguishes teaching-unit ids from `PLAN.md` node ids and checks
  the link before writing practice. Existing workspaces keep their paths and numbers.
- Checks and mastery checks are chat-only; learning records now require `Date`, `Units`, and
  `Evidence`, while untested claims and failed checks stay in `OBSERVATIONS.md`.
- Mastery checks use dated spacing at 7, 14, and 28 days, with 5 to 8 new tasks, no lookup,
  and at most one error. Two failures on an open node trigger theory again; a late failure on
  a done node starts ordinary practice without reopening it.
- Source-led materials carry `Node`, support `off-plan` state, inherit node metadata, and use
  `RESOURCES.md` or `materials/` as allowed sources. Sources now carry years and retire with a
  reason instead of being deleted.
- `PLAN.md` keeps done nodes as history and `NOTES.md` stores teaching preferences only.

## [Unreleased]

## [0.4.0] - 2026-08-23

Time now has a place to live, and getting there for a new workspace is one conversation.
Before this release a deadline or an hours-per-week figure was just prose in `MISSION.md`'s
Constraints, nothing existed to compare it against, every `Success looks like` line carried
the same weight, the mission interview and the first `PLAN.md` build were two separate
steps with the second one collecting a fresh round of the same kind of information, and a
lesson and the practice that followed it took two unrelated numbers from one shared counter
instead of one number both directories could be found under.

### Added

- Intake - for a new workspace, `SKILL.md` step 2 is now one conversation, one or two
  questions a turn: why; `Success looks like`, each line tagged `[core]` or left `extra` as it
  comes up; deadline and hours per week; how they like to learn and their usual session
  length, both into `NOTES.md`; what to leave alone; then the diagnostic. It ends by building
  `PLAN.md` and showing the course - the nodes, the hours, and what fits and gets cut when
  there is a deadline and a budget - for the user's OK. Before that OK, `MISSION.md` and
  `PLAN.md` are a draft: free to edit, no mission-revision protocol yet, and the OK itself
  writes nothing extra (see THE MISSION).
- `MISSION.md`'s Constraints - `Deadline: {date}` and `Budget: {N} hours per week`, plain
  values instead of prose, so `PLAN.md` can do arithmetic against them. Neither is required; no
  deadline or no budget just skips the fit-check below.
- `MISSION.md`'s `Success looks like` lines may carry `[core]`; untagged lines default to
  `extra`. Decided in the intake interview above; an older `MISSION.md` without tags gets asked
  once at the first `PLAN.md` build instead.
- `PLAN.md` nodes carry a rough hour estimate (`(~Xh)`) and are built from `core` lines first -
  an `extra` line earns a node only once every `core` line already has one.
- A fit-check at every `PLAN.md` build and rebuild, when a deadline and a budget exist:
  remaining calendar (weeks to the deadline times hours per week, shrinking on its own as the
  deadline nears - no counter needed) against the sum of hour estimates on nodes not yet
  `done`. Short on time: drop `extra` nodes first, then cut format depth on the remaining
  `core` nodes - the Bloom threshold check itself is never cut. `core` still doesn't fit after
  both cuts: stop and ask the user to demote a `core` line to `extra` or extend the budget,
  never a silent drop and never a lowered threshold. Grounded in the tension Carroll (1963)
  formalizes, not a prescription from Carroll or Bloom - see `PLAN-FORMAT.md` for the exact
  wording, chosen to avoid the same overreach fixed for the 85 per cent line in 0.2.1.
- Session-length filtering - every session, intake's first pick included, asks how long today
  is, offering the usual length from `NOTES.md` as a default. Candidates are filtered to what
  fits; a short window that still fits a check (material two or more sessions old, never
  retested) gets offered one; a window that fits nothing gets told so, not started.
- A migration path for an older `MISSION.md`: step 4 asks once which untagged lines are `core`
  and captures a deadline and budget if there is one, folds an inline status note like
  "(closed)" into a `done` node, and offers to trim a `Why` that has grown into course history
  - all through the mission-revision protocol, since this mission is already established. It
  then builds and shows the plan the way intake does.

### Changed

- `SKILL.md` step 3 (`RESOURCES.md`) now runs after the intake's plan is approved and before
  the chosen step runs, not before or during the interview - an hour estimate does not need
  sources, only teaching the step itself does.
- `PLAN.md`'s node-change rule gains a third trigger, mission revision, alongside observation
  and learning record. A mission revision that adds, drops, or re-tags a `Success looks like`
  line updates `PLAN.md`'s nodes in the same turn, without asking a second time.
- **Contract change - numbering.** A lesson claims the next number, the highest one already
  used across `lessons/` and `practice/` plus one. Practice tied to a lesson inherits its
  number instead of claiming a new one; practice with no lesson of its own (a check, a
  transfer task, a drill on old material - the most recent lesson among several it draws on)
  claims a number the same way a lesson does. `practice/NNNN-<slug>/` is now one directory per
  topic rather than per step - several rounds of practice on the same topic land in the same
  directory over time, told apart by the format named in each task, not by the filename. No
  workspace is renumbered retroactively; the rule already accounts for a workspace where the
  old shared counter left a practice number higher than any lesson number, since it always
  looks at the highest number in either directory, not just at lessons.

## [0.3.0] - 2026-08-23

A short backbone now survives between sessions. Before this release THE NEXT STEP rebuilt
direction from nothing every time, which kept the promise of never locking in a rigid
programme but also meant nothing about where the course was heading carried over from one
session to the next.

### Added

- `PLAN.md` in the workspace - 3 to 5 nodes, each a skill tied to one line of `MISSION.md`'s
  "Success looks like," with no activities, dates, or reasons attached.
  `skills/me/PLAN-FORMAT.md` is the template and the rules for it. Listed in `README.md`'s
  workspace table and Layout section alongside the other format files.
- `OBSERVATIONS.md` entries may now point at a `PLAN.md` node by its number - a number is
  assigned once and never reused, so the pointer never goes stale.

### Changed

- `SKILL.md`, PROCEDURE - step 1 reads `PLAN.md` alongside `MISSION.md`. Step 4 builds the
  plan's first nodes the first time a step is chosen, if it does not exist yet, and picks
  candidates from its open nodes. Step 5 will not write a task to disk unless its title names
  the practice format it came from, out of the catalogue in `PRACTICE-FORMAT.md`, and will not
  write a lesson block that repeats a previous lesson word for word until that block is a
  shared component in `assets/` - the check ASSETS and PRACTICE already asked for, now made
  explicit before anything is written. Step 7 is now three questions, one per file it updates
  - a new source for `RESOURCES.md`, a new term the user is using for `GLOSSARY.md`, a
  rereadable piece of the lesson for `reference/`, distilled in the same session rather than
  left for later - plus the covered-ground line in `NOTES.md` as before. Step 8 closes the plan
  node a step was advancing when the learning record clears the Bloom threshold.
- `LEARNING-RECORD-FORMAT.md` - a record now has a length to aim for, up to about 80 words; a
  third sentence is a prompt to check whether it is two facts rather than one. Evidence is now
  one line pointing at what closed the record (`practice/NNNN-<slug>` or the lesson), not a
  paragraph, and it is required rather than optional when the record also closes a `PLAN.md`
  node - the node's `done` status carries the record's number, so the record needs the pointer
  back.
- `SKILL.md`, THE NEXT STEP - "no programme written in advance" now names what that bans: a
  detailed programme and lessons or tasks prepared before their turn. It no longer bans a short
  backbone. A plan node changes only when an observation or a learning record contradicts it,
  and rebuilding it is a visible move with a one-line reason to the user, never a silent
  overwrite. Running out of open nodes with the mission unmet calls for a replan; running out
  with it met is a mission conversation instead.

## [0.2.1] - 2026-08-23

Pedagogy claims that carried no citation, or carried the wrong one, now cite the specific
research behind them and note where that research stops applying.

### Changed

- `SKILL.md`, THE NEXT STEP - the 85 per cent success line is now attributed (Wilson et al.
  2019) and separated from a new rule: closing an `OBSERVATIONS.md` line with a learning
  record needs roughly 80 to 90 per cent on an independent check (Bloom 1968), not a clean run
  inside the same practice format that taught the skill. That check is named as format 10,
  MASTERY CHECK, and the format's entry in `PRACTICE-FORMAT.md` now points back to this rule.
- `SKILL.md`, LESSONS - "Short" now cites the segmenting principle it rests on (Mayer and
  Pilegard 2014) with its actual scope: complex material, novice learner. "Themed to the
  system" no longer claims both themes are equivalent; it names the two different things they
  are each good for, reading comprehension against eye comfort, without a source neither claim
  currently has.
- `PRACTICE-FORMAT.md`, format 2 (WORKED EXAMPLE) - notes that Barbieri et al. 2023 is a
  mathematics-only meta-analysis, not general evidence.
- `PRACTICE-FORMAT.md`, format 9 (INVENTION BEFORE INSTRUCTION) - notes the effect reverses
  for younger learners and domain-general skills.
- `PRACTICE-FORMAT.md`, "Explain your own solution" add-on - no longer a default on top of a
  worked example; the same Barbieri et al. 2023 result shows self-explanation paired with a
  worked example can get in the way.

## [0.2.0] - 2026-08-20

The programme now moves with the learner. Before this release the course was picked from whatever the last session discussed, and practice defaulted to a blank-sheet task because no other format was described. Both are addressed by the same mechanism: the skill keeps a running list of what the learner has not settled, and chooses the next step against it.

### Added

- `OBSERVATIONS.md` in the workspace - where the learner stalled, what they had to look up, a question they asked twice, a wrong answer on a check, prior knowledge claimed and untested. One dated line each, written while it happens, deleted when closed. Learning records hold the settled half of the picture and this file holds the unsettled half.
- A step is now theory, practice, or a check, and the skill puts up to four candidates to the learner before running one. Each candidate names the observation it closes and roughly how long it takes.
- `skills/me/PRACTICE-FORMAT.md` - ten practice formats with the evidence behind each, plus two add-ons and the rules for choosing between them. Recall probe, worked example, completion, error hunt, predict-run-explain, transfer, whole task with fading support, part-task drill, invention before instruction, mastery check.
- Understanding and fluency are separated. Some formats build understanding through a task the learner has not met; others repeat a primitive to a threshold. The signal that calls for the second is the learner following an explanation and still being unable to produce the thing without looking it up.
- A calibration figure for difficulty: about 85 per cent success, so roughly one attempt in six fails. Everything green first time means the step was too small.
- `practice/NNNN-<slug>/` - one directory for everything the learner produces, numbered from the same sequence as the lessons.
- A CONDUCT section: a stuck learner is shown the mechanism before the answer, the directory the learner works in is never written to, and nothing is prepared in advance.
- Checks are steps rather than a tail on a practice, run as questions in chat with no files. Where the work can be inspected it is inspected; where it cannot, three questions stand in, and what the learner had to look up is the fluency probe.

### Changed

- No roadmap is written in advance. The next step is worked out each session from the mission, the observations, and the learning records.
- Practice is issued only against an open observation or theory just taught, and the tie is written into the task. Pointing at a neighbouring lesson does not count as having taught the theory.
- Interleaving is now qualified rather than stated flatly: it helps in some subjects and hurts in others, so it is a setting chosen per topic.
- `NOTES.md` is held to two jobs, how to teach this learner and what has been covered, with the rest of what accumulated there moved to `OBSERVATIONS.md` or into the skill itself.

## [0.1.0] - 2026-08-08

First release. `/teach:me` treats the current directory as a course that survives between sessions: a mission that says why the topic matters, curated sources the lessons cite, numbered HTML lessons, reference sheets distilled out of them, and learning records that fix what the user has actually demonstrated. The next lesson is chosen from those records rather than from whatever was last discussed.

The pedagogy is the part worth stating. Knowledge is taken from sources rather than recall; skills are built through immediate feedback loops; judgement is delegated to communities, because a model cannot supply it. Lessons are designed against fluency mistaken for mastery - recall over recognition, spacing across sessions, interleaving once several skills exist to mix.

### Added

- `skills/me/SKILL.md` - the command. Reads the workspace, interviews for a mission when there is none, fills the sources before teaching from them, picks the next lesson just past the current floor, and writes a learning record only against demonstrated understanding.
- `skills/me/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `GLOSSARY-FORMAT.md`, `LEARNING-RECORD-FORMAT.md` - the templates for the four workspace documents, each with the rules that keep it useful. All four are linked from `SKILL.md` and read on demand.
- The mission interview also probes the topic with two or three real questions instead of taking a self-report, and lands the answer as the first learning record. Without it the opening lessons aim at a floor nobody measured.
- Each lesson is built around one skill, carries only the knowledge that skill needs, and teaches it before handing over the practice.
- Lessons teach the current state of a topic. Anything superseded is labelled, with its replacement named, because a source can be high-trust and stale at the same time.
- Lessons follow `prefers-color-scheme`, with both themes carrying real contrast from the shared stylesheet.
- Quiz rules: shuffle the correct answer's position, keep every option the same length, and make each wrong option a mistake people actually make. The distractor a user picks names the misconception to attack next.
- Preferences the user states in passing go to `NOTES.md` when they are said, so they survive the session.
- Learning records are read in full only while there are fewer than eight. Past that it is the three most recent plus a covered-ground list kept in `NOTES.md`, so a long course does not reread its whole history every session.
