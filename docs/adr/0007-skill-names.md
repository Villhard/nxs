# Skill names stay short words the user already understands

A skill name is a command the user types, so it is chosen for recognition at a glance rather than for a naming scheme. The rule is `dev-` plus one short lowercase word: `/dev-review`, `/dev-commit`. A verb is welcome and not required. `dev-rnd` and `dev-spec` keep their names because the user reads them faster than a rewritten action name, and renaming all seven currently costs 686 references in 84 files without changing what any skill does.

The `dev-` prefix is the namespace. No installed companion skill uses it, so a name stays clear of a skill from mattpocock/skills or anthropics/skills and of a client built-in command such as `/review`. The word after it carries the work. A bare-word set reads like a team's task list (`spec`, `bug`, `cr`, `commit`) but gives up that separation, and in the case of `spec` it moves a word that already means durable project specs onto feature specs.

Rejected alternatives: `to-<artifact>` names in the Pocock style (`to-spec`, `to-tickets`) state the output well but collide with the installed mattpocock copies and read poorly for process skills (`to-delivery`, `to-setup`); verb-object names (`shape-feature`, `commit-changes`) are unambiguous but longer than anything the user says.

Existing names are precedents rather than exceptions to fix later. Propose a rename only when a name hides what the skill does, state its cost and let the user decide. New skills follow the rule from the start: the word is chosen with the user, checked against the shared agents directory and the client's built-in commands, and kept for the artifact the skill reads or writes.
