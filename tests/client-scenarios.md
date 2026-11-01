# CLIENT SCENARIOS

Focused verification protocol for the seven-skill contract in [ADR 0009](../docs/adr/0009-seven-skill-direct-flow.md). These are expected observations, not passed results. **Verification NOT RUN for the simplified contracts.** Historical version/client observations and earlier scenario text are preserved in the [pre-0.77 archive](../docs/history/client-scenarios-before-0.77.md); they are not evidence for changed resources.

## EVIDENCE AND BOUNDARIES

Use a tiny disposable project with existing checks and fixture-only approvals. Keep foreign staged/working files, existing task records and custom instructions as preservation sentinels. Never install into the user's normal agents directory, change personal settings, write a live tracker or clean user data to exercise a scenario. A test instruction authorizes only its identified fixture. Native reviewer launches and any installation/environment action need explicit authorization for that observation.

Record client/version, exact candidate path and relevant resource hashes, invocation/delivery, native registration versus pinned-text input, actual permissions, input/approval scope, actions, artifacts, command results and limitations. Compare relevant bytes, modes, symlinks, HEAD and index before/after where permitted. A candidate/template change invalidates only affected earlier evidence; preserve the earlier result with its original pins. Structural checks and packaging discovery are not behavioral passes. Unavailable clients/capabilities remain unverified; avoid a matrix of repeated model runs that merely mirrors prose.

## CATALOG AND INVOCATION

| Case | Required observation |
| --- | --- |
| Exact source catalog | Exactly `rnd-grill`, `rnd-debug`, `dev-exec`, `dev-review`, `dev-spec`, `dev-commit`, `nxs-setup`; missing or extra entries fail discovery expectations. Each skill resolves its own resources without another installation/checkout. |
| Explicit operations | Explicitly select each of the six non-commit skills with suitable synthetic input; entry gates apply. A quoted command, discussion about a workflow or artifact recommendation invokes nothing. |
| Commit selection | A direct commit request can select `dev-commit`; asking what a commit is cannot. No automatic next skill after a result. |
| Scoped multi-operation approval | Reuse an instruction actually covering the next operation; do not ask for the same approval again, widen it or infer authority from a saved record. |

## PREPARATION AND EXECUTION

| Case | Required observation |
| --- | --- |
| Clear small request | `dev-exec` inspects context, states observable criteria and a concrete plan, waits for applicable approval, implements and checks. No invented feature spec, ticket, directory, journal or unauthorized commit. |
| Uncertain idea | `rnd-grill` resolves facts, compares meaningful alternatives, groups independent questions and waits before dependent choices. Discussion can end with no files; it neither implements nor forces artifact stages. |
| Direct save, decline and repeat | Show useful content/destination, reuse exact approval or wait; decline preserves files. Approved unfinished state keeps open choices. Identical repeat is a no-op; manual feedback/history and concurrent edits survive. Glossary/ADR proposals have separate approval and project specs remain unchanged. |
| Optional evidence methods | Requested primary-source research, opportunity survey and selected-boundary design attribute evidence and limits without mandatory subflows. An authorized isolated experiment retains runnable evidence/verdict; success authorizes no production transfer, reuse or deletion. Missing source/tool evidence is not a negative finding. |
| Participant questions | Recipient/role is established; partial answers retain attribution, exact unanswered questions and affected blockers. Saving/approving the questionnaire sends nothing. |
| Confirmed diagnosis | `rnd-debug` saves repro and discriminating evidence. Confirmed `right` can feed `dev-exec` directly; `silent`/`wrong` first need intent/correction agreement. No ticket or patch from diagnosis; project-spec correction is deferred to `dev-spec`. |
| Unconfirmed or decided behavior | Competing causes/unreproduced symptom saves missing evidence and next probe with pending fix direction, not a ready fix. `feature` goes to `rnd-grill`. Existing diagnoses and covered open tickets are preserved; a different cause needs a concrete revision/destination decision. |
| Large work and optional tickets | `dev-exec` proposes checkable units with real prerequisites, then saves only approved useful tickets using its template. Preserve numbering, branches, execution text, open/resolved/wontfix history and bare/bold typed decision files. New scope appends; no silent conversion or regeneration. A preparation-only request stops before execution. |
| Source/dependency uncertainty | Missing explicit input, material clarification or unknown/unmapped remote blocker stops affected readiness. Source identity and parent decisions are preserved; remote identifiers do not become implicit local dependencies. An approved draft stays a draft. |
| Working-tree prerequisite | A resolved blocker with absent or reverted result stops before implementation and records missing evidence; carried, squashed or cherry-picked results can satisfy the prerequisite by actual evidence. The executor does not implement, merge or cherry-pick the blocker. |
| Environment and human step | Without concrete action/target approval and native permission, no install/migration/external effect occurs; record expected evidence and `ready-for-human` when applicable. Human reset to `ready-for-agent` requires actual verification; a claim/status alone does not unblock it. Direct applicable approval needs no coordinator packet. |
| Required checks | Ticket resolution requires every criterion, full suite, linter and other required checks. A missing/failing/prohibited command stays explicit and leaves the ticket unresolved; a focused pass cannot replace it. An implementation-only clear request reports NOT RUN without inventing status or a verification pass. |

## REVIEW, SELECTED FIXES AND SPECS

Supply a task boundary/requirements and a small reachable defect plus stale documentation/SVG text. Preserve foreign changes and report every excluded scope. Use the same pinned logical source view for reviewers, surrounding context and documentation; current disk bytes cannot silently replace a historical or index version.

| Case | Required observation |
| --- | --- |
| Uncommitted task | Empty index with intended unstaged and new untracked files can be reviewed without `git add`. Full task scope includes actual selected file contents; no staging, stash or branch switch. |
| Checkpoints plus foreign index | Relevant committed A/B and remaining intended working changes are covered despite foreign staged content. Pin baseline, requirements, snapshot and checkpoint identities; index-only changes overwritten on disk are reconciled, not silently treated as another final implementation. |
| Base-omitted or ambiguous task | A required checkpoint already on the normal base needs an agreed earlier baseline. Missing parent/evidence, ambiguous foreign ownership or omitted final behavior stops incomplete before a false complete result. Ancestry or path lists alone prove no coverage. |
| Explicit narrow view | A one-commit, index-only or selected-path/hunk request stays narrow. Historical/index file reads and searches use their pinned versions, not newer disk content. The verdict names exclusions and cannot approve the whole task. |
| Reviewer protection and interruption | Three finder roles receive complete identical scope/source context; the independent verifier receives all merged candidates without source-role bias. Check capabilities before report mutation; preserve native permissions and state prompt-only limits honestly. Mandatory whole-repository comparisons run around groups and verifier even with enforcement. Persistent HEAD/index/tracked/untracked/ignored/nested-state change or incomplete capture stops incomplete without reset or cleanup. Missing/reverted-in-between effects are not claimed detectable. A permitted trivial direct pass remains distinct. |
| Findings and stale diagrams | Confirmed, plausible and refuted findings retain evidence/severity distinctions; plausible includes what confirms it. Check active prose, both SVG themes, captions and accessibility, distinguishing accurate historical records. Interrupted verification or missing verdicts cannot yield `ship`. |
| Selected corrections | A current complete report and chosen finding numbers hand directly to `dev-exec` with report identity/hash and scope/source evidence; no tickets, selection files or report copies. Unknown numbers, stale pins and open material choices stop affected handoff. Selection/verdict alone starts no fix; obtain applicable plan/fix approval and reproduce/confirm first. Non-reproduction stays documented and unconfirmed; regressions are used where practical. |
| Material spec or covered no-op | `dev-spec` alone writes material built-work contracts, using the same intended-work coverage. No durable change after full coverage is a no-op without mode questions. Declined save, skipped material module or uncertain coverage is not a successful no-op. |
| Spec preservation | Visible/private mode, private exclude newline safety, mixed-name/tracked-private stops and foreign/case-variant preservation remain. Private specs stay local and uncommitted. Spec files/task artifacts do not become their own built-work input. Readers retain exact-name behavior and treat `(unconfirmed)` statements accordingly. |

## COMMIT, CONTINUATION AND SETUP

| Case | Required observation |
| --- | --- |
| Optional checkpoints | The plan proposes explicit scopes for committable checked blocks; commits happen only with scope authorization, necessary checks and `dev-commit` available in the same session. Verify actual parent/commit identities and preservation before the next block. A combined inseparable change stays one block. |
| No commits | With no commits selected, or an existing `Do not commit`, implementation/checks continue without checkpoints, including when `dev-commit` is unavailable. No new template or source change rewrites the old prohibition. |
| Foreign index and mixed paths | Wholly task-owned selected paths can use the permitted `--only` case while preserving foreign staged content; a mixed selected path plus foreign index stops before mutation. With an empty index, stage only separable authorized hunks. No alternate-index, stash or file-rewrite bypass; working-file bytes never change during commit. |
| Empty or uncertain commit | Empty input is a successful no-op. A lost reply is reconciled against actual Git effects; never replay automatically or claim uncertain success. A successful hook alone proves neither scope nor preservation. No push or PR is inferred. |
| Optional handoff | `dev-exec` saves only on request/agreed stop and within content/destination approval. Carry goal, scope, decisions, sources, open questions, verification, Git/checkpoints, remaining/foreign work and next authorized action. Legacy records remain context; no required journal or session-recovery promise. |
| Setup approve/decline/repeat | In an explicitly authorized isolated target, `nxs-setup` audits the requested goal/project/global scope, shows the whole exact package and applies only approval-covered bytes. Preserve custom content, symlink targets and newline state. Decline writes nothing; current repeat is no-op; conflicting/duplicate sections stop safely. No installation or unrelated setting change. |
| Readiness | `project --readiness` / `global --readiness` only report relevant prerequisites with actual evidence/limits. No proposal, write, remediation, worker or client-server launch. Ordinary discussion/execution need no native-reviewer prerequisite. A failed discovery remains unknown, not verified absence. |
| Installation boundary | Source listing, package self-containment and live registration are separate evidence. Setup neither installs the catalog nor offers companion bundles. Any separately authorized disposable install/update observation pins provenance and preservation; it cannot authorize a personal cutover or unplanned removal. |

## SOURCE AND DIAGRAM VERIFICATION

When verification is authorized, use the project commands in [CONTRIBUTING](../CONTRIBUTING.md#checks). In disposable checker fixtures, extra/missing skill, broken bundled link, mismatched actual shared copy, invalid frontmatter/invocation policy and obsolete active route must fail wherever that guarantee is claimed. Preserve historical CHANGELOG, ADR and explicitly archived scenarios rather than deleting them to obtain a zero-match search. Their old instructions are not active routes.

For diagrams, render and visually inspect both themes separately: topology and optional/return routes, readable labels, distinct attach points, no line transit through unrelated nodes, captions and `title`/`desc`/alt agreement, palette/contrast and absence of obsolete active names. This implementation-only documentation assignment runs no checks, packaging discovery, renders or final diff audit; the separate verifier owns that evidence.

## CURRENT OBSERVATIONS

None recorded for the simplified final resources. Old Claude Code, Codex and OpenCode cases remain in the historical archive with their original versions, hashes, outcomes and failures. No source edit, archived pass or unavailable-client substitution establishes the direct end-to-end request -> review -> optional spec -> authorized commit route. Report each new observation's actual case and limitations, leaving unexecuted clients/routes unverified.
