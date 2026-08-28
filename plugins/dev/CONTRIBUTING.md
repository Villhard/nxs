# CONTRIBUTING (dev)

How to author a skill or an agent for the `dev` plugin. The rules here govern this plugin only - the other plugins in this marketplace have their own. Repository-wide rules (house style, public safety, how a plugin is added) live in the root `CONTRIBUTING.md`.

## PLUGIN LAYOUT

```
plugins/dev/
  .claude-plugin/
    plugin.json          # name: dev (the namespace of every command)
  skills/
    <name>/SKILL.md      # command skill -> /dev:<name>
  agents/
    <agent-name>.md      # self-contained subagent
  README.md CONTRIBUTING.md CHANGELOG.md
```

The global `~/.claude/CLAUDE.md` and `settings.json` stay out of this repo - you write those yourself.

## TWO TIERS

- Global `~/.claude/CLAUDE.md`: always on, applies to every response. Lives outside the plugin.
- Command skills `/dev:<name>`: the workflow, visible in the `/` menu. There are six: `rnd`, `bug`, `plan`, `exec`, `review`, `commit`.

There is no third tier. A rule lives in exactly one file - the command that uses it, or the agent that uses it. No background skills, no `reference/` directories, no cross-skill injection.

Nothing sits alongside the tiers. The plugin ships no hook and injects nothing into a session it was not invoked in.

## UBIQUITOUS LANGUAGE

One term, one meaning, everywhere in this plugin. A word in this table is never used in another sense, and never replaced by a synonym.

| term | means | never call it |
| --- | --- | --- |
| command | a `/dev:<name>` entry point the user invokes. There are six | a skill, in user-facing text |
| skill | the `skills/<name>/SKILL.md` file implementing a command. An authoring word | a command, in CONTRIBUTING |
| agent | a subagent a command spawns: `worker` and the five `review-*` | a skill |
| feature | one directory `.scratch/<feature-slug>/`: a feature document and the tickets cut from it | a project, an epic, a story |
| ticket | one whole unit of work: one file `.scratch/<feature-slug>/issues/NN-<slug>.md` | a story, a folder, a work item |
| artifact | one durable markdown file a command writes, or the pair of sections `/dev:plan` appends to a ticket | a commit, a report, a follow-up |
| spec | the feature document `/dev:rnd` writes, `spec.md` | a brief |
| root cause | the feature document `/dev:bug` writes, `root-cause.md` | a root-cause brief, a brief, a diagnosis |
| plan | the `## Conventions` and `## Implementation` sections `/dev:plan` appends to a ticket | a plan file, `plan.md` |
| task | one `### Task N:` block under a ticket's `## Implementation` | a step, the user's incoming work |
| task checkbox | one `- [ ]` / `- [x]` line inside a task: a unit of work `exec` executes | a criterion, an item |
| acceptance criterion | one `- [ ]` / `- [x]` line above `## Implementation`: what the ticket delivers | a task, a step |
| status | the ticket's `**Status:**` line, one of the seven values | a label, a state field |
| request | what the user arrives with: a description, an idea, a question, a ticket | a task |
| tracker key | the key or URL of an external ticket | a tracker identifier |
| sweep | the first review pass: five agents over the diff as it arrived | a round, a first round |
| re-check | the narrowed pass after fixes land: two agents, critical and major only | a second round, a retry |
| fix mode | a `/dev:review` run carrying the `fix` argument, the only run that writes | a fix phase, auto-fix |

Three collisions this table exists to prevent: `task` used to mean both the incoming work and a numbered block under `## Implementation`; `brief` used to mean both feature documents that feed `/dev:plan`, which is why neither is called one now; and `- [ ]`, which is an acceptance criterion above `## Implementation` and a task checkbox inside a `### Task N:` section - one token, opposite meanings, separated by position and by nothing else. Every term this plugin uses in that load-bearing way has a row here. Add one the moment you notice it missing; whether the skill or the row landed first does not matter.

## PLACEMENT RULE

Where a rule, policy, or term belongs:

- always on (language, style, safety) -> global `CLAUDE.md`, outside the plugin;
- one command needs it -> inline in that skill's `SKILL.md`;
- one agent needs it -> inline in that agent's file;
- two commands need it -> write it twice.

That last one is deliberate. The plugin used to carry four background skills and six `reference/` files, and one change meant editing four places to keep them consistent. A few duplicated lines cost less than another layer of indirection. If duplication ever gets genuinely painful, the fix is a narrower contract between the two commands, not a shared file.

Security-critical content (never commit secrets, confirm destructive operations) lives in the global tier, which always fires. A skill can state workflow detail around it - that a push needs an explicit request - but never carries the protection itself.

## THE HANDOFF CONTRACTS

Work is handed on through four named, minimal contracts. Nothing beyond what a contract names crosses between them.

**`rnd` -> `plan`** - the ticket header block and two spec headings. `plan` reads the ticket's `**What to build:**` line and its acceptance criteria, plus `## Implementation Decisions` and `## Testing Decisions` from `spec.md`; the rest it reads as text.

**`bug` -> `plan`** - the headings of `root-cause.md`. `plan` reads `## Root cause` and `## Fix direction`; the rest it reads as text. When a feature directory holds both documents, the fix comes from `root-cause.md` and the build conventions from `spec.md`, and a contradiction between them is a question rather than a merge.

**`plan` -> `exec`** - two structural tokens and one optional section, all inside the ticket:

- `### Task N: <title>` - the task heading, never written above `## Implementation`;
- `- [ ]` / `- [x]` - the checkboxes. Inside a `### Task N:` section it is a task checkbox; above `## Implementation` it is an acceptance criterion. `exec` finds work only in the first kind;
- `## Conventions` - optional, at h2 so the token survives verbatim. `exec` passes it to every worker, and a worker inherits nothing else, so a rule missing from it does not reach the code.

**the ticket -> `exec`** - the fourth contract, and the only one shared with another toolchain: the `**Status:**` line, the `**Blocked by:**` line, and the acceptance criteria. `exec` is the only writer of all three after the ticket is created, and a blocker counts as satisfied only when the file it names carries `resolved`.

`exec` takes one ticket per run and, inside it, the first task section with open checkboxes; it reads the rest as text.

Keep all four that narrow. Any new required section is a new coupling between two files that are otherwise independent, and a heading a reader depends on can no longer be renamed without a version bump.

## WHEN TO ADD SOMETHING NEW

This plugin stays small on purpose: six commands, six agents, nothing else. Add a command only when all of these hold at once:

- the intent is distinct and does not reduce to an existing command, not even through a mode word;
- the intent is frequent - you reach for it several times a month, not once a quarter;
- it earns its own autocomplete slot in the `/` menu;
- the idea has settled and is no longer experimental.

Miss even one and it is not a command. It is an upgrade to an existing skill or an inline rule.

Things that bloat the plugin and get rejected: copying an external skill wholesale, one new command per imported recipe, abstract guidance with no concrete failure mode behind it, and side edits made while you happened to be in the file.

## AUTHORING PLAYBOOK

- The command name is the skill DIRECTORY name. `skills/plan/` -> `/dev:plan`.
- The `dev` namespace comes from the `name` field in `plugin.json`. Invocation is always namespaced; there is no bare alias.
- Leave the frontmatter `name` field out of bundled skills. It is a display label, and setting it hides the namespace prefix in the `/` menu; without it the menu shows `dev:<dir>`.
- Write the body of `SKILL.md` in compact English. The global tier decides what language the user reads in the chat.
- The body loads on invocation and stays for the whole session, so write standing instructions, not one-off steps.
- A skill that grows past roughly 120 lines is doing more than one job. Split the job, do not add a reference file.
- `skills/rnd/SKILL.md` is the file nearest that ceiling. 0.20.0 put slicing on top of shaping, so it now clarifies, explores, stresses, writes the spec, and cuts the tickets, and it is the next split candidate. Before splitting, run the four tests in WHEN TO ADD SOMETHING NEW against a `/dev:tickets` command: distinct intent already passes, frequency and settledness are the two that failed in 0.20.0.
- Validate as you go, from the repository root: `claude plugin validate --strict plugins/dev`

### COMMAND SKILL FRONTMATTER

```yaml
---
description: <one line; when-to-use trigger + short what-it-produces, not the process>
argument-hint: "[...]"
disable-model-invocation: true
---
```

Keep `description` to the trigger plus a short clause on what the skill produces. Do not list phases or explain how the body works: a description that retells the workflow makes the model follow the retelling and skip the body, which is where the actual procedure lives. Every command skill also carries one `Example:` line with a real invocation right after the intro.

`disable-model-invocation: true` is the default for a workflow command, and it takes the command out of the model's skill listing - it runs only when the user types `/dev:<name>`. Leave the flag off only when the intent is one a user expresses without naming a command; `commit` is the sole case, and a second one needs an argument here first.

### AGENT FRONTMATTER

```yaml
---
name: <agent file name, without .md - this is what a skill spawns as dev:<name>>
description: <the role in one line, plus which command uses it>
tools: <the exact tool list this agent may use>
---
```

Unlike a skill, an agent DOES carry `name` - a skill spawns it by that name, so it is part of the contract.

An agent is self-contained: it states its own subject, its own bounds, and its own output format, and it never refers to a file the orchestrator has to inject. Every reviewer ends with a `## WHAT TO REPORT` block, and every one of them fetches the diff itself instead of receiving it in the prompt.

## ARTIFACT PATHS

Everything a command writes goes under `.scratch/<feature-slug>/` in the current repository, which is the local-markdown layout of the issue tracker the wider toolchain uses. Two files and one appended pair of sections:

| command | artifact | file |
| --- | --- | --- |
| `rnd` | spec, plus one ticket per slice | `.scratch/<feature-slug>/spec.md`, `.scratch/<feature-slug>/issues/NN-<slug>.md` |
| `bug` | root cause | `.scratch/<feature-slug>/root-cause.md` |
| `plan` | plan | `## Conventions` and `## Implementation`, appended to `.scratch/<feature-slug>/issues/NN-<slug>.md` |

Each of those three skills states its own path in its `## ARTIFACT` section, and that is the only place the path lives. The table above is a map, not a second source. README carries the human-facing overview.

`review` and `commit` write no artifact. `exec` writes none either, but it is the exception this rule now has to name: it MUTATES a ticket another command wrote - the `**Status:**` line, the task checkboxes, the acceptance criteria, and one `## Comments` line on a stop. Creating a file and updating the state of one are different acts, and only the first earns an `## ARTIFACT` section. None of the three carries one, and none should grow one.

`rnd` and `plan` resolve the tracker layout before their first write into a NEW feature directory: `docs/agents/issue-tracker.md` in the repository, then the global default at the same relative path, then local markdown. Local markdown is what the wider toolchain falls back to as well, so the fallback is copied rather than chosen. In a repository configured for GitHub or GitLab neither command picks silently. Neither ever writes that config file or runs a setup skill, and this plugin ships no `gh` or `glab` dependency.

Never create files outside those templates silently, and never write into a `.scratch/<x>/` that holds a `map.md` - that directory belongs to another skill's effort.

The pre-0.20.0 story directory is gone, and no command reads or writes it. Nothing is renamed, moved, or converted either: turning an old plan into a ticket means inventing acceptance criteria it wrote as prose, so an unfinished one is finished by hand or dropped. Moving a finished story to a `completed/` directory was the user's action and has no successor - `**Status:** resolved`, written by `exec`, is what it stood for.

## DEV LOOP

Install caches a SNAPSHOT of the plugin rather than reading the repo live:

```
# once - connect the local dev marketplace
claude plugin marketplace add ~/dev/nxs
claude plugin install dev@nxs

# after every edit
claude plugin marketplace update nxs   # then reinstall the plugin
```

An edited skill only becomes invocable after the session restarts.

## VERSIONING

Every edit to bundled content - skills, agents, manifests - bumps the `version` field in `plugin.json` and adds an entry to `CHANGELOG.md` (Keep a Changelog, newest section on top). The size of the diff does not decide which part of the version moves. Whether the CONTRACT changed does.

### WHAT THE CONTRACT IS

What a user or another plugin file depends on:

1. command names `/dev:<name>`, their arguments and modes;
2. agent names, since skills spawn them by name;
3. artifact paths and naming schemes (`.scratch/<feature-slug>/issues/NN-<slug>.md`);
4. the four handoff contracts: the ticket's `**What to build:**` line and the headings of `spec.md` and `root-cause.md` that `plan` reads, the two ticket tokens `exec` depends on - `### Task N:` and `- [ ]` with its positional meaning - the `## Conventions` heading `exec` passes on to every worker, and the `**Status:**` line, the `**Blocked by:**` line and the acceptance criteria that `exec` writes;
5. the gates that govern git and files: when a commit is allowed, what counts as a stop condition, what a skill writes to disk.

Everything else is internal: wording inside `SKILL.md`, agent criteria and focus areas, README and CONTRIBUTING.

### MAJOR / MINOR / PATCH

- **PATCH** - the contract is untouched. Rewritten wording, a sharpened agent criterion, documentation fixes.
- **MINOR** - the contract changed. A command added, removed, or renamed; its arguments changed; an agent renamed; the path scheme changed; a handoff contract or a gate changed. Renaming a heading a downstream command reads counts here, however small the diff.
- **MAJOR** - `0.x` is initial development per semver: the public contract is not stabilized and can change in any minor. `1.0.0` ships together with the decision to declare the contract stable, and from that point a breaking change costs a major bump. Until then major stays put, however large the diff.

When in doubt: if you type tomorrow what you typed yesterday, do you get the same thing in the same place? Yes, but the output reads differently -> patch. No -> minor.
