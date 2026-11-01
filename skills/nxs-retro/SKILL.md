---
name: nxs-retro
description: Review exactly one current or explicitly selected session and save evidence-based, scoped improvement proposals.
argument-hint: "[one session or evidence path]"
disable-model-invocation: true
---

# /nxs-retro

Review one session and save an evidence-based retrospective. Run only on explicit invocation or in an explicit controlled scope. Read [session evidence](references/session-evidence.md), [writing for agents](references/writing-for-agents.md), [project specs](references/project-specs.md) for affected paths and the [template](assets/retro.md). Read [task journal](references/task-journal.md) before a task write, question or handoff when applicable; an explicit controlled packet also requires [controlled run](references/controlled-run.md).

## REVIEW

1. Select exactly the current session by default, or one explicitly identified session. Use only an actually available source for that session; if its transcript or identity cannot be established, report the missing access and ask for an accessible source. Do not scan a period, build an index or infer activity from timestamps. Do not claim support for an unobserved client access path.
2. Inspect available session evidence and relevant artifacts for outcomes, friction and successful practices, even when no failure is reported. Attribute each observation to a source and distinguish evidence, inference and unknowns. Consider prior retrospective results that were supplied or can be found in the existing task context; state that discovery may be incomplete. Do not scan other sessions to reconstruct history.
3. For each supported problem, propose a concrete, actionable solution immediately; do not defer the solution to a later discussion. In the saved report and final response, use a numbered list with a plain-language **Problem** paragraph followed by a blank line and a **Solution** paragraph. Explain what to change and where, with expected benefit, cost, evidence and any required approval. Choose placement by scope and repetition: global or project instructions for durable rules, a project, global or plugin skill for repeatable intent, and checks or tools for mechanically enforceable behavior. Show options when that boundary changes the outcome. If the evidence does not support a concrete solution, state what is missing rather than inventing one. A reasoned no-change result is valid when evidence supports none.
4. Save under an explicit or established destination, otherwise `.scratch/<feature-slug>/research/retro-<session-slug>.md` for a known task or `.scratch/retros/<session-slug>.md` for a taskless session. Ask when task or destination is ambiguous. Preserve existing results and unrelated content. Cite available evidence without secrets or unnecessary private transcripts and record access limitations.
5. Apply only changes already authorized within their exact scope and permitted by applicable project ownership rules. New personal rules and substantial ambiguous changes require a separate concrete proposal and approval before editing. Reuse existing authorization for precise in-scope work; a retrospective request alone authorizes the report, not unrelated instruction, skill, tool or configuration edits. Verify authorized changes and report applied versus proposed work and remaining limits.
