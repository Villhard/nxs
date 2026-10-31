# nxs

## Goal

Provide self-contained development skills for explicit, bounded work with coding agents, from investigation and decisions through execution, review, project specifications and atomic commits.

## Architecture

The source catalog contains 19 target commands. Discussion, decisions, feature specifications, tickets and execution are separate operations; research, diagnosis, prototyping, design, audit, mapping, handoff, questionnaires, retrospective and setup can also stand alone. A saved artifact or an approval for one stage does not itself authorize the next. Skills bundle the references they need, so an installed skill does not depend on another installed skill or this checkout.

`nxs-lead` coordinates entrusted work using the selected client's native subagent facility; the lead independently checks results and retains approval and permission boundaries. The retained `dev-lead` and `dev-review` routes also use native subagents. Native client permissions remain independent of instructions. See [ADR 0008](docs/adr/0008-native-subagent-coordination.md).

Project specs record durable intent established by built work. `dev-spec` alone writes `SPEC.md` or private `.SPEC.md`; other skills read the applicable specs along the directory tree. Feature records and decision logs preserve task context and evidence separately. Domain terminology belongs in [GLOSSARY.md](GLOSSARY.md) and decisions in `docs/adr/`.

The source retains `dev-rnd`, `dev-bug`, `dev-lead` and `dev-setup` as legacy routes alongside the target catalog. The transition is additive: legacy callers, `/plan` handoffs and installed copies are not switched by source presence. `dev-review` retains its existing ticket route as well as the separate `--to-tickets` selection route.

## Boundaries

`nxs-setup` audits a selected goal, project or global configuration and applies an approved change package; readiness is report-only. It neither requires nor offers companion bundles. The retained `dev-setup` has its own legacy bundle behavior. Neither route silently replaces an installed skill; provenance, user changes and authorization matter for any replacement.

Ticket executors check that prerequisite results exist in the working tree, not merely that blockers are marked resolved. A human step returns through `ready-for-agent` and the executor checks evidence before continuing. Controlled runs additionally carry approved scope and result boundaries; a journal path alone does not activate one.

The repository has shell structural and runtime-removal checks. The former bundled orchestration runtime, Python files and automated tests have been removed. Client scenarios are evidence and manual verification guidance, not an automated test suite.

## Known limitations

Source presence and passing shell checks do not establish native registration or a complete live workflow. Claude Code native delegation, candidate setup and upgrade, guarded auto and final route cutover remain unverified. Recorded Codex and OpenCode native-subagent observations cover only the cases in [client scenarios](tests/client-scenarios.md), not end-to-end coordination or enforced read-only permissions.

A private `.SPEC.md` exists only in its working tree; a fresh clone or `git clean -x` loses it. `dev-spec` does not see work already committed on the base branch and excludes project spec files from its built-work input. Recovery requires evidence of uncertain effects and does not authorize replay merely because a result is missing.

Legacy retirement and installation replacement depend on route-specific evidence and are not complete. Historical records remain evidence; the removed runtime does not guarantee recovery of former sessions. Shell checks are structural, not proof of client behavior or complete metadata validity.

## Rationale

Independent commands let a user stop after a useful decision or artifact and choose the next step without mandatory development. Native delegation avoids maintaining a separate orchestration engine, while explicit result checking and preserved legacy routes limit the cost of unverified client capabilities. Checking blocker results in the working tree handles reverted, squashed and cherry-picked work without treating status or ancestry as proof. Self-contained copies support independent installation; shell checks detect drift without restoring the removed runtime.
