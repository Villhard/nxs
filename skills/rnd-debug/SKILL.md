---
name: rnd-debug
description: Investigate a reported failure and save a confirmed root cause or the precise missing evidence, without implementing a fix or creating tickets.
argument-hint: "[tracker key | bug description | path]"
disable-model-invocation: true
---

# /rnd-debug

Investigate a failure and save its evidence. Run only on explicit invocation or an instruction explicitly covering this skill's work. Read [feature directory](references/feature-directory.md) before input and [project specs](references/project-specs.md) for applicable domain evidence. Read supplied input before probing; a missing or unreadable file stops the affected work. Reuse existing approval only within its actual scope. No feature spec, ticket, journal or run packet is required; existing records are context, not independent authorization. Clarify conflicting legacy instructions rather than activating a removed coordination procedure.

## INVESTIGATE

Build the cheapest feedback loop for the reported symptom, reproduce it and minimize its steps and data. Rank checkable hypotheses with distinct predictions. Change one parameter or probe at a time; trace the supported explanation through evidence-backed why steps to a fixable cause. Confirm the symptom and a discriminating probe before naming a cause. Record the smallest supported fix direction and a cheap, stable regression check at the nearest practical public seam. Distinguish observed results from source contracts, expectations and assumptions.

Use read-only inspection or bounded disposable probes; do not instrument or edit product code/tests. Keep necessary temporary probe files and outputs under the feature's `research/`, away from production data. Clean up only disposable probe files whose deletion is covered by the diagnostic scope; preserve existing work and useful evidence and report cleanup actually performed. An install, migration or external action requires approval covering the concrete action and target, plus native permissions. Without it, stop that affected probe and state the expected result and missing evidence. After interruption, reconcile observable effects before repeating an uncertain action.

If reproduction fails, evidence is unavailable or multiple causes still fit, save the attempts, ranked hypotheses, exact missing evidence and next discriminating probe. Mark cause unconfirmed and fix direction and regression test pending. Do not offer a ready fix or execution handoff.

Classify a confirmed cause against the glossary, decisions and project specs:

| Class | Evidence | Handoff |
| --- | --- | --- |
| `right` | Records establish the intended behavior and code differs | Eligible for `dev-exec`. |
| `silent` | Records do not establish intended behavior | Obtain the user's agreement on intent before `dev-exec`. |
| `wrong` | A record describes outdated or buggy behavior | Obtain agreement on its correction; project specs are corrected only by `dev-spec` after the fix. |
| `feature` | The current behavior was decided and the request changes that decision | Suggest `rnd-grill`; no ready fix handoff. |

Ask about the class only when evidence supports multiple classes. Record the relevant path for `wrong` and `feature` and evidence of agreement for `silent` and `wrong`.

## ARTIFACT AND REPEAT

Save `.scratch/<feature-slug>/root-cause.md` using the location rules. Include `## Symptom`, `## Repro`, `## Evidence`, `## Hypotheses`, `## 5-Why`, `## Root cause`, `## Fix direction` and `## Regression test`; state confirmed or unconfirmed and the class explicitly. Name exact repro steps, predictions, probe results, evidence paths, cleanup and any assumptions. For `feature`, state that a decision change is needed and regression is pending that decision.

Inspect the existing diagnosis and local issues naming the root cause before writing. For an open ticket covering the same confirmed cause, preserve both files unchanged and report reuse plus any new evidence in dialogue. For a different confirmed cause against an open ticket, show the proposed diagnosis revision and the conflict; obtain a decision on that revision or a distinct destination before writing. Any ticket revision or closure belongs to separately authorized `dev-exec`, not diagnosis. Preserve ticket identity, branch restrictions, `Do not commit`, status and history; resolved or wontfix history stays unchanged. Preserve manual additions and prior evidence in an approved diagnosis revision; an identical result is a no-op. Never edit implementation tickets, domain/project specs, product code/tests, Git/index, settings or installations; diagnosis creates no ticket or fix.

## NEXT

Return the artifact, confirmation status, intended-behavior class, source evidence, agreements, actual probe results and remaining prerequisites. Suggest `dev-exec` directly with the root-cause path only for a confirmed `right` cause or a confirmed `silent`/`wrong` cause with the required intent agreement. No intermediate decision, feature spec or ticket is required; `dev-exec` owns acceptance criteria, plan approval, optional decomposition, implementation and verification. Cause confirmation does not prove prerequisites satisfied or authorize a fix. An unconfirmed cause names missing evidence; `feature` suggests `rnd-grill`. A later `dev-spec` records material project-spec corrections after the fix. Never start the next skill implicitly.
