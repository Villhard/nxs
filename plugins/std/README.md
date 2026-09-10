# std

Study books, courses, or topics through conversation with `teach`. [Install and configure](../../README.md#install) `std@nxs`; see [compatibility](../../README.md#compatibility).

## Start

**Claude Code**

```text
/std:teach Help me understand this chapter. Start with the author's example.
```

**Codex**

Select `teach` from `std` with `/skills` or the `$` picker in CLI/IDE, or ask:

```text
Use the teach skill from the std plugin to help me understand this chapter.
```

Continue naturally in either client:

- "Explain that more simply. Show the complete example."
- "I think your example assumes something the book does not say."
- "Let's pause. Save where we stopped."

The teacher chooses and begins the next useful learning step after a sound answer; you do not need to keep asking it to continue. It uses your reasoning and saved evidence to deepen a case, introduce an application, or explain a specific gap. Repeated confusion calls for a different example or approach. Your questions, requests for a full solution, and pauses take priority. Checks are useful when they guide the lesson, not after every explanation.

Theory stays in chat; HTML requires a request or agreement. A factual question alone creates no learning workspace. Coding or an applied project is not required.

## Saved progress

| File | Contents |
| --- | --- |
| `MISSION.md` | Purpose, desired outcomes, boundaries |
| `RESOURCES.md` | Main material and inspected sources with annotations |
| `PROGRESS.md` | Current focus, evidence, self-reports, gaps, assistance, unsuccessful explanations, pending task or proposed next step |
| `learning-records/` | Consequential demonstrated insights with evidence and assistance, corrections, goal changes |

To resume, open the same learning directory and request `teach`: "Continue from the previous session." It reads saved progress to choose the next move and its difficulty. The current checkpoint replaces answered questions and stale focus. Saying "understood" allows progress but stays distinct from independent application; later examples can revisit an unverified gap. These files are not transcripts or overall ability scores.

Existing Matt Pocock `teach` workspaces, including `NOTES.md`, are reused without migration or deletion.

The agent needs material access and permission to save files. It searches for useful supplementary sources, separates them from the author's explanation, and identifies unavailable material. Extraction depends on host tools. No additional skills, MCP, hooks, scheduler, or automatic commits are required.

## Sources of ideas

Independently written instructions informed by:

- [Matt Pocock: teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach): mission, sources, learning records.
- [Learning Opportunities](https://github.com/DrCatHicks/learning-opportunities): prediction and waiting for an answer.
- [supertutor](https://github.com/cskwork/supertutor-skill): explain-back and transfer to new examples.
- [misconception-detector](https://github.com/yugash007/edu-agent-skills/tree/main/skills/assessment/misconception-detector): examine and correct mental models.

[Update](../../README.md#update) · [Local preview](../../CONTRIBUTING.md#local-development-and-release) · [Authoring](CONTRIBUTING.md)
