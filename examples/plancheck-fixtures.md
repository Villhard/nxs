# PLANCHECK FIXTURES

Two plans in `plancheck-fixtures/`, written against this repository so `/nxs:plancheck` can
actually check their claims. They are a calibration target for the review bar, not sample
output and not work to do. Never run `/nxs:exec` on them.

The expected verdicts live here rather than beside the plans on purpose: a plan that states
its own expected verdict leaks it into the review.

```
/nxs:plancheck examples/plancheck-fixtures/bait.md
/nxs:plancheck examples/plancheck-fixtures/clean.md
```

## bait.md

Renames the `plan-reviewer` agent. Expected: `NEEDS CHANGES` with exactly one BLOCK.

The BLOCK: `skills/plancheck/SKILL.md` spawns `nxs:plan-reviewer` by name and no task
touches that file, so after execution `/nxs:plancheck` spawns an agent that does not exist.
Neither verification the plan names catches it - `claude plugin validate --strict .` reads
manifests, not prose, and the house-style lint reads Unicode - and the per-task review only
ever sees `agents/` and `README.md`.

The stale mention of the agent in `skills/plancheck/reference/plan-review-policy.md` is a NIT:
prose that reads wrong, with the right end state still shipping.

What must not come back as a BLOCK: no `Test cases` block on either task (neither changes
behavior), the plan not naming which line of `README.md` to edit (it is in the Files block),
anything about plugin snapshots cached by an installed session, and the shape of the two tasks.

## clean.md

Moves the frontmatter lint out of `ci.yml` into a script. Expected: `APPROVE`, with the nits on
a line each. The nit worth having: nothing tells a contributor the new script exists. No task updates
the PR checklist in `.github/PULL_REQUEST_TEMPLATE.md`, which lists the other two checks by
name, or the `.github/` line in `CONTRIBUTING.md`, which glosses the directory as holding one
linter. The plan's own goal still ships - the script runs locally and CI calls it - so the cost
is a stale line, not a wrong result.

The other nit on offer: the two tasks are one capability - the script is dead until the workflow
calls it, and both are verified by the same CI run - so they merge. A NIT, never a BLOCK, and the
same holds for the two tasks in `bait.md`.

Anything blocking here is a false positive, and each one is a bug in the bar.
