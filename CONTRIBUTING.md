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

Journal resources (`references/task-journal.md`, `references/controlled-run.md` and `scripts/journal.py`) are copied from `dev-lead` into `dev-rnd`, `dev-bug`, `dev-review`, `dev-spec` and `dev-commit`. Propagate canonical edits byte-for-byte. Runtime helpers needed by the native CLI review adapter are also bundled in `dev-review`; keep their copies identical to `dev-lead`. No installed skill may depend on a developer checkout or another skill's installation path.

The `## Done when` block of `skills/to-tickets/assets/ticket.md` is also copied into the fenced block of `skills/dev-setup/assets/issue-tracker.md`; update it by hand.

`rnd-grill` owns `references/discussion.md` and `references/domain-modeling.md`; copy edits byte-for-byte into `to-decision`. Both new commands also consume unchanged project-spec reader copies from `dev-rnd`, and journal/controlled-run/helper copies from `dev-lead`. The checker lists every consumer. Keep both commands explicit through `disable-model-invocation: true` and `allow_implicit_invocation: false`; direct domain-document requests are supported within an expressly invoked or controlled scope, without a wrapper artifact.

`to-spec` bundles unchanged discussion rules from `rnd-grill`, project-spec reader rules from `dev-rnd`, and journal/controlled-run/helper resources from `dev-lead`. Its `references/feature-source.md` owns the independent spec input/location rules; the legacy feature-directory reference keeps its consumers. All three feature spec template copies stay byte-identical. Keep the new command explicit through both invocation policies; adding it does not switch the manual or coordinator route.

`to-tickets` owns the shared ticket rules/template; legacy producers keep identical bundled copies and their current routes. Its feature-spec entry owns `references/spec-input.md`, with unchanged project-spec reader resources from `dev-rnd` and journal/controlled-run/helper resources from `dev-lead`. Include it in the checker catalog and every applicable shared fixture, and keep both invocation policies explicit. The executor handoff remains `/plan` until the separate executor cutover; no installed copy is replaced by source edits.

`dev-exec` owns its execution-context reference and bundles unchanged ticket rules/template from `to-tickets`, project-spec reader from `dev-rnd` and journal/controlled-run/helper resources from `dev-lead`. Include it in both explicit invocation policies and applicable checker/shared-copy fixtures, including all-consumer edit loops. Its additive entry does not change generated `/plan` handoffs, the setup tracker block or legacy routes. Keep approval gates in the skill and ticket semantics in their bundled references; native permissions remain independent of instructions.

Keep process rules with their owning skill or role; a rule several skills apply goes into one shared reference instead of divergent copies. Keep personal preferences in client/project instructions; the exception is a setup skill, which may write rules and config into client instructions only through a diff the user approved. Do not add background skills, cross-skill injection or client hooks. Add a skill only for a distinct, settled intent used regularly that deserves its own entry; otherwise extend an existing skill.

## NAMES

A skill name is a command the user types, so it is chosen to be read at a glance, not to follow a naming scheme.

- Take `dev-` plus one short lowercase word: `dev-review`, `dev-commit`. The prefix is the namespace that keeps the name clear of companion skills and client built-in commands; check a candidate against the shared agents directory and the client before proposing it.
- Prefer the shortest word the user already says for the work. A verb is welcome and not required: `dev-rnd` and `dev-spec` stay because the user reads them faster than a rewritten action name. Rename an existing skill only when its name hides what the skill does, and state the cost before the user decides.
- Keep the word for the artifact the skill reads or writes (`spec.md`, `SPEC.md`) and do not move it onto another skill.
- Add a second word only when the one-word candidate is taken or would be misread.

The reasoning and the rejected alternatives are in [ADR 0007](docs/adr/0007-skill-names.md).

The approved independent-workflow naming extension adds `rnd-` for investigation/discussion and `to-` for producing a named artifact. `rnd-grill` and `to-decision` are additive candidates under that extension; the existing `dev-` routes and installation behavior remain available. Naming does not activate another workflow stage.

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
python3 -m unittest discover -s tests -p 'test_*.py' -v
bash .github/scripts/lint-house-style.sh
git diff --check
```

The checker supports three read-only comparisons:

| Arguments | Compared state |
| --- | --- |
| none | Working files against HEAD |
| `--staged` | Index against HEAD |
| `--base REF --head REF` | Two Git snapshots |

The first two require HEAD. It validates the skill set, frontmatter contracts, invocation policy, role files, identical shared copies, the tracker's Done when copy, links that stay inside their skill and resolve, and the CHANGELOG entry shape. Link checks do not cover anchors or every Markdown form: inspect links, headings and the final diff yourself. Pass untracked Markdown paths explicitly to the style script.

The [pre-commit hook](.githooks/pre-commit) runs the staged check in every client. Enable it once per clone with `git config core.hooksPath .githooks`.

The sequential lead and controlled-run adapters target Claude Code, Codex and OpenCode v2. Discover native skills/models rather than hardcoding names or effort support. Codex uses app-server; Claude uses Agent SDK control metadata; OpenCode uses its native HTTP catalog after plugin readiness. Preserve native permissions and enforce repository write denial for read-only workers. State live verification separately from protocol fixtures; missing CLI never implies a verified live route. Tests use disposable repositories and fixture-only approvals, never the user installation.

For behavior changes, use disposable projects and the [client scenarios](tests/client-scenarios.md); documentation-only edits need source, command and link checks, not repeated workflows.

## LOCAL DEVELOPMENT AND RELEASE

Preview a candidate in a disposable agents directory:

```bash
home=$(mktemp -d)
HOME="$home" npx skills@latest add "$PWD" -g -y -s '*' -a claude-code
```

Run the client against that `HOME`, then remove the temporary directory, keeping credentials out of Git. Repeat the add after edits to refresh the copies. The temporary home has no usual authentication or global settings; sign in if needed.

Publish by pushing to `main` before updating installations; users update with `npx skills update`. Do not modify the user's installed skills during source edits unless requested.
