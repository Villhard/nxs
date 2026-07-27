# Using nxs

This session has the nxs plugin - a plan -> exec -> review loop. Its commands (`rnd`, `bug`, `plan`, `plancheck`, `exec`, `review`, `commit`) are listed with their triggers in the `Skill` tool. Match the task to a command and invoke it rather than hand-rolling a workflow a command already owns.

If you were dispatched as a subagent to execute a specific task, this does not apply - your task is already scoped.

Two triggers are easy to miss because no command name is spoken:

- **Any `git add` / `git commit` / `git push`** -> load the `commit-conventions` skill first (message format, atomicity, git safety).
- **Input carries a tracker key / URL or a pasted ticket** -> read the ticket first (through the tracker if reachable, otherwise ask the user to paste it; never invent its content from the key), and name any brief or plan by the key: `YYYYMMDD-<KEY>-<slug>`.

`/nxs:commit` is user-invoked only - it runs when the user types it, not on your initiative.
