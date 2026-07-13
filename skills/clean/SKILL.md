---
description: Archive completed plans, outdated / superseded briefs, and completed epic maps into their archive folders after the user approves the proposed moves. Use when wrapping up a feature or clearing finished / stale planning docs - it relocates docs only, never touches git history and never deletes content.
argument-hint: "[plans | briefs | epics]"
---

# /nxs:clean

Move completed plans, outdated / superseded briefs, and completed epic maps into their archive folders, only after the user approves the proposed set. This is docs-hygiene, not git history. Self-contained skill; output language and response style come from global rules, not this file.

Example: /nxs:clean plans

## SCOPE

Relocate finished planning docs across three directories:
- completed plans -> `docs/plans/completed/`
- outdated / superseded briefs -> `docs/briefs/archive/`
- completed epic maps -> `docs/epics/archive/`

The argument selects scope: no argument processes `docs/plans/`, `docs/briefs/`, and `docs/epics/`; `plans` / `briefs` / `epics` processes only that kind (skip the other steps).

## GUARDS

- APPROVAL-FIRST - propose the candidate moves and get the user's approval before moving anything. Never auto-archive.
- NO AUTO-ARCHIVE BY DATE - age alone is never a reason to archive. Every candidate needs a concrete reason beyond "old".
- MOVE, NOT DELETE - relocate files; never delete content.
- DOCS-ONLY - touch only `docs/plans/`, `docs/briefs/`, and `docs/epics/`. This is not git history cleanup (that is `/nxs:recommit`) and not source-code cleanup.

## ARTIFACT PATHS

- completed plan: `docs/plans/YYYYMMDD-<slug>.md` -> `docs/plans/completed/YYYYMMDD-<slug>.md`
- archived brief: `docs/briefs/YYYYMMDD-<slug>.md` -> `docs/briefs/archive/YYYYMMDD-<slug>.md`
- archived epic: `docs/epics/YYYYMMDD-<slug>.md` -> `docs/epics/archive/YYYYMMDD-<slug>.md`; the map's notes folder `docs/epics/YYYYMMDD-<slug>/` moves with it

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

3. Detect completed epics.
   - Read `docs/epics/*.md` (excluding `docs/epics/archive/`).
   - Candidate: the header says `Status: complete`. Corroborate before proposing: Frontier and Not yet specified are empty, every task is done. `Status: complete` without that corroboration -> show it as unclear, do not archive.
   - The map and its notes folder (`docs/epics/YYYYMMDD-<slug>/`) move together as one unit.
   - Any open item, fog entry, or task -> keep as active, do not touch.

4. Propose. Print the candidate moves as a list (plans, briefs, epics, and what stays active), then ask for approval. Move nothing before approval.

```
Cleanup proposal:

Plans -> docs/plans/completed/:
- 20260428-foo.md (12/12 tasks checked)

Briefs -> docs/briefs/archive/:
- 20260301-baz.md (plan 20260305-baz.md completed)
- 20260201-qux.md (proposed fix merged, no further work planned)

Epics -> docs/epics/archive/:
- 20260210-checkout-v2.md + notes folder (Status: complete, all tasks done)

Active (not touching):
- 20260506-bar.md (brief awaiting grooming)

Approve? (yes / partial / no)
```

5. Approval.
   - `yes` -> perform all moves.
   - partial (file names / "only plans" / "only the first brief") -> perform only the selected ones.
   - `no` -> close the proposal, move nothing.

6. Execute (only after approval).
   - `mkdir -p docs/plans/completed/`, `docs/briefs/archive/`, `docs/epics/archive/` only if there is something to move into them.
   - `git mv` when the file is tracked, otherwise `mv`. An epic map moves together with its notes folder.
   - Report the moved files as a list.
   - If a plan's final task item is "move into `docs/plans/completed/`", mark it `[x]` after the move.

## RULES

- Read-mostly until approved; no move without approval.
- No deletions - moves only.
- Do not modify file contents (exception: a plan's final move-item gets `[x]` after its own move).
- Do not touch files outside `docs/plans/`, `docs/briefs/`, and `docs/epics/`.
- Do not recreate empty `completed/` / `archive/` when there is nothing to move.
- A brief is NOT stale solely because it is old by date (without other signals), lacks a linking plan (the plan may live in another repo or not yet exist), or contains open questions / a draft. These are reasons to ask, not to archive silently.

## NEXT

Docs archived. For cleaning up git commit history (not docs) -> `/nxs:recommit`. For a code review of the branch -> `/nxs:review`.
