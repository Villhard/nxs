---
name: dev-lead
description: Coordinate a development task through clarification, an approved feature plan, native subagent delegation, review, project specs and atomic commits when the user explicitly invokes /dev-lead. Use individual dev skills for a single manual stage.
argument-hint: "[request | feature dir | ticket path]"
disable-model-invocation: true
---

# /dev-lead

Own one task from its current state through verified delivery. Delegate bounded work to the active client's native subagents, on one feature branch. Require Git, the selected client and a native subagent facility that starts a fresh-context agent with a complete prompt and reports or waits for its result. Never substitute another client and never launch a nested CLI runner in place of a native subagent. Read [native subagents](references/subagents.md) for the delegation contract and permission differences.

## START

Before any task record, branch operation, discovery or launch, inspect the exposed tools and select the native subagent facility. Record the selected client, subagent tool and available model catalog in the feature plan. If the client exposes no fresh-context subagent with a completion wait, stop in the conversation with the missing capability; standalone dev skills remain available. A matching tool name alone is not a route: check the actual schema.

1. Read [project specs](references/project-specs.md) before using specs. Resolve the explicit request, feature directory or ticket. Read applicable instructions, glossary, decision records, project specs and existing artifacts. With competing task directories, ask which one; a branch name alone never selects a task. Preserve user changes and ticket history.
2. Read [journal](references/task-journal.md) and [controlled runs](references/controlled-run.md). Reconcile an existing journal and saved step state before doing work. One feature has one active lead; a second lead must not launch writers. Local records live under `research/dev-lead/`; `decision.log` is at the feature root.
3. Discover actual skills and models for the task cwd where the client exposes a catalog. Check enabled state, discovery errors, exact paths and candidate hashes. A candidate delivered as pinned context must be explicitly selected and identified as such in the feature plan; its name alone never proves native registration. The required route uses `dev-rnd`, ticket execution, `dev-review`, `dev-spec` and `dev-commit`; a reported failure may first use `dev-bug`. Read the selected runtime contracts and confirm the decision-only and controlled-run interfaces before launch; availability alone does not establish compatibility. Missing, disabled, discovery failure and launch restriction are distinct stops. Companion discovery establishes availability only; this version uses nxs alone.

## AGREE THE FEATURE

Use focused `dev-rnd --decision-only` through a native subagent for questions that need investigation. Give each subagent a narrow question and the relevant evidence, then combine the conclusions. Ask the user all independent unresolved questions together through [local progress and questions](references/questions.md). Answer from verified facts and agreed decisions yourself; return a choice of scope, external contract or recorded decision to the user.

Show a feature plan using [the template](assets/feature-plan.md): behavior, exclusions, work breakdown and dependencies, acceptance checks, feature branch, allowed writes, environment actions with exact targets, and a table of purpose, client, actual catalog model and supported effort (or native default when effort metadata is absent). Favor quality for decisions and final review; choose a faster suitable model only for a bounded clear task. Model names are runtime choices, never guide defaults.

Keep draft and approved feature plans at `research/dev-lead/feature-plan.md`. Save the user's explicit approval and the approved plan's content hash in the journal. Existing authorization is reused only for the same content and scope. A new material decision reopens its affected part. Permission to write a draft is not approval to implement it.

After approval, use normal `dev-rnd` through a native subagent to slice the approved spec without reopening settled choices. All controlled tickets use the feature branch; prerequisites must exist in its working tree. Existing tickets on another branch require reconciliation before execution.

## EXECUTE SEQUENTIALLY

Publish stage/action changes and keep status visible through the lead-only [local progress](references/questions.md#progress). During subagent or question waits, remain active and use the host's completion mechanism, not repeated short polls. Preserve covering questions and answers, report actual failures in the conversation, consume answers without another user message and keep workflow choices in this lead.

For each bounded step, prepare the [context packet](assets/context-packet.md) and its allowed outputs. Record intent in the journal before launch, with a unique run ID, step ID, selected client, subagent route and packet hash. Launch one writing subagent at a time with the complete packet and role text, exact cwd, write boundaries and result contract; do not pass the parent conversation. Confirm the launch and wait for its completion.

A ticket worker first proposes its ticket plan and returns `needs_input`; inspect its branch, prerequisites, acceptance checks and permissions against the feature plan. Record lead approval before continuing that exact step. If the host supports exact continuation, resume the same subagent session; otherwise start a new bounded subagent with the approved plan and the saved artifacts. The approval covers technical steps within the user's plan, never new user consent. Executors leave commits to `dev-commit`.

Validate each envelope and independently check the files, acceptance evidence, command results and Git state before accepting `done`. A ticket's status retains its existing meaning. A saved `done` is not enough after evidence changes. For `needs_input`, save the question and end that subagent turn; answer from settled evidence or ask the user, then continue. For `blocked`, record the reason and the evidence needed to proceed. Subagents perform mechanics; the lead chooses every next action.

After accepting an implementation or fix ticket, complete the [review/spec/commit checkpoint](#review-and-finish) before the next independent ticket. Research and planning turns create no empty commits.

Close or release a subagent session only through the host's documented mechanism after collecting its result. Preserve run IDs, packets and native evidence in the journal. A lost reply is reconciled from artifacts and observations, never replayed automatically. There is no terminal inventory or owned-terminal cleanup outside the host.

## REVIEW AND FINISH

Apply this checkpoint after each accepted implementation or fix ticket. Keep explicit status/action updates and bounded waits throughout it.

1. Run relevant checks and the project's full required checks; retain actual outputs, exit codes and input hashes. Inspect the diff and prepare explicit task review scope, preserving user hunks and the original index. Follow the selected `dev-commit` contract's index cases: foreign staged groups plus any mixed selected path stops before index mutation; only wholly task-owned selected paths qualify for its `--only` route. Separable task hunks with an empty or task-only index stay separable. Never bypass these boundaries with an alternate index, stash or temporary file rewrites. Review itself never stages or changes source.
2. Act as the `dev-review` orchestrator in the same lead, with the approved context and pinned scope/requirements. Launch all existing read-only finder roles, then the verifier, directly as native subagents. Only this lead writes the report. Journal selected in-scope fixes and execute them through the normal ticket-plan approval and exact-continuation boundary. A fix requiring new behavior returns to the user.
3. Keep dependent review corrections in this active checkpoint. Verify each correction against its findings and explicit scope, record closure of the original review and corrections, and rerun relevant and full required checks. Do not start another independent ticket with findings, specs or commits outstanding. Invoke `dev-spec` as the only project-spec writer for built durable changes; record changed specs or its justified no-change result and check those changes before committing.
4. Invoke `dev-commit` for atomic task groups. Record [commit intent and recovery evidence](references/subagents.md#commit-recovery) in the journal before each authorized effect; verify actual parent/HEAD, committed diff and preserved working/index content afterward. Append `ticket.checkpoint.accepted` with the exact HEAD, covered tickets and evidence only after checks, review closure, specs and commits are verified. Publish that event/HEAD in the status file. A no-change group is a recorded no-op, never an empty commit. The approved feature plan authorizes these internal stages; standalone invocation gates still apply outside controlled context. Executors never stage/commit. Never push.

After all tickets, run a final review of the complete feature from its approved baseline, including committed tickets and remaining task changes. Repeat checks, resolve findings, reconcile built-work specs and any remaining atomic commits. Earlier scoped reviews do not replace this review. Reconcile final HEAD, index, working tree and evidence and record handoff. Update the status file with final progress and no current run. Report commits, actual verification and limitations. An incomplete stage prevents a delivery claim.

For an explicitly selected additive review handoff, run `dev-review --to-tickets` with the approved scope, then pass its current report and approved selection to `to-tickets` as a separate bounded step. Verify resulting tickets and report links before the existing plan approval and checkpoint. Discover and pin `to-tickets` for this route. The existing review-to-fix route remains available until its switch gate passes; do not select the candidate silently.

## RECOVERY

On interruption, read [native subagents](references/subagents.md) and [question and progress recovery](references/questions.md#recovery) before any retry. Reconcile saved questions, answers and recorded use before reopening a question. Compare intent and run records, subagent sessions, artifacts, hashes, HEAD, index and working tree. Continue a reconciled unfinished step; skip only a completion whose evidence is still current. Unknown launch, migration or commit effects remain blocked until reconciled. Never retry an unknown side effect automatically. Continue a native subagent session only when the host supports it and the saved identity is verified; otherwise start a new bounded step after the prior effect is known.
