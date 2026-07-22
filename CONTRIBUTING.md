# CONTRIBUTING (nxs)

How to author a skill or an agent for the `nxs` plugin.

## REPO LAYOUT

```
nxs/
  .claude-plugin/
    plugin.json          # name: nxs (the namespace of every command)
    marketplace.json     # local dev marketplace (source "./")
  skills/
    <name>/              # tier 2, command skill -> /nxs:<name>
      SKILL.md
      reference/         # optional, on-demand detail
    <background-name>/   # tier 3, user-invocable: false
  agents/
    <agent-name>.md      # self-contained subagent
  examples/              # filled sample artifacts (plan, brief)
  .github/               # CI, house-style linter, PR template
  README.md CONTRIBUTING.md CHANGELOG.md LICENSE
```

Tier 1 (global `~/.claude/CLAUDE.md`) and `settings.json` stay out of this repo - you write those yourself.

## THREE TIERS

- Tier 1 - global `~/.claude/CLAUDE.md`: always on, applies to every response. Lives outside the plugin.
- Tier 2 - command skills `/nxs:<name>`: the workflow, visible in the `/` menu. There are six: `rnd`, `bug`, `plan`, `plancheck`, `exec`, `review`.
- Tier 3 - background skills (`user-invocable: false`): shared rules, loaded by relevance. There are five: `plan-conventions`, `review-protocol`, `verify`, `commit-conventions`, `intake`.

## NAMING

- A command is `/nxs:<name>` - flat, no flow prefix.
- The command name is the skill DIRECTORY name. `skills/plan/` -> `/nxs:plan`.
- The `nxs` namespace comes from the `name` field in `plugin.json`. Invocation is always namespaced; there is no bare alias.
- Background skills get a role name (`commit-conventions`, `plan-conventions`) because command skills call for them by name. Renaming one means updating every file that references it, so pick the name once and leave it alone.

## PLACEMENT RULE

Where a rule, policy, or term belongs:

- always on (language, style, safety) -> tier 1, outside the plugin;
- one command needs it -> inline in that skill's `SKILL.md` or its `reference/`;
- several commands need it -> a tier 3 background skill;
- several agents share it -> one single-source file that the orchestrator reads once and injects verbatim into every agent prompt;
- exactly one agent needs it -> inline in that agent's file.

Security-critical content (never commit secrets, confirm destructive) never lives on tier 3 ALONE. Auto-load is heuristic and can miss; tier 1 always fires, so tier 1 has to carry the protection. Tier 3 may still state the workflow gate around it - when a commit is allowed, that a push needs an explicit request - because that is workflow detail, and it is worthless as the only line of defence.

## WHEN TO ADD SOMETHING NEW

This repo stays small on purpose: six commands, five background skills, six agents. Add a tier-2 command skill only when all of these hold at once:

- the intent is distinct and does not reduce to an existing command, not even through a mode word;
- the intent is frequent - you reach for it several times a month, not once a quarter;
- it earns its own autocomplete slot in the `/` menu;
- the idea has settled and is no longer experimental.

Miss even one and it is not a command. It is an upgrade to an existing skill, a background skill, or an inline rule.

Things that bloat the repo and get rejected: copying an external skill wholesale, one new command per imported recipe, abstract guidance with no concrete failure mode behind it, and side edits made while you happened to be in the file.

## AUTHORING PLAYBOOK

- The command name is the skill DIRECTORY name.
- Leave the frontmatter `name` field out of bundled skills. It is a display label, and setting it hides the namespace prefix in the `/` menu; without it the menu shows `nxs:<dir>`.
- Write the body of `SKILL.md` in compact English. Tier 1 decides what language the user reads in the chat.
- The body loads on invocation and stays for the whole session, so write standing instructions, not one-off steps.
- Put heavy detail in `reference/*.md`, which loads only when `SKILL.md` points at it.
- Validate as you go: `claude plugin validate --strict .`

### COMMAND SKILL FRONTMATTER

```yaml
---
description: <one line, drives model-invocation; when-to-use trigger + short what-it-produces, not the process>
argument-hint: "[...]"
---
```

Keep `description` to the trigger plus a short clause on what the skill produces. Do not list phases or explain how the body works: a description that retells the workflow makes the model follow the retelling and skip the body, which is where the actual procedure lives. Every command skill also carries one `Example:` line with a real invocation right after the intro.

### BACKGROUND SKILL FRONTMATTER

```yaml
---
description: <what these rules are> - load before/when <trigger>. Background knowledge, not a user command.
user-invocable: false
---
```

### AGENT FRONTMATTER

```yaml
---
name: <agent file name, without .md - this is what a skill spawns as nxs:<name>>
description: <the role in one line, plus which command uses it>
tools: Read, Grep, Glob
---
```

Unlike a skill, an agent DOES carry `name` - a skill spawns it by that name, so it is part of the contract. `tools` is the read-only enforcement: every reviewer is limited to `Read, Grep, Glob`, and only `worker` gets write and Bash.

## ARTIFACT PATHS

Each skill that writes an artifact states its own path in its `## ARTIFACT` section, and that is the only place the path lives. There is deliberately no shared table here - the old one duplicated those lines and drifted out of sync with them. README carries the human-facing overview.

Everything a skill writes goes under `docs/nxs/` in the current repository. Never create files outside those templates silently.

### PUBLIC SAFETY

Anything durable can end up in a public repository. Before committing, strip local paths like `/Users/<name>`, private git remotes, real tracker keys and URLs, secrets, tokens, `.env` values, colleague names and emails, and raw session or tool output. Swap in neutral placeholders: `<user_home>`, `<github_owner>/<repo>`, `PROJ-123`.

## DEV LOOP

Install caches a SNAPSHOT of the plugin rather than reading the repo live:

```
# once - connect the local dev marketplace
claude plugin marketplace add ~/nxs
claude plugin install nxs@nxs

# after every edit
claude plugin marketplace update nxs   # then reinstall the plugin
```

An edited skill only becomes invocable after the session restarts.

## VERSIONING

Every edit to bundled content - skills, agents, manifests - bumps the `version` field in `plugin.json` and adds an entry to `CHANGELOG.md` (Keep a Changelog, newest section on top). The size of the diff does not decide which part of the version moves. Whether the CONTRACT changed does.

### WHAT THE CONTRACT IS

What a user or another plugin file depends on:

1. command names `/nxs:<name>`, their arguments and modes;
2. the names of background skills and agents, since other skills call for them by name;
3. artifact paths and naming schemes (`docs/nxs/plans/YYYYMMDD-<slug>.md`);
4. artifact sections another skill reads: `## SOURCE ARTIFACTS`, `## ACCEPTANCE CRITERIA`, `## DEVELOPMENT APPROACH`, `## CONVENTIONS`, and `- [ ]` checkboxes;
5. the gates that govern git and files: when a commit is allowed, what counts as a stop condition, what a skill writes to disk.

Everything else is internal: wording inside `SKILL.md`, lens criteria and focus areas, how `reference/` files are split, README and CONTRIBUTING.

### MAJOR / MINOR / PATCH

- **PATCH** - the contract is untouched. Rewritten wording, a sharpened lens criterion, `reference/` files rearranged without changing behavior, documentation fixes.
- **MINOR** - the contract changed. A command added, removed, or renamed; its arguments changed; a skill or agent renamed; the path scheme changed; a required artifact section or a gate changed.
- **MAJOR** - `0.x` is initial development per semver: the public contract is not stabilized and can change in any minor. `1.0.0` ships together with the decision to declare the contract stable, and from that point a breaking change costs a major bump. Until then major stays put, however large the diff.

When in doubt: if you type tomorrow what you typed yesterday, do you get the same thing in the same place? Yes, but the output reads differently -> patch. No -> minor.
