---
description: Archive completed plans and outdated / superseded briefs into their archive folders after the user approves the proposed moves. Use when wrapping up a feature or clearing finished / stale planning docs - it relocates docs only, never touches git history and never deletes content.
argument-hint: "[plans | briefs]"
---

# /nxs:dev-cleanup

Move completed plans and outdated / superseded briefs into their archive folders, only after the user approves the proposed set. This is docs-hygiene, not git history. Self-contained skill; output language and response style come from global rules, not this file.

## SCOPE

Relocate finished planning docs across two directories:
- completed plans -> `docs/plans/completed/`
- outdated / superseded briefs -> `docs/briefs/archive/`

The argument selects scope: no argument processes both `docs/plans/` and `docs/briefs/`; `plans` processes only plans (skip the briefs step); `briefs` processes only briefs (skip the plans step).

## GUARDS

- APPROVAL-FIRST - propose the candidate moves and get the user's approval before moving anything. Never auto-archive.
- NO AUTO-ARCHIVE BY DATE - age alone is never a reason to archive. Every candidate needs a concrete reason beyond "old".
- MOVE, NOT DELETE - relocate files; never delete content.
- DOCS-ONLY - touch only `docs/plans/` and `docs/briefs/`. This is not git history cleanup (that is `/nxs:dev-recommit`) and not source-code cleanup.

## ARTIFACT PATHS

- completed plan: `docs/plans/YYYYMMDD-<slug>.md` -> `docs/plans/completed/YYYYMMDD-<slug>.md`
- archived brief: `docs/briefs/YYYYMMDD-<slug>.md` -> `docs/briefs/archive/YYYYMMDD-<slug>.md`

## PROCEDURE

1. Detect completed plans.
   - Read `docs/plans/*.md` (excluding `docs/plans/completed/`).
   - Count `- [ ]` and `- [x]` in each plan.
   - Candidate: all checkboxes are `[x]` and there are zero `[ ]`. State the reason concretely, e.g. "12/12 tasks checked".
   - Any unchecked item -> keep as active, do not touch.

2. Detect stale briefs.
   - Read `docs/briefs/*.md` (excluding `docs/briefs/archive/`).
   - Candidate only when at least one concrete signal holds:
     - a plan in `docs/plans/` or `docs/plans/completed/` links to the brief or shares its topic and that plan is completed -> worked through;
     - the brief's "Next step" / proposed fix is already done (plan exists, fix visible in code, merge in git log) -> worked through;
     - the topic is outdated / superseded and no further work is planned.
   - Attach a reason the user can dispute to each candidate.
   - Hard to classify -> show it as unclear, do not guess, do not archive.

3. Propose. Print the candidate moves as a list (plans, briefs, and what stays active), then ask for approval. Move nothing before approval.

```
Cleanup proposal:

Plans -> docs/plans/completed/:
- 20260428-foo.md (12/12 tasks checked)

Briefs -> docs/briefs/archive/:
- 20260301-baz.md (plan 20260305-baz.md completed)
- 20260201-qux.md (proposed fix merged, no further work planned)

Active (not touching):
- 20260506-bar.md (brief awaiting grooming)

Approve? (yes / partial / no)
```

4. Approval.
   - `yes` -> perform all moves.
   - partial (file names / "only plans" / "only the first brief") -> perform only the selected ones.
   - `no` -> close the proposal, move nothing.

5. Execute (only after approval).
   - `mkdir -p docs/plans/completed/` and `docs/briefs/archive/` only if there is something to move into them.
   - `git mv` when the file is tracked, otherwise `mv`.
   - Report the moved files as a list.
   - If a plan's final task item is "move into `docs/plans/completed/`", mark it `[x]` after the move.

## RULES

- Read-mostly until approved; no move without approval.
- No deletions - moves only.
- Do not modify file contents (exception: a plan's final move-item gets `[x]` after its own move).
- Do not touch files outside `docs/plans/` and `docs/briefs/`.
- Do not recreate empty `completed/` / `archive/` when there is nothing to move.
- A brief is NOT stale solely because it is old by date (without other signals), lacks a linking plan (the plan may live in another repo or not yet exist), or contains open questions / a draft. These are reasons to ask, not to archive silently.

## NEXT

Docs archived. For cleaning up git commit history (not docs) -> `/nxs:dev-recommit`. For a code review of the branch -> `/nxs:dev-review`.
