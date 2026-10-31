# Parallel implementation converges on the feature branch

Independent code changes may run in parallel in separate Git worktrees. The lead brings their results together on one feature branch. Separate working trees avoid simultaneous edits to the same checkout; isolation does not establish that the combined behavior is correct.

This is a later implementation stage, after the [sequential cycle and recovery contract](0005-bounded-runs-and-recovery-first.md) have been verified.

The lead may autonomously run `dev-commit` for verified task results and merge their branches into the feature branch, preserving task history. The ticket executor still finishes without committing; the lead organizes committing as a separate stage. Implementing this requires a merge-completion contract in `dev-commit`.

A ticket's branch must match its worktree, and required blocker results must exist in that working tree. Launch dependent work from the integrated feature state once its prerequisites are available and checked together. Tests of an isolated task do not replace checks of the integrated result.

Ignored task records and private `.SPEC.md` files do not appear automatically in a new worktree. Shared task context and the applicable private specs need an explicit transfer or access mechanism. That mechanism, journal concurrency and integration conflict handling remain open.
