# Rename the plan-reviewer agent to plan-lens

## Overview

`plan-reviewer` reads like a job title while the code lenses read like lenses.
Rename the agent to `plan-lens` so every read-only reviewer in `agents/` is named the
same way. Pure rename: the body of the agent is unchanged.

## SOURCE ARTIFACTS

- Tracker: PROJ-451

## ACCEPTANCE CRITERIA

- `agents/plan-lens.md` exists, carries `name: plan-lens`, and its body is unchanged.
- `agents/plan-reviewer.md` no longer exists.
- `claude plugin validate --strict .` passes.
- The house-style lint passes.

## DEVELOPMENT APPROACH

default - a file rename plus the documentation line that names the agent.

## Implementation

### Task 1: Rename the agent file and its documentation line

**Files:**
- Create: `agents/plan-lens.md`
- Modify: `README.md`

- [ ] copy `agents/plan-reviewer.md` to `agents/plan-lens.md` and set `name: plan-lens`
- [ ] delete `agents/plan-reviewer.md`
- [ ] update the agent list line in `README.md` to say `plan-lens`
- [ ] run `claude plugin validate --strict .` - must pass before task 2

Success: the plugin validates and `agents/` holds `plan-lens.md` and no `plan-reviewer.md`.

### Task 2: Bump the version and record the rename

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `CHANGELOG.md`

- [ ] bump `version` to the next minor - an agent rename is a contract change
- [ ] add a CHANGELOG entry under a new version heading naming the old and new agent
- [ ] run `bash .github/scripts/lint-house-style.sh` - must pass

Success: the version and the changelog match the rename that shipped.
