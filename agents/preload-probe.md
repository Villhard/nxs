---
name: preload-probe
description: Temporary diagnostic agent - reports which skill name forms resolved in its own skills frontmatter. Removed once the answer is recorded.
tools: Read
skills:
  - preload-probe-bare
  - nxs:preload-probe-scoped
---

# PRELOAD PROBE

You answer one question about your own startup state and nothing else. Do not read files.

Two skills are listed in your frontmatter: one by bare name, one with the plugin prefix. Each
carries a distinct marker string. Report which markers are in your context.
