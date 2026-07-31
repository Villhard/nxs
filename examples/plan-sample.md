# Add pagination to the items list endpoint

## Overview

`GET /items` returns the full table in one response, which grows unbounded and times out
on large accounts. Add offset / limit pagination with a stable sort and a total count so
clients can page through results. Small, backward-compatible change: no pagination params
keeps today's behavior for the first page.

## SOURCE ARTIFACTS

- Tracker: PROJ-123

## ACCEPTANCE CRITERIA

- `GET /items?limit=20&offset=40` returns at most 20 items starting at offset 40.
- Response includes `total` (unfiltered row count) and echoes `limit` / `offset`.
- No params -> first page at the default limit; existing clients keep working.
- `limit` above the max is clamped to the max; negative `limit` / `offset` -> 400.
- Results are ordered by a stable key so pages do not overlap or skip rows.

## DEVELOPMENT APPROACH

default - tests written together with the code for each task.

## Implementation

### Task 1: GET /items serves a bounded, stably ordered page

**Files:**
- Create: `src/items/pagination.py`
- Create: `tests/items/test_pagination.py`
- Modify: `src/items/repository.py`
- Modify: `tests/items/test_repository.py`
- Modify: `src/items/handler.py`
- Modify: `tests/items/test_handler.py`

**Test cases:**
- parse_page_params({}) -> limit=DEFAULT_LIMIT, offset=0
- parse_page_params({limit: 5000}) -> limit clamped to MAX_LIMIT
- parse_page_params({limit: -1}) -> raises InvalidPageParams
- list_items(limit=20, offset=40) -> rows 41..60 ordered by id, plus the unfiltered total
- list_items with offset past the end -> empty page, total unchanged
- GET /items?limit=20&offset=40 -> 200, <=20 items, body has total/limit/offset
- GET /items (no params) -> 200, first page at DEFAULT_LIMIT
- GET /items?limit=-1 -> 400 with an error body

- [ ] add `parse_page_params(query)` returning a validated `(limit, offset)` pair, with
      DEFAULT_LIMIT / MAX_LIMIT clamping and rejection of negative values
- [ ] add `limit` / `offset` and a stable `ORDER BY id` to the list query, returning the
      unfiltered total alongside the page
- [ ] call parse_page_params from the handler and shape the body with `items`, `total`,
      `limit`, `offset`
- [ ] map InvalidPageParams to a 400 response
- [ ] write tests from Test cases above (parsing, clamping, rejection)
- [ ] update / parametrize repository tests for the paging cases above
- [ ] write tests from Test cases above (the three HTTP outcomes)
- [ ] run `pytest tests/items -q` and `ruff check src tests`, then check against
      ACCEPTANCE CRITERIA

Success: `GET /items` returns a bounded, stably ordered page with `total`, `limit`, and
`offset`, answers 400 on invalid params, and serves the same first page as before when
called with no params.
