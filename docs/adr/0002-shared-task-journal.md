# A shared task journal supports manual work and lead handoff

The task's `decision.log` is a shared artifact maintained by the skills participating in the work, including when they are invoked without `dev-lead`. A journal written only by the lead could not reliably support joining a task already in progress.

The journal records decisions and concise progress entries: the current stage, an awaited question or result, links to existing artifacts and the next action. Specs, tickets and review reports keep their own content; the journal links to them. It supports continuing with another coordinator or harness without treating the previous conversation as the only record of the work.

The intended integration puts the journal rule directly in nxs task skills and the ticket executor contract. A general rule installed through `dev-setup` in global agent instructions also applies to companion skills working on the task; the lead additionally passes the journal path to its executors. This does not require modifying the companion skills themselves.

The journal contract is explicit and checkable for nxs and controlled lead launches. A global instruction alone cannot guarantee a complete journal for manually invoked companion skills. When taking over that work, reconcile the available journal with artifacts and actual state, and resolve missing context before proceeding. Do not assume that the recorded history is complete.

Record meaningful decisions and state changes: an open question, an answer, a completed stage, a blocker or a handoff. Do not record every technical action. Taskless global setup, an empty review and a declined write proposal do not require a task-journal entry.

Resolve the journal from an explicit ticket or task-directory path, or unambiguous conversation context. Ask when multiple tasks fit; a Git branch name alone is not enough to select a task. Pass the same journal path when handing the work to the lead or another executor.

Journal placement when no task directory exists, format, concurrent writes and verification on resume remain open. This is an accepted design direction, not a change to the existing skills' write boundaries.
