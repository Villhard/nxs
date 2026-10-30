---
name: dev-lead
description: Coordinate a development task through clarification, an approved feature plan, sequential native CLI execution, review, project specs and atomic commits when the user explicitly invokes /dev-lead. Use individual dev skills for a single manual stage.
argument-hint: "[request | feature dir | ticket path]"
disable-model-invocation: true
---

# /dev-lead

Own one task from its current state through verified delivery. Use native Claude Code, Codex or OpenCode workers in visible agterm sessions, on one feature branch. Require Python 3, Git, agterm and the selected CLI. Default to the active client, record it explicitly, and never silently substitute Codex. Read-only Claude/OpenCode launches additionally require macOS sandbox-exec. See the runner for protocol and permission differences.

## START

Before any task record, controller acquisition, discovery, branch operation or worker launch, run the read-only [agterm preflight](references/runner.md#agterm-entry). Require a reachable explicit socket and a live lead session with consistent window/workspace/session IDs. Outside agterm, stop in the conversation: "dev-lead requires agterm; open this repository in agterm and invoke dev-lead again." Standalone dev skills remain available. Report missing CLI, socket permissions/connectivity and stale or contradictory identity by their actual cause. An inaccessible socket does not prove the app is absent. Do not attach to another session or start partial coordination. Read-only instruction inspection may precede this gate.

1. Read [project specs](references/project-specs.md) before using specs. Resolve the explicit request, feature directory or ticket. Read applicable instructions, glossary, decision records, project specs and existing artifacts. With competing task directories, ask which one; a branch name alone never selects a task. Preserve user changes and ticket history.
2. Read [journal](references/task-journal.md) and [controlled runs](references/controlled-run.md). Reconcile an existing journal and run state before doing work. Acquire the system controller lock through [runner](references/runner.md) for the whole coordinating lifetime; a second controller stops. Local records live under `research/dev-lead/`; `decision.log` is at the feature root.
3. Discover actual skills and models for the task cwd with the runner. Check enabled state, discovery errors, exact paths and candidate hashes. A Claude candidate delivered as pinned context must be explicitly selected and identified as such in the feature plan; its name alone never proves native registration. The required route uses `dev-rnd`, ticket execution, `dev-review`, `dev-spec` and `dev-commit`; a reported failure may first use `dev-bug`. Read the selected runtime contracts and confirm the decision-only and controlled-run interfaces before launch; availability alone does not establish compatibility. Missing, disabled, discovery failure and launch restriction are distinct stops. Companion discovery establishes availability only; this version uses nxs alone.

## AGREE THE FEATURE

Use focused `dev-rnd --decision-only` for questions that need investigation. Give each worker a narrow question and the relevant evidence, then combine the conclusions. Ask the user all independent unresolved questions together through [visible status and questions](references/visibility.md). Answer from verified facts and agreed decisions yourself; return a choice of scope, external contract or recorded decision to the user.

Show a feature plan using [the template](assets/feature-plan.md): behavior, exclusions, work breakdown and dependencies, acceptance checks, feature branch, allowed writes, environment actions with exact targets, and a table of purpose, harness, actual catalog model and supported effort (or native default when effort metadata is absent). Favor quality for decisions and final review; choose a faster suitable model only for a bounded clear task. Model names are runtime choices, never guide defaults.

Keep draft and approved feature plans at `research/dev-lead/feature-plan.md`. Save the user's explicit approval and the approved plan's content hash in the journal. Existing authorization is reused only for the same content and scope. A new material decision reopens its affected part. Permission to write a draft is not approval to implement it.

After approval, use normal `dev-rnd` to slice the approved spec without reopening settled choices. All controlled tickets use the feature branch; prerequisites must exist in its working tree. Existing tickets on another branch require reconciliation before execution.

## EXECUTE SEQUENTIALLY

Publish stage/action changes and keep status visible through the lead-only [presentation helpers](references/visibility.md). During worker/result or questionnaire waits, remain active with lifetime ownership and bounded polls at most 60 seconds apart. Preserve covering UI, report actual UI failures, consume answers without another user message and keep workflow choices in this lead.

For each bounded step, prepare the [context packet](assets/context-packet.md) and its allowed outputs. Record intent before launch and keep run ID, launch parameters, agterm session ID and native session ID and harness. Run writing workers through `agtermctl session new --command ... --wait`, confirm the process in `tree`, and stream events both to disk and the terminal. Use the runner's bounded execution and exact session continuation.

Pass the saved preflight identity to prepare. Workers use that socket/window/workspace regardless of GUI focus; terminal labels are normalized unique `nxs_<feature>_<step>_<run>` names, separate from original run IDs and native session identity. Keep lifetime controller ownership and one sequential writer.

A ticket worker first proposes its ticket plan and returns `needs_input`; inspect its branch, prerequisites, acceptance checks and permissions against the feature plan. Record lead approval before resuming that exact session to implement. The approval covers technical steps within the user's plan, never new user consent. Executors leave commits to `dev-commit`.

Validate each envelope and independently check the files, acceptance evidence, command results and Git state before accepting `done`. A ticket's status retains its existing meaning. A saved `done` is not enough after evidence changes. For `needs_input`, save the question and end the worker turn; answer from settled evidence or ask the user, then resume only the saved session. For `blocked`, record the reason and the evidence needed to proceed. Helpers perform mechanics; the lead chooses every next action.

Retire a worker terminal only through the runner's [owned cleanup](references/runner.md#owned-terminal-cleanup), after current independent acceptance, stopped-worker evidence and a recorded reason establish it is no longer needed. For a superseded answered or resolved blocked turn, explicitly identify its verified exact continuation under that contract. Preserve unanswered, unresolved blocked, live, invalid, stale and uncertain runs until reconciled, and all lead, foreign and previous-task terminals. Lost close replies require observation, never an automatic second close. Terminal closure retains exact native continuation evidence.

## REVIEW AND FINISH

1. Run the project's full checks and inspect the diff. Prepare staged scope explicitly from task changes only. Separate user hunks; if they cannot be separated safely, ask about that concrete scope before staging. Review itself never stages or changes source.
2. Act as the `dev-review` orchestrator in the same persistent controller, with the complete approved context and pinned requirements. Launch its bounded read-only roles directly from that controller; a nested writing review coordinator cannot acquire its parent controller lock. Use all existing finder roles and then the verifier through its native CLI read-only route. Only its orchestrator writes the report. Select fixes within the approved feature plan, save the decision, then execute fix tickets sequentially. A fix requiring new behavior returns to the user.
3. Rerun relevant checks after fixes. Invoke `dev-spec` as the only project-spec writer, then `dev-commit` for atomic task commits. The explicit lead invocation and approved plan authorize these internal stages; standalone invocation gates still apply outside controlled context. Never push.
4. Reconcile final HEAD, index, working tree and evidence, record handoff, release the controller lock, and report commits, actual verification and remaining limitations. Completion requires the acceptance checks, complete review, matching specs and verified commits. If any stage is incomplete, name it without claiming delivery.

## RECOVERY

On interruption, read [runner](references/runner.md) and [question/presentation recovery](references/visibility.md#recovery) before any retry. Reconcile saved questions, page outcomes and recorded answer use before reopening UI. Compare intent/run records, processes, events, outcome files, artifact hashes, HEAD, index and working tree. Continue a reconciled unfinished step; skip only a completion whose evidence is still current. Unknown launch, migration or commit effects remain blocked until reconciled. Never retry an unknown side effect automatically.
