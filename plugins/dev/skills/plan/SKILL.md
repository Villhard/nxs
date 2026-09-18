---
description: Plan one ticket from a request, spec, or confirmed root cause when explicitly asked to use /dev:plan. Save sequenced tasks in the ticket; do not implement them. Use /dev:rnd to split a larger request into tickets.
argument-hint: "[request | ticket path | feature dir | tracker key]"
disable-model-invocation: true
---

# /dev:plan

Turn a ticket into an implementation plan and stop. The plan is written into the ticket itself, as `## Conventions` and `## Implementation`, and `/dev:exec` executes it from there.

Accepted input: a ticket path under `.scratch/<feature-slug>/issues/`, a feature directory or its `root-cause.md`, a request in words, or a tracker key / URL / pasted ticket. With no input, resolve the feature and its frontier under PROCEDURE.

A tracker key or URL is read before anything else - through the tracker when it is reachable, otherwise ask the user to paste the ticket. Never infer its content from the key.

Example: /dev:plan .scratch/rate-limiting/issues/02-per-key-quota.md

Run only when the user selects this command or directly asks to use it. Discussion, quotations, handoffs and mentions are not invocation. Suggest the next command at a handoff; never start it automatically.

## STANCE

- Write the plan into the ticket and stop. Implementation code, the build, and any behavior change belong to `/dev:exec`.
- Inspect and draft the proposal before writing. Show the concrete plan and obtain approval to save it unless the user has already authorized that plan or explicitly asked you to write it. Reuse that authorization; do not ask again. Permission to save a plan does not invoke exec.
- A small single-step request needs no plan - say so and offer a direct edit instead of ceremony. Never route it to `/dev:exec`, which stops on a ticket without `## Implementation`.

## TRACKER CONFIG

Before the first write into a feature directory that does not exist yet, read the layout: `docs/agents/issue-tracker.md` in this repo, failing that the same relative path under the user's Claude config directory, failing both local markdown - the fallback `/wayfinder` itself uses. Every variant of that file opens with `# Issue tracker: <GitHub|GitLab|Local Markdown>`, so it is one line to read and no parser.

Local Markdown, or no such file anywhere: write under `.scratch/` without asking. GitHub or GitLab: never pick silently and never invent tracker calls. Name the tracker, say in one sentence that writing under `.scratch/` here leaves the shaping in local files while the issues live on that tracker, then let the user pick - write locally anyway and own the split, or stop and drive the tracker with `/to-spec` and `/to-tickets` and come back with the ticket path. Ask once; the answer holds for the session. Never write `docs/agents/issue-tracker.md` yourself and never run a setup skill; that file belongs to another toolchain.

## PROCEDURE

1. **Resolve the input** using the table below, before requiring an existing ticket. Read an existing ticket's `**What to build:**` and every acceptance criterion above `## Implementation`, whether `- [ ]` or `- [x]`. A checked criterion remains a requirement. Say which ticket will be planned or created.
2. **Read the feature document when present.** Read `## Implementation Decisions` and `## Testing Decisions` from `spec.md`, or `## Root cause`, `## Evidence` and `## Fix direction` from `root-cause.md`. Also read applicable exclusions, answers and rejected alternatives in the rest of the document. Preserve these decisions unless new evidence contradicts them; show that evidence before reopening a question. With both documents, take the fix from root cause and conventions from spec; ask about a contradiction. With neither, use the explicit request and inspected code.

   A root cause described as unconfirmed, conditional or unsupported by its recorded evidence blocks an executable fix plan. Name the missing evidence and return to `/dev:bug`; do not create tasks that assume the hypothesis is true. An older document without a clear conclusion gets the same evidence check, not an automatic rewrite.
3. **Read the code.** Inspect the files, patterns, and dependencies the work touches - directly or through the built-in Explore agent. Do not over-read. Clarify a fuzzy domain term before encoding it into the plan. Carry applicable decisions, constraints and their reasons from the feature document and this session into the plan: shared ones in `## Conventions`, task-specific ones in that task's text. Include the code references needed to act on them. Preserve exclusions and reasons for rejecting alternatives when they constrain the work; omit unrelated history. Collect the surrounding code patterns every task follows in `## Conventions` too.
4. **Close the open questions.** Ask one at a time, 2-4 concrete options with a recommendation. For several viable approaches, lay out the trade-offs and ask once.
5. **Decompose.** As many tasks as the work has working units, no floor and no target. Each is one working unit: the code plus the tests for it, leaving the project green. Sequence by dependency - a task never calls what a later task creates. Every task earns its place; cut the rest. No task exists only to run the suite or the linter - `/dev:exec` runs both once itself at the close.
6. **Read [assets/implementation.md](assets/implementation.md)** relative to this installed skill directory before writing. Append `## Conventions` and `## Implementation` to the ticket using that template and the rules below - before `## Comments` when that heading exists, at the end of the file otherwise.
7. **Run the self-check** before handing the plan over.

Input resolution, in priority order:

| Input | Action |
| --- | --- |
| Explicit ticket path | Read that ticket. A missing explicit file is an error; do not silently create a replacement. Apply ARTIFACT's re-plan gates. |
| Explicit request, pasted tracker content or a successfully read tracker item | Plan a new ticket for that request. Use a named feature, otherwise derive its directory under ARTIFACT. Do not require a pre-existing `issues/` directory. If that directory exists, inspect its tickets and ask before duplicating existing work. |
| Feature directory, or its `root-cause.md` path | Inspect its documents and tickets. Reuse the ticket referencing this root cause; if several match, ask. Create a ticket for a confirmed root cause with no matching ticket, or when no tickets exist and the feature document defines one unit of work. Otherwise select the frontier below. |
| No input | Use the feature explicitly established in this session, else the single `.scratch/<slug>/` with `issues/`, `spec.md` or `root-cause.md`, excluding directories with `map.md`. Several candidates: ask. None: request a ticket, feature or description and stop. Apply the feature-directory row. |

The frontier is the lowest-numbered `ready-for-agent` ticket without `## Implementation`, whose numbered blockers are all resolved with no unfinished execution close. Missing or ambiguous blockers stop selection. With no eligible ticket, report why; do not create extra work to bypass a blocker.

For a new ticket, draft `issues/<NN>-<slug>.md`, where `NN` is one past the highest existing number, or `01` when none exist. Use five fields in order: `# <NN>: <title>`, `**What to build:**`, `**Blocked by:** None (can start immediately)`, `**Status:** ready-for-agent`, then acceptance criteria as `- [ ]` lines. Add the plan only after the evidence, questions and approval gates pass. Work requiring several tickets goes to `/dev:rnd` instead.

Example: an explicit request in a repository without `.scratch/` can create `issues/01-<slug>.md`; invoking plan with no request and no feature stops for input.

An open decision that would change the plan is marked in the ticket rather than guessed:

```
[NEEDS CLARIFICATION: <specific question>]
```

Mark only when the answer changes the decision. An approved saved draft with an open question has status `needs-info` and is not an executable handoff. Before handing over, search the ticket and each existing feature document with `rg -n 'NEEDS CLARIFICATION' -- <paths>` and read the ticket's `## Comments`.

Set `ready-for-agent` only when no clarification marker remains in those documents and no unresolved question or blocker remains in that ticket's Comments. Otherwise keep `needs-info` and name what remains open. Apply this rule to other `needs-info` tickets only when the same answer cleared their blocker; local blockers still count. Historical execution notes alone are not open questions.

This command writes `needs-info` and `ready-for-agent`, here and when it opens a ticket. The execution transitions - `claimed`, `ready-for-human`, `needs-info` on a stop, `resolved` - belong to `/dev:exec`, and this command never writes them.

## TEMPLATE

Before writing, read [assets/implementation.md](assets/implementation.md), resolved relative to this installed skill directory, and use its template.

Rules the template does not show:

- `### Task N:` and `- [ ]` are structural - `/dev:exec` finds the work by them, so keep both exactly as written, in English, whatever language the plan body uses.
- Position decides what a checkbox means. Above `## Implementation` a `- [ ]` line is an acceptance criterion, written when the ticket was created and flipped once by `/dev:exec` after the last task is green; inside a `### Task N:` section it is a unit of work. Never put a task heading above `## Implementation`, and never put a checkbox between `## Implementation` and `### Task 1:`.
- Tests are their own checkbox, never bundled into the implementation step.
- The last checkbox of a task names the concrete command this project runs for that task's tests, not a bare "run tests" and not the whole suite - the whole suite and the linter run once, in `/dev:exec`, at the close.
- A config-only or declarative task has no tests to write; verification is that the change takes effect.
- `Files:` lists what the task is expected to touch. It bounds the task, it is not a contract - reaching one file further to finish the same capability is fine.

## SELF-CHECK

Before handing the plan over, verify it against the repository and fix what fails. State the result in one line.

- `assets/implementation.md` was read from this installed skill directory before writing, and the plan follows its structure and the template rules above;
- for a new plan, no `### Task` heading existed before the append; an approved replacement replaces the old plan rather than appending another one. Afterward no `- [` line sits between `## Implementation` and `### Task 1:`;
- the ticket's `**Blocked by:**` line names only lower numbers - a ticket blocked by a higher one is an authored cycle;
- walk tasks in execution order: a `Modify:` path exists now or is created by an earlier task; a `Create:` path does not exist now and is not already created by an earlier task;
- each required function, interface or seam exists in the expected shape or is explicitly established by an earlier task; no task depends on later work;
- a task with code changes has a checkbox for its tests;
- dependencies run forward: no task calls what a later task creates;
- every acceptance criterion above `## Implementation`, and every requirement from the spec or the root cause, is covered by a task or explicitly deferred - read the other tasks for it under different words first;
- a worker given only its task, the acceptance criteria it serves, and `## Conventions` has every applicable decision, constraint and reason; none depends on reading the conversation or the full feature document;
- nothing the requirements never asked for: no abstraction with one consumer, no future-proofing, no fallback for a case that cannot happen;
- no clarification marker remains in the ticket or existing feature documents, and Comments contain no unresolved question or blocker. A saved incomplete draft stays `needs-info` and is not handed to exec.

## ARTIFACT

The plan is not a file of its own. It is two sections inside one ticket, and one ticket is one whole unit of work:

```
.scratch/<feature-slug>/issues/NN-<slug>.md   ->   ## Conventions, ## Implementation
```

`<feature-slug>` is two to four lowercase english words from the request, hyphenated; a tracker key names the directory instead - `.scratch/<KEY>-<slug>/` - so the feature stays navigable by the key. `NN` is the ticket number, from `01`, in dependency order. Never write into a `.scratch/<x>/` that holds a `map.md`: that directory is a `/wayfinder` effort. Pick another slug and say why in one line.

A ticket that already holds an `## Implementation` section is never overwritten silently - say what is there and ask whether to replace it. A ticket at `**Status:** claimed` or `**Status:** resolved` is never re-planned without asking either: its task checkboxes are execution history.

## NEXT

Return the ticket path, whether it is ready or blocked, and a one-line self-check result. Name any check that could not be completed; do not call that plan ready. For a ready plan, suggest `/dev:exec`, followed later by review and fix. Do not invoke another command.
