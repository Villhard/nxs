# Using nxs

<EXTREMELY-IMPORTANT>
Before acting on any development task - including clarifying questions, reading code, or running a command - check whether an nxs skill applies, and if one does, invoke it with the `Skill` tool first. If a skill applies to your task, you do not get to skip it. This is not negotiable.
</EXTREMELY-IMPORTANT>

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this - your task is already scoped.
</SUBAGENT-STOP>

## The rule

The nxs commands (`rnd`, `bug`, `plan`, `plancheck`, `exec`, `review`, `commit`) are listed with their triggers in the `Skill` tool. Match your task to a command and invoke it before you start - do not hand-roll a workflow a command already owns.

Two triggers are easy to miss because no command name is spoken:

- **Any `git add` / `git commit` / `git push`** -> load the `commit-conventions` skill first (message format, atomicity, git safety). When the user asks to commit working changes, use `/nxs:commit`.
- **Input carries a tracker key / URL or a pasted ticket** -> read the ticket first (through the tracker if reachable, otherwise ask the user to paste it; never invent its content from the key), and name any brief or plan by the key: `YYYYMMDD-<KEY>-<slug>`.

## Red flags

These thoughts mean stop and check for a skill:

- "This is a simple change, I'll just do it" - simple changes are still tasks.
- "Let me explore the code first" - a skill tells you how to explore; check first.
- "I'll commit this quickly" - a git write pulls `commit-conventions`.

User instructions override this discipline. Only skip a skill when the user told you to.
