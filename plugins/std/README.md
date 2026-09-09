# std

Learn from books, courses, and topics through conversation in Claude Code or Codex. One shared `teach` skill explains small pieces, answers follow-up questions, and checks understanding when the learner is ready.

## Install

Follow the marketplace [install instructions](../../README.md#install), selecting `std@nxs`:

```bash
# Claude Code
claude plugin install std@nxs

# Codex
codex plugin add std@nxs
```

The shared [update instructions](../../README.md#update) give the marketplace-refresh and plugin-update commands for both clients. Start a new session after installing or updating.

Installation and skill discovery are verified in both clients. Sample learning dialogues were exercised in Claude Code and in Codex using the same skill; these are spot checks, not a guarantee of every lesson's correctness. Both manifests use the shared `skills/teach` implementation.

## Use

In Claude Code:

```text
/std:teach Help me understand this chapter. Start with the author's example.
```

In Codex, select the plugin's `teach` skill or explicitly ask to use `teach` from `std`. In either client, continue naturally:

- "I don't understand why that step works. Explain it more simply."
- "Show the complete example, then let me try a variation."
- "I think your example assumes something the book does not say."
- "Let's pause. Save where we stopped."
- "Continue from the previous session."

A plain factual question does not require a learning workspace. During a lesson, questions get direct answers; checks do not replace explanations. Theory stays in chat. HTML is optional when requested or agreed for an interactive demonstration.

## What is saved

| Artifact | Purpose |
| --- | --- |
| `MISSION.md` | Learning purpose, desired outcomes, and boundaries |
| `RESOURCES.md` | Anchor material and inspected additional sources with annotations |
| `PROGRESS.md` | Current focus, evidence of understanding, gaps, and next step |
| `learning-records/` | Consequential insights, corrections, and goal changes |

Existing Matt Pocock `teach` workspaces are reused, including preferences from `NOTES.md`. No migration or deletion is required. Progress is a compact checkpoint, not a transcript or a generated textbook. Demonstrated understanding is recorded separately from material merely discussed or self-reported as understood.

## Requirements and limits

The agent needs read access to the material and write access to the chosen learning directory to save progress. Web search helps verify supplementary sources. If a source is unavailable, the skill says so and works from accessible material or asks for the needed excerpt.

There are no required MCP servers, hooks, scheduler, separate teaching agents, or automatic commits. Document extraction depends on the host's available tools. Skill instructions guide behavior; source grounding and progress records do not guarantee factual correctness or objectively measure mastery.

## Design influences

These are independently written instructions informed by the following public skills:

- [Matt Pocock: teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) - mission, trusted resources, and durable learning records.
- [Dr. Cat Hicks: Learning Opportunities](https://github.com/DrCatHicks/learning-opportunities) - prediction, active recall, and waiting for the learner's answer.
- [cskwork: supertutor](https://github.com/cskwork/supertutor-skill) - explaining back, specific gaps, and checking transfer to a new example.
- [edu-agent-skills: misconception-detector](https://github.com/yugash007/edu-agent-skills/tree/main/skills/assessment/misconception-detector) - examining and correcting the learner's mental model.

## Development

For a local Claude Code preview from the marketplace checkout:

```bash
claude --plugin-dir ./plugins/std
```

This loads local content for that session without changing an installed plugin. See [CONTRIBUTING.md](CONTRIBUTING.md) for the versioned contract and verification scenarios, and the repository [development guidance](../../CONTRIBUTING.md#local-development-and-release) for source and cache behavior.
