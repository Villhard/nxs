---
description: Plan a ticket - decompose a spec, a root cause, or a request into sequenced tasks with checkboxes written into the ticket file. Use before executing non-trivial work, after a brainstorm or an investigation.
argument-hint: "[request | ticket path | feature dir | tracker key]"
disable-model-invocation: true
---

# /dev:plan

Turn a ticket into an implementation plan and stop. The plan is written into the ticket itself, as `## Conventions` and `## Implementation`, and `/dev:exec` executes it from there.

Accepted input: a ticket path under `.scratch/<feature-slug>/issues/`, a feature directory `.scratch/<feature-slug>/`, a request in words, or a tracker key / URL / pasted ticket. With no input, take the frontier ticket of the feature in play.

A tracker key or URL is read before anything else - through the tracker when it is reachable, otherwise ask the user to paste the ticket. Never infer its content from the key.

Example: /dev:plan .scratch/rate-limiting/issues/02-per-key-quota.md

## STANCE

- Write the plan into the ticket and stop. Implementation code, the build, and any behavior change belong to `/dev:exec`.
- The plan is a proposal, read-only until the user approves it.
- A small single-step request needs no plan - say so and offer a direct edit instead of ceremony. Never route it to `/dev:exec`, which stops on a ticket without `## Implementation`.

## TRACKER CONFIG

Before the first write into a feature directory that does not exist yet, read the layout: `docs/agents/issue-tracker.md` in this repo, failing that the same relative path under the user's Claude config directory, failing both local markdown - the fallback `/wayfinder` itself uses. Every variant of that file opens with `# Issue tracker: <GitHub|GitLab|Local Markdown>`, so it is one line to read and no parser.

Local Markdown, or no such file anywhere: write under `.scratch/` without asking. GitHub or GitLab: never pick silently and never invent tracker calls. Name the tracker, say in one sentence that writing under `.scratch/` here leaves the shaping in local files while the issues live on that tracker, then let the user pick - write locally anyway and own the split, or stop and drive the tracker with `/to-spec` and `/to-tickets` and come back with the ticket path. Ask once; the answer holds for the session. Never write `docs/agents/issue-tracker.md` yourself and never run a setup skill; that file belongs to another toolchain.

## PROCEDURE

1. **Read the ticket.** Its `**What to build:**` line and the `- [ ]` acceptance criteria above `## Implementation` are the requirements. With no ticket named, resolve the feature first: the directory the argument names, else the single `.scratch/<slug>/` that holds an `issues/` directory and no `map.md` - several of those, list them and ask; none, say so and stop. Then take its frontier ticket: `**Status:** ready-for-agent`, no `## Implementation` yet, every number on its `**Blocked by:**` line at `**Status:** resolved`, lowest first. Say which ticket you took.
2. **Read the feature document.** `## Implementation Decisions` and `## Testing Decisions` from `spec.md`, or `## Root cause` and `## Fix direction` from `root-cause.md`. Read the rest of the document for applicable agreements too, including exclusions in `## Out of Scope` and answers or rejection reasons in `## Further Notes` when present. Those carry the decisions already made - the plan implements them rather than reopening them. Do not ask an answered question again unless new evidence contradicts the answer; then show that evidence. A directory holding both takes the fix from `root-cause.md` and the build conventions from `spec.md`; a contradiction between the two is a question, not a call you make.
3. **Read the code.** Inspect the files, patterns, and dependencies the work touches - directly or through the built-in Explore agent. Do not over-read. Clarify a fuzzy domain term before encoding it into the plan. Carry applicable decisions, constraints and their reasons from the feature document and this session into the plan: shared ones in `## Conventions`, task-specific ones in that task's text. Include the code references needed to act on them. Preserve exclusions and reasons for rejecting alternatives when they constrain the work; omit unrelated history. Collect the surrounding code patterns every task follows in `## Conventions` too.
4. **Close the open questions.** Ask one at a time, 2-4 concrete options with a recommendation. For several viable approaches, lay out the trade-offs and ask once.
5. **Decompose.** As many tasks as the work has working units, no floor and no target. Each is one working unit: the code plus the tests for it, leaving the project green. Sequence by dependency - a task never calls what a later task creates. Every task earns its place; cut the rest. No task exists only to run the suite or the linter - `/dev:exec` runs both once itself at the close.
6. **Append `## Conventions` and `## Implementation`** to the ticket using the template below - before `## Comments` when that heading exists, at the end of the file otherwise.
7. **Run the self-check** before handing the plan over.

With no ticket named and a `root-cause.md` that no existing ticket references, or with no `issues/` directory at all, open a new ticket first: `issues/<NN>-<slug>.md`, `NN` one past the highest number present and `01` when `issues/` is empty or absent. Five fields in this order: the heading `# <NN>: <title>`, `**What to build:**` as the end-to-end behavior in the user's terms, `**Blocked by:** None (can start immediately)`, `**Status:** ready-for-agent`, then the acceptance criteria as `- [ ]` lines. Then plan into it. Work too large for one unit of work goes back to `/dev:rnd`, which is where slicing lives.

An open decision that would change the plan is marked in the ticket rather than guessed:

```
[NEEDS CLARIFICATION: <specific question>]
```

Mark only when the answer changes the decision, and set the ticket to `**Status:** needs-info` while one is open. Before handing over, `rg NEEDS CLARIFICATION` over the ticket and the feature document, and read the ticket's `## Comments`. One rule decides the status, for this ticket and for every other `needs-info` ticket in the feature that the same answer touched: no marker in the ticket, none in `spec.md`, and no open question under its `## Comments` - `**Status:** ready-for-agent`; anything else - `needs-info`, naming what is still open. A ticket with a local reason keeps `needs-info` however the spec changed. `/dev:exec` refuses to start while a marker is open.

This command writes `needs-info` and `ready-for-agent`, here and when it opens a ticket. The execution transitions - `claimed`, `ready-for-human`, `needs-info` on a stop, `resolved` - belong to `/dev:exec`, and this command never writes them.

## TEMPLATE

````markdown
## Conventions

<rules every task follows - style, naming, a repeated step, a standing preference. /dev:exec passes this
section to every worker, so what is missing here does not reach the code. Do not copy in what the project's
CLAUDE.md already says: exec passes the project rules separately, and a duplicate only inflates every worker
prompt. No such rules, no section.>

## Implementation

### Task 1: A visitor registers with an email and lands in the database

**Files:**
- Create: migrations/0007_users.sql
- Create: src/auth/hash.go
- Modify: src/users/service.go
- Modify: src/api/routes.go

- [ ] add the users migration with a unique index on email
- [ ] add HashPassword in src/auth/hash.go (bcrypt, configurable cost)
- [ ] add service.Register: normalize, hash, persist, ErrEmailTaken on a duplicate
- [ ] wire POST /api/users to the service and map errors to 201 / 409 / 422
- [ ] write tests: fresh email stores a hash and never the plaintext, duplicate gives 409, malformed gives 422
- [ ] run `go test ./users/... ./api/...`
````

Rules the template does not show:

- `### Task N:` and `- [ ]` are structural - `/dev:exec` finds the work by them, so keep both exactly as written, in English, whatever language the plan body uses.
- Position decides what a checkbox means. Above `## Implementation` a `- [ ]` line is an acceptance criterion, written when the ticket was created and flipped once by `/dev:exec` after the last task is green; inside a `### Task N:` section it is a unit of work. Never put a task heading above `## Implementation`, and never put a checkbox between `## Implementation` and `### Task 1:`.
- Tests are their own checkbox, never bundled into the implementation step.
- The last checkbox of a task names the concrete command this project runs for that task's tests, not a bare "run tests" and not the whole suite - the whole suite and the linter run once, in `/dev:exec`, at the close.
- A config-only or declarative task has no tests to write; verification is that the change takes effect.
- `Files:` lists what the task is expected to touch. It bounds the task, it is not a contract - reaching one file further to finish the same capability is fine.

## SELF-CHECK

Before handing the plan over, verify it against the repository and fix what fails. State the result in one line.

- `rg "### Task" <ticket>` returned nothing before the append, and after it no `- [` line sits between `## Implementation` and `### Task 1:`;
- the ticket's `**Blocked by:**` line names only lower numbers - a ticket blocked by a higher one is an authored cycle;
- every `Modify:` path exists, every `Create:` path does not;
- everything the plan leans on - a function it calls, an interface it implements, a seam it assumes - exists in the shape it expects;
- a task with code changes has a checkbox for its tests;
- dependencies run forward: no task calls what a later task creates;
- every acceptance criterion above `## Implementation`, and every requirement from the spec or the root cause, is covered by a task or explicitly deferred - read the other tasks for it under different words first;
- a worker given only its task, the acceptance criteria it serves, and `## Conventions` has every applicable decision, constraint and reason; none depends on reading the conversation or the full feature document;
- nothing the requirements never asked for: no abstraction with one consumer, no future-proofing, no fallback for a case that cannot happen;
- `rg "NEEDS CLARIFICATION" <ticket>` returns nothing.

## ARTIFACT

The plan is not a file of its own. It is two sections inside one ticket, and one ticket is one whole unit of work:

```
.scratch/<feature-slug>/issues/NN-<slug>.md   ->   ## Conventions, ## Implementation
```

`<feature-slug>` is two to four lowercase english words from the request, hyphenated; a tracker key names the directory instead - `.scratch/<KEY>-<slug>/` - so the feature stays navigable by the key. `NN` is the ticket number, from `01`, in dependency order. Never write into a `.scratch/<x>/` that holds a `map.md`: that directory is a `/wayfinder` effort. Pick another slug and say why in one line.

A ticket that already holds an `## Implementation` section is never overwritten silently - say what is there and ask whether to replace it. A ticket at `**Status:** claimed` or `**Status:** resolved` is never re-planned without asking either: its task checkboxes are execution history.

## NEXT

Plan written -> `/dev:exec` to implement it, then `/dev:review` for the review gate and `/dev:fix` to apply the saved findings.
