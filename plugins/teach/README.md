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
| `PLAN.md` | 3 to 5 nodes tied to what success looks like, so direction survives between sessions |
| `RESOURCES.md` | trusted sources, plus the communities where judgement comes from |
| `GLOSSARY.md` | the settled vocabulary, used the same way in every lesson |
| `OBSERVATIONS.md` | what you have not settled yet: where you stalled, what you looked up, what you got wrong |
| `NOTES.md` | how you want to be taught |
| `lessons/` | the lessons, numbered, one HTML file each |
| `practice/` | everything you produce: drills, exercises, projects |
| `reference/` | cheat sheets distilled from lessons, built to be reread |
| `learning-records/` | what you have demonstrably learned, and what it unlocks |
| `assets/` | the shared stylesheet and reusable lesson components |

One mission per workspace. Two unrelated topics are two directories.

## How it teaches

Knowledge comes from sources in `RESOURCES.md` rather than from the model's recall, and lessons carry citations back to them. Skills come from short interactive lessons built around an immediate feedback loop. Judgement comes from practising among people who already have it, so the skill points you at communities instead of pretending to be one.

Lessons are designed against the illusion of fluency: recall over recognition, the same material spaced across sessions, related skills interleaved once there are several to mix. Each lesson is deliberately small - one win, then out.

There is a short plan, 3 to 5 nodes tied to what success looks like, but no detailed programme and no lesson written before its turn - one written out in full at the start survives about two sessions. The course also keeps `OBSERVATIONS.md`: where you stalled, what you had to look up, what you got wrong on a check. That list, alongside the plan, is what the next step is chosen against, so the programme follows the gaps rather than an outline. Practice is chosen from a catalogue of ten formats with the evidence behind each, and no practice is handed over before the theory it needs.

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
  MISSION-FORMAT.md
  PLAN-FORMAT.md
  RESOURCES-FORMAT.md
  GLOSSARY-FORMAT.md
  LEARNING-RECORD-FORMAT.md
  PRACTICE-FORMAT.md
```

The format files are the templates for the workspace files the skill writes, plus the catalogue of practice formats. They are read on demand, not loaded up front.
