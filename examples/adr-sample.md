# Store all timestamps in UTC

- Status: accepted

## Context

Timestamps were written using each service's local server time. Servers ran in different
regions, so the same event could be recorded with different wall-clock values, and daylight
saving shifts produced ambiguous and out-of-order rows. Comparing or sorting events across
services became unreliable.

## Decision

Persist every timestamp in UTC, in a timezone-aware column type. Conversion to a user's
local zone happens only at the presentation edge, never in storage or business logic.

## Considered options

- UTC everywhere in storage (chosen) - one canonical instant per event; convert at the edge.
- Store local time plus an offset column - preserves the original zone but complicates every
  comparison and index. Rejected: the offset is presentation metadata, not identity.

## Consequences

- A one-time migration normalizes existing local timestamps to UTC; the migration needs each
  row's original zone, so it runs before any further region rollout.
- All comparisons, sorting, and range queries become straightforward and stable.
- Clients must format to local time themselves; the API contract now documents UTC.

## Explicitly not doing

- Not storing the originating timezone per row - the presentation layer resolves the viewer's
  zone instead.
- Not backfilling sub-second precision for historical rows created before this change.
