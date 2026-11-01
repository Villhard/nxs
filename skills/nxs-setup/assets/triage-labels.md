# Triage labels

The skills speak in canonical triage roles. This file maps each role to the value used in the tracker.

| Role | Value in this tracker | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | A maintainer needs to evaluate the issue |
| `needs-info` | `needs-info` | Waiting for more information; an open `[NEEDS CLARIFICATION: ...]` sits in the ticket |
| `ready-for-agent` | `ready-for-agent` | Fully specified, ready for an agent |
| `ready-for-human` | `ready-for-human` | A required install, migration or external action lacks concrete action/target approval, native permission or checkable results. Record the action and expected evidence; after the human step, return to `ready-for-agent` and have the executor verify the actual environment before continuing. |
| `wontfix` | `wontfix` | Will not be actioned |
| `resolved` | `resolved` | Done: set by the executor only after all criteria and required checks pass under `## Done when` |

When a skill names a role, such as "apply the AFK-ready triage label", use the matching value from this table.

The local Markdown tracker has no real labels: the value goes on the `**Status:**` line of the issue file.

Edit the middle column to match the vocabulary you use.

Existing typed decision records and their statuses remain read-only context, not implementation tickets. Do not convert, relabel or clean up their history as part of setup.
