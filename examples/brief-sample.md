# Brief: pagination for the items list endpoint

- Date: YYYY-MM-DD
- Status: ready for `/nxs:plan`
- Tracker: PROJ-123

## Task

`GET /items` returns the whole table in one response. On large accounts the payload grows
unbounded and the request times out. Add pagination so clients fetch a bounded page at a
time, without breaking existing callers.

## Context (facts from the code)

- The handler in `src/items/handler.py` calls `list_items()` with no bounds and serializes
  the full result.
- The repository query in `src/items/repository.py` has no `ORDER BY`, so row order is not
  stable across calls.
- Existing clients call `GET /items` with no query params and expect a list body.

## Acceptance criteria

- `GET /items?limit=&offset=` returns a bounded page and a `total` count.
- `GET /items` with no params keeps today's first-page behavior; existing clients are
  unaffected.

## Options

### O1. Offset / limit pagination - recommended

- pro: trivial to implement over the current SQL; maps directly to `LIMIT` / `OFFSET`;
  familiar to clients; a stable `ORDER BY` makes pages consistent.
- con: deep offsets get slower on very large tables; a concurrent insert can shift rows
  between pages.

### O2. Cursor / keyset pagination - rejected for now

- pro: constant-time deep paging; stable under concurrent inserts.
- con: opaque cursor tokens and more client-side handling; overkill for the current table
  size. Reconsider if row counts reach the millions.

### O3. Cap the response, no paging - rejected

- pro: one-line change.
- con: silently drops rows past the cap; clients cannot reach the rest. Not acceptable.

## Chosen approach

O1: offset / limit with a validated `(limit, offset)` pair, a `MAX_LIMIT` clamp, a stable
`ORDER BY id`, and a `total` count in the response. No params keeps today's first-page
behavior, so existing clients are unaffected.

Explicitly not doing: cursor pagination and filtering / search params in this iteration.

## Next

`/nxs:plan` on this brief -> `/nxs:exec`.

## CLARIFICATIONS

### Session YYYY-MM-DD

- Q: Should this iteration also add filtering / search, or pagination only?
  -> A: pagination only; filtering is a separate task.
