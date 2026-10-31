---
name: rnd-map
description: Map a broad uncertain goal into linked decision questions and dependencies, preserving existing map history.
argument-hint: "<goal | map path>"
disable-model-invocation: true
---

# /rnd-map

Chart or continue a map of decisions toward a broad goal. Run only on explicit invocation or within an explicit controlled scope. Read an explicit map or input before proceeding; a missing path is a stop. Read [map rules](references/map.md), [discussion](references/discussion.md) and [project specs](references/project-specs.md). Read [task journal](references/task-journal.md) before a task write, question or handoff; an explicit controlled packet also requires [controlled run](references/controlled-run.md).

## CHART

1. Establish the destination and scope with the user; an ambiguous goal needs clarification before charting dependent decisions. Inspect applicable code, decisions and domain terms. Preserve declared execution scope in Notes; mapping alone is planning.
2. Identify precise decision questions and their blockers. Keep in-scope questions that cannot yet be stated precisely in Not yet specified; keep excluded work in Out of scope. Create the local map and numbered decision files using [map rules](references/map.md), then wire dependencies to actual numbers. A map is an index, not a duplicate decision store.
3. Report the map and frontier. Charting does not itself authorize answering every question or implementing the destination.

## CONTINUE

Read the existing map and scan decision files, distinguishing Type decisions from implementation tickets. Reconcile their statuses, blockers, answers and actual files. Use the frontier and claim rules in [map rules](references/map.md); a missing, unresolved or ambiguous prerequisite blocks dependent work. Do not reset a claimed or resolved ticket, renumber, erase an answer or convert a decision to implementation.

Before working each individual frontier question, obtain explicit permission for that question. Name the feature directory when requesting permission to save its supporting evidence. A user may authorize multiple named questions, but permission for one does not authorize the next; denial stops that question. Save `Status: claimed` before starting the permitted work. Discuss material choices under [discussion](references/discussion.md); do not invent the user's answers. For authorized research use [research output](references/research.md): investigate primary sources, distinguish evidence from assumptions and save findings and limits. For an authorized prototype use [prototype](references/prototype.md): test a specific hypothesis, retain the experiment and save its verdict, including its separate transfer, reuse and deletion gates. Persist supporting evidence under the feature and link it from the decision. A task requiring an unapproved external action waits for authorization.

After an answer is established, append it to the decision, set `Status: resolved` and add a linked one-line gist to Decisions so far. Preserve history; recompute the frontier and graduate only now-precise in-scope questions. Record uncertainty instead of resolving without evidence. Several small decisions may be worked in one session only with explicit permission for each.

## HANDOFF

Return the map, agreed answers, open frontier, blockers and unverified evidence. Offer separately scoped research, prototype, decision, spec or ticket work where helpful. Start a subsequent stage only within the original or subsequent authorization. Mapping alone authorizes no product edits, ready implementation tickets, deployment, project-spec writes, Git changes or installation. An explicitly included implementation scope is a separate authorized action, not a conversion of the decision files.
