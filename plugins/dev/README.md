# dev

Seven commands for development work. [Install and configure](../../README.md#install) `dev@nxs`; read the [client compatibility limits](../../README.md#compatibility).

## Start

In Claude Code, run each command when ready for the next step:

```text
/dev:rnd add rate limiting to the public API
/dev:plan
/dev:exec
/dev:review
/dev:fix
```

In Codex, select the corresponding `dev` skill with `/skills` or the `$` picker in CLI/IDE, or name it:

```text
Use the plan skill from the dev plugin for .scratch/rate-limiting/issues/01-rate-limit.md.
```

Use the same selection method for every command below. For a bug, start with `bug`, then `plan`. A clear request can start with `plan`. Review the plan before execution; commands stop at their handoff instead of starting the next command automatically.

## Commands

| Command | Result |
| --- | --- |
| [rnd](skills/rnd/SKILL.md) | A spec and tickets from a feature request or open question. |
| [bug](skills/bug/SKILL.md) | A confirmed root cause before proposing a fix. |
| [plan](skills/plan/SKILL.md) | Sequenced tasks and checkboxes inside one ticket. |
| [exec](skills/exec/SKILL.md) | One unblocked ticket implemented and verified, with a commit per completed task. |
| [review](skills/review/SKILL.md) | A saved review report; no code, index, or commit changes. |
| [fix](skills/fix/SKILL.md) | Reverified findings applied, code committed, and report updated separately. |
| [commit](skills/commit/SKILL.md) | Existing changes split into atomic commits; use outside `exec`. |

In Claude Code, six commands require explicit invocation. `commit` also activates on requests such as "commit this".

## Modes

**Execution without commits**

```text
/dev:exec .scratch/rate-limiting/issues/01-rate-limit.md no commits
```

Codex: "Use the exec skill from dev for that ticket, no commits."

This writes code and ticket progress. The recorded mode survives a new session. With commits enabled, the orchestrator commits completed tasks; workers never commit. Push and PR creation require an explicit request.

**Review scope**

```text
/dev:review
/dev:review staged
/dev:review src/api
/dev:review quick
```

The default reviews the committed branch; `staged` selects the index, and a repository-relative path narrows the branch diff. A ticket or feature path supplies requirements, not a code selector. To review another PR, check out its branch first. In Codex, pass the same selectors when requesting `review`.

A normal sweep uses five reviewers, or a direct pass for a trivial diff. `quick` uses two reviewers with broader duties and is not a full review gate. Run `fix` separately; critical or major fixes get a two-agent re-check.

A stale or unfinished report requires another review. Already-applied reports and findings all dropped during verification produce no commit. Fix commits exclude the report, even when tracked. See [report validation](skills/fix/SKILL.md#check-the-report) and [git checks](skills/fix/SKILL.md#preflight).

## Working files and resume

Files live under `.scratch/<feature-slug>/`, or `.scratch/<KEY>-<slug>/` with a tracker key.

| File | Written by |
| --- | --- |
| `spec.md`, `issues/NN-<slug>.md` | `rnd`: spec and tickets |
| `root-cause.md` | `bug`: investigation |
| `issues/NN-<slug>.md` | `plan`: plan sections; `exec`: status, checkboxes, execution notes |
| `review.md` | `review`: findings; `fix`: outcomes |

Without a matching feature, reports go to `.scratch/reviews/<branch-slug>/review.md`. `commit` writes no artifact. Ignore `.scratch/` in git to keep working records local; `exec` then commits code alone. Do not rerun an external slicer over planned tickets: it can overwrite their plans.

After a pause, invoke `exec` again with the same ticket, using your client's method above. It reads the saved stopping point, keeps `no commits`, and finishes interrupted validation, commits, or ticket closure before selecting more work. Completed commits are not repeated. Uncertain or foreign changes stop recovery. `resolved` means verified implementation, not completed review. See [resume rules](skills/exec/SKILL.md#resume).

For shared tracker configuration, use `docs/agents/issue-tracker.md` in the project. The current `rnd` and `plan` global fallback uses the Claude configuration directory; Codex `AGENTS.md` does not redirect it. The plugin writes local Markdown, requires no `gh`/`glab`, and asks before doing so in GitHub/GitLab-configured projects.

[Update](../../README.md#update) · [Local preview](../../CONTRIBUTING.md#local-development-and-release) · [Authoring](CONTRIBUTING.md)
