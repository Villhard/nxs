# Companion automation requires a verified execution contract

Manual invocation of mattpocock/skills keeps each upstream skill's dialogue, approval gates and outputs. An unmodified companion skill is not required to emit nxs worker outcomes or JSON. Shared journal instructions remain useful, but their presence alone does not establish a complete history; takeover follows the reconciliation rule in the [task journal decision](0002-shared-task-journal.md).

Autonomous invocation through the lead requires a supported, verified integration for the particular skill. Define its input context, completion conditions, question relay, expected artifacts and structured runner outcome: `done`, `needs_input` or `blocked`. This is the nxs execution contract around the invocation, not an assumed upstream contract. Skill discovery establishes availability, not workflow compatibility. A context-dependent skill must receive the relevant agreed decisions and evidence explicitly when launched in a fresh session.

The baseline workflow remains usable with nxs alone. Establish the [sequential cycle and recovery](0005-bounded-runs-and-recovery-first.md) before adding companion integrations. This decision does not require editing or replacing installed companion skills.

## Future investigation

Study how the user actually uses mattpocock/skills, identify the useful parts and overlap with nxs, and assess bringing selected skills into nxs under contracts aligned with the user's workflow and vision. Adoption may include changes and need not include the whole skillset. The selection, changes and maintenance approach remain undecided; this is a follow-up investigation, not approval of a particular migration.
