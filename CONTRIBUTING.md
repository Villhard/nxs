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

A skill may link only to files inside its own directory. Files shared by several skills are copied into every consuming skill and must stay byte-identical; the check enforces this. Edit the `dev-rnd` copy, then propagate:

```bash
cp skills/dev-rnd/references/ticket.md skills/dev-bug/references/ticket.md
cp skills/dev-rnd/references/ticket.md skills/dev-review/references/ticket.md
cp skills/dev-rnd/references/feature-directory.md skills/dev-bug/references/feature-directory.md
cp skills/dev-rnd/references/project-specs.md skills/dev-bug/references/project-specs.md
cp skills/dev-rnd/references/project-specs.md skills/dev-review/references/project-specs.md
cp skills/dev-rnd/references/project-specs.md skills/dev-spec/references/project-specs.md
cp skills/dev-rnd/assets/spec.md skills/dev-bug/assets/spec.md
cp skills/dev-rnd/assets/ticket.md skills/dev-bug/assets/ticket.md
cp skills/dev-rnd/assets/ticket.md skills/dev-review/assets/ticket.md
```

Keep process rules with their owning skill or role; a rule several skills apply goes into one shared reference instead of divergent copies. Keep personal preferences in client/project instructions; the exception is a setup skill, which may write rules and config into client instructions only through a diff the user approved. Do not add background skills, cross-skill injection or client hooks. Add a skill only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing skill.

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

Run from the repository root with Git, Bash and Python 3 available:

```bash
bash .github/scripts/check-skills.sh
python3 .github/scripts/test_check_skills.py
bash .github/scripts/lint-house-style.sh
git diff --check
```

The checker supports three read-only comparisons:

| Arguments | Compared state |
| --- | --- |
| none | Working files against HEAD |
| `--staged` | Index against HEAD |
| `--base REF --head REF` | Two Git snapshots |

The first two require HEAD. It validates the skill set, frontmatter contracts, invocation policy, role files, identical shared copies, links that stay inside their skill and resolve, and the CHANGELOG entry shape. Link checks do not cover anchors or every Markdown form: inspect links, headings and the final diff yourself. Pass untracked Markdown paths explicitly to the style script.

The [pre-commit hook](.githooks/pre-commit) runs the staged check in every client. Enable it once per clone with `git config core.hooksPath .githooks`.

For behavior changes, use disposable projects and the [client scenarios](tests/client-scenarios.md); documentation-only edits need source, command and link checks, not repeated workflows.

## LOCAL DEVELOPMENT AND RELEASE

Preview a candidate in a disposable agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Run the client against that `HOME`, then remove the temporary directory, keeping credentials out of Git. Repeat the add after edits to refresh the copies. The temporary home has no usual authentication or global settings; sign in if needed.

Publish by pushing to `main` before updating installations; users update with `npx skills update`. Do not modify the user's installed skills during source edits unless requested.
