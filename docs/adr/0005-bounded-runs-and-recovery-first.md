# Verify bounded worker runs and recovery before parallel orchestration

Status: partly superseded by [ADR 0008](0008-native-subagent-coordination.md) where it prescribes deterministic Python helpers for launch, journal and recovery mechanics.

The target lead workflow remains autonomous execution of an approved feature plan. Implement and verify a sequential full cycle first, then interruption and recovery, before adding parallel worktrees and companion integrations. This reduces the number of interacting failure modes without dropping the target workflow. A successful first cycle should remove manual handoffs and context transfers; routine recovery must not depend on the user reconstructing the run.

Workers perform bounded steps and return a structured outcome: `done`, `needs_input` or `blocked`, with a short conclusion and artifact references. These are worker outcomes, not replacements for ticket statuses. The lead can continue the identified session with the relevant answer. Avoid requiring two clients to control one live interactive TUI. Codex documents schema-constrained final responses and session continuation in its [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode); the actual skill and question workflow still needs an end-to-end probe.

In manual nxs use, preserve ordinary dialogue and human-readable results. Record the same semantic step outcomes in the journal; a user answer continues the current conversation. The structured JSON envelope belongs to controlled worker launches, not every message or an entire feature's status.

Keep inventory, launch parameters, outcome validation, journal writes and worktree preparation in small deterministic helpers. The lead owns task decomposition, interpretation of findings and selection of the next action. Use existing harness and Git capabilities rather than introducing a universal workflow engine. A valid outcome shape does not prove completion: inspect artifacts, acceptance evidence, checks and actual Git state before advancing.

One controller is active for a task. Persist meaningful progress and reconcile it with files, branches and processes after interruption. A missing command response is not evidence that the command did nothing: do not blindly repeat migrations, commits or worker launches. Preserve the unanswered question and enough context to continue the intended worker.

Verify the sequential cycle, question continuation, interruption after file changes, lost result delivery, and recovery without duplicate actions. Add parallel worktrees only after those checks establish the sequential contract, then verify combined behavior and integration conflicts. Companion integrations follow that baseline; OpenCode remains the next harness after Codex verification.
