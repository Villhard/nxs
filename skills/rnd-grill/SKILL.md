---
name: rnd-grill
description: Investigate an uncertain idea or plan through evidence-backed choices; optionally use an isolated experiment and directly save approved decisions, feature descriptions, domain records or participant questions without implementing.
argument-hint: "[question | plan | source path | save request]"
disable-model-invocation: true
---

# /rnd-grill

Investigate uncertainty, compare meaningful alternatives and stop at the agreed conclusion or exact open question. Accept an idea, question, plan, saved discussion, selected boundary, source document or direct artifact request. A clear request may need no interview or saved artifact.

## ENTRY

Run only on explicit invocation or an instruction explicitly covering this skill's work. Read [discussion](references/discussion.md), [domain modeling](references/domain-modeling.md) when domain terms or records matter, and [project specs](references/project-specs.md) for affected paths. Read explicit input before proceeding; a missing or unreadable file is a stop, not a fresh request. For tracker input, use the source rules in [saving](references/saving.md).

Reuse existing task context and approval only within their actual scope. A feature path, saved record or status is context, not permission. No task directory, typed decision tickets, journal, run packet or orchestration is required. Preserve existing records and clarify conflicting legacy instructions rather than activating a removed coordination procedure.

## DISCUSS

1. Inspect relevant code, callers, tests, documents and current behavior. Report facts affecting the choice with source paths or primary-source links; distinguish observations, recorded intent, inferences, assumptions and unavailable evidence.
2. Work the discussion frontier in independent rounds. Give real alternatives, consequences and a recommendation for each material choice. Wait for the user's choices before deriving dependent questions. Resolve routine technical details from evidence instead of inventing an interview.
3. Use only the evidence methods needed for the actual question. Read [evidence methods](references/evidence-methods.md) for dependent questions, deeper research, a requested opportunity survey or design of a selected boundary. Read [prototype](references/prototype.md) only when a small isolated experiment is justified and explicitly authorized. These are optional techniques, not stages to complete in order.
4. Pressure-test significant conclusions against concrete edge cases, assumptions and failure signals. Contradictory evidence reopens only the affected conclusion. Stop when no material choice remains silently assumed, or name the precise pending choice and wait.

For a requested participant questionnaire, read [questionnaire](references/questionnaire.md), establish the recipient and their role, reuse known answers and prepare focused answerable questions. Preparing or approving the document never authorizes sending it or inventing responses.

## FINISH OR SAVE

Summarize agreed conclusions, proposals and open questions in dialogue. Agreement alone creates no files and authorizes no implementation. If saving is requested, use [saving](references/saving.md) directly: show the destination and concrete content or revision, reuse exact applicable approval or obtain it, and write only approved content. No separate saving command or prerequisite decision file is required. A direct approved domain request needs no decision wrapper; a clear request can become an approved feature description without prior research artifacts.

Report written or reused paths, declined proposals, evidence limitations and unresolved questions. Suggest `dev-exec` directly when agreed scope is sufficient; it owns acceptance criteria, plan approval, optional decomposition, implementation and verification. Material unresolved intent blocks the affected work, not unrelated authorized preparation. A saved draft or successful prototype is not a ready implementation plan. Never start a subsequent skill implicitly.

## BOUNDARIES

Permitted writes are approved preparation artifacts and glossary/ADR records, plus explicitly scoped isolated prototype files and evidence. Never edit product code or tests, implementation tickets, project `SPEC.md` or `.SPEC.md`, Git/index, settings or installations. Project specs remain `dev-spec`-owned. Prototype success permits no production transfer, reuse or deletion; each needs separate authorization for that action. An install, migration or external action needs approval covering the concrete action and target, plus native permissions; otherwise stop that affected work and state the expected result and missing evidence. Never automatically repeat an uncertain effect after interruption; reconcile observable state first. HTML approval alone requests no save and approves no unseen content.
