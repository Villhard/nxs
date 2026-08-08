# teach

A tutor that remembers. `/teach` turns the current directory into a teaching workspace and keeps the state of a course there: why you are learning the topic, which sources are trustworthy, the lessons you have been through, and what you have actually demonstrated. Next session picks up from that record rather than from an empty prompt.

## Quickstart

```
mkdir ~/learning/weightlifting && cd ~/learning/weightlifting
claude
/teach olympic weightlifting
```

The first session interviews you about why you want this and writes the mission. Every session after that reads the workspace, picks the next lesson just past what you can already do, and writes it as a self-contained HTML page you can reopen later.

## What appears in the workspace

| path | holds |
| --- | --- |
| `MISSION.md` | the concrete outcome you are chasing. Everything else is judged against it |
| `RESOURCES.md` | trusted sources, plus the communities where judgement comes from |
| `GLOSSARY.md` | the settled vocabulary, used the same way in every lesson |
| `NOTES.md` | how you want to be taught |
| `lessons/` | the lessons, numbered, one HTML file each |
| `reference/` | cheat sheets distilled from lessons, built to be reread |
| `learning-records/` | what you have demonstrably learned, and what it unlocks |
| `assets/` | the shared stylesheet and reusable lesson components |

One mission per workspace. Two unrelated topics are two directories.

## How it teaches

Knowledge comes from sources in `RESOURCES.md` rather than from the model's recall, and lessons carry citations back to them. Skills come from short interactive lessons built around an immediate feedback loop. Judgement comes from practising among people who already have it, so the skill points you at communities instead of pretending to be one.

Lessons are designed against the illusion of fluency: recall over recognition, the same material spaced across sessions, related skills interleaved once there are several to mix. Each lesson is deliberately small - one win, then out.

## Setup

```
claude plugin marketplace add Villhard/nxs
claude plugin install teach@nxs
```

Restart Claude Code so the plugin snapshot loads. `/teach` is invoked by hand only; the model will not start a course on its own.

## Layout

```
.claude-plugin/
  plugin.json
skills/teach/
  SKILL.md
  MISSION-FORMAT.md
  RESOURCES-FORMAT.md
  GLOSSARY-FORMAT.md
  LEARNING-RECORD-FORMAT.md
```

The four format files are the templates for the workspace files the skill writes. They are read on demand, not loaded up front.
