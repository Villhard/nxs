# Focused R&D resolves questions before ticket slicing

Add an explicit decision-only mode to `dev-rnd`. It reuses code investigation, clarification, approach comparison and stress testing, but completes with an agreed conclusion, supporting evidence and any remaining questions, without implementation tickets. The normal `dev-rnd` invocation keeps its full flow.

The lead can delegate the needed focused investigations, relay their questions to the user and combine their results into an agreed solution and feature plan before implementation tickets are prepared. This keeps nxs usable without mattpocock/skills and avoids duplicating a full interview contract inside the lead. Available companion grilling skills may perform focused investigations as an optional route.

The mode's exact invocation syntax and output format remain implementation details to settle before shipping. This record approves the design direction; it does not change the current skill contract.
