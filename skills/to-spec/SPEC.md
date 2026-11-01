# to-spec

## Purpose

Prepare an approved local feature spec from a saved decision or clear request independently of ticket slicing. Preserve what was agreed and what remains uncertain so saving a draft cannot silently authorize downstream work.

## Ownership

Own the feature spec format and the independent source/location contract. The feature template remains byte-identical in the `rnd-debug` consumer. Bundle shared discussion, project-spec reader and journal/controlled-run resources unchanged so independent installation needs no other installed skill.

## Boundaries

Explicit invocation or an explicit controlled scope permits preparation. Writes are limited to the authorized local feature spec under `.scratch/` and applicable task journal records. Source decisions and map histories, tickets, domain/project specs, product code, Git/index, settings and installations remain unchanged. Ticket slicing and implementation require separately covering authorization; lead selects subsequent stages in a controlled run.

## Contracts

- Validate the source, existing target and relevant current project evidence before proposing content. A missing or unreadable explicit file stops instead of becoming a new request. Established destinations take precedence over defaults; a decision map does not authorize implementation artifacts in its directory. Source identity and exact-content hashes preserve provenance, not approval.
- Carry requirements, conditions, defaults, integrated answers, exclusions, rationale/source links, testing requirements and acceptance checks into the spec. Keep the seven permitted headings in template order, requiring Problem Statement and Solution and omitting only empty optional sections. Settled choices reopen only for contradictory evidence or the user's request; clear requests need no forced interview.
- Show content and exact destination before saving; reuse approval only within its covered scope. Reuse identical content without rewriting. A different existing spec requires approval of the concrete revision; changed source or target evidence requires reconciliation before saving. Preserve manual additions and history, then verify saved bytes against the approved content.
- An expressly requested draft retains its draft label and specific material questions. Permission to save uncertainty never answers it. Material unknowns and contradictory evidence prevent a ready-to-tickets handoff, including after draft approval.
- Remote or pasted input retains source identity, applicable parent decisions and blocker evidence. Missing remote content stops consumption; unknown or unmapped blockers prevent readiness. Known open remote blockers require verified local mappings and remain explicit; required results are checked in the working tree, never inferred from status alone. Closed blockers need supporting evidence. A suggested `to-tickets` handoff reports unavailable or unverified consumer support and starts no next stage.
