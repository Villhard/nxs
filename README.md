# nxs

Development skills for coding agents: shape features and bugs into tickets for the client's plan mode, review changes with three finder roles and a verifier, and commit in atomic groups.

## Skills

| Skill | Use it to |
| --- | --- |
| [dev-rnd](skills/dev-rnd/SKILL.md) | Shape a feature or open question into an agreed spec and tickets. |
| [dev-bug](skills/dev-bug/SKILL.md) | Investigate a reported failure; write a fix ticket once the cause is confirmed. |
| [dev-review](skills/dev-review/SKILL.md) | Review staged changes, or the branch; create only the tickets you pick. |
| [dev-spec](skills/dev-spec/SKILL.md) | Record durable project specs from landed work. |
| [dev-commit](skills/dev-commit/SKILL.md) | Commit existing changes in atomic groups. |

`dev-rnd`, `dev-bug`, `dev-review` and `dev-spec` run only on explicit invocation; `dev-commit` also accepts a direct request such as "commit this". Start each step explicitly; commands do not start the next step for you.

## Install

Install with the [skills CLI](https://skills.sh) and pick your agents at the prompt:

```bash
npx skills@latest add -g Villhard/nxs
```

The CLI installs one copy per skill into the shared agents skills directory (`~/.agents/skills`) and links it into each selected agent; agents that read that directory natively need no link. For a project-level install, drop `-g`. To install from a local checkout, pass its path instead of the repository.

## Update

```bash
npx skills@latest update -g
```

Start a new session after updating.

## Workflow

A ticket runs in the client's own plan mode. Each arrow is a user-selected handoff:

```text
Idea -> dev-rnd [spec + tickets] -> /plan <ticket-path>
Bug -> dev-bug [root cause + fix ticket] -> /plan <ticket-path>
Clear request -> /plan <request>
Approved spec -> dev-rnd <spec-path> [reuse + slice] -> /plan <ticket-path>
Landed work -> dev-spec [project specs] -> dev-commit
```

Run `dev-spec` after review and before commit. It writes `SPEC.md` files that the other commands read, or private `.SPEC.md` files kept out of Git where a project does not allow committed specs.

`dev-review` runs the three finder roles concurrently, then a verifier that marks each candidate finding confirmed, plausible or refuted. It saves the report under `.scratch/`, explains the findings and proposes tickets as groups of finding numbers; answer with finding numbers, such as "1, 3", "all" or "none", and it creates only those tickets.

Everything is saved locally under `.scratch/<feature-slug>/` (spec, root cause, tickets, research, review reports); tracker issues are read, never written. Ignore `.scratch/` in Git to keep these records local.

## Migration from the dev plugin

Releases up to 0.43.0 shipped as the `dev` plugin for Claude Code, Codex and OpenCode. To migrate, uninstall the plugin and install the skills:

```bash
claude plugin uninstall dev@nxs && claude plugin marketplace remove nxs
codex plugin remove dev@nxs && codex plugin marketplace remove nxs
python3 nxs/plugins/dev/opencode/install.py --uninstall  # from a 0.43.0 checkout
npx skills@latest add -g Villhard/nxs
```

Command names change: `/dev:rnd` becomes `/dev-rnd`, and likewise for bug, review and commit.

For local previews and contributions, see [CONTRIBUTING.md](CONTRIBUTING.md).
