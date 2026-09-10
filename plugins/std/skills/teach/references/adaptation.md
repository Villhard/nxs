# ADAPTATION EXAMPLES

Use these illustrative trajectories to choose a teaching move from evidence. They are invented cases, not scripts or claims about the learner. Cases 1 and 2 share a task: their different answers warrant different responses. Each teacher response stops where learner participation is useful; it does not supply an answer to its own check. The rationale and checkpoint notes are for the agent, not lines to say to the learner.

## 1. SOUND REASONING: BEGIN A DEEPER APPLICATION

Context: the learner wants to apply the open/closed principle (OCP), not only define it. The teacher has explained that a chosen kind of extension should leave stable policy unchanged; this does not forbid all edits. In this example, `send_report` receives an exporter with `encode(rows)` and sends its result. Both the existing CSV exporter and the proposed JSON exporter accept the same rows and return bytes. The teacher asks: "Where would you add JSON support, and what would stay unchanged?"

Learner: "Add a JSON exporter and select it where we assemble the application. `send_report` already calls `encode`, so it doesn't need a JSON branch. The setup still changes; OCP can't mean no file ever changes."

Teacher:

> Yes, that would work. `send_report` keeps calling `encode(rows)` and gets bytes back, whether you pass it CSV or JSON. You still change which object gets passed in when you assemble the application. That's fine: the part you wanted to leave alone was the sender.
>
> Now suppose someone adds an exporter that does the encoding in the background. It returns a job ID straight away; the bytes won't be ready until later. The sender still expects to send them now. Would you plug this one in the same way, or is there something we'd need to sort out first?

Why: the learner explained the mechanism and its boundary, so another definition check adds little. The changed return behavior tests whether they can reason about the contract, not merely count new classes. The setup edit is correctly acknowledged, not treated as a misconception.

Checkpoint: record demonstrated reasoning about synchronous CSV/JSON extension without help. Remove that answered task; current focus is the exporter contract, with the job-ID case actually pending. Do not record success on the new case before an answer.

## 2. PARTIAL REASONING: TEACH THE MISSING MECHANISM

Same explanation and task as case 1.

Learner: "Add a JSON exporter class, then add an `if format == 'json'` branch in `send_report` to call it. The new class makes this follow OCP."

Teacher:

> The separate JSON exporter makes sense. The part I'd change is that `if` inside `send_report`: the sender is still choosing the format itself. Every new format means going back into this function.
>
> We can make that choice earlier, when we assemble the application, and pass in the exporter we've picked. Then the sender just calls `encode(rows)`. It doesn't need to know who turned the rows into bytes.
>
> So you've already moved the encoding out. The format choice is still inside the function you wanted to leave alone. If we kept your version and added XML tomorrow, where would you have to edit it?

Why: the answer identifies a useful component but explicitly equates a new class with OCP. Explain the dependency mechanism before asking about a small consequence of their own design. The job-ID challenge from case 1 would add difficulty before this gap is resolved. If the learner had only said "add a class," the gap would be ambiguous; ask where it is selected before diagnosing branch-based dispatch.

Checkpoint: record the correct encoder separation and the unresolved sender-dispatch gap, with the explanation supplied. Replace the original question with the XML consequence check; any subsequent success on that check follows assistance.

## 3. RECURRING CONFUSION: CHANGE THE EXAMPLE AND REPAIR AN OBJECTION

Context: the learner wants to evaluate causal claims. Twice, the teacher has contrasted "correlation" with "causation" using abstract definitions. The learner still asks: "But if the result improves after the change, why isn't that enough?" The teacher switches to a concrete comparison: "A school starts tutoring and scores rise. Maybe the pupils also got older. Comparing with pupils who did not get tutoring could help."

Learner: "But if that comparison group is younger, age could still explain the difference. Your comparison doesn't fix it."

Teacher:

> Yes - I left that out. Comparing older pupils with younger ones could leave us with exactly the problem you pointed out. Let's fix the example.
>
> Suppose we take pupils from the same year and randomly split them into two groups. One gets tutoring, the other studies as usual. Both take the same test before and after the term. The first group's average goes up by 12 points. The second group's goes up by 8.
>
> Those 8 points matter: the pupils without tutoring improved too. So we can't credit tutoring with the whole 12-point rise. The extra gain is 4 points, which gives us an estimate of its effect in this setup. Random assignment helps make the groups comparable on average, though a small group can still differ by chance.
>
> Back in the original story, we only knew that scores went up after tutoring. What does seeing the second group's result let us account for that we couldn't before?

Why: a numerical worked comparison replaces the failed verbal distinction. The learner's objection is valid evidence of reasoning about comparability, not continued confusion about everything. The teacher repairs its own underspecified example and qualifies the estimate. It does not claim this explanation has resolved the original gap.

Checkpoint: retain the unresolved inference from before/after improvement, note that abstract definitions did not help, and record the worked comparison now supplied. The learner demonstrated a comparability objection; interpreting the comparison independently remains unverified. Save the concrete case for resume, not another generic "explain causation" prompt.

## 4. SELF-REPORT: PROCEED AND REVISIT THROUGH TRANSFER

Context: the goal is to reason about relative changes. On a price falling from 100 to 80, then rising by 20%, the learner correctly found 80 but claimed the final price was 100 because the percentages cancel. The teacher worked through 20% of 80 as 16, giving 96, and explained that the two percentages use different bases.

Learner: "Okay, I get it now."

Teacher:

> That same changing base shows up when something keeps growing. Suppose a town has 1,000 people and grows by 10% each year for two years.
>
> In the first year, it gains 100 people and reaches 1,100. Next year, 10% means another 110 people, so it reaches 1,210. Same percentage, bigger starting number, bigger increase.
>
> That's why we multiply the current population by 1.1 each year. If we added a fixed 100 people each time instead, we'd end up at 1,200. The difference comes from those extra people becoming part of next year's starting number too.

The teacher leaves room to discuss this distinction; it need not demand another confirmation or immediately retest the worked price problem. Checkpoint now distinguishes the independently correct first discount, the assisted changing-base explanation, self-reported understanding, and unverified application. Current focus is repeated growth, not an unanswered price question.

Later, after discussing the growth example, the teacher returns to the gap through a new application: "Let's go back to prices, but this time we're trying to undo a change. A shop raised a price from 80 to 100 and now wants it back at 80. What percentage discount would get it there? Tell me which price you're taking the percentage of."

Why: "understood" permits forward teaching without establishing mastery. The later reverse calculation probes the base in a changed case and does not reveal the answer. Record the actual response and any help before updating demonstrated understanding; do not invent a successful transfer. If the learner pauses before this check is issued, save it only as a proposed next step.
