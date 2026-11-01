# CONTRIBUTING

Read these shared rules before editing. `CLAUDE.md` and `AGENTS.md` are equivalent entry points.

## STRUCTURE

Each skill is one self-contained directory under `skills/`, installable on its own:

```text
skills/<name>/
  SKILL.md                     # frontmatter: name, description; optional argument-hint, disable-model-invocation
  agents/openai.yaml           # optional Codex invocation policy
  references/                  # rule files read at the point of use
  assets/                      # artifact templates
  roles/                       # independent reviewer role files (dev-review)
tests/client-scenarios.md
README.md CONTRIBUTING.md CHANGELOG.md
```

A skill may link only to files inside its own directory. Copy genuinely shared resources into their actual consumers and keep the copies byte-identical. Do not depend on a developer checkout, bundled helper or another skill's installation path. The seven-skill ownership is:

| Owner | Resources |
| --- | --- |
| `rnd-grill` | Discussion, domain modeling, optional evidence/experiment guidance and direct-save decision, feature-description and questionnaire templates. |
| `rnd-debug` | Diagnosis and feature-location rules. |
| `dev-exec` | Execution context, optional decomposition, ticket rules/template and handoff guidance/template. |
| `dev-review` | Selected snapshot, findings, review report, native reviewer launch rules and four reviewer roles. No ticket producer. |
| `dev-spec` | Project-spec reader rules and project-spec template. |
| `dev-commit` | Commit safety and format. |
| `nxs-setup` | Setup templates, readiness/capability guidance and writing guidance. |

Propagate `skills/dev-spec/references/project-specs.md` to the retained readers in `rnd-grill`, `rnd-debug`, `dev-exec` and `dev-review`. The canonical ticket rules/template live only in `dev-exec`; review does not bundle them. The feature-description template belongs to `rnd-grill`, not diagnosis. Do not retain shared-copy requirements for resources with no remaining consumer.

When the setup tracker embeds `## Done when`, copy that block verbatim from `skills/dev-exec/assets/ticket.md` into `skills/nxs-setup/assets/issue-tracker.md`. Keep the structural checker's actual-consumer catalog synchronized with resource moves.

Existing user tickets, journals, decision records, prototypes and worktrees are not migration inputs to rewrite or delete. No mandatory task journal, controlled-run packet, approval hashes, lock orchestration or worker envelope belongs in the direct flow. Resolve conflicting historical instructions explicitly rather than emulating a removed mode.

Keep process rules with their owning skill or role; a rule several skills apply goes into one shared reference instead of divergent copies. Keep personal preferences in client/project instructions; the exception is a setup skill, which may write rules and config into client instructions only through a diff the user approved. Do not add background skills, cross-skill injection or client hooks. Add a skill only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing skill.

## NAMES

A skill name is a command the user types, so it is chosen to be read at a glance, not to follow a naming scheme.

- Choose a short name that describes the work and avoids client and installed-skill collisions. The retained namespaces are `rnd-` for investigation, `dev-` for development and `nxs-` for setup support.
- Check the installed path and provenance when names collide; naming does not activate another stage.

[ADR 0007](docs/adr/0007-skill-names.md) records the earlier naming decision; [ADR 0009](docs/adr/0009-seven-skill-direct-flow.md) preserves the seven retained names and supersedes the old fixed-prefix/catalog scope.

## STYLE AND SAFETY

Write concise English with ASCII hyphens and straight quotes. Use UPPERCASE instruction headings and sentence case in README and CHANGELOG. Artifact templates retain their required headings.

Keep private paths/remotes, tracker identifiers, secrets, environment values, personal contact details and raw session output out of public changes. Use neutral examples.

## INSTRUCTION CONTRACTS

README explains how to use the skills; CONTRIBUTING explains how to change them. Skills, roles and references own the full execution contract. Link to those rules instead of retelling them in guides. Keep model names and evaluation results out of guides.

- State inputs, entry checks, ordered actions, outputs, stops and handoffs. Put exceptions beside the affected step; use tables for competing states.
- Give descriptions a concrete trigger, result and distinction from neighboring commands. Separate invocation from discussion and internal operations.
- Mark required and optional template fields. Preserve structural names and distinguish completed requirements from removed ones.
- Make installed skills self-contained through bundled resources read at the point of use. Root documents are not runtime context.
- Reuse user authorization within its scope. Report missing evidence explicitly.
- Test normal use and plausible misreadings through actions and artifacts. Line count and structural lint do not prove instruction quality.

## VERSIONS

The root CHANGELOG is the only version record; skills carry no manifests. Every bundled edit, including documentation and file modes, needs a dated CHANGELOG entry under Keep a Changelog headings (`Added`, `Changed`, `Fixed`, `Removed`, `Deprecated`), one line per bullet naming the skill, role or artifact that changed. Keep every past version heading and date, newest first; past entries may be condensed but never dropped.

An unchanged contract is a patch. During `0.x`, contract changes require a minor release; after `1.0.0`, breaking changes require a major release. The versioned contract: skill names, arguments and invocation policy; role names, launch routes and context packets; artifact paths, formats and handoffs; write/Git boundaries.

## CHECKS

Run from the repository root with Git and Bash available:

```bash
bash .github/scripts/check-skills.sh
bash .github/scripts/check-no-runtime.sh
bash .github/scripts/lint-house-style.sh
git diff --check
```

The structural checker is read-only and inspects the working tree. Its catalog must contain exactly the seven README skills, not merely find them among extra commands. Keep frontmatter, invocation policies, reviewer roles, actual shared copies, tracker Done when, ticket/review handoffs, self-contained links, external-path boundaries and dated CHANGELOG entries covered. The runtime guard rejects bundled runtime files; the structural checker's obsolete-route scan covers skill sources under `skills/`, not root guides. Historical CHANGELOG, ADR and explicitly archived scenario text is not a current execution contract. Link checks do not cover anchors or every Markdown form: inspect links and headings yourself. Pass untracked Markdown paths explicitly to the style script. A source pass proves no live behavior, permission enforcement or registration.

The [pre-commit hook](.githooks/pre-commit) runs both structural checks against a temporary staged snapshot in every client. Enable it once per clone with `git config core.hooksPath .githooks`.

Only independent review requires its selected native reviewer route; ordinary discussion and execution need no subagents. Review keeps three finder roles and an independent verifier, with a direct pass only for the trivial cases its contract permits. Discover available capabilities without hardcoding models or effort support. Use host-enforced reviewer restrictions when available; otherwise report prompt-only restrictions honestly and follow mandatory before/after repository checks even with enforcement. These checks detect persistent differences, not every attempted or reverted write. No nested client is a fallback. State live observations separately from source or protocol fixtures; a missing CLI leaves that client's route unverified. Use disposable repositories and fixture-only approvals, never the user installation.

For behavior changes, use the focused [client scenarios](tests/client-scenarios.md); documentation-only edits need proportionate source, command and link checks, not repeated workflows. Review and spec cases must include committed checkpoints plus intended staged, unstaged and untracked work, with no implicit staged-only narrowing. If an approved implementation-only assignment reserves verification for another worker, do not run excluded checks, renders or final diff audit; report each as NOT RUN and leave verification pending. Otherwise inspect the final diff and verify both themes of affected diagrams, including captions/accessibility and preserved history.

## LOCAL DEVELOPMENT AND RELEASE

Preview a candidate in a disposable agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Run the client against that `HOME`, then remove the temporary directory, keeping credentials out of Git. Repeat the add after edits to refresh the copies. The temporary home has no usual authentication or global settings; sign in if needed.

Publish by pushing to `main` before updating installations; users update with `npx skills update`. Do not modify the user's installed skills during source edits unless requested.

The catalog contract contains seven skills. `rnd-grill`, eligible diagnosis and selected review findings can feed `dev-exec` directly; no artifact chain is mandatory. `dev-spec` remains optional and commits require explicit scope authorization. Source changes do not update installations or establish native registration. `nxs-setup` does not offer companion bundles or install the catalog. See [README](README.md) and [client scenarios](tests/client-scenarios.md) for the current boundary and evidence.
