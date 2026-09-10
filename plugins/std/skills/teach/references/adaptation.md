# ADAPTATION EXAMPLES

Use these illustrative trajectories to choose a teaching move from evidence. They are invented cases, not scripts or claims about the learner. Cases 1 and 2 share a task: their different answers warrant different responses. Each teacher response stops where learner participation is useful; it does not supply an answer to its own check.

## 1. SOUND REASONING: BEGIN A DEEPER APPLICATION

Context: the learner wants to apply the open/closed principle (OCP), not only define it. The teacher has explained that a chosen kind of extension should leave stable policy unchanged; this does not forbid all edits. In this example, `send_report` receives an exporter with `encode(rows)` and sends its result. Both the existing CSV exporter and the proposed JSON exporter accept the same rows and return bytes. The teacher asks: "Where would you add JSON support, and what would stay unchanged?"

Learner: "Add a JSON exporter and select it where we assemble the application. `send_report` already calls `encode`, so it doesn't need a JSON branch. The setup still changes; OCP can't mean no file ever changes."

Teacher: "That separates the extension point from application setup correctly. For this format change, the sending policy stays untouched because both exporters meet the same contract. Let's test the limit: a proposed exporter returns a background job ID immediately, and the bytes become available later. The sender still expects bytes it can send now. What must we establish before treating this as another interchangeable exporter?"

Why: the learner explained the mechanism and its boundary, so another definition check adds little. The changed return behavior tests whether they can reason about the contract, not merely count new classes. The setup edit is correctly acknowledged, not treated as a misconception.

Checkpoint: record demonstrated reasoning about synchronous CSV/JSON extension without help. Remove that answered task; current focus is the exporter contract, with the job-ID case actually pending. Do not record success on the new case before an answer.

## 2. PARTIAL REASONING: TEACH THE MISSING MECHANISM

Same explanation and task as case 1.

Learner: "Add a JSON exporter class, then add an `if format == 'json'` branch in `send_report` to call it. The new class makes this follow OCP."

Teacher: "A separate JSON encoder is a useful part of that design. The branch still makes the sender change for every new format, though. Here the sender already receives an exporter, so it can always call `encode(rows)` without knowing whether it got CSV or JSON. Setup chooses the object; that object supplies the format-specific behavior. Moving encoding into a class only protects the sender if the sender uses that shared contract. In your version with a format branch still inside the sender, what would happen to `send_report` when XML is added?"

Why: the answer identifies a useful component but explicitly equates a new class with OCP. Explain the dependency mechanism before asking about a small consequence of their own design. The job-ID challenge from case 1 would add difficulty before this gap is resolved. If the learner had only said "add a class," the gap would be ambiguous; ask where it is selected before diagnosing branch-based dispatch.

Checkpoint: record the correct encoder separation and the unresolved sender-dispatch gap, with the explanation supplied. Replace the original question with the XML consequence check; any subsequent success on that check follows assistance.

## 3. RECURRING CONFUSION: CHANGE THE EXAMPLE AND REPAIR AN OBJECTION

Context: the learner wants to evaluate causal claims. Twice, the teacher has contrasted "correlation" with "causation" using abstract definitions. The learner still asks: "But if the result improves after the change, why isn't that enough?" The teacher switches to a concrete comparison: "A school starts tutoring and scores rise. Maybe the pupils also got older. Comparing with pupils who did not get tutoring could help."

Learner: "But if that comparison group is younger, age could still explain the difference. Your comparison doesn't fix it."

Teacher: "You're right: I did not specify comparable groups, so that comparison is inadequate. Here is a better hypothetical. Pupils from the same year are randomly assigned to tutoring or ordinary study; both groups take the same test before and after the same term. The tutoring group's average rises by 12 points, the other group's by 8. The 12-point rise includes improvement that can happen without tutoring; the 8-point rise makes that visible. The difference in gains is 4 points, an estimate of the tutoring effect under these conditions, not proof from timing alone. Random assignment helps make the groups comparable on average, but a small sample can still differ by chance. Which part of this comparison was missing from the original claim that scores rose after tutoring?"

Why: a numerical worked comparison replaces the failed verbal distinction. The learner's objection is valid evidence of reasoning about comparability, not continued confusion about everything. The teacher repairs its own underspecified example and qualifies the estimate. It does not claim this explanation has resolved the original gap.

Checkpoint: retain the unresolved inference from before/after improvement, note that abstract definitions did not help, and record the worked comparison now supplied. The learner demonstrated a comparability objection; interpreting the comparison independently remains unverified. Save the concrete case for resume, not another generic "explain causation" prompt.

## 4. SELF-REPORT: PROCEED AND REVISIT THROUGH TRANSFER

Context: the goal is to reason about relative changes. On a price falling from 100 to 80, then rising by 20%, the learner correctly found 80 but claimed the final price was 100 because the percentages cancel. The teacher worked through 20% of 80 as 16, giving 96, and explained that the two percentages use different bases.

Learner: "Understood."

Teacher: "Let's use that changing base in a related situation. A town of 1,000 grows by 10% in each of two years. The first increase is 100, making 1,100; the second is 110, making 1,210. The same rate adds more people when it starts from a larger population. This is why repeated percentage changes multiply: here the factor is 1.1 each year. For comparison, adding exactly 100 people each year would give 1,200."

The teacher leaves room to discuss this distinction; it need not demand another confirmation or immediately retest the worked price problem. Checkpoint now distinguishes the independently correct first discount, the assisted changing-base explanation, self-reported understanding, and unverified application. Current focus is repeated growth, not an unanswered price question.

Later, after discussing the growth example, the teacher returns to the gap through a new application: "A shop raises a price from 80 to 100. It now wants to return to 80 using one percentage discount from the current price. What discount would do that, and which amount is its base?"

Why: "understood" permits forward teaching without establishing mastery. The later reverse calculation probes the base in a changed case and does not reveal the answer. Record the actual response and any help before updating demonstrated understanding; do not invent a successful transfer. If the learner pauses before this check is issued, save it only as a proposed next step.
