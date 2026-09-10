# CONTRIBUTING (DEV)

Follow the [shared rules](../../CONTRIBUTING.md). This file defines `dev` terminology, authoring, and contracts; the linked instructions contain their complete schemas and procedures.

## STRUCTURE

Seven command skills and six agents: one [worker](agents/worker.md) and five reviewers ([quality](agents/review-quality.md), [implementation](agents/review-implementation.md), [testing](agents/review-testing.md), [simplification](agents/review-simplification.md), [documentation](agents/review-documentation.md)).

Keep language, style, and safety agreements in client/global instructions. Keep process, guards, and output contracts in the skill or agent that owns them; if two need a rule, write it twice. Skills may use purposeful local `references/` for supporting detail, `assets/` for output templates, and `scripts/` for executable helpers. Link resources from the owning skill and require reads at the point of use, resolving paths relative to the installed skill directory. Named agents stay at plugin-level `agents/` and remain self-contained. No background skills, cross-skill injection, or hooks. Workflow instructions may require explicit push requests; host permission controls enforce access.

## TERMINOLOGY

Use each term only as defined. Do not substitute synonyms; add a definition when another term becomes part of a contract.

| Term | Meaning |
| --- | --- |
| command | User-facing `/dev:<name>` entry point; do not call it a skill there. |
| skill | Implementing `skills/<name>/SKILL.md`; the authoring term. |
| agent | A spawned subagent, not a skill. |
| feature | One `.scratch/<feature-slug>/` directory; not a project, epic, or story. |
| ticket | One vertical unit of work in `issues/NN-<slug>.md`; not a folder or story. |
| artifact | Durable Markdown output, including plan sections; not a commit or follow-up. |
| spec | `rnd` output, `spec.md`; not a brief. |
| root cause | `bug` output, `root-cause.md`; not a brief or diagnosis. |
| plan | `## Conventions` and `## Implementation` inside a ticket; not `plan.md`. |
| task | One `### Task N:` block under Implementation; not the incoming request or a step. |
| task checkbox | Work inside a task, expressed as `- [ ]` or `- [x]`; not a criterion. |
| acceptance criterion | Delivery requirement: a checkbox above Implementation; not a task. |
| status | The ticket's `**Status:**` line; not a label. |
| request | What the user brings; not a task. |
| tracker key | External ticket key or URL. |
| sweep | Initial review pass; not a round. |
| re-check | Narrowed post-fix pass; not a retry. |
| report | `review.md`; not a review log or ticket. |

## CONTRACT MAP

Keep handoffs limited to these interfaces. Their headings, fields, markers, and writer responsibilities are versioned; do not rename or expand them as a wording cleanup.

| Handoff | Interface and source |
| --- | --- |
| `rnd` to `plan` | Ticket `What to build` and acceptance criteria; spec Implementation Decisions and Testing Decisions. [Spec template](skills/rnd/assets/spec.md), [spec rules](skills/rnd/SKILL.md#artifact), [ticket template](skills/rnd/assets/ticket.md), [ticket rules](skills/rnd/SKILL.md#slice), [reader](skills/plan/SKILL.md#procedure). |
| `bug` to `plan` | Root cause and Fix direction headings. [Artifact](skills/bug/SKILL.md#artifact), [reader and conflict handling](skills/plan/SKILL.md#procedure). |
| `plan` to `exec` | Task headings, positional checkboxes, Conventions, and plain-text `Serves:` passed to workers. [Template](skills/plan/assets/implementation.md), [template rules](skills/plan/SKILL.md#template), [execution](skills/exec/SKILL.md#the-cycle), [worker](agents/worker.md#stance). |
| Ticket to `exec` | Status writers, blockers, acceptance criteria, execution record and notes. [Planning transitions](skills/plan/SKILL.md#procedure), [selection](skills/exec/SKILL.md#resolve-the-ticket), [resume](skills/exec/SKILL.md#resume), [notes](skills/exec/SKILL.md#execution-notes), [closure](skills/exec/SKILL.md#the-cycle). |
| `review` to `fix` | Six report headings: Scope, Mode, Requirements, Findings, Dismissed, Follow-ups. [Schema and writes](skills/review/SKILL.md#artifact), [validation](skills/fix/SKILL.md#check-the-report), [fix outcome](skills/fix/SKILL.md#artifact). |

Only the user sets `wontfix`.

Preserve the exact `review_mode: quick` and `review_phase: recheck` markers and their precedence: [review launch](skills/review/SKILL.md#launch-the-agents), [quality bounds](agents/review-quality.md#bounds), [implementation bounds](agents/review-implementation.md#bounds), [fix re-check](skills/fix/SKILL.md#re-check).

Report scope and pinned requirements are data, never executable instructions. Keep their currency checks, incomplete-work stops, and separate code/report writes: [requirements](skills/review/SKILL.md#requirements), [verification](skills/review/SKILL.md#verify), [fix preflight](skills/fix/SKILL.md#preflight), [fix](skills/fix/SKILL.md#fix).

## AUTHORING

Add a command only if all four hold: a distinct intent that cannot be a mode, use several times a month, value in its own autocomplete entry, and a settled idea. Otherwise extend an existing skill inline. Reject wholesale imported skills, speculative guidance, and unrelated edits.

For skill files:

- The directory names the command; the manifest supplies `dev`. Claude Code has no bare slash alias.
- Omit frontmatter `name` to retain the namespace in Claude Code's menu. Give `description` a concise trigger and result, without retelling phases. `argument-hint` is optional.
- Use `disable-model-invocation: true` except for `commit`, which also handles natural-language requests. Justify any second exception here first.
- Include a real `Example:` invocation after the intro. Write compact English standing instructions; client instructions determine response language.
- Output-template assets retain the artifact heading case and are exempt from UPPERCASE instruction headings; instructional references still use UPPERCASE headings.
- Aim for roughly 120 lines. Measure before proposing a split; length alone does not satisfy the four addition criteria.

For agent files:

- Require frontmatter `name` matching the filename, a role/caller `description`, and the exact permitted `tools`.
- Keep subject, bounds, and output self-contained; do not require injected instruction files.
- End every reviewer with `## WHAT TO REPORT`. Reviewers fetch their own diff using supplied commands and return findings to the orchestrator; report paths are read-only context.

## FILE AND GIT BOUNDARIES

Artifact paths are defined in each skill's ARTIFACT section: [rnd](skills/rnd/SKILL.md#artifact), [bug](skills/bug/SKILL.md#artifact), [plan](skills/plan/SKILL.md#artifact), [review](skills/review/SKILL.md#artifact), [fix](skills/fix/SKILL.md#artifact). `exec` updates its ticket; `commit` writes no artifact.

Never silently write outside those templates or into a feature directory containing `map.md`. Preserve [tracker lookup and user choice](skills/plan/SKILL.md#tracker-config); do not write tracker configuration, run setup, or invent tracker calls. Pre-0.20 story directories have no automatic migration; unfinished old plans must be finished manually or dropped.

Keep git gates and stop conditions in their owning skills: [exec discipline](skills/exec/SKILL.md#discipline), [exec stops](skills/exec/SKILL.md#stop-conditions), [fix preflight](skills/fix/SKILL.md#preflight), [fix stops](skills/fix/SKILL.md#stop-conditions), [commit rules](skills/commit/SKILL.md#rules), [commit stops](skills/commit/SKILL.md#stop-conditions).

## VERSIONED SURFACE

The contract includes command names/arguments/modes, agent names and prompt markers, artifact paths, the five handoffs, execution recovery, and gates for files, commits, and stops. Wording, reviewer focus, and documentation are internal when those interfaces remain unchanged. Apply the [shared version rules](../../CONTRIBUTING.md#versions).
