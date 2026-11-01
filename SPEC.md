# nxs

## Goal

Provide self-contained development skills for explicit, bounded work with coding agents, from investigating uncertainty through approved implementation, independent review, optional project specs and authorized atomic commits.

## Architecture

The catalog has seven independently installable skills: `rnd-grill`, `rnd-debug`, `dev-exec`, `dev-review`, `dev-spec`, `dev-commit` and `nxs-setup`. The direct development flow is investigation or a clear request into execution, then review with selected corrections returning to execution, optional project-spec recording and authorized commits. Setup is outside that chain. [ADR 0009](docs/adr/0009-seven-skill-direct-flow.md) supersedes the former coordination and mandatory journaling design while retaining historical records.

`rnd-grill` owns proportionate investigation and direct approved preparation/domain saves. Evidence methods and isolated experiments are chosen for the question, not hidden stages. `dev-exec` owns plan approval, optional decomposition, tickets and handoffs. Review writes its report and returns selected findings directly, not tickets. Resources are bundled within each skill; only actual shared consumers carry byte-identical copies. Installed skills depend on neither another installation nor this checkout.

Project specs record material intent established by built work. In normal execution, only `dev-spec` writes project `SPEC.md` or private `.SPEC.md`; applicable readers inspect specs along the affected directory tree. A lowercase feature `spec.md` is preparation context, not built-work proof. Domain terminology belongs in [GLOSSARY.md](GLOSSARY.md) and decisions in `docs/adr/`.

## Boundaries

An artifact, status, finding selection or approval for one operation never implicitly starts or authorizes another. An existing instruction explicitly covering several operations can be reused within its actual scope. Execution requires approval of a concrete plan; material scope, contract or settled-decision changes return for approval. Small work requires no feature record, ticket, task directory or journal. Existing records and execution prohibitions are preserved, not silently migrated.

`nxs-setup` audits a concrete goal, project or global configuration and applies an exact approved package; readiness is report-only and concerns relevant prerequisites. Setup does not install the catalog, offer companion bundles or silently replace installations/settings. Discussion and ordinary execution require no native workers. Independent review retains its native finder/verifier roles and permitted trivial direct pass, without a separate coordination stage or nested client fallback.

Ticket execution checks prerequisites in the selected working tree and environment, not merely status or ancestry. Human-step return requires actual result verification. An install, migration or external action requires concrete action/target approval plus native permissions. Uncertain effects, including interrupted commits, must be reconciled before retrying.

Checkpoints are optional and require explicit commit-scope approval through the `dev-commit` safety procedure; see [dev-exec](skills/dev-exec/SPEC.md). Review and spec inputs cover intended net work, including relevant committed checkpoints and remaining staged, unstaged and untracked changes. A nonempty index does not narrow a task. Pin baseline, requirements and actual source snapshot first; explicit narrower scope stays narrow. An agreed earlier baseline can cover work already on the normal base. Missing coverage or ambiguous ownership stops the affected stage without staging, stashing or rewriting foreign work.

Reviewers use host-enforced read-only restrictions where available; otherwise report prompt-only restrictions. Mandatory repository-state comparisons remain necessary in both cases, stop incomplete on failure or detected change, and preserve all unfamiliar work. They detect persistent differences, not every attempted or reverted write. Missing reviewer results never imply a complete sweep. A selected fix requires confirmation before implementation; non-reproduction is not a silent fix or rejection.

Required verification must pass before a ticket resolves. Explicit implementation-only boundaries leave prohibited checks NOT RUN and required verification unresolved. Implementation without a commit is valid. Source changes do not publish or modify installed copies, user configuration or task data.

## Known limitations

Source contracts and shell checks establish neither native registration, permission enforcement nor live end-to-end behavior. The simplified flow, setup/upgrade and current reviewer route require separate observations. [Client scenarios](tests/client-scenarios.md) distinguish current protocols from version-specific historical evidence; old observations are not evidence for changed resources.

A private `.SPEC.md` exists only in its working tree; a fresh clone or `git clean -x` loses it. Spec input excludes its own output and task artifacts. Saved handoffs preserve usable context, not guaranteed cross-client session recovery. Historical coordination records activate no removed workflow and grant no fresh authorization.

## Rationale

Seven user intents retain distinct write and approval boundaries without a mandatory decision/spec/ticket pipeline. Direct saving and optional decomposition keep useful engineering behavior while removing coordination overhead. Independent review and commit safety remain separate from implementation. Actual prerequisite and intended-work evidence prevent status, staging or checkpoint history from being mistaken for completion. Self-contained resources support independent installation; verification claims remain limited to observed cases.
