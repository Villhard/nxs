# dev

Choose where to start:

- An idea that needs shaping: `rnd`, which writes a spec and tickets.
- A bug to investigate: `bug`, which writes a fix ticket once the cause is confirmed.
- A clear task: `plan`, which can create a ticket directly.
- An approved spec: `plan` for one implementation unit, or `rnd` to reuse it and split several tickets.

A ticket from `rnd` or `bug` runs in the client's own plan mode:

```text
/plan <ticket-path> -> git add -> review -> commit
```

`/plan` is the built-in command of Claude Code and Codex, not part of `dev`. The ticket's `Done when` section tells the executor when to stop, to run the full test suite and linter, to check the criteria and set `resolved`, and not to commit. A `Branch:` line names the branch the work goes on; edit or remove it before running.

`review` explains its findings and ends with proposed tickets, similar findings already combined. Answer in text, such as "T1, T3", "T2 and T4 together" or "none"; it creates only those tickets, each ready for `/plan`. Commit with `commit` or by hand after review. Run review after each ticket on the staged changes, or once at the end of the feature on the branch.

The previous route still works for any ticket:

```text
plan -> exec -> review
```

Read the plan before execution: `plan <ticket-path>` saves it without a separate approval step, so this read is the check. Start each step explicitly; commands do not start the next step for you. Mentioning or quoting a command does not invoke it.

[Install dev@nxs](../../README.md#install).

## Commands

| Command | When to use it | Result |
| --- | --- | --- |
| [rnd](skills/rnd/SKILL.md) | Shape a feature or open question | Agreed spec and tickets. |
| [bug](skills/bug/SKILL.md) | Investigate a failure | Confirmed cause, or missing evidence to investigate next. |
| [plan](skills/plan/SKILL.md) | Prepare one clear task or ticket | Implementation steps inside the ticket. |
| [exec](skills/exec/SKILL.md) | Implement or resume a planned ticket | Verified changes, committed per completed task by default. |
| [review](skills/review/SKILL.md) | Check staged changes, or the branch | Saved findings and the tickets you pick; code and Git state unchanged. |
| [commit](skills/commit/SKILL.md) | Commit changes made outside `exec` | Atomic commits from existing changes. |

`commit` also accepts a direct request such as "commit this". `exec` handles its own commits. Push and PR creation require a separate request.

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

If review finds issues, pick the proposed tickets to create and run `/plan` on each.

In Codex, select the corresponding `dev` skill with `/skills` or the `$` picker in CLI/IDE, or request it directly: "Use the plan skill from dev to add --uppercase to the greeting CLI, using its existing tests and no new dependencies." Use the same method for `exec` and `review`, passing the saved path.

## Shaping routes

NXS provides the complete local route without another shaping package or tracker setup. Each arrow below is a user-selected handoff:

```text
Idea -> rnd [spec + tickets] -> /plan <ticket-path>
Bug -> bug [root cause + fix ticket] -> /plan <ticket-path>
Clear request -> plan [ticket + tasks] -> exec <ticket-path>
Approved spec -> rnd <spec-path> [reuse + slice] -> /plan <ticket-path>
```

Any ticket can also go through `plan <ticket-path>` and `exec <ticket-path>` instead of `/plan`.

For one implementation unit, `/dev:plan docs/approved-spec.md` creates the ticket and plan directly; for several, `/dev:rnd docs/approved-spec.md` reuses settled decisions and slices them. A compatible local ticket from another shaping workflow, such as `grill-me -> to-spec -> to-tickets`, can go straight to `plan`. Do not run an external slicer over tickets that already have plans or execution history: NXS preserves that work when re-slicing, an external tool may not.

NXS saves everything under `.scratch/`, reads tracker issues without writing to them, and needs no tracker setup. The rules live in [feature directory](references/feature-directory.md), [ticket](references/ticket.md), [rnd](skills/rnd/SKILL.md) and [plan](skills/plan/SKILL.md).

## Options

| Option | Effect |
| --- | --- |
| `exec <ticket-path> no commits` | Change code and save progress without creating commits. Git inspection still runs. |
| `review` | Review the staged changes; with nothing staged, the committed branch changes against the default branch. On the default branch with nothing staged, it stops. |
| `review <ticket-path>` | The same review, with that ticket or feature as the requirements. |

Use these arguments with `/dev:` in Claude Code or with the selected Codex skill. A ticket or feature path supplies review requirements, not a code filter. `no commits` does not change review scope: unstaged edits are never reviewed. Branch review compares against the default branch, so `exec` asks once before committing a new ticket there: continue, or create a branch.

## Working files and resume

Working files live under `.scratch/<feature-slug>/`, or `.scratch/<KEY>-<slug>/` for a tracker key:

- `spec.md`: feature definition.
- `root-cause.md`: bug investigation.
- `issues/NN-<slug>.md`: ticket with its `Done when` rules, plus plan and execution progress under `exec`.
- `research/<topic>.json` or `.md`, `research/<topic>/`: saved research results and the scripts and raw data behind them.
- `checks/NN-<slug>/`: local checks of one ticket outside the project test suite.
- `review.md`: findings and the tickets proposed for them.

Reviews without a matching feature use `.scratch/reviews/<branch-slug>/review.md`, and their tickets go to `issues/` beside it. Without a path argument, review matches the resolved tickets whose `Branch:` line names the current branch. Ignore `.scratch/` in Git to keep these records local.

After a pause, invoke `exec` with the same ticket. It reads saved progress and retains `no commits` when selected. A `resolved` ticket means implementation is verified; review is still a separate step.

[Update](../../README.md#update) | [Contribute](CONTRIBUTING.md)
