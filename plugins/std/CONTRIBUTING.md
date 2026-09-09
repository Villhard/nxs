# CONTRIBUTING

Follow the repository's authoring and public-safety rules.

## CONTRACT

The contract is the plugin name `std`, the `teach` skill, conversational teaching by default, and the workspace artifacts documented in the README. Changes to those interfaces are minor releases; internal instruction refinements are patches. Update both plugin manifest versions together and add a CHANGELOG entry for bundled changes.

Keep the Claude Code and Codex manifests pointed at one shared skill. Do not introduce platform-specific lesson implementations or require additional skills for the core dialogue.

## VERIFICATION

Run the repository house-style and frontmatter checks, strict Claude Code marketplace/plugin validation, and Codex plugin and skill validation. Include new Markdown files explicitly in the house-style check before they are tracked. Check both manifests agree on name/version and all relative references resolve.

Exercise the skill in temporary learning directories using real agent conversations. Judge behavior and saved artifacts, not exact wording:

1. Start from a supplied book excerpt with a clear goal. Observe a small in-chat explanation and grounded mission/resources.
2. Say you are confused and request a complete example. Observe an explanation rather than more interrogation.
3. Challenge an ambiguous or wrong example with a valid counterexample. Observe source/assumption rechecking and correction.
4. Give a partly correct answer, then say "understood". Inspect that progress separates the supported insight from the remaining gap and does not invent independent mastery.
5. Pause with an unfinished exercise. Start a fresh session from saved files and observe continuation without leaking its answer.
6. Study a nontechnical topic with an inaccessible source. Observe honest source limitations, suitable examples, and no requirement to write code.

Also try a one-off factual question without explicitly invoking the skill: it should not create learning files. Validate discovery in both clients without changing a user's working plugin configuration. Record actual limits of the checks; format validation alone is not a behavioral evaluation.
