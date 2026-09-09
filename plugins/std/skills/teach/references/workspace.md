# WORKSPACE STATE

Use ordinary Markdown at the learning workspace root. Create files as their contents become known; create `learning-records/` only with its first record. Read before editing, preserve unrelated content, and do not initialize Git or commit learning artifacts automatically.

If this directory already has an unrelated mission, clarify which learning directory to use before replacing anything. Related chapters can share a mission. Respect read-only locations: continue the conversation and state that progress could not be saved.

## MISSION

Capture the topic, why it matters to the learner, desired outcomes, and stated constraints or exclusions. A goal such as understanding a chapter is valid; translate it into useful outcomes without demanding a product or deadline.

```markdown
# Mission: <topic>

## Purpose
<Why the learner wants to understand this.>

## Desired outcomes
- <What the learner wants to explain, distinguish, or apply.>

## Boundaries
<Relevant constraints and topics intentionally left aside, if any.>
```

Keep it short. Change it when the learner changes the goal; do not silently substitute your own goal.

## RESOURCES

List the learner's anchor material first, followed by additional sources actually inspected. For each source record its title/author, URL or local path, relevant chapter/page/section when known, and one sentence on what it helps explain. Note version/date when material facts depend on it.

Distinguish unavailable sources and unresolved source gaps from verified resources. Do not record guessed citations. Supplementary reading is optional unless needed to support the current lesson.

## PROGRESS

A current checkpoint, updated in place rather than appended after every turn. Omit empty sections.

```markdown
# Progress: <topic>

## Current focus
<Chapter/concept and what we are working toward.>

## Understanding
- Discussed: <covered, not yet checked.>
- Self-reported: <what the learner says they understand.>
- Demonstrated: <specific evidence; link to a learning record if useful.>

## Open questions
<Unresolved questions or gaps, including uncertainty in our own explanation.>

## Resume here
<Pending task/question, necessary scenario or file reference, help already given,
and the next action. Do not store an answer the learner has not seen, even inside a note about what not to reveal.>

## Preferences
<Only preferences actually stated or confirmed by the learner.>
```

Revise the snapshot as evidence changes. If there is no pending exercise, save the next topic or question. Do not infer a misconception from a typo or infer mastery from agreement.

## LEARNING RECORDS

Use `learning-records/NNNN-short-title.md`, incrementing the highest existing number. Record the insight and its consequence for future teaching in a short paragraph, with evidence and any hints or worked solutions supplied. For a mission change, record the learner's decision and link to `MISSION.md`; it is not evidence of concept mastery.

If later evidence overturns an earlier conclusion, retain the old record with a note linking to the correction and update current progress. Do not turn every exchange into a record, copy full conversations, or reproduce theory already available in sources.

## EXISTING TEACH WORKSPACES

Reuse existing `MISSION.md`, `RESOURCES.md`, and `learning-records/` in their current formats. Read `NOTES.md` for preferences and relevant context; leave it in place. Create `PROGRESS.md` from known state without requiring migration or rewriting the old files to match these examples. Preserve any HTML lessons, reference sheets, and learner code. When a legacy record lacks evidence, treat its claim cautiously rather than inventing a demonstration.
