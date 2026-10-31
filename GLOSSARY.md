# nxs

The language used to coordinate development work across the agreed workflow.

## Language

**Lead**:
The coordinator responsible for advancing a development task through its agreed workflow and bringing decisions that require human judgment back to the user.

**Native subagent**:
A fresh-context agent started by the selected client's own subagent facility with a complete prompt, write boundaries and result contract; the lead waits for its result and verifies it independently.

**Decision log**:
The chronological record of a task's decisions and progress, used to continue the work when its coordinator or harness changes.

**Feature plan**:
The user-approved approach and scope for delivering one feature, including its work breakdown, dependencies and completion checks.

**Ticket plan**:
The steps for completing one ticket, reviewed by the lead against the feature plan when the lead coordinates the task.

**Target catalog**:
The 19 source commands that separate independent workflow operations; their presence does not establish client registration or a completed cutover.

**Legacy route**:
A retained `dev-rnd`, `dev-bug`, `dev-lead` or `dev-setup` entry and its existing callers, kept until the applicable replacement is verified.

**Cutover**:
A route-specific switch of callers or installations after the required evidence and authorization; source additions and shell checks alone do not complete it.
