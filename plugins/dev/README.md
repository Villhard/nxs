# dev

Choose where to start:

- An idea that needs shaping: `rnd`, which writes a spec and tickets.
- A bug to investigate: `bug`, which writes a fix ticket once the cause is confirmed.
- A clear task: describe it to `/plan` directly; no ticket is needed.
- An approved spec: `rnd <spec-path>`, which reuses it and splits the tickets.

A ticket runs in the client's own plan mode:

```text
/plan <ticket-path> -> git add -> review -> commit
```

`/plan` is the built-in command of Claude Code and Codex, not part of `dev`. OpenCode has no built-in `/plan`: the dev installer adds one that switches to the Plan agent, which only plans; switch to Build (Shift+Tab) to execute. The ticket's `Done when` section tells the executor when to stop, to run the full test suite and linter, to check the criteria and set `resolved`, and not to commit. A `Branch:` line names the branch the work goes on; edit or remove it before running.

Optional companion: in Claude Code, the [revdiff-planning](https://github.com/umputun/revdiff) plugin opens each `/plan` plan in revdiff. An annotation sends the plan back for revision, the next round shows the change against the previous plan, and a clean review keeps the normal plan approval. Verified with revdiff-planning 0.3.10 in agterm. In Codex it does not detect Plan mode yet: plans run unreviewed, with the normal approval. In OpenCode, revdiff's own OpenCode integration opens each Plan agent response in revdiff; verified that it opens in agterm.

`review` runs three finder roles, then a separate verifier that marks each candidate confirmed, plausible or refuted; a plausible finding is kept, marked `(plausible)` with what would confirm it, and its ticket reproduces it first. It explains its findings and ends with recommended tickets as groups of finding numbers: each critical or major finding on its own unless a named reason joins them, minor findings together or with the major one that touches the same place. Answer with finding numbers, such as "1, 3", "all", "7 separately", "1 and 3 together" or "none"; selected findings follow their recommended groups unless the answer says otherwise, and review creates only those tickets for `/plan`. Commit with `commit` or by hand after review. Run review after each ticket on the staged changes, or once at the end of the feature on the branch.

Start each step explicitly; commands do not start the next step for you. Mentioning or quoting a command does not invoke it.

[Install dev@nxs](../../README.md#install). In Claude Code 2.1.275 or later, one command also works:

```text
/plugin install dev --marketplace Villhard/nxs
```

## Commands

| Command | When to use it | Result |
| --- | --- | --- |
| [rnd](skills/rnd/SKILL.md) | Shape a feature or open question | Agreed spec and tickets. |
| [bug](skills/bug/SKILL.md) | Investigate a failure | Confirmed cause, or missing evidence to investigate next. |
| [review](skills/review/SKILL.md) | Check staged changes, or the branch | Saved findings and the tickets you pick; code and Git state unchanged. |
| [commit](skills/commit/SKILL.md) | Commit existing changes | Atomic commits from existing changes. |

`commit` also accepts a direct request such as "commit this". Push and PR creation require a separate request.

## Example

For an existing greeting CLI, add an uppercase option without new dependencies.

In Claude Code, the task is clear, so start plan mode with it:

```text
/plan Add --uppercase to the greeting CLI, using its existing tests and no new dependencies.
```

Approve the plan and let it run. Stage the changes with `git add`, then run:

```text
/dev:review
```

If review finds issues, pick the proposed tickets to create and run `/plan <ticket-path>` on each. Commit with `/dev:commit`.

In Codex, use `/plan` the same way. Select the `dev` skill with `/skills` or the `$` picker in CLI/IDE, or request it directly: "Use the review skill from dev on the staged changes." Verified in Codex: installation and skill selection. The ticket handoff to `/plan` and the reviewer launch in `review` are not verified in Codex yet.

In OpenCode, [install dev](../../README.md#install) with its installer and use the `/dev/<name>` commands, such as `/dev/review`. Reviewers run as `dev/review-*` subagents limited to read, grep, glob and shell, which can still write, as Bash can for the native roles. Verified in OpenCode 2.1.2: installation, `/dev/<name>` invocation, the reviewer launch in `review`, and the ticket handoff to `/plan` and Build.

## Shaping routes

NXS provides the complete local route without another shaping package or tracker setup. Each arrow below is a user-selected handoff:

```text
Idea -> rnd [spec + tickets] -> /plan <ticket-path>
Bug -> bug [root cause + fix ticket] -> /plan <ticket-path>
Clear request -> /plan <request>
Approved spec -> rnd <spec-path> [reuse + slice] -> /plan <ticket-path>
```

`/dev:rnd docs/approved-spec.md` reuses settled decisions and slices them into tickets, even when there is only one. A compatible local ticket from another shaping workflow, such as `grill-me -> to-spec -> to-tickets`, can go straight to `/plan`. Do not run an external slicer over tickets that already have history: NXS preserves that work when re-slicing, an external tool may not.

NXS saves everything under `.scratch/`, reads tracker issues without writing to them, and needs no tracker setup. The rules live in [feature directory](references/feature-directory.md), [ticket](references/ticket.md) and [rnd](skills/rnd/SKILL.md).

## Options

| Option | Effect |
| --- | --- |
| `review` | Review the staged changes; with nothing staged, the committed branch changes against the default branch. On the default branch with nothing staged, it stops. |
| `review <ticket-path>` | The same review, with that ticket or feature as the requirements. |

Use these arguments with `/dev:` in Claude Code, with the selected Codex skill or with `/dev/` in OpenCode. A ticket or feature path supplies review requirements, not a code filter. Unstaged edits are never reviewed.

## Working files

Working files live under `.scratch/<feature-slug>/`, or `.scratch/<KEY>-<slug>/` for a tracker key:

- `spec.md`: feature definition.
- `root-cause.md`: bug investigation.
- `issues/NN-<slug>.md`: ticket with its `Done when` rules.
- `research/<topic>.json` or `.md`, `research/<topic>/`: saved research results and the scripts and raw data behind them.
- `review.md`: findings and the tickets proposed for them.

Reviews without a matching feature use `.scratch/reviews/<branch-slug>/review.md`, and their tickets go to `issues/` beside it. Without a path argument, review matches the resolved tickets whose `Branch:` line names the current branch, in feature directories and under `.scratch/reviews/`. A finding that an open ticket already covers links to that ticket instead of being proposed again. Ignore `.scratch/` in Git to keep these records local.

A `resolved` ticket means implementation is verified; review is still a separate step.

[Update](../../README.md#update) | [Contribute](CONTRIBUTING.md)
