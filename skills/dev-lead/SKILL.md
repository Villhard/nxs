---
name: dev-lead
description: Coordinate a development task through clarification, an approved feature plan, sequential Codex execution, review, project specs and atomic commits when the user explicitly invokes /dev-lead. Use individual dev skills for a single manual stage.
argument-hint: "[request | feature dir | ticket path]"
disable-model-invocation: true
---

# /dev-lead

Own one task from its current state through verified delivery. This adapter supports Codex workers in visible agterm sessions, on one feature branch. Python 3, Git, Codex and agterm are required. Other clients may read the records but have no verified lead adapter.

## START

1. Read [project specs](references/project-specs.md) before using specs. Resolve the explicit request, feature directory or ticket. Read applicable instructions, glossary, decision records, project specs and existing artifacts. With competing task directories, ask which one; a branch name alone never selects a task. Preserve user changes and ticket history.
2. Read [journal](references/task-journal.md) and [controlled runs](references/controlled-run.md). Reconcile an existing journal and run state before doing work. Acquire the system controller lock through [runner](references/runner.md) for the whole coordinating lifetime; a second controller stops. Local records live under `research/dev-lead/`; `decision.log` is at the feature root.
3. Discover actual skills and models for the task cwd with the runner. Check enabled state, discovery errors, exact paths and candidate hashes. The required route uses `dev-rnd`, ticket execution, `dev-review`, `dev-spec` and `dev-commit`; a reported failure may first use `dev-bug`. Read the selected runtime contracts and confirm the decision-only and controlled-run interfaces before launch; availability alone does not establish compatibility. Missing, disabled, discovery failure and launch restriction are distinct stops. Companion discovery establishes availability only; this version uses nxs alone.

## AGREE THE FEATURE

Use focused `dev-rnd --decision-only` for questions that need investigation. Give each worker a narrow question and the relevant evidence, then combine the conclusions. Ask the user all independent unresolved questions together. Answer from verified facts and agreed decisions yourself; return a choice of scope, external contract or recorded decision to the user.

Show a feature plan using [the template](assets/feature-plan.md): behavior, exclusions, work breakdown and dependencies, acceptance checks, feature branch, allowed writes, environment actions with exact targets, and a table of purpose, actual catalog model and supported effort. Favor quality for decisions and final review; choose a faster suitable model only for a bounded clear task. Model names are runtime choices, never guide defaults.

Keep draft and approved feature plans at `research/dev-lead/feature-plan.md`. Save the user's explicit approval and the approved plan's content hash in the journal. Existing authorization is reused only for the same content and scope. A new material decision reopens its affected part. Permission to write a draft is not approval to implement it.

After approval, use normal `dev-rnd` to slice the approved spec without reopening settled choices. All controlled tickets use the feature branch; prerequisites must exist in its working tree. Existing tickets on another branch require reconciliation before execution.

## EXECUTE SEQUENTIALLY

For each bounded step, prepare the [context packet](assets/context-packet.md) and its allowed outputs. Record intent before launch and keep run ID, launch parameters, agterm session ID and Codex session ID. Run writing workers through `agtermctl session new --command ... --wait`, confirm the process in `tree`, and stream events both to disk and the terminal. Use the runner's bounded execution and exact session continuation.

A ticket worker first proposes its ticket plan and returns `needs_input`; inspect its branch, prerequisites, acceptance checks and permissions against the feature plan. Record lead approval before resuming that exact session to implement. The approval covers technical steps within the user's plan, never new user consent. Executors leave commits to `dev-commit`.

Validate each envelope and independently check the files, acceptance evidence, command results and Git state before accepting `done`. A ticket's status retains its existing meaning. A saved `done` is not enough after evidence changes. For `needs_input`, save the question and end the worker turn; answer from settled evidence or ask the user, then resume only the saved session. For `blocked`, record the reason and the evidence needed to proceed. Helpers perform mechanics; the lead chooses every next action.

## REVIEW AND FINISH

1. Run the project's full checks and inspect the diff. Prepare staged scope explicitly from task changes only. Separate user hunks; if they cannot be separated safely, ask about that concrete scope before staging. Review itself never stages or changes source.
2. Act as the `dev-review` orchestrator in the same persistent controller, with the complete approved context and pinned requirements. Launch its bounded read-only roles directly from that controller; a nested writing review coordinator cannot acquire its parent controller lock. Use all existing finder roles and then the verifier through its Codex read-only route. Only its orchestrator writes the report. Select fixes within the approved feature plan, save the decision, then execute fix tickets sequentially. A fix requiring new behavior returns to the user.
3. Rerun relevant checks after fixes. Invoke `dev-spec` as the only project-spec writer, then `dev-commit` for atomic task commits. The explicit lead invocation and approved plan authorize these internal stages; standalone invocation gates still apply outside controlled context. Never push.
4. Reconcile final HEAD, index, working tree and evidence, record handoff, release the controller lock, and report commits, actual verification and remaining limitations. Completion requires the acceptance checks, complete review, matching specs and verified commits. If any stage is incomplete, name it without claiming delivery.

## RECOVERY

On interruption, read [runner](references/runner.md) before any retry. Compare intent/run records, processes, events, outcome files, artifact hashes, HEAD, index and working tree. Continue a reconciled unfinished step; skip only a completion whose evidence is still current. Unknown launch, migration or commit effects remain blocked until reconciled. Never retry an unknown side effect automatically.
