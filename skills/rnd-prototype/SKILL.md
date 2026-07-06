---
description: Run a controlled throwaway experiment to answer one specific design question through observable behavior. Use when a design choice depends on runtime behavior that reading code, tests, or docs cannot settle, and shipping the real implementation to find out would be too costly.
argument-hint: "[design question]"
---

# /nxs:rnd-prototype

Answer exactly one design question by building the smallest throwaway thing that produces observable behavior, then decide. Self-contained skill. Output language and response style come from global rules, not this file.

Accepted input: a design question, or nothing (ask one clarifying question to formulate it). The prototype code is disposable - the deliverable is a decision, not shippable code.

## STANCE (PROTOTYPE ONLY)

- One prototype answers one question through runtime behavior. It is not production code, not a feature, and not the first step of a plan.
- The prototype is spike-like and time-boxed: build the smallest runnable form, observe, decide. If it grows past one screen or one run command, stop - the question is answered or was the wrong one.
- Do not commit, clean up, or delete the prototype branch without explicit user confirmation. Do not silently build production on top of prototype code.
- Route away when this is not a prototype: a bug -> `/nxs:dev-diagnose`; structural friction with no code to run -> `/nxs:rnd-architecture`; the answer already visible in code / tests / docs, or the approach already chosen -> `/nxs:dev-plan`.

## PROCEDURE

1. Formulate the single design question up front. If vague, ask exactly one clarifying question, not a list. State it in one line - what runtime fact would settle the design choice. One question, one prototype.
2. Choose the smallest runnable form that produces observable behavior, matched to the question:
   - logic / state model -> tiny runnable CLI / script with fixed input and explicit output;
   - API / data contract -> minimal fixture / harness that calls the contract and prints the result;
   - integration seam -> smallest stub of both sides plus one run;
   - UI variation -> minimal page / component in the existing UI scaffold, no production data (only when the project has a UI and the user asked).
3. Build the minimal prototype, ideally on a throwaway branch or scratch area. Mark it explicitly as a prototype. Surface relevant state / output after each step.
4. Run and observe the actual behavior. Record only what the run shows. If the answer does not come, change the prototype - do not deepen it.
5. Decide and hand off: delete it, absorb it into the real task, or name the next step. The output is a decision, not shippable code.

## PROTOTYPE RULES (inlined)

- Throwaway from day one, time-boxed, disposable - not a durable artifact.
- One question -> one prototype; never batch several questions "just in case".
- No persistence, no production abstractions, no broad error handling - they blur the answer.
- Every prototype must produce visible output; "it works, checked it by hand" is not an answer.
- Once done, delete or absorb - never leave a prototype in the repo without a status.
- Do not build production on top of prototype output without redoing it properly. "A production implementation I can finish later" is not a prototype - that is a plan.

## ARTIFACT

By default the prototype leaves no durable file - the code is temporary and is deleted or absorbed. Default output is to chat:

- the formulated design question;
- the chosen prototype branch / location;
- the observed behavior and the answer;
- the decision: delete / absorb into the real task / next step.

Only when the user explicitly asks to save the findings, propose a brief and write it after approval:

```text
docs/briefs/YYYYMMDD-<slug>-prototype.md
```

Fields: question, prototype branch, what was done, observable result, decision, next step.

## REFS

- When the prototype is absorbed into real work, hand off to `/nxs:dev-plan` and follow the `plan-conventions` background skill to turn the finding into a plan.
- When the run settled a significant decision, record it through the `decision-log` background skill, which applies the ADR gate and decides whether it is worth recording and where it lives.

## NEXT

Absorb into implementation -> `/nxs:dev-plan` then `/nxs:dev-exec`. Answer deserves an ADR -> `decision-log`. Question not yet formulated -> `/nxs:rnd-brainstorm`. Structural friction, not runtime behavior -> `/nxs:rnd-architecture`.
