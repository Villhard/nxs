# MAP AND DECISIONS

## STORAGE

Use an explicitly supplied map in place. Otherwise create `.scratch/<effort-slug>/map.md` and `.scratch/<effort-slug>/issues/`; choose a short lowercase hyphenated slug and inspect the destination before writing. Preserve existing artifacts and avoid overwriting another effort. Use [map template](../assets/map.md) and [decision template](../assets/decision.md) for new files. Respect existing map paths and history on resume.

Each decision is `issues/NN-<slug>.md`, numbered in ascending order from 01; choose the next unused number, never renumber or reuse history. `Type: research`, `prototype`, `grilling` or `task` distinguishes decision work from implementation tickets. Record `Status: open`, `claimed` or `resolved` and `Blocked by: NN, NN`; no implementation Branch, triage status or Done when is implied. Create all new files first, then wire actual blocker numbers. Link human-facing references by title.

## FRONTIER AND HISTORY

The frontier consists of open, unclaimed decision files whose every listed blocker exists and is resolved. Scan the issues directory; ignore implementation tickets. In the absence of an explicitly selected eligible decision, present the first numeric frontier question for permission. A selected blocked, claimed or unknown decision is not eligible; report its cause and do not claim it. Persist the claim before work; do not take a claimed item from another session. Reconcile an interrupted claim with its actual state and owner instead of resetting it automatically.

On resolution, preserve the question, type, blockers, existing answers and evidence; append `## Answer`, set resolved and add a title link plus short gist to the map index. Revisit a resolved answer only for contradictory evidence or a user request; preserve its history. A question already answered is not recreated. Closed out-of-scope work stays outside the route index and is linked with its reason in Out of scope. Never graduate it into a decision merely by resuming.

Not yet specified holds in-scope fog that is not yet a precise question. Move only a newly precise question into a new decision file and remove that corresponding fog entry. Existing saved decisions, open questions and blockers keep their identities. Preserve private data and avoid secrets or full transcripts in artifacts.
