# Changelog

All notable changes to the `teach` plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-08

First release. `/teach` treats the current directory as a course that survives between sessions: a mission that says why the topic matters, curated sources the lessons cite, numbered HTML lessons, reference sheets distilled out of them, and learning records that fix what the user has actually demonstrated. The next lesson is chosen from those records rather than from whatever was last discussed.

The pedagogy is the part worth stating. Knowledge is taken from sources rather than recall; skills are built through immediate feedback loops; judgement is delegated to communities, because a model cannot supply it. Lessons are designed against fluency mistaken for mastery - recall over recognition, spacing across sessions, interleaving once several skills exist to mix.

### Added

- `skills/teach/SKILL.md` - the command. Reads the workspace, interviews for a mission when there is none, fills the sources before teaching from them, picks the next lesson just past the current floor, and writes a learning record only against demonstrated understanding.
- `skills/teach/MISSION-FORMAT.md`, `RESOURCES-FORMAT.md`, `GLOSSARY-FORMAT.md`, `LEARNING-RECORD-FORMAT.md` - the templates for the four workspace documents, each with the rules that keep it useful. All four are linked from `SKILL.md` and read on demand.
- Quizzes must shuffle the correct answer's position and keep every option the same length, so neither habit nor formatting gives the answer away.
