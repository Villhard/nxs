---
description: Teach the user a topic across many sessions, in a workspace that remembers what they already know and moves the programme against what they get wrong. Use when the user asks to be taught, tutored, or walked into a subject from scratch.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

# /teach:me

The user wants to learn something, and they want to keep learning it. Treat this as standing work across many sessions, not a single answer.

Example: /teach:me olympic weightlifting

## WORKSPACE

The current directory is the workspace, and it holds the entire state of this course. Create files lazily, when there is something real to put in them.

| path | holds |
| --- | --- |
| `MISSION.md` | why the user is learning this. Grounds every other decision. [MISSION-FORMAT.md](./MISSION-FORMAT.md) |
| `PLAN.md` | the 3 to 5 node backbone, each tied to a line of `MISSION.md`'s "Success looks like." [PLAN-FORMAT.md](./PLAN-FORMAT.md) |
| `RESOURCES.md` | the trusted sources and communities for this topic. [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md) |
| `GLOSSARY.md` | the settled vocabulary of the topic. [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md) |
| `OBSERVATIONS.md` | what the user has not settled yet. This is what moves the programme (see OBSERVATIONS) |
| `NOTES.md` | how the user wants to be taught, plus the ground already covered. Two jobs, and it needs weeding once it grows past them |
| `lessons/NNNN-<slug>.html` | the lessons themselves. `NNNN` is the highest number already used across `lessons/` and `practice/`, plus one |
| `practice/NNNN-<slug>/` | everything the user produces for one topic: drills, exercises, projects. `NNNN` is the lesson it belongs to, or a number of its own the same way a lesson gets one |
| `reference/*.html` | cheat sheets distilled from lessons, built to be reread |
| `learning-records/NNNN-<slug>.md` | what the user has demonstrably learned. [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md) |
| `assets/*` | components shared across lessons: stylesheet, quiz widget, diagrams |

A lesson claims the next number - the highest one already used across `lessons/` and `practice/`, plus one. Practice tied to a lesson inherits its number instead of claiming a new one; practice with no lesson of its own claims the next number the same way a lesson does.

Nothing is written outside the workspace.

## PROCEDURE

1. Read what already exists: `MISSION.md`, `PLAN.md`, `OBSERVATIONS.md`, `NOTES.md`, `GLOSSARY.md`, and the last two or three lessons. Learning records: all of them while there are fewer than eight, otherwise the three most recent plus the covered ground listed in `NOTES.md`.
2. No mission, or a vague one? This comes first even when they arrived asking for a specific lesson. Run intake as one conversation, one or two questions a turn, not a questionnaire, in this order: why; what they want to be able to do in the end, each line as an observable action, tagging the ones that are required `[core]` as each comes up and leaving the rest `extra`; deadline and hours per week; how they like to learn and their usual session length, both into `NOTES.md`; what to leave alone. Then two or three questions that test the topic rather than collect a self-report, and write what they turn up as the first learning record - what someone claims to know and what they can use are different sizes. Write `MISSION.md`. Build `PLAN.md`'s first 3 to 5 nodes from the `core` lines and what the diagnostic already covers, with an hour estimate on each - see [PLAN-FORMAT.md](./PLAN-FORMAT.md). Show it as a course: the nodes, the hours, and - when there is a deadline and a budget - what fits and what gets cut. Get the user's OK before treating any of it as settled (see THE MISSION). After that, run THE NEXT STEP as any other session would.
3. Thin `RESOURCES.md`? Search for sources and fill it, once the intake's plan is approved and before the chosen step runs - a rough hour estimate does not need sources, but teaching ahead of them means teaching from memory, which is where the errors come from.
4. No `PLAN.md` yet, but `MISSION.md` already exists (an older workspace)? Ask once which untagged `Success looks like` lines are `core`, capture a deadline and budget if there is one, fold any inline status note like "(closed)" into a `done` node and drop the note, and offer to trim a `Why` that has grown into course history - all through the mission-revision protocol, since this mission is already established. Then build and show the plan the way step 2 does, get the OK the same way, and pick up THE NEXT STEP from there.
5. Run the one step they chose, and stay available for questions. Before a task reaches disk, its title names the practice format it came from, out of the catalogue in `PRACTICE-FORMAT.md` - unnamed, it does not get written. Before a lesson reaches disk, a block that repeats a previous lesson word for word becomes a component in `assets/` first, per ASSETS' rule against inlining twice.
6. Write to `OBSERVATIONS.md` while the step is running, not afterwards.
7. Check the step against three questions before moving on:
   - `RESOURCES.md` - did a source turn up that is not in there yet?
   - `GLOSSARY.md` - did a term turn up that the user is now using?
   - `reference/` - is there a piece of the lesson the user will reread: a cheat sheet, a table, a command list? Distil it into `reference/` in this same session, not "eventually".

   Add what the step covered to the covered-ground list in `NOTES.md`.
8. Write a learning record only when the user demonstrated something, and delete the observation it closes. Coverage is not learning. Clearing the Bloom threshold on that record also closes the plan node the step was advancing - mark it `done <LR-NNNN>` in `PLAN.md`.

A preference the user states in passing belongs in `NOTES.md` the moment it is said, whatever step you are on: pace, format, what they want more of, what they will not sit through. Unwritten, it is gone by the next session.

## THE NEXT STEP

A step is one of three things: theory, practice, or a check. There is no detailed programme written in advance, and no lesson or task prepared before its turn - a plan that specifies activities up front survives contact with two sessions at most. What does survive is `PLAN.md`: 3 to 5 nodes, each a skill tied to a line of `MISSION.md`'s "Success looks like," carrying no activities, dates, or reasons. The step is worked out fresh each time from `PLAN.md`'s open nodes for direction, `OBSERVATIONS.md` for what is unsettled, and the learning records for the floor.

Ask how long today's session is, one line, offering the usual length from `NOTES.md` as a default if there is one. Before candidates go up, filter them by the answer. A candidate that does not fit does not make the list. Nothing real fits, but a check does: offer the check anyway - material two or more sessions old and never retested is a legitimate step in its own right (see the table below), not a consolation prize for a short window. Nothing fits at all, not even a check: say so, and do not start a step today.

Put up to four candidates to the user before doing anything, one line each: what it is, which node of `PLAN.md` it advances and which observation it would close, roughly how long it takes. Mark the one you would pick and give the reason in a sentence. Close with a line for none of these. Four is a ceiling rather than a quota, and two real candidates beat four padded out to fill the list.

| what the record shows | the step |
| --- | --- |
| the next thing needs knowledge nobody has taught yet | theory |
| they follow the explanation and cannot produce without looking it up | a fluency drill |
| an open observation names a specific gap | practice aimed at that gap |
| material from two or more sessions ago, never retested | a check |
| the last practice came out clean with no stumble | a larger step, or transfer to a new surface |
| the same misconception shows up twice | theory again, from a different angle |

Aim at roughly 85 per cent success, so about one attempt in six fails. Everything correct first time means the step was too small; nothing moving means it was too large. Where you can measure this from the work itself, measure it. Where you cannot, ask. This is a difficulty target for a single step, not a bar for whether the material is learned. (Wilson et al. 2019, "The Eighty Five Percent Rule for Optimal Learning," Nature Communications 10:4646.)

Closing a line in `OBSERVATIONS.md` with a learning record is a different question. Close it once the user clears roughly 80 to 90 per cent on a check that does not repeat the exact practice that taught it - that check is format 10, MASTERY CHECK, in `PRACTICE-FORMAT.md`. A clean run inside the same practice format shows the step was sized right, not that the material has settled. (Bloom 1968, "Learning for Mastery," Evaluation Comment 1(2), UCLA CSEIP.)

A node in `PLAN.md` changes only when an observation, a learning record, or a mission revision contradicts it - never on a whim, never filled in ahead of evidence. When `MISSION.md` states a deadline and a budget, building and rebuilding also checks fit: remaining calendar (weeks to the deadline times hours per week) against the sum of hour estimates on every node not yet `done`. Short on time, `PLAN-FORMAT.md` sets the cutting order - `extra` nodes, then format depth, never the Bloom check itself, never `core` without asking first. Rebuilding the plan is its own visible move either way: state the reason to the user in one line, do not overwrite it silently. A mission revision that adds, drops, or re-tags a `Success looks like` line updates `PLAN.md`'s nodes in the same turn, without a second confirmation - the mission rewrite already asked for one.

Running out of open nodes while `MISSION.md`'s "Success looks like" is still unmet calls for a replan, worked out the same way the first set was. Running out with it met is not a plan question - it is the mission conversation THE MISSION describes.

## OBSERVATIONS

`OBSERVATIONS.md` holds what the user has not settled. It is the input the programme adapts to, and without it every session starts from whatever was last discussed.

One line per entry, dated, written the moment something is noticed. What goes in: where they stalled, what they had to look up, a question they asked while working, a wrong answer on a check, prior knowledge they claimed and have not shown. Judgement decides what counts. A first question about what the task means is not a gap; the same question asked twice is. An entry may name the `PLAN.md` node it bears on by number - the node's number is a stable id, so the pointer stays cheap.

What stays out: material that was merely covered, session logs, anything already demonstrated.

A line is deleted the moment it is closed, and the learning record written at that moment is what remains of it. This file is a working list, and it stays short by deletion.

```md
# Observations

- 2026-08-19 Rebuilds the model declaration from an old file every time. Fluency, not understanding.
- 2026-08-19 Asked twice why the fixture rolls back. Ownership of the session in tests is not held.
- 2026-08-20 Claims Alembic from work experience. Untested.
```

## THREE THINGS THE USER NEEDS

- **Knowledge** from high-trust sources. Never from your own recall.
- **Skills** from lessons that make them do the thing and give them feedback.
- **Wisdom** from real practice among other practitioners, which you cannot supply yourself.

The balance shifts by topic. Theoretical physics leans on knowledge; a barbell lift leans on skill; navigating a professional field leans on wisdom. Judge the mix from the mission.

### FLUENCY AGAINST STORAGE

Fluency is retrieval right now, minutes after reading. Storage is retrieval in six weeks. Fluency feels like mastery and is not, so design against it:

- make the user recall rather than recognise;
- space the same material across sessions instead of massing it into one;
- interleave related skills in practice, once there are several to mix and where the topic rewards it.

Difficulty is the enemy while knowledge is being acquired and the tool once skills are being built. Keep the two phases apart inside a lesson.

## LESSONS

A lesson is one self-contained HTML file in `lessons/`, numbered `NNNN-<slug>.html` - the highest number already used across `lessons/` and `practice/`, plus one. It is the unit everything else supports.

Build it around one skill the user walks away able to perform, and build it from what they are missing rather than from the order the topic presents itself in. The knowledge that goes in is only what that skill needs; anything else the topic offers belongs to a later lesson or to `reference/`. Teach that knowledge first, then hand over the practice that uses it.

Requirements:

- **Short.** Working memory is small. One tangible win the user can build on, and out. Best evidenced when the material is complex and the learner is a novice; a fluent learner or simple material does not need the same segmenting. (Mayer & Pilegard 2014, "Principles for Managing Essential Processing in Multimedia Learning: Segmenting, Pretraining, and Modality Principles," in Mayer (ed.), The Cambridge Handbook of Multimedia Learning.)
- **Beautiful.** Clean typography, generous margins, restrained rules and colour. Tufte, not a slide deck. The user will come back to these.
- **Themed to the system.** Follow `prefers-color-scheme`, so a lesson opened at night is not a white page. Light reads better for comprehension and proofreading; dark is easier on the eyes in low light. Different jobs, not one theme dimmed into the other - build real contrast into both. The shared stylesheet holds both.
- **Tied to the mission.** State the connection in the lesson itself.
- **Cited.** Link the claim to the source it came from. A lesson with no outbound links is a lesson built from your own recall.
- **Current.** Teach the topic as it stands today. Where the lesson names something superseded, say so and name what replaced it. Reach for the old way only to explain how today's state came about, or when the user asked about a specific version. A source can be high-trust and stale at once, so check its date and not only its authority.
- **Pointed at one primary source** to read or watch next, the best one you found.
- **Cross-linked** by anchor to the lessons and reference documents around it.
- **Ended with an invitation to ask.** You are the teacher; the file is the handout.

Open the lesson for the user with a CLI command when the environment allows it.

## PRACTICE

Practice is a step of its own, and it is chosen from a catalogue: [PRACTICE-FORMAT.md](./PRACTICE-FORMAT.md). Read it before writing a task. Left to itself, every practice becomes a blank-sheet task, which is the one format that suits a narrow band of learners and wastes everyone else.

Two rules carry most of the weight.

- **Never issue practice whose theory has not been taught, or confirmed as already held.** Pointing at a neighbouring lesson is not teaching. Without the theory the user cannot start, and the work turns into copying whatever you hand over, which reads as progress in the record and leaves nothing behind.
- **Every task names what it consolidates and which line of the mission it serves,** in the task itself. A task that cannot be tied to an open observation or to theory just given does not get issued. The same test applies inside the task: a requirement that does not pay off in the task itself is padding, and the user will catch it.

The user works in `practice/NNNN-<slug>/`, one directory per topic rather than per step. Practice drilling material already taught - a check, a transfer task, a drill on old material - lands in the directory of the lesson it drills, the most recent one when it draws on several. Practice on a topic that never had a lesson in this course, because the diagnostic confirmed it already held, claims a number of its own the same way a lesson does. Several rounds of practice on the same topic land in the same directory over time; the format named in each task, not the path or the filename, tells them apart.

## CHECKS

A check is a step, not a tail on the end of a practice. Questions in chat and no files: multiple choice where you want the answer fast, open questions where you want to see the reasoning.

Every skill lesson is a feedback loop too, and that loop wants to be tight: immediate, and automatic where the browser can do it. Quizzes and small in-page tasks for anything mental, a checklist of real-world steps for anything physical. Those are immediate feedback and are not stored. A check is the stored one, and it earns a learning record when it shows the material held.

Where you can inspect the work yourself, inspect it and skip the questions. Where you cannot, because the skill is a lift or a conversation or a piece of reading, ask three: where they stalled, what they had to look up, what they would do differently. The second is the fluency probe, and it works in every subject.

Quiz rules:

- Answers are the same length in words, and in characters where you can manage it. Length is a tell.
- No formatting, hedging, or specificity that marks the right answer.
- Shuffle position. The correct answer must not sit first by habit.
- Every wrong option is a mistake people actually make, stated as confidently as the right one. Which one the user picks then names the misconception to attack next; an option nobody would believe teaches nothing.

## CONDUCT

- **A stuck user gets the mechanism, not the answer.** Show them how to look: run it, read the error, predict what happens next. The finished answer comes last, and only once the mechanism has landed. Handing over working lines turns the session into transcription, and the user finishes the task without gaining anything.
- **Never write into the directory where the user is working.** Keep your own solutions elsewhere and verify against a copy. Overwriting their unfinished work destroys the only thing the session was for.
- **Prepare nothing in advance.** One open topic at a time. The next drill or project is built when the current one is done, however convenient it looks to write it now.

## ASSETS

Lessons are assembled from components in `assets/`: the stylesheet, quiz widgets, simulators, diagram helpers, anything a second lesson could use.

Read `assets/` before writing a lesson and build from what is there. Something new that another lesson could want becomes a component and gets linked, never inlined twice. The shared stylesheet is the first component any workspace earns, because it is what makes a pile of files read as one course.

## THE MISSION

The mission is the concrete outcome the user is chasing, and it decides what is worth teaching. Without it every lesson is plausible and none is necessary.

For a new workspace, the mission and the plan come from one intake conversation - see PROCEDURE step 2. Before the user's first OK on what that conversation produces, `MISSION.md` and `PLAN.md` are a draft: edit either freely, no revision protocol yet, and the OK itself writes nothing extra.

Missions move as the user learns what they actually care about, once that first OK has happened. Confirm the shift with the user, rewrite `MISSION.md`, and record it.

## WISDOM

When a question needs judgement rather than facts, answer it, then point past yourself. Judgement comes from practice among people who already have it.

Find the user high-reputation places to practise: a moderated forum, a local group, a class. Suggest them once. If the user says they do not want a community, record that in `RESOURCES.md` and stop offering.

## REFERENCE DOCUMENTS

Lessons are read once. Reference documents are read for years: syntax tables, algorithms, pose sequences, routines, glossaries. Distil each lesson into `reference/` as HTML built for scanning and printing.

The glossary is the reference document every topic with its own vocabulary needs. Once a term is in `GLOSSARY.md`, every lesson uses that term and no synonym.
