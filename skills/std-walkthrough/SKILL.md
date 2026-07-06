---
description: Give a short, meaning-grouped overview of a branch / flow / code path, or map an explicit source - what it does and how the pieces fit, in reading order. Not a review; it does not hunt for bugs. Use when you want orientation, not evaluation.
argument-hint: "[branch | flow | path | source]"
---

# /nxs:std-walkthrough

Walk the target and produce a short overview grouped by meaning - what it does and how the pieces fit, not a file-by-file listing. Self-contained skill. Output language and response style come from global rules, not this file.

## PROCEDURE

1. Resolve the target:
   - **branch** - diff vs base; detect the base explicitly (e.g. `main`, `develop`, a commit range like `abc123..HEAD`), do not assume it.
   - **flow / code path** - a natural-language flow (`"auth flow"`, `"checkout flow"`) or one or more paths; walk that path / subtree.
   - **explicit source** - pasted text or a local `.txt` / `.md` / `.srt` path, detected from the argument shape; map that source instead of session context.
   - *(no argument)* - current branch vs inferred base, or current session context when no repo scope applies.
2. Source mode: if the argument is an explicit source, run source intake first - extract text, denoise, segment into contexts, surface signal vs noise, decisions, open questions, contradictions, uncertainty. If no focus was given, map the useful contexts before narrowing. Source mode is adapter-based: unsupported source types block before analysis.
3. Read the relevant code / diff (or the extracted source). Read enough to understand, do not over-read.
4. Group by meaning, not by file. Taxonomy: **Enhancement** (features / capabilities), **Configuration** (settings, env, build/deploy), **Tests** (coverage changes), **Docs** (documentation / comments).
5. Produce a compact overview in reading order - what each meaning-group does and how the groups connect.
6. Draw a simple ASCII diagram only if a flow touches several components and it genuinely makes the structure easier to follow.

## BOUNDARY (not a review)

- Describe what is there and how it fits together. Keep it descriptive.
- Do NOT flag bugs, security issues, or quality problems, and do not make review claims. Finding problems in a diff is `/nxs:dev-review`.

## OUTPUT

- Chat overview only; read-only, no durable file by default.
- What the branch / flow / source does - a few bullets.
- Grouping by meaning, each group described briefly.
- Source map in source mode: contexts found, signal vs noise, decisions, open questions, contradictions, useful follow-up directions.
- Optional file table: path / change type / brief role - when it aids orientation.
- Optional ASCII diagram of affected components, if useful.
- List of non-obvious details that orientation-only reading would miss (if any).

## DEPTH

Short and meaning-grouped by default. Expand a group only on request.

## ROUTING

- `/nxs:std-walkthrough` - a structural overview of existing code / a branch (this skill).
- `/nxs:std-explain` - a plain-language explanation of one thing.
- `/nxs:std-onboard` - an onboarding map of a whole domain / subsystem.
- `/nxs:dev-review` - find problems in a diff.
