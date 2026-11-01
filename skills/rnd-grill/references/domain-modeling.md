# DOMAIN MODELING

Read when domain terms or durable decisions affect discussion, when preparing save-time domain proposals, or for a direct domain-document request inside an explicitly authorized scope. rnd-grill owns these rules and approved domain-record writes.

## DISCOVER AND SHARPEN

Read project instructions and existing GLOSSARY.md, GLOSSARY-MAP.md and relevant ADRs. A glossary map selects the affected context; ask when the context is materially ambiguous. Missing domain documents are normal and do not block unrelated work.

Use the project's canonical terms. Surface conflicting definitions and sharpen vague terms before decisions that depend on them. Check claimed behavior against code and probe relationships with concrete edge-case scenarios. Show contradictions with their sources; the user decides changed intent.

## PROPOSE AT SAVE TIME

Present concrete glossary additions/revisions and worthwhile ADRs with the proposed saved result. Agreement on a term alone does not authorize an unshown document edit. Reuse an existing approval covering the exact entry/diff; otherwise wait. Apply only approved entries. Declining one proposal does not approve another. A direct approved domain-document request may produce only the requested records, without a decision wrapper or a new feature directory.

Create records lazily after approval. Follow the project's format and context locations; preserve unrelated entries, user edits and existing ADR history. A repeated identical proposal is a no-op. Different existing content requires a concrete revision decision, not replacement from a broad save request. Never write project SPEC.md or .SPEC.md; those remain dev-spec-owned.

## GLOSSARY

Record only terms specific to the domain, with concise definitions of the concepts, not implementation details, plans or generic programming vocabulary. With no established format, use:

```markdown
# <Context>

<Purpose of this context.>

## Language

**<Canonical term>**:
<One or two sentence definition.>
_Avoid_: <Confusing synonyms, when relevant.>
```

Use an existing glossary map rather than creating competing root definitions. If no context structure exists, a root GLOSSARY.md is the lazy default for the first approved term.

## ADR

Offer an ADR only when all three hold: reversing the decision has meaningful cost; a future reader would find the choice surprising without context; and real alternatives were weighed. Routine obvious or easily reversible choices need no ADR.

Use existing ADR conventions. Otherwise use docs/adr/NNNN-<slug>.md, after inspecting the highest existing number, with a short title and a paragraph stating context, decision and reasons. Add alternatives or consequences only when useful. Record changed decisions through an approved revision/superseding record that preserves the earlier rationale. Create the directory only for an approved entry.
