# SMELL BASELINE (reference)

Loaded on demand from `/nxs:review` and injected into the `nxs:review-quality-reviewer` and `nxs:review-simplification-reviewer` lenses. A fixed set of Fowler code smells (_Refactoring_, ch.3) those two lenses carry on top of the project's documented standards, so review has a shared vocabulary even when the repo documents nothing. Each smell is a leading word - one pretrained term that anchors a whole class of findings.

This file does not restate the base classification. A smell is scored through the `review-protocol` base and the `review-policy.md` refinements; the binding rules below only say how a smell enters that base.

## BINDING RULES

- Heuristic, not a rule. Each smell is a labelled candidate ("possible Feature Envy"), never a violation on its own. It runs through the base BLOCK / NIT / DROP: by default a smell lands NIT; it reaches BLOCK only with a concrete cost (a real bug path, code genuinely unreadable); a smell without a concrete file / line / cost is DROP. Do not emit a smell to look thorough.
- Documented standard and stated intent override. A repo standard (Standards axis) or a stated intent in the plan / brief / nearby comments that endorses what a smell would flag suppresses it - this is the evidence bar's "deliberate decision -> drop".
- Skip what tooling enforces. A smell that lint / formatter / typecheck already catches -> drop.
- Diff scope only. The smell must appear in the diff under review, not in untouched surrounding code.

## THE SMELLS

Format: `name [primary lens] - what it is -> how to fix`. A smell may fire in either lens; the orchestrator dedups cross-lens overlap.

- **Mysterious Name** [quality] - a function, variable, or type whose name does not reveal what it does or holds -> rename it; if no honest name comes, the design is murky.
- **Duplicated Code** [simplification] - the same logic shape appears in more than one hunk or file of the diff -> extract the shared shape, call it from both.
- **Feature Envy** [simplification] - a method reaches into another object's data more than its own -> move the method onto the data it uses.
- **Data Clumps** [simplification] - the same few fields or params keep travelling together (a type wanting to be born) -> bundle them into one type, pass that.
- **Primitive Obsession** [simplification] - a primitive or string stands in for a domain concept that deserves its own type -> give the concept its own small type.
- **Repeated Switches** [simplification] - the same `switch` / `if`-cascade on the same type recurs across the change -> replace with polymorphism, or one map both sites share.
- **Shotgun Surgery** [simplification] - one logical change forces scattered edits across many files in the diff -> gather what changes together into one place.
- **Divergent Change** [simplification] - one file or module is edited for several unrelated reasons -> split so each module changes for one reason.
- **Speculative Generality** [simplification] - abstraction, params, or hooks added for a need the spec does not have -> delete it; inline back until a real need shows.
- **Message Chains** [quality/simplification] - long `a.b().c().d()` navigation the caller should not depend on -> hide the walk behind one method on the first object.
- **Middle Man** [simplification] - a class or function that mostly just delegates onward -> cut it, call the real target directly.
- **Refused Bequest** [simplification] - a subclass or implementer that ignores or overrides most of what it inherits -> drop the inheritance, use composition.

## POINTERS

- Base classification, tie-breaks, the evidence bar, output format - `review-protocol` (already injected into every lens).
- Speculative Generality and other over-engineering escalation is scored relative to task complexity - `review-policy.md` OVER-ENGINEERING - RELATIVE COMPLEXITY. Do not restate it here.
