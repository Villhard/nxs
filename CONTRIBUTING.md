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
  roles/                       # agent role files (dev-review)
tests/client-scenarios.md
README.md CONTRIBUTING.md CHANGELOG.md
```

A skill may link only to files inside its own directory. Files shared by several skills are copied into every consuming skill and must stay byte-identical; the check enforces this. For ticket rules and the ticket template, edit the `to-tickets` copy; `dev-rnd` owns legacy feature resources and `to-spec` owns the feature spec template. Propagate shared edits:

```bash
cp skills/to-tickets/references/ticket.md skills/dev-rnd/references/ticket.md
cp skills/to-tickets/references/ticket.md skills/dev-bug/references/ticket.md
cp skills/to-tickets/references/ticket.md skills/dev-review/references/ticket.md
cp skills/dev-rnd/references/feature-directory.md skills/dev-bug/references/feature-directory.md
cp skills/dev-rnd/references/project-specs.md skills/dev-bug/references/project-specs.md
cp skills/dev-rnd/references/project-specs.md skills/dev-review/references/project-specs.md
cp skills/dev-rnd/references/project-specs.md skills/dev-spec/references/project-specs.md
cp skills/dev-rnd/references/project-specs.md skills/dev-lead/references/project-specs.md
cp skills/to-spec/assets/spec.md skills/dev-rnd/assets/spec.md
cp skills/to-spec/assets/spec.md skills/dev-bug/assets/spec.md
cp skills/to-tickets/assets/ticket.md skills/dev-rnd/assets/ticket.md
cp skills/to-tickets/assets/ticket.md skills/dev-bug/assets/ticket.md
cp skills/to-tickets/assets/ticket.md skills/dev-review/assets/ticket.md
```

Journal resources (`references/task-journal.md` and `references/controlled-run.md`) are copied from `dev-lead` into `dev-rnd`, `dev-bug`, `dev-review`, `dev-spec`, `dev-commit`, `rnd-grill`, `rnd-debug`, `rnd-research`, `rnd-prototype`, `rnd-design`, `rnd-audit`, `rnd-map`, `to-decision`, `to-spec`, `to-tickets`, `dev-exec`, `to-questionnaire`, `to-handoff`, `nxs-retro` and `nxs-lead`. Propagate canonical edits byte-for-byte. No installed skill may depend on a developer checkout, a bundled helper or another skill's installation path.

The `## Done when` block of `skills/to-tickets/assets/ticket.md` is also copied into the fenced block of `skills/dev-setup/assets/issue-tracker.md`; update it by hand.

Shared discussion and domain references are owned by `rnd-grill`; `to-decision` and `rnd-design` bundle copies. `nxs-setup` owns writing guidance, copied into `nxs-retro`. `dev-review` owns the review report reference, copied into `to-tickets`. Keep the checker catalog and every applicable shared copy synchronized.

Keep process rules with their owning skill or role; a rule several skills apply goes into one shared reference instead of divergent copies. Keep personal preferences in client/project instructions; the exception is a setup skill, which may write rules and config into client instructions only through a diff the user approved. Do not add background skills, cross-skill injection or client hooks. Add a skill only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing skill.

## NAMES

A skill name is a command the user types, so it is chosen to be read at a glance, not to follow a naming scheme.

- Choose a short name that describes the work or artifact and avoids client and installed-skill collisions. Existing namespaces include `rnd-` for investigation, `to-` for artifact production, `dev-` for development and `nxs-` for project-wide support.
- Check the installed path and provenance when names collide; naming does not activate another stage.

[ADR 0007](docs/adr/0007-skill-names.md) records the earlier naming decision; the additive catalog extends it.

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

The structural checker is read-only and inspects the working tree. It validates the skill set, frontmatter contracts, invocation policy, role files, identical shared copies, the tracker's Done when copy, links that stay inside their skill and resolve, external-path boundaries and the CHANGELOG entry shape. The runtime guard rejects any `.py` file, bundled `scripts/` or `__pycache__` directory, and active documentation that still names Python 3, the removed terminal app or a bundled Python helper. Historical `CHANGELOG.md` entries and `docs/adr/` records keep their original text. Link checks do not cover anchors or every Markdown form: inspect links, headings and the final diff yourself. Pass untracked Markdown paths explicitly to the style script.

The [pre-commit hook](.githooks/pre-commit) runs both structural checks against a temporary staged snapshot in every client. Enable it once per clone with `git config core.hooksPath .githooks`.

The retained lead and review routes use the selected client native subagent facility. Discover available skills and models without hardcoding names or effort support; readiness uses its documented native discovery probes. Preserve native permissions and enforce repository write denial for read-only workers. State live verification separately from protocol fixtures; missing CLI never implies a verified live route. Tests use disposable repositories and fixture-only approvals, never the user installation.

For behavior changes, use disposable projects and the [client scenarios](tests/client-scenarios.md); documentation-only edits need source, command and link checks, not repeated workflows.

## LOCAL DEVELOPMENT AND RELEASE

Preview a candidate in a disposable agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Run the client against that `HOME`, then remove the temporary directory, keeping credentials out of Git. Repeat the add after edits to refresh the copies. The temporary home has no usual authentication or global settings; sign in if needed.

Publish by pushing to `main` before updating installations; users update with `npx skills update`. Do not modify the user's installed skills during source edits unless requested.

The checked catalog contains 19 target commands and four retained legacy routes: `dev-rnd`, `dev-bug`, `dev-lead` and `dev-setup`. Preserve legacy callers and `/plan` handoffs until their route-specific cutover gates pass. Source changes do not update installations or establish native registration. `nxs-setup` does not offer companion bundles; the legacy `dev-setup` contract still does. See [README](README.md) and [client scenarios](tests/client-scenarios.md) for the current boundary and evidence.
