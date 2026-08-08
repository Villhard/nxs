---
description: Create an implementation plan that becomes the source of truth for execution - decompose a task, brief, or ticket into sequenced tasks with checkboxes. Use before executing non-trivial work, after a brainstorm or a diagnosis.
argument-hint: "[task | story path | tracker key]"
---

# /nxs:plan

Turn a task, brief, or ticket into an implementation plan and stop. The plan is what `/nxs:exec` executes.

Accepted input: a task description, a story directory under `docs/nxs/stories/` holding a brief or a root-cause brief, or a tracker key / URL / pasted ticket. With no input, gather it here first.

Example: /nxs:plan docs/nxs/stories/20260711-auth-refactor

## STANCE

- Write the plan and stop. Implementation code, the build, and any behavior change belong to `/nxs:exec`.
- The plan is a proposal, read-only until the user approves it.
- A small single-step task needs no plan - route to `/nxs:exec` or a direct edit instead of ceremony.

## PROCEDURE

1. **Read the code.** Inspect the files, patterns, and dependencies the task touches - directly or through the built-in Explore agent. Do not over-read. Clarify a fuzzy domain term before encoding it into the plan.
2. **Close the open questions.** Ask one at a time, 2-4 concrete options with a recommendation. For several viable approaches, lay out the trade-offs and ask once.
3. **Decompose.** 3-7 tasks. Each is one working unit: the code plus the tests for it, leaving the project green. Sequence by dependency - a task never calls what a later task creates. Every task earns its place; cut the rest.
4. **Write the file** using the template below.
5. **Run the self-check** before handing the plan over.

An open decision that would change the plan is marked in the file rather than guessed:

```
[NEEDS CLARIFICATION: <specific question>]
```

Mark only when the answer changes the decision. A marker answered in conversation is edited out in the same turn. `/nxs:exec` refuses to start while one is open.

## TEMPLATE

````markdown
# <Plan title>

- Tracker: <key or URL - drop the line if there is none>

## Overview

<what this plan does and why, in a few lines>

## Acceptance criteria

<verifiable readiness criteria for the whole plan: what the user, the API, or the system can do afterwards>

## Context

<the files, patterns, and dependencies the work leans on>

## Conventions

<rules every task follows - style, naming, a repeated step, a standing preference. /nxs:exec passes this
section to every worker, so what is missing here does not reach the code. No such rules, no section.>

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

### Task 2: <title>

...

### Task N: Verify acceptance criteria

- [ ] run the full suite: `go test ./...`
- [ ] run the linter: `golangci-lint run`
````

Rules the template does not show:

- `### Task N:` and `- [ ]` are structural - `/nxs:exec` finds the work by them, so keep both exactly as written, in English, whatever language the plan body uses.
- Tests are their own checkbox, never bundled into the implementation step.
- The last checkbox of a task names the concrete command this project runs, not a bare "run tests".
- A config-only or declarative task has no tests to write; verification is that the change takes effect.
- `Files:` lists what the task is expected to touch. It bounds the task, it is not a contract - reaching one file further to finish the same capability is fine.

## SELF-CHECK

Before handing the plan over, verify it against the repository and fix what fails. State the result in one line.

- every `Modify:` path exists, every `Create:` path does not;
- everything the plan leans on - a function it calls, an interface it implements, a seam it assumes - exists in the shape it expects;
- a task with code changes has a checkbox for its tests;
- dependencies run forward: no task calls what a later task creates;
- every requirement from the brief or the ticket is covered by a task or explicitly deferred - read the other tasks for it under different words first;
- nothing the requirements never asked for: no abstraction with one consumer, no future-proofing, no fallback for a case that cannot happen;
- `rg "NEEDS CLARIFICATION" <plan>` returns nothing.

## ARTIFACT

```
docs/nxs/stories/YYYYMMDD-<slug>/plan.md
```

Write it into the story directory the input names, creating the directory when the input is a bare task with no prior brief. A tracker key names the directory - `docs/nxs/stories/YYYYMMDD-<KEY>-<slug>/` - so the story stays navigable by the key. The files inside keep their fixed names.

A finished story moves to `docs/nxs/stories/completed/` by hand, on explicit user confirmation.

## NEXT

Plan written -> `/nxs:exec` to implement it, then `/nxs:review` for the review gate.
