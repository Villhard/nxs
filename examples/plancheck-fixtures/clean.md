# Move the frontmatter lint out of the CI workflow into a script

## Overview

The house-style lint lives in `.github/scripts/lint-house-style.sh` and CI calls it in one
line. The frontmatter lint is a 20-line shell block pasted inside `.github/workflows/ci.yml`,
so it cannot be run locally before pushing. Move it to a script beside the other one and
have the workflow call it. Same checks, same exit codes, no new rules.

## SOURCE ARTIFACTS

- Tracker: PROJ-452

## ACCEPTANCE CRITERIA

- `bash .github/scripts/lint-frontmatter.sh` runs from the repository root and exits 0 on the
  current tree.
- It exits 1 and names the file when a `SKILL.md` has a missing or empty `description`, and
  when a `user-invocable` field is present but is not exactly `true` or `false`.
- It exits 1 when no `skills/*/SKILL.md` matches at all.
- CI runs the script instead of the inline block, and the workflow keeps both jobs.

## DEVELOPMENT APPROACH

default - the script and its checks land together, exercised from the shell.

## Implementation

### Task 1: Add the frontmatter lint script

**Files:**
- Create: `.github/scripts/lint-frontmatter.sh`

**Test cases:**
- run on the current tree -> exit 0, no output
- a `SKILL.md` with `description:` and nothing after it -> exit 1, the path is printed
- a `SKILL.md` with `user-invocable: yes` -> exit 1, the path is printed
- a `SKILL.md` with `user-invocable: false` -> exit 0
- no `skills/*/SKILL.md` present -> exit 1 with an explicit message

- [ ] add the script with the same checks the workflow block runs today
- [ ] make it executable and give it the usage comment the sibling script carries
- [ ] check the cases above from the shell against the current tree and a scratch copy
- [ ] run `bash .github/scripts/lint-frontmatter.sh` - must exit 0 before task 2

Success: the script reports the same failures the inline block reports, from the shell.

### Task 2: Call the script from the workflow

**Files:**
- Modify: `.github/workflows/ci.yml`

**Test cases:**
- the two lint steps of the `lint` job are each a single `run:` line calling a script
- the `Checkout` step and the `validate` job are unchanged
- no `run:` block longer than one line remains in the workflow

- [ ] replace the inline frontmatter block with one `run:` line calling the script
- [ ] run both scripts locally and confirm no `run:` block in the workflow is inline
- [ ] run `bash .github/scripts/lint-house-style.sh` - must pass

Success: CI calls two scripts and the workflow carries no pasted shell.
