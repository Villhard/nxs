# Triage labels

The skills speak in canonical triage roles. This file maps each role to the value used in the tracker.

| Role in mattpocock/skills | Value in this tracker | Meaning |
| --- | --- | --- |
| `needs-triage` | `needs-triage` | A maintainer needs to evaluate the issue |
| `needs-info` | `needs-info` | Waiting for more information; an open `[NEEDS CLARIFICATION: ...]` sits in the ticket |
| `ready-for-agent` | `ready-for-agent` | Fully specified, ready for an agent |
| `ready-for-human` | `ready-for-human` | Needs a human: set by the executor under `## Done when` for a migration, a dependency install or an external check; after the step the human sets it back to `ready-for-agent` and reruns `/plan` |
| `wontfix` | `wontfix` | Will not be actioned |
| `resolved` | `resolved` | Done: set by the executor under `## Done when`, or by `/wayfinder` for a decision ticket |
| `claimed` | `claimed` | Taken by a `/wayfinder` session; decision tickets only |

When a skill names a role, such as "apply the AFK-ready triage label", use the matching value from this table.

The local Markdown tracker has no real labels: the value goes on the `**Status:**` line of the issue file.

Edit the middle column to match the vocabulary you use.
