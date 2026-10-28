# Rule groups

Each `##` heading is one group, offered as a whole; each bullet is one rule.

## Communication

- Start with the answer or result, then the reasoning.
- Write plainly, without filler; keep the context needed to act on the answer.
- Keep identifiers, code, paths, commands and technical terms in their original form.
- Distinguish verified facts from assumptions, and explain a recommendation through its consequences.

## Investigation

- Read the relevant code, instructions and documentation before proposing a change; check discoverable facts yourself.
- Base explanations on observed behavior, code paths or primary sources.
- Resolve questions from the task, existing decisions and evidence; ask when a choice needs the user's priorities or a wrong assumption would be costly or irreversible.

## Code changes

- Establish an observable success criterion before editing.
- Trace the affected behavior and its callers before fixing a bug.
- Reuse existing code, the standard library and platform features before adding a dependency or an abstraction.
- Match the surrounding style and keep changes within the request.
- Preserve unrelated changes; mention unrelated dead code instead of removing it, and remove code your change made unused.
- Treat a linter or type checker error as a design signal and fix its cause; ask before adding a suppression.

## Verification

- Run the project's checks appropriate to the change.
- For a bug fix, add or update a regression test when practical.
- Inspect the final diff for accidental changes.
- Report what was verified; when a check could not run, say what remains unverified and why.

## Git

- Work on a branch; create it before the first commit when on the default branch.
- Commit, push or open a pull request only when asked.
