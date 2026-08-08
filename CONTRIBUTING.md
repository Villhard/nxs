# CONTRIBUTING (nxs)

How to author a skill or an agent for the `nxs` plugin.

## REPO LAYOUT

```
nxs/
  .claude-plugin/
    plugin.json          # name: nxs (the namespace of every command)
    marketplace.json     # local dev marketplace (source "./")
  skills/
    <name>/SKILL.md      # command skill -> /nxs:<name>
  agents/
    <agent-name>.md      # self-contained subagent
  hooks/                 # SessionStart hook -> injects using-nxs (not a skill)
    hooks.json
    session-start.sh
    using-nxs.md
  .github/               # CI, house-style linter, PR template
  README.md CONTRIBUTING.md CHANGELOG.md LICENSE
```

The global `~/.claude/CLAUDE.md` and `settings.json` stay out of this repo - you write those yourself.

## TWO TIERS

- Global `~/.claude/CLAUDE.md`: always on, applies to every response. Lives outside the plugin.
- Command skills `/nxs:<name>`: the workflow, visible in the `/` menu. There are six: `rnd`, `bug`, `plan`, `exec`, `review`, `commit`.

There is no third tier. A rule lives in exactly one file - the command that uses it, or the agent that uses it. No background skills, no `reference/` directories, no cross-skill injection.

Alongside the tiers, a SessionStart hook (`hooks/`) injects the `using-nxs` discipline so a session checks for the right command before acting. It is infrastructure, not a skill - it lives in `hooks/`, not `skills/`.

## UBIQUITOUS LANGUAGE

One term, one meaning, everywhere in the repo. A word in this table is never used in another sense, and never replaced by a synonym.

| term | means | never call it |
| --- | --- | --- |
| command | a `/nxs:<name>` entry point the user invokes. There are six | a skill, in user-facing text |
| skill | the `skills/<name>/SKILL.md` file implementing a command. An authoring word | a command, in CONTRIBUTING |
| agent | a subagent a command spawns: `worker` and the five `review-*` | a skill |
| story | one whole unit of work: one directory `docs/nxs/stories/YYYYMMDD-<slug>/` | a folder, a work item |
| artifact | one durable markdown file a command writes into a story. There are exactly three | a commit, a report, a follow-up |
| brief | the artifact `/nxs:rnd` writes, `brief.md` | - |
| root cause | the artifact `/nxs:bug` writes, `root-cause.md` | a root-cause brief, a brief, a diagnosis |
| plan | the artifact `/nxs:plan` writes, `plan.md` | - |
| task | one `### Task N:` block inside a plan | a step, the user's incoming work |
| checkbox | one `- [ ]` / `- [x]` line inside a task | a step, an item |
| request | what the user arrives with: a description, an idea, a question, a ticket | a task |
| tracker key | the key or URL of an external ticket | a tracker identifier |

Two collisions this table exists to prevent: `task` used to mean both the incoming work and a numbered block in a plan, and `brief` used to mean both artifacts that feed `/nxs:plan`. A new term is added here before it appears in a skill, an agent, or the README.

## PLACEMENT RULE

Where a rule, policy, or term belongs:

- always on (language, style, safety) -> global `CLAUDE.md`, outside the plugin;
- one command needs it -> inline in that skill's `SKILL.md`;
- one agent needs it -> inline in that agent's file;
- two commands need it -> write it twice.

That last one is deliberate. The plugin used to carry four background skills and six `reference/` files, and one change meant editing four places to keep them consistent. A few duplicated lines cost less than another layer of indirection. If duplication ever gets genuinely painful, the fix is a narrower contract between the two commands, not a shared file.

Security-critical content (never commit secrets, confirm destructive operations) lives in the global tier, which always fires. A skill can state workflow detail around it - that a push needs an explicit request - but never carries the protection itself.

## THE HANDOFF CONTRACTS

Three commands hand work to the next one, and each handoff is a named, minimal contract. Nothing else crosses between them.

**`rnd` -> `plan`** - the headings of `brief.md`. `plan` reads `## Acceptance criteria` and `## Chosen approach`; the rest of the brief it reads as text.

**`bug` -> `plan`** - the headings of `root-cause.md`. `plan` reads `## Root cause` and `## Fix direction`; the rest it reads as text.

**`plan` -> `exec`** - two structural tokens:

- `### Task N: <title>` - the task heading;
- `- [ ]` / `- [x]` - the checkboxes.

`exec` takes the first task section with open checkboxes and reads the rest as text.

Keep all three that narrow. Any new required section is a new coupling between two files that are otherwise independent, and a heading a reader depends on can no longer be renamed without a version bump.

## WHEN TO ADD SOMETHING NEW

This repo stays small on purpose: six commands, six agents, one hook. Add a command only when all of these hold at once:

- the intent is distinct and does not reduce to an existing command, not even through a mode word;
- the intent is frequent - you reach for it several times a month, not once a quarter;
- it earns its own autocomplete slot in the `/` menu;
- the idea has settled and is no longer experimental.

Miss even one and it is not a command. It is an upgrade to an existing skill or an inline rule.

Things that bloat the repo and get rejected: copying an external skill wholesale, one new command per imported recipe, abstract guidance with no concrete failure mode behind it, and side edits made while you happened to be in the file.

## AUTHORING PLAYBOOK

- The command name is the skill DIRECTORY name. `skills/plan/` -> `/nxs:plan`.
- The `nxs` namespace comes from the `name` field in `plugin.json`. Invocation is always namespaced; there is no bare alias.
- Leave the frontmatter `name` field out of bundled skills. It is a display label, and setting it hides the namespace prefix in the `/` menu; without it the menu shows `nxs:<dir>`.
- Write the body of `SKILL.md` in compact English. The global tier decides what language the user reads in the chat.
- The body loads on invocation and stays for the whole session, so write standing instructions, not one-off steps.
- A skill that grows past roughly 120 lines is doing more than one job. Split the job, do not add a reference file.
- Validate as you go: `claude plugin validate --strict .`

### COMMAND SKILL FRONTMATTER

```yaml
---
description: <one line, drives model-invocation; when-to-use trigger + short what-it-produces, not the process>
argument-hint: "[...]"
---
```

Keep `description` to the trigger plus a short clause on what the skill produces. Do not list phases or explain how the body works: a description that retells the workflow makes the model follow the retelling and skip the body, which is where the actual procedure lives. Every command skill also carries one `Example:` line with a real invocation right after the intro.

### AGENT FRONTMATTER

```yaml
---
name: <agent file name, without .md - this is what a skill spawns as nxs:<name>>
description: <the role in one line, plus which command uses it>
tools: <the exact tool list this agent may use>
---
```

Unlike a skill, an agent DOES carry `name` - a skill spawns it by that name, so it is part of the contract.

An agent is self-contained: it states its own subject, its own bounds, and its own output format, and it never refers to a file the orchestrator has to inject. Every reviewer ends with a `## WHAT TO REPORT` block, and every one of them fetches the diff itself instead of receiving it in the prompt.

## ARTIFACT PATHS

There are three artifacts, one per command that writes one:

| command | artifact | file |
| --- | --- | --- |
| `rnd` | brief | `docs/nxs/stories/YYYYMMDD-<slug>/brief.md` |
| `bug` | root cause | `docs/nxs/stories/YYYYMMDD-<slug>/root-cause.md` |
| `plan` | plan | `docs/nxs/stories/YYYYMMDD-<slug>/plan.md` |

Each of those three skills states its own path in its `## ARTIFACT` section, and that is the only place the path lives. The table above is a map, not a second source. README carries the human-facing overview.

`exec`, `review`, and `commit` write no artifact. They leave commits, flipped checkboxes, and a spoken report, none of which is a file this plugin owns - so none of them carries an `## ARTIFACT` section, and none should grow one.

Everything a skill writes goes under `docs/nxs/` in the current repository. Never create files outside those templates silently.

Moving a finished story to `docs/nxs/stories/completed/` is the user's action, not a command's. No skill performs it or asks about it. `exec` skips `completed/` when it resolves the latest story, which is a resolution rule and nothing more.

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
2. agent names, since skills spawn them by name;
3. artifact paths and naming schemes (`docs/nxs/stories/YYYYMMDD-<slug>/plan.md`);
4. the three handoff contracts: the headings of `brief.md` and `root-cause.md` that `plan` reads, and the two plan tokens `exec` depends on, `### Task N:` and `- [ ]`;
5. the gates that govern git and files: when a commit is allowed, what counts as a stop condition, what a skill writes to disk.

Everything else is internal: wording inside `SKILL.md`, agent criteria and focus areas, README and CONTRIBUTING.

### MAJOR / MINOR / PATCH

- **PATCH** - the contract is untouched. Rewritten wording, a sharpened agent criterion, documentation fixes.
- **MINOR** - the contract changed. A command added, removed, or renamed; its arguments changed; an agent renamed; the path scheme changed; a handoff contract or a gate changed. Renaming a heading a downstream command reads counts here, however small the diff.
- **MAJOR** - `0.x` is initial development per semver: the public contract is not stabilized and can change in any minor. `1.0.0` ships together with the decision to declare the contract stable, and from that point a breaking change costs a major bump. Until then major stays put, however large the diff.

When in doubt: if you type tomorrow what you typed yesterday, do you get the same thing in the same place? Yes, but the output reads differently -> patch. No -> minor.
