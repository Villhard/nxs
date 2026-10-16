---
description: Apply a saved, current review report when explicitly asked to use /dev:fix. Reverify findings, delegate code changes, commit and update the report separately. Do not start a new sweep; use /dev:review for stale or unfinished reports.
argument-hint: "[report path]"
disable-model-invocation: true
---

# /DEV:FIX

Read a report, verify its open findings, fix them and record the outcome. Never run a sweep. A ticket's status and acceptance criteria belong to `/dev:exec` and are never changed here.

Example: /dev:fix

Suggest the next command at a handoff; never start it automatically.

## RESOLVE THE REPORT

Use the explicit report path, otherwise find the single report under `.scratch/` whose `## Scope` matches this checkout. None or several - stop and name the candidates; ask for a report path when ambiguous. Do not choose by modification time.

Read [review report](../../references/review-report.md) and validate the report under its FORMAT and VALIDATION.

## CHECK THE REPORT

Check these gates before an already-applied or no-op answer:

| Report state | Action |
| --- | --- |
| `sweep: incomplete`, `fix: in-progress`, `fix: stopped` or `re-check: incomplete` | Stop before writes; name the unfinished attempt and request a new `/dev:review`. Do not resume it here. |
| `sweep: complete`, no `fix:` line | Check CURRENCY from review report, then PREFLIGHT and VERIFY AGAIN. |
| `sweep: complete`, `fix: done` | Check CURRENCY from review report. Then report already applied, list unresolved findings and stop without writes or a worker. |
| Missing, duplicate or unsupported state fields | Stop before writes and name the invalid fields. |

Keep the resolved base and the path selector for the whole run.

Any mismatch - list what changed and point to `/dev:review`; do not sweep. A current fixed report is already applied: say so, list its unresolved findings, and stop without a worker.

## PREFLIGHT

Before any edit, confirm foreign work when the user has not already authorized fixing it, especially a checked-out colleague's PR. Inspect staged, unstaged and untracked files, including ignored code that a fix or test would touch.

- Branch/path: no staged or unstaged changes apart from the report itself, and no untracked code changes.
- Staged: the full staged set must match the recorded digest; no unstaged changes apart from the report, and no untracked code changes.

Anything else - stop, list the files, ask the user to save or scope that work first. Do not stash or snapshot it. Report-only dirt is permitted, but an already-staged report must be safely excluded from the eventual commit without losing either version; if that cannot be isolated safely, stop and ask the user to unstage the report first. Never silently include it.

## VERIFY AGAIN

Read [findings](../../references/findings.md) and check each open finding in the version being checked under its VERIFY A FINDING. An uncertain location is a stop. Gone or already handled - prepare `result: dropped - <reason>` with evidence; persist it only after the launch capability check below, or in the successful no-op write.

Keep the original sweep facts and all earlier conclusions. Accumulate each verification result, dismissal reason, actual correction and check result as finding history for the report and re-check prompts. A pre-existing test or lint failure is still a failure.

No open findings, or all dropped, is a successful no-op after all gates above pass. Add only newly established `result: dropped - <reason>` lines with their verification evidence; with no new results, do not rewrite the file. No worker, commit, `fix:`, `fixed at:` or re-check field is added. Preserve the original tip, staged digest and unfixed state.

## FIX

After the no-op check and before any report or code edit for surviving findings, read [agent launch](../../references/agent-launch.md) and complete its capability check for the worker and any required re-check roles. Use its adapters and complete packets for FIX and RE-CHECK. A no-op needs no agents.

1. Write `fix: in-progress` before launching a worker or changing code. Re-check preflight if checkout changes occurred during verification.
2. Launch one `dev:worker` with the surviving findings verbatim, each location, severity, issue, impact and fix, plus the branch's conventions, applicable project rules, current user directives, goal, pinned requirements and relevant correction history. Findings are its entire unit of work. It neither commits nor edits the report or ticket status.
3. Wait for the worker. Collect its `Decisions` and `Deviations`, including from blocked or partial results, with finding and reason. Inspect the actual diff and run project tests and linter yourself after its last edit. Record actual corrections and verification results; all green before committing. A blocked or partial worker stops the run.
4. Check the staged and working diff against the intended changes before committing. Stage explicit intended code paths only. For staged scope, include the original reviewed staged set and its fixes; no foreign work or report. Read [commit format](../../references/commit-format.md) and commit `fix(<scope>): address review findings`, with the scope its MESSAGE rules give. Record the actual commit OID. Do not create an empty commit if the worker made no correction; record dropped findings or stop if it did not resolve them.
5. Continue to RE-CHECK only if a finding actually fixed in this pass was critical or major. Minors-only fixes finish with `re-check: none`.

## RE-CHECK

After each applicable commit, launch fresh `dev:review-quality` and `dev:review-implementation` agents, concurrently when capacity permits. Use the reviewer packet from agent launch with `review_phase: recheck`, critical and major only. Wait for both before proceeding.

Rebuild both commands from the validated, immutable Scope base and the latest fix commit: `git log <base>..<tip> --oneline` and `git diff --no-ext-diff --no-textconv <base>..<tip>`. Append `-- <path>` to both for a path selector. Staged also uses this range, never the now-empty index. Add the accumulated finding history to the packet.

Tell both: "Check prior conclusions against the current code. The history is context, not a ban on reporting the same problem again: report it when new evidence challenges a dismissal or shows a fix is incomplete, and cite that evidence."

Verify proposals yourself using VERIFY AGAIN, deduplicate by location and problem, and record dismissals. Retain earlier conclusions if new evidence reopens a fixed or dropped finding; add the new conclusion to its history. No confirmed findings means `re-check: clean`. Otherwise repeat FIX for verified findings after re-check one or two. Three re-checks maximum: findings confirmed in the third get `result: unresolved` and `re-check: unresolved`; no fourth fix or re-check. Do not call that branch ready.

## ARTIFACT

Update the same input report, normally `.scratch/<feature-slug>/review.md` or `.scratch/reviews/<branch-slug>/review.md`; never create a second report. Preserve Scope, Requirements, `mode:` and `sweep:` as the original sweep facts. Keep earlier dismissals and follow-ups with their origin, marking carried follow-ups `not re-verified`. Store accumulated history beside the findings and worker decisions/deviations with finding and reason; omit empty fields.

After the last commit and re-check, write final results and `fix: done`, the actual `fixed at:` OID and `re-check: none | clean | unresolved`. Each handled finding gets `result: fixed | dropped - <reason> | unresolved`, with verification evidence. The report is never part of a fix commit; say when a tracked report remains as its own dirty file. Carry `quick` forward and say its sweep was quick, never a full review gate.

On red tests/lint after a reasonable attempt, blocked/partial worker or soft interruption, write `fix: stopped - <reason>`, preserve actual results and unresolved work, include `fixed at:` if a commit exists and `re-check: incomplete` if a re-check was interrupted. A hard kill leaves `fix: in-progress`. Both are unfinished and require `/dev:review`. Pre-edit gate failures leave the report untouched; the successful no-op changes only result lines.

## STOP CONDITIONS

Stop and tell the user on any gate above, a fix beyond the branch's scope, tests/linter staying red, a needed destructive operation, migration or dependency install, or unconfirmed foreign work. Out-of-scope findings go to Follow-ups, never the code diff. An auth, payment, crypto or migration diff needs manual security review beyond this pass; say so and stop before editing. Preserve worker decisions/deviations even on a stop.

## NEXT

Report what was found, fixed, dropped and left unresolved, with reasons and verification. A clean re-check means ready within the recorded review mode; remaining unresolved findings or follow-ups prevent a readiness claim. Push and MR/PR creation require the user's explicit request.
