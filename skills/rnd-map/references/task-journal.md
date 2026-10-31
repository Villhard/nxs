# TASK JOURNAL

Read before a task's first durable write, a material question or a handoff, in controlled and standalone use. Resolve the feature from an explicit task/ticket path or unambiguous context; ask when several fit. A branch alone is insufficient. A review without a feature uses its resolved `.scratch/reviews/<branch-slug>/` directory. Taskless setup, an empty review and a declined write proposal create no journal.

## RECORD

Append meaningful decisions, questions, answers, stage completions, blockers and handoffs to `<feature>/decision.log` as JSONL. Use a unique event ID, timestamp, kind, step ID, concise conclusion and relative evidence/artifact links. Keep specs, tickets and review contents in their own files. Exclude secrets and full conversations. A question includes its exact text; an answer links the question ID; approval pins the approved artifact's hash and scope. Record intent before a side effect and completion only after checking its result.

Append one complete line at a time with the host's file-write or shell tool. The lead is the only writer during coordinated work, so no helper or lock is required. If several independent processes can write the same journal, serialize them through the host's own file edit or a lock command available on that system; do not add a bundled script. Repeating an event ID with the same payload is a no-op; conflicting reuse is an error. A completion event may precede any derived summary: read the event and verify evidence rather than redoing the effect.

## CONTINUE

Read the journal and task artifacts and compare them with the actual working tree. For a controlled run, also reconcile `research/dev-lead/` state, subagent run IDs, launch intents, artifacts, result envelopes, HEAD and index. A recorded status or an incomplete companion journal proves neither completion nor absence of an effect. Preserve unresolved questions. Missing evidence is a recorded blocker until reconciled; never automatically replay an uncertain launch, migration or commit.

Standalone calls keep ordinary dialogue and existing approval gates. Their journal records the same semantic outcomes, not a JSON envelope in every reply. Pass the same journal path at every handoff. Companion instructions alone cannot guarantee a complete manual journal; takeover must check the artifacts.
