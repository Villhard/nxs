---
description: Explain the current context or an explicit source (file, path, branch, pasted text, prior skill output) in plain words - what it means, why it matters, which files/components/decisions are involved. Use for a plain-language breakdown; with no argument explains the current session context.
argument-hint: "[topic | path | pasted text]"
---

# /nxs:std-explain

Explain the target in plain language. Self-contained skill. Output language and response style come from global rules, not this file.

## PROCEDURE

1. Determine the target. No argument -> current session context. Ask only if genuinely unclear.
2. Source mode: if the argument is pasted text or a local `.txt` / `.md` / `.srt` path, run source intake first - extract text, denoise, segment into contexts, surface signal / conflicts / uncertainty. If no focus and several useful contexts exist, explain the source map before narrowing.
3. Gather minimal context: read the code / plan / root cause. Do not over-read.
4. Output facets:
   - what we are doing - one sentence;
   - why it matters - one or two reasons;
   - where - files, components, integration points;
   - what comes next - next step or open questions.
5. Depth: default core + components. More detail only on request. If not understood, go one level lower (fewer details, closer to core); do not restate the same level in other words, do not add analogies.

## RULES

- Plain words; technical terms stay English where customary.
- Audience: a smart person outside this domain. Supply missing domain context, no ELI5, no condescension.
- One idea at a time. No architectural essays. No motivational endings.
- The explanation saves time, not spends it. On doubt, prioritize clarity.
- Source mode is adapter-based: unsupported source types block before analysis.

## NEXT

Deeper structural pass -> `/nxs:std-walkthrough`. Turn into a plan -> `/nxs:dev-plan`.
