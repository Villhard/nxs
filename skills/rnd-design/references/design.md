# MODULE DESIGN

## COMPARE

A module has an interface and implementation at any scale. Its interface is everything callers must know, including ordering, invariants, errors and relevant performance, not just signatures. A seam is where behavior can be changed without editing its callers; an adapter satisfies the interface there. Depth means useful behavior available behind a small interface, giving callers leverage and concentrating change and verification in one place. Compare actual caller obligations and implementation changes; line counts are not depth.

Use responsibility and SOLID principles as questions tied to the observed change: which reasons for change belong together, what behavior callers can depend on, what variations exist and where dependencies belong. Evaluate whether a seam improves a real variation or test need. Do not require layers, interfaces, dependency injection or abstractions merely to satisfy a principle. Include the option of keeping the current design when viable. Identify contracts, migration impact, failure paths and tests at the public interface for each meaningful alternative.

## RESULT AND PRESERVATION

Use an explicitly supplied feature directory, or choose `.scratch/<topic-slug>/` with a short lowercase hyphenated slug. If the candidate directory contains `map.md`, choose another slug unless the user explicitly authorizes work there. Save `research/<module-slug>-design.md` under that directory. Inspect the destination and existing design history first. Preserve other artifacts and user edits; a materially different existing result needs a concrete revision decision rather than silent overwrite. Never edit project `SPEC.md` or `.SPEC.md`.

The artifact distinguishes agreed decisions, rejected alternatives and reasons, proposals, assumptions, open questions and user feedback. Name the selected module and scope, source paths and relevant callers, current and chosen responsibilities, interface and seam, consequences, failure cases, verification implications and any missing evidence. An unfinished result remains explicitly open and cannot be handed off as ready work. Do not include secrets, private configuration or raw session transcripts.
