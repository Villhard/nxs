# Skill bundles

Each `##` heading is one bundle from `mattpocock/skills`, offered as a whole. The first line under it is its purpose; `Recommended.` marks the bundle offered as recommended; `Needs:` names the bundle that holds the skills its members call. Each bullet is one skill name, followed by `needs` and the skills it calls when it calls any: those decide what an install adds.

## Core

Stress-test a plan, shape its domain language, and turn the result into a spec and tickets for `dev-rnd` or direct execution.

Recommended.

- grilling
- grill-me: needs grilling
- domain-modeling
- grill-with-docs: needs grilling, domain-modeling
- to-spec
- to-tickets

## Wayfinding

Map an open effort into decision tickets and answer them with sources and throwaway prototypes.

Needs: Core

- wayfinder: needs grilling, domain-modeling, research, prototype
- research
- prototype

## Architecture

Find deepening opportunities in a codebase and design the module interfaces behind them.

Needs: Core

- improve-codebase-architecture: needs codebase-design, domain-modeling, grilling
- codebase-design

## Sessions

Hand work between sessions, look back on them, write instructions for agents, and collect answers in one questionnaire.

- handoff
- retro: needs writing-for-agents
- writing-for-agents
- to-questionnaire

## Never offered

Never install or remove these; report an installed copy as installed.

- setup-matt-pocock-skills: `dev-setup global` writes its config
