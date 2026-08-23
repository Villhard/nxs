# Changelog

All notable changes to the `teach` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
