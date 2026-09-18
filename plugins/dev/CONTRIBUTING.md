# CONTRIBUTING (DEV)

Follow the [shared rules](../../CONTRIBUTING.md). This guide covers authoring; the linked instructions own execution behavior.

## STRUCTURE

- `skills/<command>/SKILL.md`: seven commands, with local `assets/`, `references/` or `scripts/` when needed.
- `agents/`: one worker and five review roles, each with complete instructions.
- [Agent launch](references/agent-launch.md): shared launch and context delivery, read by exec, review and fix when needed.

Keep process rules with their owning command or role, and personal preferences in client/project instructions. Do not add background skills, cross-skill injection or plugin hooks. Add a command only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing command.

## TERMINOLOGY

| Distinction | Meaning |
| --- | --- |
| command / skill / agent | User-facing `/dev:<name>` / its `SKILL.md` implementation / a spawned worker or reviewer. |
| feature / ticket / task | One `.scratch/<feature-slug>/` directory / one deliverable in `issues/NN-<slug>.md` / one implementation step inside that ticket. |
| acceptance criterion / task checkbox | Required outcome / work needed to implement it. Completed criteria remain requirements. |

## AUTHORING

**Skills**

- The directory names the command; the manifest supplies `dev`. Omit frontmatter `name` to retain Claude Code's namespace. Use `description` for trigger, result and command boundaries; `argument-hint` is optional.
- Keep `rnd`, `bug`, `plan`, `exec`, `review` and `fix` explicit-only: `disable-model-invocation: true` for Claude Code and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. Discussion, quotations and handoffs never invoke them.
- `commit` alone also accepts natural-language commit requests. Internal exec/fix commits follow their owning contracts.
- Include an `Example:` invocation after the intro. Resolve supporting files relative to the installed skill and require them at the point of use. Follow the shared [instruction contracts](../../CONTRIBUTING.md#instruction-contracts).

**Agents**

- Frontmatter requires `name` matching the filename, a role/caller `description` and the exact permitted `tools`.
- Keep each role's scope, prohibitions and output self-contained. Native hosts load it; generic adapters pass the complete role and task packet without inherited conversation.
- End reviewers with `## WHAT TO REPORT`. Reviewers read the specified diff themselves and return findings; the orchestrator writes the report.

## CONTRACT OWNERS

| Contract | Owners |
| --- | --- |
| Feature and investigation outputs | [rnd](skills/rnd/SKILL.md), [bug](skills/bug/SKILL.md) |
| Ticket and implementation plan | [plan](skills/plan/SKILL.md), [templates](skills/plan/assets/implementation.md) |
| Task execution and recovery | [exec](skills/exec/SKILL.md), [worker](agents/worker.md) |
| Review report and fix outcomes | [review](skills/review/SKILL.md), [fix](skills/fix/SKILL.md) |
| Standalone commits | [commit](skills/commit/SKILL.md) |
| Agent launch and context | [Launch reference](references/agent-launch.md) |

Preserve artifact headings, status values, paths, writer ownership and prompt markers, including `review_mode: quick` and `review_phase: recheck`. Only the user sets `wontfix`. Keep scope, Git checks, tracker selection and stop rules with their owners; do not copy their schemas or procedures here.

## VERSIONED SURFACE

Versioned interfaces include command names, arguments and invocation policy; role names, launch routes and context packets; artifact paths, formats and handoffs; execution recovery and write/Git boundaries. Editorial changes preserve those interfaces. Apply the shared [version rules](../../CONTRIBUTING.md#versions).

## CLIENT CHECKS

Run shared checks for every change. For invocation or launch changes, run the [client scenarios](tests/client-scenarios.md) in temporary projects and installations.

`python3 .github/scripts/test_dev_invocation.py` checks Codex request assembly through a local stub; it requires Codex CLI and permission to bind localhost. Behavioral checks grade tool actions, artifacts and Git state separately from installation and discovery. Keep raw results outside the public package; report only what was verified.
