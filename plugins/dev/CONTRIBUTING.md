# CONTRIBUTING (DEV)

Follow the [shared rules](../../CONTRIBUTING.md). This guide covers authoring; the linked instructions own execution behavior.

## STRUCTURE

- `skills/<command>/SKILL.md`: four commands, with local `assets/`, `references/` or `scripts/` when needed.
- `agents/`: three review finder roles and one verifier, each with complete instructions.
- `references/`: rules shared by several commands, read at the point of use. See CONTRACT OWNERS.
- `opencode/install.py`: the OpenCode 2 installer. It copies this version and generates the subagents and `/plan` at install time; nothing generated is committed.

Keep process rules with their owning command or role; a rule two commands apply goes to one reference instead of two copies. Keep personal preferences in client/project instructions. Do not add background skills, cross-skill injection or plugin hooks. Add a command only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing command.

## TERMINOLOGY

| Distinction | Meaning |
| --- | --- |
| command / skill / agent | User-facing `/dev:<name>` (`@<name>` in OpenCode) / its `SKILL.md` implementation / a spawned reviewer. |
| feature / ticket | One `.scratch/<feature-slug>/` directory / one deliverable in `issues/NN-<slug>.md`. |
| acceptance criterion | Required outcome of a ticket, a `- [ ]` line. Completed criteria remain requirements. |

## AUTHORING

**Skills**

- The directory names the command; the manifest supplies `dev`. Omit frontmatter `name` to retain Claude Code's namespace. Use `description` for trigger, result and command boundaries; `argument-hint` is optional.
- Keep `rnd`, `bug` and `review` explicit-only: `disable-model-invocation: true` for Claude Code and OpenCode and `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. Discussion, quotations and handoffs never invoke them.
- `commit` alone also accepts natural-language commit requests.
- Include an `Example:` invocation after the intro. Resolve supporting files relative to the installed skill and require them at the point of use. Follow the shared [instruction contracts](../../CONTRIBUTING.md#instruction-contracts).

**Agents**

- Frontmatter requires `name` matching the filename, a role/caller `description` and the exact permitted `tools`. Each tool needs an OpenCode permission action in the installer.
- Keep each role's scope, prohibitions and output self-contained. Native hosts load it; generic adapters pass the complete role and task packet without inherited conversation.
- End reviewers with `## WHAT TO REPORT`. Reviewers read the specified diff themselves and return findings; the orchestrator writes the report.

## CONTRACT OWNERS

| Contract | Owners |
| --- | --- |
| Feature and investigation outputs | [rnd](skills/rnd/SKILL.md), [bug](skills/bug/SKILL.md) |
| Feature location, storage, tracker input, external specs, domain documents | [feature directory](references/feature-directory.md), read by rnd and bug |
| Ticket template, numbering, fields, `Branch` and `Done when` | [ticket](references/ticket.md), read by rnd, bug and review; [template](skills/rnd/assets/ticket.md) |
| Review sweep, summary and proposed tickets | [review](skills/review/SKILL.md) |
| Review report format, validation and currency | [review report](references/review-report.md), read by review |
| Severity and finding verification | [findings](references/findings.md), read by review and passed to the [verifier](agents/review-verify.md) |
| Standalone commits | [commit](skills/commit/SKILL.md) |
| Commit message and Git rules | [commit format](references/commit-format.md), read by commit |
| Agent launch and context packets | [agent launch](references/agent-launch.md), read by review |
| OpenCode install layout, generated subagents and `/plan` | [installer](opencode/install.py) |

Preserve artifact headings, status values, paths, writer ownership and prompt markers. Only the user sets `wontfix`, except the executor under the first criterion of a ticket from review. Keep scope, Git checks, tracker selection and stop rules with their owners; do not copy their schemas or procedures here.

## VERSIONED SURFACE

Versioned interfaces include command names, arguments and invocation policy; role names, OpenCode agent IDs and command names, launch routes and context packets; artifact paths, formats and handoffs; write/Git boundaries. Editorial changes preserve those interfaces. Apply the shared [version rules](../../CONTRIBUTING.md#versions).

## CLIENT CHECKS

Run shared checks for every change. For invocation or launch changes, run the [client scenarios](tests/client-scenarios.md) in temporary projects and installations.

`python3 .github/scripts/test_dev_invocation.py` checks Codex request assembly through a local stub; it requires Codex CLI and permission to bind localhost. `python3 .github/scripts/test_dev_opencode.py` checks the OpenCode installer's generated files and config edits against temporary directories with a stub `opencode`. Behavioral checks grade tool actions, artifacts and Git state separately from installation and discovery. Record context isolation, native or generic execution and permission enforcement separately too; installation success or desktop support does not prove CLI support. Keep raw results outside the public package; report only what was verified.
