# teach

A tutor that remembers. `/teach:me` turns the current directory into a teaching workspace and keeps the state of a course there: why you are learning the topic, which sources are trustworthy, the lessons you have been through, and what you have actually demonstrated. Next session picks up from that record rather than from an empty prompt.

## Quickstart

```
mkdir ~/learning/weightlifting && cd ~/learning/weightlifting
claude
/teach:me olympic weightlifting
```

The first session interviews you about why you want this and writes the mission. Every session after that reads the workspace, offers you up to four candidates for the next step, and runs the one you pick. A step is theory, practice, or a check on something taught a while ago.

## What appears in the workspace

| path | holds |
| --- | --- |
| `MISSION.md` | the concrete outcome you are chasing. Everything else is judged against it |
| `PLAN.md` | 3 to 5 open nodes tied to what success looks like; done nodes remain as stable history |
| `RESOURCES.md` | trusted sources, plus the communities where judgement comes from |
| `GLOSSARY.md` | the settled vocabulary, used the same way in every lesson |
| `OBSERVATIONS.md` | what you have not settled yet: where you stalled, what you looked up, what you got wrong |
| `NOTES.md` | how you want to be taught |
| `materials/` | book chapters, course lessons, and transcripts supplied as theory |
| `lessons/` | the lessons, numbered, one HTML file each |
| `practice/` | everything you produce: drills, exercises, projects |
| `reference/` | cheat sheets distilled from lessons, built to be reread |
| `learning-records/` | what you have demonstrably learned, and what it unlocks |
| `assets/` | the shared stylesheet and reusable lesson components |

One mission per workspace. Two unrelated topics are two directories.

## How it teaches

Knowledge comes from entries in `RESOURCES.md` or supplied files in `materials/`, and lessons cite one or carry `Unsourced: agreed YYYY-MM-DD` metadata. Skills come from short interactive lessons built around an immediate feedback loop. Judgement comes from practising among people who already have it, so the skill points you at communities instead of pretending to be one.

You can also bring your own theory. `/teach:me` stores a supplied chapter or transcript in `materials/`, checks recall without the text, chooses practice for the observed gaps, and gives supplemental theory under the same `unit_id` when needed.

### Source-led sessions

The material header names its plan link:

```md
Unit: `0042`
First shown: 2026-08-25
Node: 2
```

For material outside the mission, use `Node: off-plan`. A following chapter from the same course and source inherits the previous node until the header assigns another. A plan-linked session runs in this order: recall with the source closed, practice for the gaps, observations during the work, remediation, then the chat-only mastery check. An off-plan material is saved as a source and gets no practice, observations, learning record, or plan change. Two off-plan materials prompt a mission review.

The state contract is small: `PLAN.md` holds 3 to 5 open nodes and keeps done nodes as history; `NOTES.md` holds teaching preferences; `OBSERVATIONS.md` holds open gaps, claims, and failed checks with dates and unit ids; learning records hold `Date`, `Units`, and `Evidence`. Practice tasks use `Unit`, `Date`, `Theory`, `Format`, and optional `Also uses` headers. Checks and mastery checks happen in chat and do not allocate a new unit id. Ordinary checks are due seven days after `First shown` or the latest dated practice and create no learning record. Mastery checks use dates at 7, 14, and 28 days after remediation or the preceding successful check.

Lessons are designed against the illusion of fluency: recall over recognition, the same material spaced across sessions, related skills interleaved once there are several to mix. Each lesson is deliberately small - one win, then out.

There is a short plan, 3 to 5 open nodes tied to what success looks like, but no detailed programme and no lesson written before its turn. Done nodes stay in the plan as history. The course also keeps `OBSERVATIONS.md`: where you stalled, what you had to look up, what you got wrong on a check. Lessons, materials, and matching reference files are selected by unit metadata when the next step is chosen. Practice is chosen from a catalogue of ten formats with the evidence behind each, and no practice is handed over before the theory it needs.

## Setup

```
claude plugin marketplace add Villhard/nxs
claude plugin install teach@nxs
```

Restart Claude Code so the plugin snapshot loads. `/teach:me` is invoked by hand only; the model will not start a course on its own.

## Layout

```
.claude-plugin/
  plugin.json
skills/me/
  SKILL.md
  evals/evals.json
  MISSION-FORMAT.md
  PLAN-FORMAT.md
  RESOURCES-FORMAT.md
  GLOSSARY-FORMAT.md
  LEARNING-RECORD-FORMAT.md
  PRACTICE-FORMAT.md
```

The format files are the templates for the workspace files the skill writes, plus the catalogue of practice formats. They are read on demand, not loaded up front.
