---
name: rnd-debug
description: Investigate a reported failure and save a confirmed root cause or the precise missing evidence, without implementing a fix or creating tickets.
argument-hint: "[tracker key | bug description | path]"
disable-model-invocation: true
---

# /rnd-debug

Investigate a failure and save its evidence. Run only on explicit invocation or in an explicit controlled scope. Read [feature directory](references/feature-directory.md) before input and [project specs](references/project-specs.md) for applicable domain evidence. Read [task journal](references/task-journal.md) before a task write, question or handoff; an explicit controlled packet also requires [controlled run](references/controlled-run.md).

## INVESTIGATE

Build the cheapest feedback loop for the reported symptom, reproduce it and minimize its steps and data. Rank checkable hypotheses with distinct predictions. Change one parameter or probe at a time; trace the supported explanation through evidence-backed why steps to a fixable cause. Confirm the symptom and a discriminating probe before naming a cause. Record the smallest supported fix direction and a cheap, stable regression check at the nearest practical public seam. Remove temporary instrumentation and harnesses; retain useful probe outputs under the feature's `research/` and record cleanup.

If reproduction fails, evidence is unavailable or multiple causes still fit, save the attempts, ranked hypotheses, exact missing evidence and next discriminating probe. Mark cause unconfirmed and fix direction and regression test pending. Do not offer a ready ticket handoff.

Classify a confirmed cause against the glossary, decisions and project specs:

| Class | Evidence | Handoff |
| --- | --- | --- |
| `right` | Records establish the intended behavior and code differs | Eligible for `to-tickets`. |
| `silent` | Records do not establish intended behavior | Obtain the user's agreement on intent before `to-tickets`. |
| `wrong` | A record describes outdated or buggy behavior | Obtain agreement on its correction; project specs are corrected only by `dev-spec` after the fix. |
| `feature` | The current behavior was decided and the request changes that decision | Suggest `rnd-grill`; no fix ticket. |

Ask about the class only when evidence supports multiple classes. Record the relevant path for `wrong` and `feature` and evidence of agreement for `silent` and `wrong`.

## ARTIFACT AND REPEAT

Save `.scratch/<feature-slug>/root-cause.md` using the location rules. Include `## Symptom`, `## Repro`, `## Evidence`, `## Hypotheses`, `## 5-Why`, `## Root cause`, `## Fix direction` and `## Regression test`; state confirmed or unconfirmed and the class explicitly. Name exact repro steps, predictions, probe results, evidence paths, cleanup and any assumptions. For `feature`, state that a decision change is needed and regression is pending that decision.

Before overwriting, inspect existing issues naming the root cause. For an open ticket covering the same confirmed cause, preserve both files unchanged. For a new confirmed cause against an open ticket, show the concrete changes and ask whether to revise that ticket or close it before writing; preserve its identity, branch, status and history when revising. Resolved or wontfix history remains unchanged. Never edit product code, project specs, Git or the index; diagnosis creates no ticket or fix.

## NEXT

Return the artifact, confirmation status and evidence. Suggest an explicitly authorized `to-tickets <root-cause-path>` only for an eligible confirmed cause; an unconfirmed cause names the missing evidence and `feature` suggests `rnd-grill`. A later `dev-spec` records project-spec corrections after the fix. Controlled runs return evidence to lead without starting another stage.
