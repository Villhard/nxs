# ISOLATED PROTOTYPE

Read only when evidence warrants a small experiment. An experiment is optional; discussion or source inspection may be enough.

## AUTHORIZE AND ISOLATE

Name one question, a falsifiable hypothesis, representative bounded input and an observable expected outcome before running anything. Propose the smallest useful experiment, exact local boundary, data, checks and possible side effects. Obtain authorization covering those writes and execution, reusing existing approval only within its scope. Ambiguous hypotheses, costly or irreversible actions and visual/personal choices require the user's answer before dependent work. A demonstration cannot answer a preference question on the user's behalf.

Use an explicit or established feature directory, otherwise `.scratch/<topic-slug>/`. Inspect the destination and use a distinct `research/prototypes/<experiment-slug>/` directory, with a linked `research/<experiment-slug>-verdict.md`. Preserve existing work and source bytes; a map's presence is context, not automatic permission to modify its records. Ask if ownership is ambiguous. Create only the bounded prototype and evidence, using disposable isolated data, never product edits or production scaffolding.

An install, migration, network/external effect or action against a shared target needs approval covering that concrete action and target, plus native permissions. Without it, stop the affected experiment and state the expected result and missing evidence. Never use production credentials or send private input externally without authorization.

## OBSERVE AND RETAIN

Make the temporary experiment easy to run. Record setup, exact steps, inputs, observed outputs and cleanup actually performed within the authorized boundary. Separate expectations, observations and interpretation. If a check cannot run, preserve the experiment and report the blocker rather than inventing a result. Apply [saving](saving.md) to the proposed verdict; authorization to build the experiment does not approve unseen conclusions.

The verdict names the question, hypothesis, why the check matters, retained files, setup and steps, evidence, status (`supported`, `rejected` or `inconclusive`), assumptions and limits. A failed hypothesis is useful evidence. Inconclusive results name the next discriminating check. Exclude secrets, private configuration and raw session transcripts.

Retain prototype files and verdict locally and uncommitted by default. Do not stage, commit or change Git state. A successful result authorizes neither production transfer nor reuse of prototype parts nor deletion; each requires separate authorization for that action. Preserve source and prototype bytes until it is given. Interruption is not evidence of no effect: reconcile actual state before repeating any uncertain action.
