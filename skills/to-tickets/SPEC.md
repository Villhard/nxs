# to-tickets

## Purpose

Turn an approved feature spec, confirmed eligible root cause or selected current review findings into bounded implementation tickets independently of execution. Preserve existing decisions and execution history so repeated slicing cannot silently reopen, replace or authorize work.

## Ownership

Own the shared ticket rules and template, including their executor contract. Legacy `dev-rnd`, `dev-bug` and `dev-review` producers bundle byte-identical copies while retaining their own entry gates. The checker enforces shared-copy agreement and the setup tracker's execution-block copy. Bundle project-spec reader and journal/controlled-run resources unchanged so independent installation needs no other installed skill.

## Boundaries

Explicit invocation or an explicit controlled scope permits preparation of tickets from an eligible source. Writes are limited to authorized local implementation tickets and applicable task journal records. Source/local specs, decision/map histories, product code, domain/project specs, Git/index, settings, installations and remote records remain unchanged, except for the narrowly authorized review report ticket links. Ticket creation starts no execution, review or commit; lead chooses subsequent stages in a controlled run.

## Contracts

- For feature-spec input, consume a prepared source with approval evidence and a compatible authorized local feature `spec.md`. Established feature paths take precedence over defaults; external input stays unchanged. Source identity and exact-content hashes preserve provenance, not approval. Missing source, incompatible local/external specs or material unresolved questions stop new tickets; draft approval never answers those questions.
- Read every existing issue before proposing a breakdown. Covered implementation tickets retain their bytes, identities, dependencies, branches, statuses, checked criteria, plans and comments, including open, resolved and rejected work. Reuse is a no-op; renewed rejected scope or an incompatible graph needs approval of a concrete revision. Genuinely new authorized work appends after the highest existing number without renumbering history.
- A map directory requires explicit permission for distinct implementation scope there; otherwise use a distinct implementation feature. Preserve map files and every bare or Markdown-bold `Type:` decision file, exclude those files from implementation coverage and execution, and count their numbers when appending.
- Carry the spec's requirements, conditions, defaults, exclusions, answers, rationale and testing requirements into independently demonstrable end-to-end tickets with observable positive and blocking criteria. Small work normally yields one ticket. New numbering follows dependency order; controlled tickets use the exact approved feature branch. Show the breakdown, branch lines and created versus preserved paths before saving, reusing approval only within its covered content, destination and scope.
- Preserve known open local prerequisites as explicit gates. Remote blockers require evidence and verified local mappings when open; unknown or unmapped blockers stop creation. A resolved prerequisite needed now requires inspection and a focused check of its working-tree result. Missing evidence stops the affected ready handoff without reopening or implementing the prerequisite.
- Recheck source and existing issue bytes before saving, reconcile concurrent changes, and verify saved tickets against the approved breakdown and preserved history. Journal source/spec pins, approval scope, created/reused paths and dependency evidence without rewriting unchanged specs or tickets. Keep the template's complete English `## Done when` verbatim and existing execution text unchanged on repeats.
- Confirmed causes require supported reproduction, classification and regression direction; selected review findings require a current pinned report, approved selection and grouping. Both paths preserve existing ticket history and stop on missing evidence.
- Suggest `/dev-exec <ticket-path>` only for the first ready non-decision implementation ticket with resolved, inspected prerequisite results and no material open questions. Open dependencies and missing evidence have no ready handoff; resolved/rejected repeats create no new execution. The shared ticket contract supports both `dev-exec` and the retained `/plan` route, including branch selection, blocker-result checks, the human round trip and the no-commit boundary.

## Known limitations

Diagnosis and selected review findings also retain their existing producers and legacy `/plan` handoffs. Separate Codex fixture observations do not establish a complete route, native registration or compatibility with other clients. Source inspection and packaging checks do not authorize installation replacement.
