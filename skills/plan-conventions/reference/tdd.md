# TDD LOOP (reference)

Loaded on demand from `plan-conventions` when the plan's development approach is TDD. For each narrow behavior: write one failing test -> write minimal code to pass -> refactor while tests stay green; one behavior per cycle.

One behavior at a time forces design through actual usage of the public interface. Minimal code until green prevents premature generalization. Refactoring only while green prevents changing structure and behavior at once. "All tests first, all code later" is not TDD - it is a test-first dump without a feedback loop.

## THE RED -> GREEN -> REFACTOR CYCLE

1. **RED** - write one failing test for an observable behavior through the public interface. Run it. Make sure it fails specifically because of the missing behavior, not because of compile / setup errors.
2. **GREEN** - write the minimal code to make exactly this test pass. No generalizations "for later use".
3. **REFACTOR** - improve the structure while all tests are green. Do not change behavior. Do not start a new RED in this phase.
4. Move on to the next behavior - a new RED.

## RULES

- **One behavior, one test, one cycle.** Do not write all tests at once.
- **Test through the public interface.** Do not couple to private internals - otherwise any refactor breaks the tests.
- **Minimal pass.** Only what the current test needs.
- **Never refactor while RED.** Green first, then structure.
- **Do not test framework guarantees.** Test your own behavior, not the language / framework.
- **TDD is a choice, not dogma.** If test-first does not help (UI exploration, spike, throwaway, pure scaffold), choose a different development approach.

## ANTI-PATTERNS

- writing all tests first and then implementing everything - a test-first dump, not TDD;
- tests coupled to the names of private methods / internal structures;
- a big "GREEN" that implements 3 future tests at once "while we're at it";
- refactoring at the same time as implementing a new behavior;
- one fat test for the whole feature that "covers it anyway".

## WHEN NOT TDD

- spike / investigation - the goal is to figure out whether it makes sense; tests come later, if the code stays;
- tracer-bullet - you need to see the UX / workflow live first through a thin end-to-end slice;
- pure scaffolding (config, renaming packages) - there is no behavior to test;
- migration without observable behavior change - regression tests, but not RED -> GREEN for each change.

In such cases the plan explicitly chooses a different Development approach.

## PLAN-LEVEL FRAMING

In a plan, TDD means:

- the task is framed through behavior, not through files;
- the Test cases block describes observable cases through the public interface, not private internals;
- the checklist contains explicit steps: `write failing test for X`, `minimal implementation until X passes`, `refactor while green`;
- one task is one or more short RED -> GREEN -> REFACTOR cycles, not a dump of all tests at the start.
