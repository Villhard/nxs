---
description: Assemble a durable task-doc snapshot (what / why / how) for reviewers and team - use to record the work done on a specific task from its branch / plan / commits.
argument-hint: "[jira key | slug]"
---

# /nxs:doc-summary

Assemble a durable task-doc snapshot of the work done on a specific task: what was done, why, and how, drawn from the current branch / plan / commits. Self-contained skill. Output language and response style come from global rules, not this file.

A task-doc is a snapshot of the work on one specific task (what / why / how / impact), assembled from the current branch, active plan, and commits. It is raw material for later ingest, not applied knowledge: the applied-knowledge FILTER (used by /nxs:doc-note) does NOT apply here. The user later moves the file from `_inbox/` to `<context>/raw/` and ingests it into a context.

Inputs: an optional task id (Jira key or slug) in the argument; the branch, plan, and commits are detected by the skill itself.

## PROCEDURE

1. Get the task identifier: from the argument if provided (Jira key or slug); otherwise from the active plan (`docs/plans/*.md` if it carries a Jira key); otherwise ask the user once. If there is no identifier, use a slug with no bracketed key.
2. Gather the task context: current branch name; active plan path if any; commits since branch divergence (`git log <base>..HEAD`); diff or a diff summary, if reasonable by size.
3. Determine the slug: from the plan name if any (`docs/plans/YYYY-MM-DD-<slug>.md` -> `<slug>`); otherwise from the branch name (`feat/<slug>` -> `<slug>`); otherwise ask.
4. Build the filename: `YYYY-MM-DD.task.[<id>].<slug>.md`, or without `[<id>]` when there is no identifier.
5. Compose the draft following the structure below, faithful to the gathered source - facts derivable from the plan / commits / diff, no fabrications.
6. Show the draft to the user and wait for approval or edits (doc mode always shows the draft before writing).
7. On approval, write to the vault inbox (`_inbox/` by default) per `note-conventions`.
8. Tell the user the file path.

## DRAFT STRUCTURE

- frontmatter: `type: task-doc`, `task: <id|null>`, `plan: <path|null>`, `commits: [...]`, `updated: today`, `tags: [type/task-doc]`;
- `# <Task title>` - from the plan or the user's answer;
- `## WHAT WAS DONE` - summary of changes from the diff / commits;
- `## WHY` - from the plan / brief if any, otherwise a placeholder asking to fill it in;
- `## HOW WE SOLVED IT` - approach plus alternatives from the plan / commits;
- `## IMPACT ON CONTEXT` - empty section with the placeholder `<!-- fill in at ingest -->`; do NOT fill it automatically, context selection is the user's job at ingest;
- `## OPEN QUESTIONS` - from the plan if any, otherwise empty;
- `## LINKS` - plan path, commits, Jira, related raw notes if known.

## RULES

Save: a snapshot of work on a specific task, with links to the plan / commits / Jira; the `IMPACT ON CONTEXT` section stays a placeholder for the user; only facts derivable from the plan / commits / diff.

Do NOT save: specs of future work (that is a plan, not a task-doc); secrets; essays about the system with no tie to a specific task.

The applied-knowledge filter does NOT gate this artifact - a task-doc is a work record, not reusable knowledge.

## CONVENTIONS

For the task-doc frontmatter schema, filename convention, vault location, and redaction of secrets, follow the `note-conventions` background skill. Do not restate them here.

- Default artifact path `~/Documents/notes/_inbox/YYYY-MM-DD.task.[<id>].<slug>.md` (`.[<id>]` segment absent when there is no identifier); the target location is vault-schema-driven and comes from `note-conventions`.
- Never write secrets, tokens, .env values, private keys, or passwords into a task-doc; redact per `note-conventions`.

## APPROVAL AND SAFETY

- Read-only until the user approves the write.
- Always show the draft and wait for approval before writing (doc mode).
- Write to the vault inbox (`_inbox/` by default) only after approval, then report the path.

## ROUTING

- /nxs:doc-summary - a durable task-doc snapshot tied to one task's branch / plan / commits (this skill).
- /nxs:doc-note - free-standing applied knowledge you already hold (cheatsheet / howto / reference / gotcha), gated by the applied-knowledge filter.
- /nxs:doc-handoff - a compact session handoff printed to chat for the next agent or session, not a durable file.
