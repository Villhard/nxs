# SPEC INPUT

Read before consuming a feature spec or selecting ticket storage. This entry consumes a prepared spec; a clear request or decision that still needs a spec returns to feature preparation without writing tickets. Diagnosis and review inputs require their separately verified entry contracts.

## SOURCE AND LOCATION

Read an explicit local source first; a missing or unreadable file stops instead of becoming a new request. Validate its requirements and source/approval evidence against the requested scope and relevant current project facts. Retain conditions, defaults, exclusions, answers, rationale and testing requirements. Ask only about material gaps or contradictions, not settled decisions.

Use the established feature directory and local `spec.md`; existing paths take precedence over new defaults. An external source remains unchanged. If no compatible authorized local spec exists, stop for feature spec preparation before creating tickets: the retained ticket executor reads the feature's local spec. If local and external specs disagree, show the concrete discrepancy and require its resolution; this skill does not overwrite either spec.

A map directory holds decision work. Use a distinct implementation feature unless an explicit instruction names distinct implementation scope in that existing directory. Such permission leaves map files and all bare or Markdown-bold `Type:` decision files byte-identical and never authorizes their execution. If the destination is ambiguous, ask before writing.

Local tickets remain under `.scratch/<feature-slug>/issues/NN-<slug>.md`. Do not consult tracker-backend preferences, run setup or publish/synchronize remote records. Record actual local source and spec paths with SHA256 hashes of their bytes; remote/pasted material retains original identity and hash of the exact read/supplied content, naming the snapshot. Hashes establish provenance, not approval.

## READINESS

Read the source and local feature spec completely, and `root-cause.md` if present. An open material `[NEEDS CLARIFICATION: ...]` or other material unresolved question, contradiction or missing source evidence stops new ticket creation. Name the missing fact/decision and its consequence. Permission to save a draft is not an answer. Preserve existing tickets on that stop.

For a remote spec, read the key/URL through an available read interface; if unavailable, request pasted content and stop until supplied. Establish source identity, applicable parent decisions/comments or evidence that no parent applies, and blocker state. An omitted blocker field or ready label does not establish absence of dependencies.

| Remote blocker evidence | Required treatment |
| --- | --- |
| Unknown or unmapped | Stop before creating tickets; name missing evidence. |
| Known open with verified local mapping | Read the mapped ticket, preserve its local dependency and gate the affected work. |
| Verified closed | Retain supporting evidence as satisfied context; check any local result needed by the handoff. |

Never equate remote and local issue numbers or synchronize their statuses. A known dependency without the result needed now is not a runnable prerequisite. Inspect actual working-tree results rather than relying on a resolved label, branch or commit history. Known future work remains an explicit dependency, not manufactured readiness.
