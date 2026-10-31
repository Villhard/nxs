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

Journal resources (`references/task-journal.md` and `references/controlled-run.md`) are copied from `dev-lead` into `dev-rnd`, `dev-bug`, `dev-review`, `dev-spec`, `dev-commit`, `rnd-grill`, `rnd-debug`, `rnd-research`, `rnd-prototype`, `rnd-design`, `rnd-audit`, `rnd-map`, `to-decision`, `to-spec`, `to-tickets`, `dev-exec`, `to-questionnaire`, `to-handoff` and `nxs-retro`. Propagate canonical edits byte-for-byte. No installed skill may depend on a developer checkout, a bundled helper or another skill's installation path.

The `## Done when` block of `skills/to-tickets/assets/ticket.md` is also copied into the fenced block of `skills/dev-setup/assets/issue-tracker.md`; update it by hand.

`rnd-grill` owns `references/discussion.md` and `references/domain-modeling.md`; copy edits byte-for-byte into `to-decision`. Both new commands also consume unchanged project-spec reader copies from `dev-rnd`, and journal and controlled-run copies from `dev-lead`. The checker lists every consumer. Keep both commands explicit through `disable-model-invocation: true` and `allow_implicit_invocation: false`; direct domain-document requests are supported within an expressly invoked or controlled scope, without a wrapper artifact.

`to-spec` bundles unchanged discussion rules from `rnd-grill`, project-spec reader rules from `dev-rnd`, and journal and controlled-run resources from `dev-lead`. Its `references/feature-source.md` owns the independent spec input/location rules; the legacy feature-directory reference keeps its consumers. All three feature spec template copies stay byte-identical. Keep the new command explicit through both invocation policies; adding it does not switch the manual or coordinator route.

`to-tickets` owns the shared ticket rules/template; legacy producers keep identical bundled copies and their current routes. Its feature-spec entry owns `references/spec-input.md`, with unchanged project-spec reader resources from `dev-rnd` and journal and controlled-run resources from `dev-lead`. Include it in the checker catalog and every applicable shared fixture, and keep both invocation policies explicit. The executor handoff remains `/plan` until the separate executor cutover; no installed copy is replaced by source edits.

`dev-exec` owns its execution-context reference and bundles unchanged ticket rules/template from `to-tickets`, project-spec reader from `dev-rnd` and journal and controlled-run resources from `dev-lead`. Include it in both explicit invocation policies and applicable checker/shared-copy fixtures, including all-consumer edit loops. Its additive entry does not change generated `/plan` handoffs, the setup tracker block or legacy routes. Keep approval gates in the skill and ticket semantics in their bundled references; native permissions remain independent of instructions.

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

Run from the repository root with Git and Bash available:

```bash
bash .github/scripts/check-skills.sh
bash .github/scripts/check-no-runtime.sh
bash .github/scripts/lint-house-style.sh
git diff --check
```

The structural checker is read-only and inspects the working tree. It validates the skill set, frontmatter contracts, invocation policy, role files, identical shared copies, the tracker's Done when copy, links that stay inside their skill and resolve, external-path boundaries and the CHANGELOG entry shape. The runtime guard rejects any `.py` file, bundled `scripts/` or `__pycache__` directory, and active documentation that still names Python 3, the removed terminal app or a bundled Python helper. Historical `CHANGELOG.md` entries and `docs/adr/` records keep their original text. Link checks do not cover anchors or every Markdown form: inspect links, headings and the final diff yourself. Pass untracked Markdown paths explicitly to the style script.

The [pre-commit hook](.githooks/pre-commit) runs both structural checks in every client. Enable it once per clone with `git config core.hooksPath .githooks`.

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

`rnd-debug` is an additive diagnosis candidate. It bundles the feature-directory, spec-template, project-spec reader and journal resources; keep those copies and the checker catalog synchronized. `to-tickets` accepts eligible confirmed causes without switching `dev-bug` or the executor handoff.

`rnd-research` is an additive, explicit research candidate. Keep its project-spec reader, journal and controlled-run copies synchronized with their canonical owners and in the checker catalog. Its result does not authorize a later stage; manual research remains available.

`rnd-prototype` is an additive, explicit experiment candidate. Keep its project-spec reader, journal and controlled-run copies synchronized and in the checker catalog. Its retained prototype and verdict do not authorize transfer, reuse or deletion.

`rnd-design` is an additive, explicit selected-module candidate. Keep its discussion and domain copies identical to `rnd-grill`, project-spec reader to `dev-rnd`, and journal and controlled-run copies to `dev-lead`; include all consumers in the checker. Its design artifact does not authorize implementation or test deletion.

`rnd-audit` is an additive, explicit project survey candidate. Keep its project-spec reader, journal and controlled-run copies synchronized with their owners and in the checker catalog. Its ranked output does not authorize selection or implementation.

`rnd-map` keeps the local wayfinder decision model. Its discussion, research, prototype, project-spec, journal and controlled-run copies match their owners and are checked as shared resources. Decision tickets are not implementation tickets; map completion does not authorize implementation.

`dev-review` owns the review report reference; copy it into `to-tickets` when changed. The explicit `--to-tickets` candidate keeps review selection separate from ticket creation while the legacy route remains available.

`to-questionnaire` is an additive participant-document candidate. Keep its project-spec, journal and controlled-run copies synchronized and cataloged. Preparing a document does not authorize sending or invent answers.

`to-handoff` is an additive resumable-context candidate. Keep its project-spec, journal and controlled-run copies synchronized and cataloged. It supports journal-free work and never uses a branch alone as task identity.

`nxs-retro` is an additive single-session candidate. It initially owns `references/writing-for-agents.md`; move canonical ownership to `nxs-setup` in ticket 30 and keep consumer copies identical. Keep its project-spec, journal and controlled-run copies synchronized and cataloged. It creates no session index or period scan.

`nxs-lead` is an additive explicit coordinator. Catalog both invocation policies and its project-spec, journal and controlled-run copies. Keep legacy routes until the separate verified cutover; source changes never update installations.

Keep `nxs-lead` continuation in its own reference: historical records remain evidence, native continuation is capability-dependent, and no recovery engine is bundled.

Keep guarded auto explicitly selected and its local HTML defense and approval order in `nxs-lead` references. Approval of the defense alone authorizes neither saving nor an unrequested stage.
