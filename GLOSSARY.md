# nxs

The language of the direct development flow. [ADR 0009](docs/adr/0009-seven-skill-direct-flow.md) records the current decision; earlier ADR terminology remains historical.

## Language

**Skill catalog**:
The seven independently installable source skills: `rnd-grill`, `rnd-debug`, `dev-exec`, `dev-review`, `dev-spec`, `dev-commit` and `nxs-setup`. Presence establishes neither client registration nor live compatibility.

**Approved plan**:
The concrete implementation approach, acceptance criteria, paths, checks and write boundaries approved for execution. Ticket readiness or a saved feature record alone does not approve it. Commit scopes require explicit authorization.

**Feature description**:
An optional preparation record, usually local lowercase `spec.md`, describing behavior, scope and acceptance checks. It is not a project spec or proof of built work.

**Implementation ticket**:
An optional independently checkable unit owned by `dev-exec`, with observable criteria and real prerequisites. Existing identities, branches, execution prohibitions and history are retained. A historical typed decision record is not an implementation ticket.

**Intended net work**:
The final task changes established by requirements and actual source evidence: relevant committed checkpoints plus remaining intended staged, unstaged and untracked work. A branch name, changed-path list or nonempty index alone cannot establish ownership or coverage.

**Selected snapshot**:
The pinned logical review view, baseline, requirements and source manifest described in the report. It is not a new checkout or artifact database; explicit narrower scopes keep their exclusions.

**Selected corrections**:
Finding numbers from a current complete review, returned with report identity, scope/source evidence, verdicts and open choices directly to `dev-exec`. Selection is not fix approval and creates no mandatory ticket.

**Checkpoint**:
An optional explicitly authorized commit of a checked execution block through `dev-commit`. Its commit and parent identities, scope and remaining changes travel with the task; a commit alone does not complete or accept it.

**Native reviewer**:
A fresh-context worker started through the selected client's native subagent facility with a complete role/scope packet. Finders propose and the independent verifier decides verdicts. Host-enforced permissions and prompt-only restrictions are different protections and must be reported honestly.

**Project spec**:
Project `SPEC.md` or private `.SPEC.md` recording material built-work intent. `dev-spec` is its exclusive writer in normal task execution.

**Handoff**:
A result in dialogue or an optional saved record carrying approved scope, decisions, open questions, relevant paths, actual verification/Git state and next authorized action. It neither starts another skill nor guarantees session recovery.

**Historical coordination record**:
An existing lead/auto packet, task journal or typed decision map from an earlier workflow. Preserve it as context and history, not a required live protocol or independent authorization. A conflict needs clarification, not emulation of a removed mode.

**Cutover**:
A separately authorized switch of installations or callers supported by route-specific evidence. Source removal and shell checks alone do not update installed copies or complete cutover.
