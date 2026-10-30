# TASK JOURNAL

Read before a task's first durable write, a material question or a handoff, in controlled and standalone use. Resolve the feature from an explicit task/ticket path or unambiguous context; ask when several fit. A branch alone is insufficient. A review without a feature uses its resolved `.scratch/reviews/<branch-slug>/` directory. Taskless setup, an empty review and a declined write proposal create no journal.

## RECORD

Append meaningful decisions, questions, answers, stage completions, blockers and handoffs to `<feature>/decision.log` as JSONL. Use a unique event ID, timestamp, kind, step ID, concise conclusion and relative evidence/artifact links. Keep specs, tickets and review contents in their own files. Exclude secrets and full conversations. A question includes its exact text; an answer links the question ID; approval pins the approved artifact's hash and scope. Record intent before a side effect and completion only after checking its result.

Use the bundled `scripts/journal.py` with Python 3 for locked append and atomic state operations; consult its `--help` for the installed interface. Copies in consuming skills are identical and have no dependency on another installation. Repeating an event ID with the same payload is a no-op; conflicting reuse is an error. A completion event may precede the state snapshot: recover from the event and verify evidence rather than redoing the effect.

## CONTINUE

Read the journal and task artifacts and compare them with the actual working tree. For a controlled run, also reconcile `research/dev-lead/` state, session IDs, launch intents, processes, events, result files, HEAD and index. A recorded status or an incomplete companion journal proves neither completion nor absence of an effect. Preserve unresolved questions. Missing evidence is a recorded blocker until reconciled; never automatically replay an uncertain launch, migration or commit.

Standalone calls keep ordinary dialogue and existing approval gates. Their journal records the same semantic outcomes, not a JSON envelope in every reply. Pass the same journal path at every handoff. Companion instructions alone cannot guarantee a complete manual journal; takeover must check the artifacts.
