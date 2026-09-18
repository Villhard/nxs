## Conventions

<task-independent decisions and constraints, with their reasons and relevant code references.
Exec passes these to every worker and passes applicable CLAUDE.md/AGENTS.md rules separately.
Omit Conventions only when there are no additional shared rules.>

## Implementation

### Task 1: A caller can preserve a zero limit

**Files:**
- Modify: limits.py
- Create: test_limits.py

- [ ] update resolve_limit so None uses the default and zero remains zero
- [ ] write unittest checks for None, zero and a positive limit
- [ ] run `python3 -m unittest test_limits`
