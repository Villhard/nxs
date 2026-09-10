# CONTRIBUTING (STD)

Follow the [shared rules and checks](../../CONTRIBUTING.md).

## CONTRACT

The contract is the `std` plugin, `teach` skill, teacher-led adaptive conversation, and [learning artifacts](skills/teach/references/workspace.md). The teacher begins the next useful step after sound reasoning, adapts to evidence and confusion, and keeps the checkpoint aligned with the conversation. Keep both manifests pointed at one shared skill; do not add platform-specific lessons or require other skills for the core dialogue.

## BEHAVIOR CHECKS

When teaching behavior changes, run real multi-turn conversations in temporary learning directories in both clients. Compare baseline and revised instructions with equivalent learner turns and the same model/settings where feasible. Use cases with different surface details from the bundled examples, without telling the teacher the expected response. Judge semantic behavior and actual saved files, not exact phrases or question counts:

1. Book excerpt: explain a coherent idea in chat; save grounded mission/resources and distinguish covered material from demonstrated understanding.
2. Two consecutive sound answers without a continuation command: give specific feedback and begin a useful next step after each. Save what each answer establishes and the actual current task; remove resolved questions from pending state.
3. Paired answers to the same task, one sound and one partial: choose materially different teaching moves. Address the partial answer's specific gap and preserve correct reasoning; saved evidence must explain the difference in help or difficulty.
4. Repeated confusion on one idea: change the representation, example, or scaffolding and actually explain. Save what remained unclear and what failed, without claiming the new approach succeeded before a learner response.
5. Valid objection: recheck assumptions/sources and repair the example. Save uncertainty or correction where relevant, without inventing a learner misconception.
6. Partly correct answer, then "understood": progress without another confirmation. Keep the supported insight, assistance, self-report, and remaining unverified gap distinct; revisit the gap naturally in a later application.
7. Pause mid-exercise, then a fresh session: honor the pause and reconcile the checkpoint. Resume using saved scenario, assistance, and unsuccessful explanations; do not reveal an unseen answer or repeat a resolved question.
8. Definitions completed for a goal that includes application: begin goal-relevant practice in the conversation and save the issued task. Do not declare the mission complete or save an unissued exercise as pending. Stop when the goal is reached or the learner requests it.
9. Explicit full-solution request: supply the worked solution rather than another hint-only check; record assistance accurately. A requested explanation does not authorize editing the learner's exercise.
10. Nontechnical topic and inaccessible source: teach without requiring code and disclose source limits in chat and resources. Preserve a usable checkpoint without fabricated citations.

Also check that a factual question without skill invocation creates no learning files. Inspect state after significant exchanges and on fresh-session resume. Replay ambiguous failures before changing instructions. Record installation, discovery, conversation behavior, saved-state results, and unavailable checks separately for Claude Code and Codex; format validation does not evaluate teaching.
