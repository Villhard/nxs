---
description: Print the flow map or route a free-text "what do I run" intent to the matching /nxs: command. Use with no argument to list all commands grouped by flow, or pass an intent to be routed to one command with a one-line reason.
argument-hint: "[what do I want to do]"
---

# /nxs:help

Deterministic discovery router for the `/nxs:` commands. A map or a single routed answer, not a tutorial. Self-contained skill; output language and response style come from global rules, not this file. The command table below is the source of truth - do not explore beyond it.

## PROCEDURE

1. No argument -> print the flow map: the four workflow flows (dev / rnd / std / doc) plus the meta family, each with its commands and a one-line trigger per command.
2. Free-text intent ("what do I run to ...") -> match it to one flow and one command; name the command with a one-line reason. Offer the nearest alternative when two commands are close. Ask one clarifying question only when the match is genuinely ambiguous.
3. Keep it short: a map or a single routed answer, not a tutorial. Point to the command's own skill for detail.
4. If an intent matches nothing in the table, say so and print the map instead of guessing.

## COMMANDS

| command | trigger |
|---|---|
| `/nxs:dev-diagnose` | bug investigation via 5-Why |
| `/nxs:dev-plan` | create an implementation plan |
| `/nxs:dev-plan-review` | review a plan before execution |
| `/nxs:dev-exec` | execute an implementation plan |
| `/nxs:dev-review` | review code changes |
| `/nxs:dev-recommit` | clean up branch commit history before review |
| `/nxs:dev-cleanup` | archive completed plans and stale briefs |
| `/nxs:rnd-brainstorm` | clarify and explore a task or idea |
| `/nxs:rnd-prototype` | run a throwaway experiment for one design question |
| `/nxs:rnd-architecture` | find architectural friction and deepening opportunities |
| `/nxs:rnd-dialectic` | compare approaches or stress-test a claim |
| `/nxs:rnd-rethink` | stop a bad approach and find another |
| `/nxs:std-explain` | explain a topic, file, branch, or source |
| `/nxs:std-walkthrough` | overview of a branch, flow, or code path |
| `/nxs:std-onboard` | onboarding map for a domain or subsystem |
| `/nxs:std-source` | learn from external material |
| `/nxs:doc-note` | save applied knowledge |
| `/nxs:doc-summary` | create a durable task-doc snapshot |
| `/nxs:doc-guide` | draft end-user / Confluence documentation |
| `/nxs:doc-handoff` | compact session handoff to chat |
| `/nxs:init` | initialize / refresh project AI context in docs/.ai/ |
| `/nxs:help` | show the flow map or route "what do I run" |

## OUTPUT FORMAT

```text
# map mode
dev - deliver a known-enough code change
  /nxs:dev-diagnose     - bug investigation via 5-Why
  /nxs:dev-plan         - implementation plan
  /nxs:dev-plan-review  - review a plan before execution
  /nxs:dev-exec         - execute an implementation plan
  /nxs:dev-review       - review code changes
  /nxs:dev-recommit     - clean up branch commit history
  /nxs:dev-cleanup      - archive completed plans and stale briefs
rnd - reduce uncertainty before a plan exists
  /nxs:rnd-brainstorm   - clarify and explore a task or idea
  /nxs:rnd-prototype    - throwaway experiment for one design question
  /nxs:rnd-architecture - find architectural friction
  /nxs:rnd-dialectic    - compare approaches or stress-test a claim
  /nxs:rnd-rethink      - stop a bad approach and find another
std - learn a codebase / course / book / article
  /nxs:std-explain      - explain a topic, file, branch, or source
  /nxs:std-walkthrough  - overview of a branch, flow, or code path
  /nxs:std-onboard      - onboarding map for a domain or subsystem
  /nxs:std-source       - learn from external material
doc - persist knowledge, split by audience
  /nxs:doc-note         - save applied knowledge
  /nxs:doc-summary      - durable task-doc snapshot
  /nxs:doc-guide        - end-user / Confluence documentation
  /nxs:doc-handoff      - compact session handoff to chat
meta - project context + this router
  /nxs:init  - init / refresh project AI context
  /nxs:help  - this router

# route mode
You want: <restated intent>
Run: /nxs:<command> - <one-line reason>
Alt: /nxs:<command> - <when instead>
```
