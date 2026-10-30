## nxs

- Branches: <required: the branch rule from AUDIT step 3>
- Tests: <optional: the full test suite command; drop the line when none was found>
- Lint: <optional: the linter command; drop the line when none was found>
- Typecheck: <optional: the type checker command; drop the line when none was found>

A ticket's "full test suite and linter" means the commands above.

- Task journal: when working on a task, append meaningful decisions, questions, answers, stage completions, blockers and handoffs as concise JSONL events with unique IDs to the feature's `decision.log`, using a system file lock. Resolve it from an explicit task/ticket path or unambiguous context, ask when several fit, and pass the same path at handoff. Record links and evidence, never secrets or full conversations. Reconcile the journal with actual artifacts and Git state before resuming; an incomplete companion journal proves no completion. Taskless setup, empty review and declined writes create no journal. Only an explicit controlled-run packet carries the lead's approved plan and bounded outcome contract; standalone calls retain their normal approval gates.
