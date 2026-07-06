---
description: Compact session handoff printed to chat for the next agent or session - use when handing a session to another agent or continuing in a fresh context; it points to existing artifacts and writes no file.
argument-hint: "[]"
---

# /nxs:doc-handoff

Print a compact, pointer-style session handoff to the chat for immediate pickup by the next agent or a fresh session. Self-contained skill. Output language and response style come from global rules, not this file.

The handoff is a pointer to existing artifacts, not a copy of their content. It is printed to chat only - never written to disk, the repo, the vault, or git. It is ephemeral: for a durable snapshot use /nxs:doc-summary instead.

Assembly sources: the active plan, the branch and recent commits, and the chat transcript of this session. Accepts an optional short goal description in the argument only if the goal cannot be derived from those sources.

## PROCEDURE

1. Gather context:
   - active plan path (`docs/plans/*.md`, not `completed/`);
   - branch / base / changed files / recent commits;
   - briefs and ADRs mentioned in the plan or in the chat;
   - Jira URL from the plan or the PR description.
2. Extract from the chat:
   - current goal (one or two lines);
   - decisions made in this session, each with its durable home indicated (plan / ADR / brief) or marked inline-only;
   - unresolved questions;
   - an assumption about the next command based on the work state.
3. Apply the pointer rule (see POINTER RULE): point to artifacts, do not copy their content.
4. Apply redaction (see REDACTION): mandatory before printing.
5. Determine the slug (used only for the handoff title):
   - from the active plan filename (`docs/plans/YYYY-MM-DD-<slug>.md` -> `<slug>`);
   - otherwise from the branch (`feat/<slug>` -> `<slug>`);
   - otherwise from the goal statement;
   - otherwise ask.
6. Print the handoff to the chat. Never write a file (no `$TMPDIR`, no `/tmp`, no repo, no vault, no git).

## OUTPUT FORMAT

Printed to the chat as a markdown block (no file, no YAML frontmatter). Each section is short. If there is no data for a section, omit it - do not add placeholders.

```markdown
# HANDOFF: <slug>

## HOW TO USE THIS HANDOFF

For a fresh agent: read this block, then open the artifacts by the links below. Do not act on the basis of this handoff alone without reading the plan / brief / diff at the indicated paths.

## CURRENT GOAL

<one or two lines>

## DECISIONS MADE

- <decision> - captured in <plan path | ADR path | brief path>
- <decision without a durable home> - inline, one line

## UNRESOLVED QUESTIONS

- <question> (needs to be resolved before <triggering step>)

## SOURCE ARTIFACTS

- plan: <docs/plans/...md>
- brief: <docs/briefs/...md>
- root-cause brief: <docs/briefs/...-root-cause.md>
- Jira: <URL>
- ADRs: <docs/adr/...md>

## CODE STATE

- branch: <name>
- base: <main | other>
- changed files: see `git diff --name-only <base>...HEAD`
- recent commits: see `git log <base>..HEAD --oneline`

## NEXT STEP

Recommended next command: `/nxs:...` with parameters `<...>`.

## SUGGESTED SKILLS

- /nxs:... - why it fits now
```

## POINTER RULE (no duplication)

Do not copy the content of:

- a plan - give the path;
- a brief - give the path;
- an ADR - give the path;
- a Jira description - give the URL;
- a diff / patch - give the command `git diff <base>...HEAD` or the PR URL;
- commit messages - give `git log <base>..HEAD` or the PR URL.

Inline is allowed only for:

- decisions made in the current session and not yet captured in a plan / ADR / brief;
- open questions that surfaced in the chat;
- assumptions that need to be checked before the next step.

## REDACTION

Mandatory before output. Skim the full handoff; on any pattern match, replace the value with `[REDACTED]`, keeping only the type (e.g. `Bearer [REDACTED]`, `AWS key [REDACTED]`). If it is unclear whether a value is a secret, drop the section rather than risk a leak.

Remove / mask:

- AWS / GCP / Azure keys and tokens (patterns `AKIA...`, `ASIA...`, `AIza...`, JWT-like `eyJ...`);
- API keys and Bearer tokens (`Bearer <...>`, `Token <...>`, `xoxb-...`, `ghp_...`, `glpat-...`, `sk-...`);
- `BEGIN ... PRIVATE KEY` blocks;
- values from `.env` and password-like fields (`password=`, `passwd=`, `secret=`, `client_secret=`);
- personal data (coworker emails, phone numbers) that ended up in the chat unintentionally.

The general never-commit / never-log-secrets safety is enforced by the global tier-1 block; the scrubbing above is the handoff-specific detail applied before printing.

## WRITES NOTHING

This skill writes to nothing:

- no disk or OS temp (`$TMPDIR`, `/tmp`);
- no repo `docs/`;
- no Obsidian vault (`_inbox/` or elsewhere);
- no git (no add / commit / push).

The handoff is printed to the chat and nowhere else. Any durable write happens only through explicit delegation to another skill - this skill itself never writes.

In the same chat message as the handoff, call out:

- redaction - if it touched a significant block, say what exactly was removed;
- decisions / questions with no durable home - flag them as inline-only;
- a weak slug - note it.

## DELEGATION

If after the handoff the user wants a durable artifact, route to the right skill - handoff does not write it:

- save applied knowledge -> /nxs:doc-note;
- save a task-doc snapshot -> /nxs:doc-summary;
- write a new plan -> /nxs:dev-plan;
- capture a decision as an ADR -> the `decision-log` background skill.

## DIFFERENTIATION

/nxs:doc-handoff vs /nxs:doc-summary:

- handoff - an ephemeral chat pointer for immediate pickup (next session or coworker within an hour); writes no file;
- summary - a durable vault snapshot for a longer horizon.

If the sense is unclear, produce a handoff: it is easier to rework into a note later than the other way around. Do not merge handoff into /nxs:doc-note or /nxs:doc-summary; they serve distinct purposes.

## ROUTING

- /nxs:doc-handoff - a compact session handoff printed to chat for the next agent or session, not a durable file (this skill).
- /nxs:doc-summary - a durable task-doc snapshot tied to one task's branch / plan / commits.
- /nxs:doc-note - free-standing applied knowledge you already hold (cheatsheet / howto / reference / gotcha).
