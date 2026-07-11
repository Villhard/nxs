---
description: Write technical documentation of a solution for other programmers who will read, extend, or operate it, assembled from the branch / plan / diff. Use when a solution needs a technical writeup for maintainers, not end users. A local draft published to Confluence per the `doc-draft` kernel.
argument-hint: "[topic | task id]"
---

# /nxs:techdoc

Produce technical documentation of a solution aimed at other programmers who will read, extend, or operate it. Assembled from the current branch, active plan, and diff. Self-contained skill. Output language and response style come from global rules, not this file.

Example: /nxs:techdoc payment webhook retry

## PROCEDURE

1. Resolve the subject: from the argument (topic or task id), otherwise from the active plan / branch. Ask once only if unresolvable.
2. Gather source: branch name, active plan path, commits since divergence, the diff or a diff summary. Read the code enough to describe the solution faithfully; no fabrication.
3. Draft following DOCUMENT SHAPE, faithful to the source - only what is derivable from the code / plan / diff / commits.
4. Show the draft and wait for approval or edits (doc mode always shows the draft before writing).
5. On approval, write and handle the draft per the `doc-draft` kernel: path scheme `docs/techdoc/<slug>.md`, Confluence as the durable home, pre-publish scrub.
6. Tell the user the path and that it is a local draft to publish to Confluence.

## DOCUMENT SHAPE

- `# <Solution title>`
- `## PROBLEM` - what this solves, in one or two lines;
- `## APPROACH` - the solution and the key decisions behind it, alternatives rejected;
- `## HOW IT WORKS` - the moving parts and how they connect, in reading order;
- `## INTERFACES` - the public surface: APIs, config, entry points, contracts other code depends on;
- `## OPERATE` - how it is run, configured, observed (config keys, metrics, logs) - only if applicable;
- `## GOTCHAS` - non-obvious constraints, edge cases, follow-ups.

Scale to the change: a small solution gets PROBLEM + APPROACH + HOW IT WORKS; omit sections that do not apply, never pad.

## WRITING FOR THE AUDIENCE

- Audience: a programmer who will maintain or extend this, not the author. Assume repo familiarity but not this solution.
- Technical and precise; describe the real code, not an idealized version. Terms stay English where customary.

## ARTIFACT AND SAFETY

The draft contract - `docs/techdoc/<slug>.md` path scheme, Confluence as the durable home, draft-before-write, and the pre-publish scrub - comes from the `doc-draft` kernel. This skill does not restate it.

## NEXT

End-user documentation -> `/nxs:userdoc`. Record a significant decision -> `decision-log`.
