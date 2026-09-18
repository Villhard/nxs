# dev

Choose where to start:

- An idea that needs shaping: `rnd`, then `plan`.
- A bug to investigate: `bug`, then `plan` once the cause is confirmed.
- A clear task: `plan`, which can create a ticket directly.

```text
plan -> exec -> review -> fix (if there are findings)
```

Read the plan before execution. Start each step explicitly; commands do not start the next step for you. Mentioning or quoting a command does not invoke it.

[Install dev@nxs](../../README.md#install).

## Commands

| Command | When to use it | Result |
| --- | --- | --- |
| [rnd](skills/rnd/SKILL.md) | Shape a feature or open question | Agreed spec and tickets. |
| [bug](skills/bug/SKILL.md) | Investigate a failure | Confirmed cause, or missing evidence to investigate next. |
| [plan](skills/plan/SKILL.md) | Prepare one clear task or ticket | Implementation steps inside the ticket. |
| [exec](skills/exec/SKILL.md) | Implement or resume a planned ticket | Verified changes, committed per completed task by default. |
| [review](skills/review/SKILL.md) | Check changes | Saved findings; code and Git state unchanged. |
| [fix](skills/fix/SKILL.md) | Apply a current review report | Verified fixes committed and outcomes recorded. |
| [commit](skills/commit/SKILL.md) | Commit changes made outside `exec` and `fix` | Atomic commits from existing changes. |

`commit` also accepts a direct request such as "commit this". `exec` and `fix` handle their own commits. Push and PR creation require a separate request.

## Example

For an existing greeting CLI, add an uppercase option without new dependencies.

In Claude Code, start with:

```text
/dev:plan Add --uppercase to the greeting CLI, using its existing tests and no new dependencies.
```

Read the saved plan. Replace `<ticket-path>` with the returned path, then run these commands one at a time:

```text
/dev:exec <ticket-path>
/dev:review <ticket-path>
```

If review finds issues, run `/dev:fix <report-path>` with the returned report path.

In Codex, select the corresponding `dev` skill with `/skills` or the `$` picker in CLI/IDE, or request it directly: "Use the plan skill from dev to add --uppercase to the greeting CLI, using its existing tests and no new dependencies." Use the same method for `exec`, `review` and `fix`, passing the saved path.

## Options

| Option | Effect |
| --- | --- |
| `exec <ticket-path> no commits` | Change code and save progress without creating commits. Git inspection still runs. |
| `review` | Review the committed branch changes. |
| `review staged` | Review changes staged for commit. |
| `review src/api` | Review committed branch changes under that code path. |
| `review quick` | Run a narrower review; this does not replace a full review. |

Use these arguments with `/dev:` in Claude Code or with the selected Codex skill. A ticket or feature path supplies review requirements, not a code filter. `no commits` does not change review scope: unstaged edits are not included by either branch or staged review.

If a report is stale or unfinished, run `review` again before `fix`.

## Working files and resume

Working files live under `.scratch/<feature-slug>/`, or `.scratch/<KEY>-<slug>/` for a tracker key:

- `spec.md`: feature definition.
- `root-cause.md`: bug investigation.
- `issues/NN-<slug>.md`: ticket, plan and execution progress.
- `review.md`: findings and fix outcomes.

Reviews without a matching feature use `.scratch/reviews/<branch-slug>/review.md`. Ignore `.scratch/` in Git to keep these records local.

After a pause, invoke `exec` with the same ticket. It reads saved progress and retains `no commits` when selected. A `resolved` ticket means implementation is verified; review is still a separate step.

[Update](../../README.md#update) | [Contribute](CONTRIBUTING.md)
